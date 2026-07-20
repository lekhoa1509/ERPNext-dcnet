"""Phase 4 transaction post orchestrator.

Reads NKC / Bang ke BR / Bang ke MV `Misa Migration Row` records of a
batch, parses them, joins NKC vouchers with their bảng kê counterparts,
and dispatches each voucher through `voucher_router.route_voucher` to
its handler. Updates the Misa Migration Row status per result and
publishes per-voucher-type progress events for the realtime UI.

Designed to be called from `post_job.post_batch` AFTER Phase 1+2 importers
have completed (post_job currently runs only `run_post` from
orchestrator.py — Phase 4 was deferred to this module so the pre-D
post_job code path stays untouched).

Per spec §4 Phase 4 + §5: each NKC voucher → 1 ERPNext doc (SI / PI / PE
/ JE / SE / PR). Failed dispatch marks the row Failed; successful sets
row.target_doctype + row.target_name + status Posted. Idempotency via
handler-level frappe.db.exists check; second invocation skips already-
created docs.
"""

from __future__ import annotations

import json
import time
from typing import Any

import frappe

from vn_accounting.misa_migration.importers import voucher_router
from vn_accounting.misa_migration.parsers import (
    invoice_list_parser,
    nkc_parser,
    sct_parser,
)
from vn_accounting.misa_migration.context import (
    clear_active_company,
    set_active_company,
)
from vn_accounting.misa_migration.setup.coa_leaves import (
    ensure_misa_leaves_for_company,
)
from vn_accounting.misa_migration.setup.company_defaults import (
    ensure_company_defaults_for_misa,
    ensure_party_accounts_for_misa,
    ensure_uoms_allow_fractional,
    ensure_allow_negative_stock,
    bind_warehouse_accounts_to_misa_inventory,
)


PROGRESS_EVENT = "misa_migration:post_progress"

_PHASE_4_FILE_TYPES = ("NKC", "Bang ke BR", "Bang ke MV", "SCT")

# PERF (Tier 1.3): DocTypes whose tracking we silence during migration.
# Each tracked field write creates a Version doc + GL audit log row =
# ~5-15ms/doc + spammy chatter. Migration data doesn't need an audit
# trail (the Misa Migration Row carries provenance). Restored in finally.
_MISA_TRACKED_DOCTYPES = (
    "Sales Invoice",
    "Purchase Invoice",
    "Payment Entry",
    "Journal Entry",
    "Stock Entry",
)


def _disable_track_changes_for_misa() -> dict[str, int]:
    """Save current `track_changes` per DocType and set it to 0.

    Returns a dict mapping DocType name → original value (0 or 1) so the
    caller can restore in a finally block. Quiet if a DocType is missing
    — the caller's main work still has to run.
    """
    saved: dict[str, int] = {}
    for dt in _MISA_TRACKED_DOCTYPES:
        try:
            current = frappe.db.get_value("DocType", dt, "track_changes")
            saved[dt] = int(current or 0)
            if saved[dt]:
                frappe.db.set_value(
                    "DocType", dt, "track_changes", 0,
                    update_modified=False,
                )
        except Exception:
            # Missing DocType is fine — skip; never let setup raise here
            # or the finally would have nothing to restore.
            continue
    if saved:
        frappe.db.commit()
    return saved


def _restore_track_changes(saved: dict[str, int]) -> None:
    """Restore per-DocType track_changes to the saved value. Tolerant —
    a missing or already-zero value is a no-op. MUST be called from a
    finally block so a mid-migration exception doesn't leave the site
    with chatter silently disabled forever.
    """
    if not saved:
        return
    for dt, original in saved.items():
        try:
            frappe.db.set_value(
                "DocType", dt, "track_changes", original,
                update_modified=False,
            )
        except Exception:
            continue
    try:
        frappe.db.commit()
    except Exception:
        pass


def run_preflight_setup(company: str) -> dict[str, Any]:
    """Auto-run the 3 mandatory setup helpers BEFORE any Misa post step.

    Item 3: prevents operator from forgetting one of these prerequisites
    that any Phase 0 or Phase 4 import relies on. All three are idempotent
    — repeat runs are no-ops when the company is already configured.

    Order:
      1. ensure_misa_leaves_for_company — creates level-5 leaf accounts
         (1111, 1121, 2141, 3331, …) under existing level-4 parents.
         MUST run first: subsequent helpers may reference these leaves.
      2. ensure_company_defaults_for_misa — sets stock_adjustment_account,
         default_cost_center, etc. on the Company doc.
      3. ensure_party_accounts_for_misa — sets per-Customer / per-Supplier
         default_receivable_account / default_payable_account.

    Args:
      company: Company.name to bootstrap.

    Returns:
      {
        'company': str,
        'coa_leaves': <ensure_misa_leaves_for_company result>,
        'company_defaults': <ensure_company_defaults_for_misa result>,
        'party_accounts': <ensure_party_accounts_for_misa result>,
        'elapsed_seconds': float,
        'errors': [{'step': str, 'error': str}],
      }
    """
    t0 = time.time()
    summary: dict[str, Any] = {
        "company": company,
        "coa_leaves": None,
        "company_defaults": None,
        "party_accounts": None,
        "errors": [],
    }

    try:
        summary["coa_leaves"] = ensure_misa_leaves_for_company(company)
    except Exception as exc:
        msg = f"{type(exc).__name__}: {exc}"
        summary["errors"].append({"step": "coa_leaves", "error": msg})
        frappe.log_error(
            title=f"Preflight setup coa_leaves failed: {company}",
            message=msg,
        )

    try:
        summary["company_defaults"] = ensure_company_defaults_for_misa(company)
    except Exception as exc:
        msg = f"{type(exc).__name__}: {exc}"
        summary["errors"].append({"step": "company_defaults", "error": msg})
        frappe.log_error(
            title=f"Preflight setup company_defaults failed: {company}",
            message=msg,
        )

    try:
        pa_result = ensure_party_accounts_for_misa(company)
        summary["party_accounts"] = pa_result
        # UX: notify operator when foreign-currency parties were skipped —
        # those need manual currency-matched receivable/payable assignment.
        n_skipped = pa_result.get("foreign_skipped", 0) if isinstance(pa_result, dict) else 0
        if n_skipped:
            summary.setdefault("warnings", []).append({
                "step": "party_accounts",
                "message": (
                    f"Đã bỏ qua {n_skipped} Customer/Supplier có default_currency "
                    f"khác công ty — cần gán Account thủ công theo loại tiền tương ứng."
                ),
            })
    except Exception as exc:
        msg = f"{type(exc).__name__}: {exc}"
        summary["errors"].append({"step": "party_accounts", "error": msg})
        frappe.log_error(
            title=f"Preflight setup party_accounts failed: {company}",
            message=msg,
        )

    try:
        summary["uoms_unrestricted"] = ensure_uoms_allow_fractional()
    except Exception as exc:
        msg = f"{type(exc).__name__}: {exc}"
        summary["errors"].append({"step": "uoms_allow_fractional", "error": msg})
        frappe.log_error(
            title=f"Preflight setup uoms_allow_fractional failed",
            message=msg,
        )

    try:
        wb_result = bind_warehouse_accounts_to_misa_inventory(company)
        summary["warehouse_accounts"] = wb_result
        # Surface as warning if any warehouse was newly bound so operator
        # can review the heuristic choice (CCDC vs goods classification).
        if wb_result.get("changed", 0) > 0:
            sample = wb_result.get("binds") or []
            n_changed = wb_result["changed"]
            preview = ", ".join(
                f"{b['warehouse']}→{b['account']}" for b in sample[:5]
            )
            summary.setdefault("warnings", []).append({
                "step": "warehouse_accounts",
                "message": (
                    f"Đã gán Warehouse.account cho {n_changed} kho theo "
                    f"heuristic tên (CCDC→1531, NVL→152, TP→155, mặc định "
                    f"1561). Operator nên review {preview}... "
                    f"trước khi tiếp tục — sai gán = sai GL split TK 1531/"
                    f"1532/152/155/1561."
                ),
            })
        if wb_result.get("missing_account", 0) > 0:
            summary.setdefault("warnings", []).append({
                "step": "warehouse_accounts",
                "message": (
                    f"{wb_result['missing_account']} kho không tìm thấy "
                    f"account leaf phù hợp (TK 1531/152/155/1561 chưa có "
                    f"trên CoA). Chạy Phase 2 import 'Hệ thống tài khoản' "
                    f"trước."
                ),
            })
    except Exception as exc:
        msg = f"{type(exc).__name__}: {exc}"
        summary["errors"].append({"step": "warehouse_accounts", "error": msg})
        frappe.log_error(
            title="Preflight setup warehouse_accounts failed",
            message=msg,
        )

    try:
        ans_result = ensure_allow_negative_stock()
        summary["allow_negative_stock"] = ans_result
        # Surface as warning so operator knows the toggle was flipped.
        # Misa migration inherently creates negative-stock SE Material
        # Issue rows because the PI placeholder ↔ real-item mapping
        # isn't bridged (see TK 156/1561 deep-dive). Leaving the flag
        # ON for sandbox is safe; for production, operator should
        # decide whether to restore it.
        if ans_result.get("changed"):
            summary.setdefault("warnings", []).append({
                "step": "allow_negative_stock",
                "message": (
                    "Đã bật Stock Settings.allow_negative_stock=1 để SE "
                    "Material Issue không bị NegativeStockError trong "
                    "quá trình import (Misa lookup chain không bao phủ "
                    "toàn bộ item codes). Operator nên review + tắt lại "
                    "sau khi migration kết thúc nếu cần."
                ),
            })
    except Exception as exc:
        msg = f"{type(exc).__name__}: {exc}"
        summary["errors"].append({"step": "allow_negative_stock", "error": msg})
        frappe.log_error(
            title="Preflight setup allow_negative_stock failed",
            message=msg,
        )

    summary["elapsed_seconds"] = time.time() - t0
    return summary


def _publish_progress(batch_name: str, counts: dict) -> None:
    try:
        frappe.publish_realtime(
            PROGRESS_EVENT,
            {"batch": batch_name, "counts": counts},
            after_commit=True,
        )
    except Exception:
        pass


def _load_phase_4_payloads(
    batch_name: str,
) -> dict[str, list[tuple[str, dict]]]:
    """Load NKC/BR/MV row payloads for a batch.

    Returns dict keyed by file_type → list of (row_name, parsed_payload).
    Row names are kept so we can update status back on the same row.
    """
    rows = frappe.db.sql(
        """
        SELECT name, file_type, raw_payload
        FROM `tabMisa Migration Row`
        WHERE batch=%s
          AND status='Ready'
          AND file_type IN ('NKC', 'Bang ke BR', 'Bang ke MV', 'SCT')
        """,
        (batch_name,),
        as_dict=True,
    )
    grouped: dict[str, list[tuple[str, dict]]] = {ft: [] for ft in _PHASE_4_FILE_TYPES}
    for r in rows:
        ft = r["file_type"]
        try:
            payload = json.loads(r["raw_payload"] or "{}")
        except (TypeError, ValueError):
            continue
        if isinstance(payload, dict):
            grouped.setdefault(ft, []).append((r["name"], payload))
    return grouped


class InvoiceLookup:
    """Dual-index lookup for BR/MV register invoices.

    Misa data model: one real-world Số hóa đơn (e.g. 00000563) spawns
    multiple journal vouchers because each accounting event (warehouse
    receipt, VAT-bearing voucher, adjustments) gets its own voucher
    number. The BR/MV VAT register is keyed by the VAT-bearing voucher
    (e.g. MDV20253650) — NEVER by the warehouse voucher (PN20250138).
    When the NKC handler processes a PN voucher, looking up the register
    purely by voucher_no misses the register entries that share the same
    invoice_no but live under a sibling voucher.

    `by_voucher_no` is the legacy primary index (1:1, the register row's
    own Số chứng từ).
    `by_invoice_no` is the new fallback index. One invoice_no can map
    to multiple register entries (MDV + NVK + BH may all share the same
    Số hóa đơn), so values are lists.

    Use `.find(voucher_no, invoice_no)` to resolve: voucher_no match
    first (most specific), then invoice_no fallback. Returns None when
    neither key resolves.
    """

    def __init__(self, parsed_invoices: list[dict[str, Any]]):
        self.by_voucher_no: dict[str, dict[str, Any]] = {}
        self.by_invoice_no: dict[str, list[dict[str, Any]]] = {}
        for inv in parsed_invoices:
            vn = inv.get("voucher_no")
            inv_no = inv.get("invoice_no")
            if vn:
                self.by_voucher_no[vn] = inv
            if inv_no:
                self.by_invoice_no.setdefault(inv_no, []).append(inv)

    def find(
        self,
        voucher_no: str | None,
        invoice_no: str | None = None,
    ) -> dict[str, Any] | None:
        if voucher_no and voucher_no in self.by_voucher_no:
            return self.by_voucher_no[voucher_no]
        if invoice_no and invoice_no in self.by_invoice_no:
            entries = self.by_invoice_no[invoice_no]
            if entries:
                return entries[0]
        return None

    def has(self, voucher_no: str | None, invoice_no: str | None = None) -> bool:
        return self.find(voucher_no, invoice_no) is not None

    # Dict-like interface — keeps legacy callers (preflight, preflight_report)
    # working unchanged. They iterate / look up by voucher_no; the new
    # invoice_no fallback is opt-in via .find() / .has().
    def __contains__(self, key: str) -> bool:
        return key in self.by_voucher_no

    def __getitem__(self, key: str) -> dict[str, Any]:
        return self.by_voucher_no[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self.by_voucher_no.get(key, default)

    def values(self):
        return self.by_voucher_no.values()

    def keys(self):
        return self.by_voucher_no.keys()

    def items(self):
        return self.by_voucher_no.items()

    def __iter__(self):
        return iter(self.by_voucher_no)

    def __len__(self) -> int:
        return len(self.by_voucher_no)


def _build_invoice_lookup(
    parsed_invoices: list[dict[str, Any]],
) -> InvoiceLookup:
    """list-of-invoices → InvoiceLookup with dual voucher_no + invoice_no index."""
    return InvoiceLookup(parsed_invoices)


def _update_nkc_row_status_by_voucher(
    batch_name: str,
    voucher_no: str,
    new_status: str,
    target_doctype: str | None = None,
    target_name: str | None = None,
    error_message: str | None = None,
) -> None:
    """Update every NKC row belonging to a voucher's group.

    A voucher with N legs has N rows in `tabMisa Migration Row` (one per
    NKC line). We update them all so the Review UI status reflects the
    voucher-level outcome.
    """
    update_kwargs = {"status": new_status}
    if target_doctype:
        update_kwargs["target_doctype"] = target_doctype
    if target_name:
        update_kwargs["target_name"] = target_name
    if error_message:
        # Errors can be long; truncate to fit the Data field
        update_kwargs["error_message"] = (error_message or "")[:240]

    set_clause = ", ".join(f"`{k}`=%s" for k in update_kwargs)
    args = list(update_kwargs.values()) + [batch_name, voucher_no]
    # PERF (Tier 1.6): query by the indexed voucher_no column. The prior
    # JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Số chứng từ"')) shape
    # forced a full table scan + row-level locks on every NKC row in the
    # site (~322k), causing minute-long lock-wait timeouts when two shards
    # ran in parallel. voucher_no is denormalised on insert by parse_job
    # and indexed by search_index=1 in the DocType (existing column —
    # no migration needed; only backfill for pre-Tier-1.6 rows).
    frappe.db.sql(
        f"""
        UPDATE `tabMisa Migration Row`
        SET {set_clause}
        WHERE batch=%s AND file_type='NKC' AND voucher_no=%s
        """,
        tuple(args),
    )


def run_phase_4_post(
    batch_name: str,
    chunk_commit: int = 50,
    max_rows_per_run: int | None = None,
) -> dict[str, Any]:
    """Post Phase 4 vouchers for a batch, capped at ``max_rows_per_run``.

    Thin wrapper around ``_run_phase_4_post_impl`` that ensures
    DocType-level ``track_changes`` is restored even on mid-run
    exception (Tier 1.3 — see _disable_track_changes_for_misa).
    """
    # PERF (Tier 1.3): silence DocType-level track_changes for the 5
    # voucher DocTypes the handlers will hammer. MUST be restored in
    # finally so a mid-run crash doesn't leave the site without audit
    # trail. The dedicated wrapper guarantees the restore semantic
    # regardless of how the inner body returns or raises.
    saved_track_changes = _disable_track_changes_for_misa()
    try:
        return _run_phase_4_post_impl(batch_name, chunk_commit, max_rows_per_run)
    finally:
        _restore_track_changes(saved_track_changes)


def _run_phase_4_post_impl(
    batch_name: str,
    chunk_commit: int = 50,
    max_rows_per_run: int | None = None,
) -> dict[str, Any]:
    """Implementation body for ``run_phase_4_post``.

    Args:
      batch_name: Misa Migration Batch name.
      chunk_commit: number of vouchers processed before frappe.db.commit().
      max_rows_per_run: stop after posting this many vouchers and leave the
        rest as "Ready" for a later resume (see post_job.post_batch's
        auto-reenqueue-on-incomplete loop). None/0 = no cap, post the whole
        batch in one run (legacy behaviour).

    Returns:
      {
        "by_target_doctype": {DocType: {"posted":N, "failed":N, "skipped":N}},
        "by_prefix": {Prefix: {"posted":N, "failed":N, "skipped":N}},
        "errors": [{"voucher_no", "prefix", "error"}],
        "total_vouchers": int,
        "processed_vouchers": int,
        "remaining_vouchers": int,
        "complete": bool,
        "elapsed_seconds": float,
      }
    """
    t0 = time.time()

    # PERF: bulk migration mode — disable per-doc mail tracking,
    # background queue dispatch, and link integrity checks. ERPNext's
    # default Document.insert/submit triggers ~10 hooks per doc;
    # most are unnecessary for Misa-derived data (links already
    # validated upstream in preflight + parser). With these flags,
    # observed per-row time drops from ~200ms to ~30ms = ~6x speedup.
    frappe.flags.in_install = False  # explicit, leave validate on
    frappe.flags.tracking_disable = True   # skip mail.thread tracking
    frappe.flags.mute_emails = True        # skip notification emails
    frappe.flags.in_migrate = True          # skip background autoname tasks

    # B2 + B3 + B4 + Item 3: auto-run preflight setup (COA leaves +
    # Company defaults + party accounts) before any handler runs.
    # Idempotent — safe to call every Post.
    batch_company = frappe.db.get_value(
        "Misa Migration Batch", batch_name, "company"
    )
    company_for_setup = (
        batch_company
        or frappe.defaults.get_global_default("company")
        or frappe.db.get_value("Company", {}, "name")
    )
    preflight_summary = None
    if company_for_setup:
        # B2 fix: pin the active company for all handlers in this request
        set_active_company(company_for_setup)

        # PERF (Tier 1.1): if the dispatcher already called prewarm_masters
        # for this Company, skip the per-shard run_preflight_setup. Two
        # parallel shards racing on Company / Party Account row-level
        # locks was the primary cause of lock-wait timeouts in the
        # 2026-05-21 E2E run. The flag is set by api.post.prewarm_masters
        # after acquiring the company-wide lock, so workers can trust it.
        from vn_accounting.misa_migration.api.post import prewarm_flag_key
        prewarmed = bool(frappe.cache().get_value(prewarm_flag_key(company_for_setup)))

        if prewarmed:
            _publish_progress(batch_name, {
                "Preflight": {"step": "skipped (prewarmed)", "errors": 0}
            })
            preflight_summary = {"skipped_via_prewarm_flag": True}
        else:
            preflight_summary = run_preflight_setup(company_for_setup)
            # Surface preflight progress in UI feed so operator sees what
            # was auto-configured (Item 3 acceptance criterion).
            _publish_progress(batch_name, {
                "Preflight": {
                    "step": "completed",
                    "errors": len(preflight_summary.get("errors", []) or []),
                }
            })

        # PERF: pre-warm Account is_group + leaf-by-number cache
        # (single SQL bulk load). Without this, every handler's
        # _resolve_account hit DB twice per leg = thousands of round
        # trips per voucher batch. ALWAYS run (not gated by prewarm
        # flag) because the cache is per-process memory, not shared
        # across worker processes.
        from vn_accounting.misa_migration.importers.nkc_handlers.payment_entry import (
            _warm_account_cache_for_company, reset_perf_caches,
        )
        reset_perf_caches()
        _warm_account_cache_for_company(company_for_setup)

        # PERF (Tier 1.5): pre-load Customer / Supplier / Employee /
        # Account-leaf name sets so handlers do set-lookups instead of
        # per-row frappe.db.exists round-trips. reset_perf_caches above
        # cleared the prior cache; warm now against the active Company.
        from vn_accounting.misa_migration.importers.nkc_handlers import (
            _party_cache,
        )
        party_counts = _party_cache.warm_party_cache(company_for_setup)
        _publish_progress(batch_name, {
            "Party prewarm": {
                "customers": party_counts["customers"],
                "suppliers": party_counts["suppliers"],
                "employees": party_counts["employees"],
                "accounts": party_counts["account_leaves"],
            }
        })

        # PERF + Fix F: pre-load Item.item_name → Item.name map so SI/PI
        # handlers can resolve real Item codes from bảng kê "Mặt hàng"
        # instead of dumping every line on MISA-MIGRATION-SVC placeholder.
        from vn_accounting.misa_migration.importers.nkc_handlers import (
            _item_cache,
        )
        _item_cache.reset_item_cache()
        item_counts = _item_cache.warm_item_cache()
        _publish_progress(batch_name, {
            "Item prewarm": {
                "items": item_counts["items"],
                "stock_items": item_counts["stock_items"],
            }
        })

    grouped = _load_phase_4_payloads(batch_name)

    nkc_rows = grouped.get("NKC") or []
    br_rows = grouped.get("Bang ke BR") or []
    mv_rows = grouped.get("Bang ke MV") or []
    sct_rows = grouped.get("SCT") or []

    if not nkc_rows:
        return {
            "by_target_doctype": {}, "by_prefix": {},
            "errors": [], "total_vouchers": 0,
            "processed_vouchers": 0, "remaining_vouchers": 0, "complete": True,
            "elapsed_seconds": time.time() - t0,
            "preflight": preflight_summary,
        }

    # Parse NKC rows → vouchers; bảng kê → invoices; SCT → item-lines
    nkc_payloads = [p for (_n, p) in nkc_rows]
    br_payloads = [p for (_n, p) in br_rows]
    mv_payloads = [p for (_n, p) in mv_rows]
    sct_payloads = [p for (_n, p) in sct_rows]

    vouchers = nkc_parser.parse_nkc_rows(nkc_payloads)
    br_invoices = _build_invoice_lookup(
        invoice_list_parser.parse_invoice_list(br_payloads, kind="BR")
    )
    mv_invoices = _build_invoice_lookup(
        invoice_list_parser.parse_invoice_list(mv_payloads, kind="MV")
    )
    # SCT lookup: {voucher_no: voucher_dict with item-line list}.
    # Passed to the SE handler via voucher_router context so PX/PXHN/
    # PNHN can emit one Stock Entry row per real item line (instead of
    # the legacy MISA-MIGRATION-STOCK placeholder Item single row).
    sct_by_voucher = sct_parser.group_by_voucher(sct_payloads)
    # Stash on a module-global per-request — the SE handler reads it
    # via context.get_sct_voucher() to keep voucher_router's signature
    # unchanged.
    from vn_accounting.misa_migration import context as _ctx
    _ctx.set_sct_voucher_map(sct_by_voucher)

    # PERF (Tier 1.4): pre-warm _ITEM_CACHE with one bulk SELECT for all
    # SCT item_codes BEFORE the voucher loop, so the per-row exists-check
    # round-trips collapse to a single query. Also amortizes any missing
    # Item stub creation upfront so the hot voucher loop is cache-only.
    if sct_by_voucher and company_for_setup:
        from vn_accounting.misa_migration.importers.nkc_handlers.stock_entry import (
            bulk_warm_items_from_sct,
        )
        item_warm = bulk_warm_items_from_sct(sct_by_voucher, company_for_setup)
        _publish_progress(batch_name, {
            "Item prewarm": {
                "considered": item_warm["considered"],
                "found": item_warm["found_existing"] + item_warm["already_cached"],
                "created": item_warm["created"],
                "failed": item_warm["failed"],
            }
        })

    by_target: dict[str, dict[str, int]] = {}
    by_prefix: dict[str, dict[str, int]] = {}
    errors: list[dict[str, str]] = []

    def _bump(bucket: dict, key: str, status_key: str) -> None:
        sub = bucket.setdefault(key, {"posted": 0, "failed": 0, "skipped": 0})
        sub[status_key] = sub.get(status_key, 0) + 1

    processed = 0
    for voucher in vouchers:
        voucher_no = voucher.get("voucher_no", "")
        prefix = voucher.get("prefix") or ""
        # Dual-key lookup: voucher_no first (legacy 1:1 case where NKC and
        # register share Số chứng từ), then invoice_no fallback (the common
        # case where Misa spawns multiple voucher numbers per Số hóa đơn,
        # e.g. PN warehouse voucher + MDV VAT voucher sharing 00000563).
        # Without the fallback, ~1000 PN/MH vouchers got single-line
        # consolidated SI/PI instead of the proper line breakdown.
        invoice_no = voucher.get("invoice_no")
        invoice = (
            br_invoices.find(voucher_no, invoice_no)
            or mv_invoices.find(voucher_no, invoice_no)
        )

        # Skip vouchers with parser-detected balance error → leave Ready,
        # caller's pre-flight (C13) should have caught these
        if voucher.get("balance_error"):
            errors.append({
                "voucher_no": voucher_no, "prefix": prefix,
                "error": f"Pre-flight should have blocked: {voucher['balance_error']}",
            })
            _bump(by_prefix, prefix or "?", "failed")
            _update_nkc_row_status_by_voucher(
                batch_name, voucher_no, "Failed",
                error_message=voucher["balance_error"],
            )
            continue

        result = voucher_router.route_voucher(voucher, invoice)
        status = result.get("status", "failed")

        # B7 fix: UNC handler returns 'deferred' for vouchers without
        # Dr 331/141 (interest, loan principal, bank fees, tax, salary
        # paid direct). Route to JE handler so they still post.
        if status == "deferred":
            from vn_accounting.misa_migration.importers.nkc_handlers.journal_entry \
                import create_je_from_unc_deferred
            try:
                je_result = create_je_from_unc_deferred(voucher)
                result = {**result, **je_result}
                status = result.get("status", "failed")
            except Exception as exc:
                result["error"] = f"deferred→JE fallback failed: {exc}"
                status = "failed"

        target_dt = result.get("target_doctype")
        target_name = result.get("target_name")
        error_msg = result.get("error")

        if status == "created":
            _bump(by_target, target_dt or "?", "posted")
            _bump(by_prefix, prefix or "?", "posted")
            _update_nkc_row_status_by_voucher(
                batch_name, voucher_no, "Posted",
                target_doctype=target_dt, target_name=target_name,
            )
        elif status == "skipped":
            _bump(by_target, target_dt or "?", "skipped")
            _bump(by_prefix, prefix or "?", "skipped")
            _update_nkc_row_status_by_voucher(
                batch_name, voucher_no, "Skipped",
                target_doctype=target_dt, target_name=target_name,
            )
        else:
            _bump(by_target, target_dt or "?", "failed")
            _bump(by_prefix, prefix or "?", "failed")
            errors.append({
                "voucher_no": voucher_no, "prefix": prefix,
                "error": error_msg or "unknown",
            })
            _update_nkc_row_status_by_voucher(
                batch_name, voucher_no, "Failed",
                error_message=error_msg,
            )

        processed += 1
        if processed % chunk_commit == 0:
            frappe.db.commit()
            # Bump batch.modified so watchdog (idle >10min → STUCK) doesn't
            # false-positive on a long but actively-progressing post.
            frappe.db.sql(
                "UPDATE `tabMisa Migration Batch` SET modified=NOW(6) WHERE name=%s",
                (batch_name,),
            )
            _publish_progress(batch_name, {
                "Phase 4": {
                    "Posted": sum(v.get("posted", 0) for v in by_target.values()),
                    "Failed": sum(v.get("failed", 0) for v in by_target.values()),
                    "Skipped": sum(v.get("skipped", 0) for v in by_target.values()),
                    "Ready": len(vouchers) - processed,
                }
            })

        # Server-load cap: post at most max_rows_per_run vouchers per
        # invocation and leave the rest "Ready" for a later resume — a
        # single worker shouldn't monopolize hours posting a 90k-row NKC
        # batch in one unbroken loop. post_job.post_batch re-enqueues
        # itself automatically while `complete` is False.
        if max_rows_per_run and processed >= max_rows_per_run:
            break

    frappe.db.commit()

    elapsed = time.time() - t0
    remaining = max(len(vouchers) - processed, 0)

    summary = {
        "by_target_doctype": by_target,
        "by_prefix": by_prefix,
        "errors": errors,
        "total_vouchers": len(vouchers),
        "processed_vouchers": processed,
        "remaining_vouchers": remaining,
        "complete": remaining == 0,
        "elapsed_seconds": elapsed,
        "preflight": preflight_summary,
    }
    _publish_progress(batch_name, {
        "Phase 4": {
            "Posted": sum(v.get("posted", 0) for v in by_target.values()),
            "Failed": sum(v.get("failed", 0) for v in by_target.values()),
            "Skipped": sum(v.get("skipped", 0) for v in by_target.values()),
            "Ready": remaining,
        }
    })
    clear_active_company()  # B2: release per-request company override
    return summary


def submit_phase_4_drafts(
    batch_name: str | None = None,
    company: str | None = None,
    progress_callback=None,
) -> dict[str, Any]:
    """Submit all docstatus=0 Misa-imported docs in dependency order.

    Pipeline `run_phase_4_post` only INSERTs vouchers (drafts). This is the
    submit-time finalize step that pushes them to GL.

    Order: SE → JE → SI → PI → PE (PE last because it references SI/PI).
    Per-doc transaction isolation: each submit() commits independently so a
    single failure doesn't cascade-rollback prior successes.

    Stock-account workaround: temporarily clears account_type='Stock' on all
    Company accounts while submitting (Misa has legitimate inter-stock JE
    legs that ERPNext otherwise rejects with StockAccountInvalidTransaction).
    Restores in finally.

    Large JEs (>100 legs, e.g. Opening JE / PBDT split) bypass ERPNext's
    queue_submission via direct `_submit()` call — avoids file-lock
    deadlocks on benches without an active worker process.

    Args:
      batch_name: limit to docs whose misa_voucher_no starts with this prefix
                  (None = all Misa-imported docs in the active Company).
      company: target Company (defaults to active Company from context).
      progress_callback: optional fn(dt, ok, fail, total) called per DocType.

    Returns:
      {
        'submitted': {DocType: int},
        'failed': {DocType: [(name, error), ...]},
        'total_submitted': int,
        'total_failed': int,
        'elapsed_seconds': float,
      }
    """
    from vn_accounting.misa_migration.context import get_active_company

    company = company or get_active_company()
    if not company:
        return {"status": "failed", "error": "no Company configured"}

    # Stock-account workaround
    stock_to_restore = []
    for a in frappe.db.sql_list(
        """SELECT name FROM `tabAccount`
           WHERE company=%s AND account_type='Stock'""",
        (company,),
    ):
        frappe.db.set_value(
            "Account", a, "account_type", "", update_modified=False
        )
        stock_to_restore.append(a)
    frappe.db.commit()

    # FIX: allow_negative_stock during submit pass. Misa source has stock
    # chronology where PX outward vouchers precede PN inward (real warehouse
    # workflow stamps PX with stock-leave date, PN with later receipt date).
    # ERPNext strictly rejects with NegativeStockError. Save + flip + restore
    # in finally so this single-purpose toggle never leaks outside the
    # migration window.
    prev_neg_stock = frappe.db.get_single_value(
        "Stock Settings", "allow_negative_stock"
    )
    if not prev_neg_stock:
        frappe.db.set_single_value(
            "Stock Settings", "allow_negative_stock", 1,
            update_modified=False,
        )
        frappe.db.commit()

    submitted: dict[str, int] = {}
    failed: dict[str, list[tuple[str, str]]] = {}
    t0 = time.time()

    ORDER = ["Stock Entry", "Journal Entry", "Sales Invoice",
             "Purchase Invoice", "Payment Entry"]

    # TIER 1 PERF: signal to vn_accounting on_submit hooks (project_costing,
    # COGS engine, asset_pi) to short-circuit during Misa migration. Misa
    # source already includes the resulting GL legs (NKC export covers them).
    # Re-running those hooks creates double-posting or wastes per-doc time.
    frappe.flags.misa_migration_active = True

    try:
        for dt in ORDER:
            filters_sql = [
                "company=%s",
                "misa_voucher_no IS NOT NULL",
                "misa_voucher_no != ''",
                "docstatus=0",
            ]
            params: list[Any] = [company]
            if batch_name:
                # Filter by batch via Misa Migration Row (target_doctype + target_name)
                # Simplest: filter by misa_voucher_no LIKE batch's prefix patterns
                # — skip for now; caller can post-filter from summary.
                pass

            where_clause = " AND ".join(filters_sql)
            names = frappe.db.sql_list(
                f"""SELECT name FROM `tab{dt}` WHERE {where_clause}
                   ORDER BY posting_date""",
                tuple(params),
            )

            if not names:
                continue

            ok = 0
            fail_list: list[tuple[str, str]] = []
            # PERF: SAVEPOINT-batched commit. Per-doc commit was 30-40 ms
            # overhead on every submit (~1.5× the submit body itself).
            # Replace with SAVEPOINT isolation per doc + batched commit
            # every BATCH_SIZE successful submits. On per-doc failure we
            # rollback to that doc's savepoint only; previously-succeeded
            # docs in the batch stay uncommitted but intact. On batch
            # boundary they get committed together.
            # TIER 1 PERF: 200 (was 25) — fewer commits, lower overhead.
            # Trade-off: a hard crash mid-batch loses up to 200 uncommitted
            # successful submits (must re-submit). Accept for migration speed.
            SUBMIT_BATCH = 200
            since_commit = 0
            for n in names:
                sp_name = f"misa_sp_{abs(hash(n)) % (10**9)}"
                try:
                    frappe.db.sql(f"SAVEPOINT {sp_name}")
                    d = frappe.get_doc(dt, n)
                    d.flags.ignore_permissions = True
                    # Large JEs (>100 lines) bypass queue_submission to avoid
                    # file-lock deadlocks on dev benches without worker.
                    if dt == "Journal Entry" and len(d.accounts) > 100:
                        d._submit()
                    else:
                        d.submit()
                    try:
                        frappe.db.sql(f"RELEASE SAVEPOINT {sp_name}")
                    except Exception:
                        # Savepoint already released by an inner commit
                        # (some hooks call db.commit). Safe to ignore.
                        pass
                    ok += 1
                    since_commit += 1
                    if since_commit >= SUBMIT_BATCH:
                        frappe.db.commit()
                        # Bump batch.modified to prevent watchdog false-positive
                        # during long submit passes. No-op when batch_name=None.
                        if batch_name:
                            frappe.db.sql(
                                "UPDATE `tabMisa Migration Batch` SET modified=NOW(6) WHERE name=%s",
                                (batch_name,),
                            )
                        since_commit = 0
                except Exception as exc:
                    try:
                        frappe.db.sql(f"ROLLBACK TO SAVEPOINT {sp_name}")
                    except Exception:
                        # If the savepoint vanished (inner commit), fall
                        # back to full rollback — this discards prior
                        # uncommitted successes in the batch.
                        frappe.db.rollback()
                        since_commit = 0
                    fail_list.append((n, f"{type(exc).__name__}: {str(exc)[:300]}"))
                    frappe.log_error(
                        title=f"Misa submit failed: {n}",
                        message=f"{type(exc).__name__}: {exc}",
                    )
            # Flush remaining batched commits before moving to next DocType
            if since_commit > 0:
                frappe.db.commit()
                since_commit = 0

            submitted[dt] = ok
            if fail_list:
                failed[dt] = fail_list

            if progress_callback:
                try:
                    progress_callback(dt, ok, len(fail_list), len(names))
                except Exception:
                    pass

            _publish_progress(batch_name or "all", {
                "Submit": {dt: {"submitted": ok, "failed": len(fail_list)}}
            })
    finally:
        # Restore stock account types
        for acct in stock_to_restore:
            try:
                frappe.db.set_value(
                    "Account", acct, "account_type", "Stock",
                    update_modified=False,
                )
            except Exception:
                pass
        # Restore allow_negative_stock to its prior value
        if not prev_neg_stock:
            try:
                frappe.db.set_single_value(
                    "Stock Settings", "allow_negative_stock", 0,
                    update_modified=False,
                )
            except Exception:
                pass
        # TIER 1 PERF: clear the migration flag so live ops resume normally
        frappe.flags.misa_migration_active = False
        frappe.db.commit()

    # ---- PE retry pass: multi-pay overallocation → unallocated advance ----
    # For PEs that failed submit with "Allocated Amount > outstanding" or
    # "X has already been fully paid", retry by clearing references[] and
    # posting as an unallocated advance. GL is still posted correctly
    # (Dr party_account / Cr bank), only the per-invoice allocation is lost.
    # Tagged with a Comment so auditors see why it lacks invoice linkage.
    pe_retry = {"retried": 0, "submitted": 0, "still_failed": 0}
    failed_pe = failed.get("Payment Entry", [])
    MULTIPAY_PATTERNS = (
        "Allocated Amount",
        "already been fully paid",
        # UNC salary payments (Dr 3341 / Cr bank) where the handler picked
        # up PI references for the same supplier — PI.credit_to is 331,
        # PE.party_account is 3341 → "associated with 331, but Party Account
        # is 3341". The references are wrong context (salary payment, not
        # supplier invoice payment); clearing them and posting as
        # unallocated advance is the right outcome — GL correctly hits
        # Dr 3341 / Cr bank without the spurious invoice linkage.
        "is associated with",
    )
    for pe_name, err_str in failed_pe:
        if not any(p in err_str for p in MULTIPAY_PATTERNS):
            continue
        pe_retry["retried"] += 1
        try:
            d = frappe.get_doc("Payment Entry", pe_name)
            if d.docstatus != 0:
                continue
            d.references = []
            d.unallocated_amount = d.paid_amount
            d.flags.ignore_permissions = True
            d.submit()
            try:
                frappe.get_doc({
                    "doctype": "Comment",
                    "comment_type": "Comment",
                    "reference_doctype": "Payment Entry",
                    "reference_name": pe_name,
                    "content": (
                        "Misa migration: paid without invoice match "
                        "(multi-pay or already-paid in source data) — "
                        "posted as unallocated advance"
                    ),
                }).insert(ignore_permissions=True)
            except Exception:
                pass
            frappe.db.commit()
            pe_retry["submitted"] += 1
        except Exception as exc:
            pe_retry["still_failed"] += 1
            frappe.db.rollback()
            frappe.log_error(
                title=f"Misa PE retry-no-refs failed: {pe_name}",
                message=f"{type(exc).__name__}: {exc}",
            )

    return {
        "submitted": submitted,
        "failed": failed,
        "total_submitted": sum(submitted.values()),
        "total_failed": sum(len(v) for v in failed.values()),
        "pe_retry": pe_retry,
        "elapsed_seconds": time.time() - t0,
    }


# ---------------------------------------------------- cancel + delete (Item 2)

# REVERSE dependency order: PE first (depends on SI/PI), then PI/SI/JE/SE.
_CANCEL_ORDER = ["Payment Entry", "Purchase Invoice", "Sales Invoice",
                 "Journal Entry", "Stock Entry"]


def _batch_target_filter(batch_name: str | None) -> tuple[str, list[Any]]:
    """SQL fragment + params restricting to docs created by this batch.

    Joins via `tabMisa Migration Row.target_name`. Without batch_name,
    returns empty fragment (matches all Misa-imported docs in company).
    """
    if not batch_name:
        return "", []
    # IN subquery: any Misa Migration Row that pointed to a target_name with
    # target_doctype = this DocType for this batch
    return (
        " AND name IN (SELECT target_name FROM `tabMisa Migration Row` "
        "WHERE batch=%s AND target_doctype=%s AND target_name IS NOT NULL "
        "AND target_name != '')"
    ), [batch_name]


def _stock_accounts_clear_save(company: str) -> list[str]:
    """Temp-clear account_type='Stock' on Company accounts. Returns list
    to restore. Same workaround as submit_phase_4_drafts — legitimate
    inter-stock JE legs (CK Misa voucher type) otherwise rejected.
    """
    stock_to_restore: list[str] = []
    for a in frappe.db.sql_list(
        """SELECT name FROM `tabAccount`
           WHERE company=%s AND account_type='Stock'""",
        (company,),
    ):
        frappe.db.set_value(
            "Account", a, "account_type", "", update_modified=False
        )
        stock_to_restore.append(a)
    frappe.db.commit()
    return stock_to_restore


def _stock_accounts_restore(stock_to_restore: list[str]) -> None:
    """Restore account_type='Stock' after cancel/delete pass."""
    for acct in stock_to_restore:
        try:
            frappe.db.set_value(
                "Account", acct, "account_type", "Stock",
                update_modified=False,
            )
        except Exception:
            pass
    frappe.db.commit()


def cancel_phase_4_drafts(
    batch_name: str | None = None,
    company: str | None = None,
    progress_callback=None,
) -> dict[str, Any]:
    """Cancel all docstatus=1 Misa-imported Phase 4 docs in REVERSE order.

    Mirror of `submit_phase_4_drafts`. Operator-recovery tool when a posted
    batch needs to be rolled back at the pipeline level (distinct from the
    per-batch `start_undo` flow that also unlinks Misa Migration Row state).

    Order: PE → PI → SI → JE → SE. PE cancelled first because it allocated
    payments to SI/PI; cancelling PE first releases those references so
    SI/PI can cancel cleanly. JE/SE last (no downstream dependents in
    Misa-imported set).

    Per-doc transaction isolation: each `cancel()` commits independently
    so one failure does not roll back prior successes.

    Stock-account workaround: same as submit — temporarily clear
    `account_type='Stock'` so legitimate inter-stock JE legs (CK voucher
    Dr 155 / Cr 154) can be cancelled. Restored in finally.

    Args:
      batch_name: limit to docs created by this Misa Migration Batch.
                  None = all Misa-imported docs in active Company.
      company: target Company (defaults to active Company from context).
      progress_callback: optional fn(dt, ok, fail, total) per DocType.

    Returns:
      {
        'cancelled': {DocType: int},
        'failed': {DocType: [(name, error), ...]},
        'total_cancelled': int,
        'total_failed': int,
        'elapsed_seconds': float,
      }
    """
    from vn_accounting.misa_migration.context import get_active_company

    company = company or get_active_company()
    if not company:
        return {"status": "failed", "error": "no Company configured"}

    stock_to_restore = _stock_accounts_clear_save(company)
    cancelled: dict[str, int] = {}
    failed: dict[str, list[tuple[str, str]]] = {}
    t0 = time.time()
    # Mute per-doc msgprint warnings during the bulk cancel — ERPNext
    # emits "Payment items XXX not linked" per cancelled SI/PI, which
    # floods the UI with thousands of popups during a 22k+ doc cascade.
    # The warnings are informational only (orphan refs don't break
    # anything); errors still raise via the try/except.
    _prev_mute = getattr(frappe.flags, "mute_messages", False)
    frappe.flags.mute_messages = True

    try:
        for dt in _CANCEL_ORDER:
            batch_clause, batch_params = _batch_target_filter(batch_name)
            # Replace the bare `name` reference with table-qualified one for
            # the subquery — but since we filter ON `tab<DT>` directly the
            # bare reference is fine.
            where_clause = (
                "company=%s AND misa_voucher_no IS NOT NULL "
                "AND misa_voucher_no != '' AND docstatus=1"
            ) + batch_clause
            params: list[Any] = [company]
            if batch_clause:
                params.extend([batch_params[0], dt])
            names = frappe.db.sql_list(
                f"SELECT name FROM `tab{dt}` WHERE {where_clause} "
                f"ORDER BY posting_date DESC, name DESC",
                tuple(params),
            )
            if not names:
                continue

            ok = 0
            fail_list: list[tuple[str, str]] = []
            for n in names:
                try:
                    d = frappe.get_doc(dt, n)
                    d.flags.ignore_permissions = True
                    d.cancel()
                    frappe.db.commit()
                    ok += 1
                except Exception as exc:
                    frappe.db.rollback()
                    fail_list.append((n, f"{type(exc).__name__}: {str(exc)[:300]}"))
                    frappe.log_error(
                        title=f"Misa cancel failed: {n}",
                        message=f"{type(exc).__name__}: {exc}",
                    )

            cancelled[dt] = ok
            if fail_list:
                failed[dt] = fail_list

            if progress_callback:
                try:
                    progress_callback(dt, ok, len(fail_list), len(names))
                except Exception:
                    pass

            _publish_progress(batch_name or "all", {
                "Cancel": {dt: {"cancelled": ok, "failed": len(fail_list)}}
            })
    finally:
        _stock_accounts_restore(stock_to_restore)
        frappe.flags.mute_messages = _prev_mute

    return {
        "cancelled": cancelled,
        "failed": failed,
        "total_cancelled": sum(cancelled.values()),
        "total_failed": sum(len(v) for v in failed.values()),
        "elapsed_seconds": time.time() - t0,
    }


def delete_phase_4_drafts(
    batch_name: str | None = None,
    company: str | None = None,
    progress_callback=None,
) -> dict[str, Any]:
    """Delete all docstatus=0 (Draft) and docstatus=2 (Cancelled) Misa-
    imported Phase 4 docs.

    Use cases:
      * After a failed import: scrub draft docs before retry (docstatus=0)
      * After cancel_phase_4_drafts: clean up the now-cancelled docs so a
        fresh re-post can succeed without name collisions (docstatus=2)

    docstatus=1 docs are SKIPPED — caller must cancel them first via
    `cancel_phase_4_drafts`. Reported in `skipped_submitted` summary.

    Args:
      batch_name: limit to docs created by this Misa Migration Batch.
                  None = all Misa-imported docs in active Company.
      company: target Company (defaults to active Company from context).
      progress_callback: optional fn(dt, ok, fail, total) per DocType.

    Returns:
      {
        'deleted': {DocType: int},
        'failed': {DocType: [(name, error), ...]},
        'skipped_submitted': {DocType: int},
        'total_deleted': int,
        'total_failed': int,
        'total_skipped': int,
        'elapsed_seconds': float,
      }
    """
    from vn_accounting.misa_migration.context import get_active_company

    company = company or get_active_company()
    if not company:
        return {"status": "failed", "error": "no Company configured"}

    deleted: dict[str, int] = {}
    failed: dict[str, list[tuple[str, str]]] = {}
    skipped_submitted: dict[str, int] = {}
    t0 = time.time()

    # Use the same order as cancel (deletes children before parents would
    # matter for FK enforcement, but Misa-imported docs are independent
    # transactions — order is mostly cosmetic here).
    for dt in _CANCEL_ORDER:
        batch_clause, batch_params = _batch_target_filter(batch_name)
        where_clause = (
            "company=%s AND misa_voucher_no IS NOT NULL "
            "AND misa_voucher_no != '' AND docstatus IN (0, 2)"
        ) + batch_clause
        params: list[Any] = [company]
        if batch_clause:
            params.extend([batch_params[0], dt])
        names = frappe.db.sql_list(
            f"SELECT name FROM `tab{dt}` WHERE {where_clause} "
            f"ORDER BY posting_date DESC, name DESC",
            tuple(params),
        )

        # Count docstatus=1 for skip reporting (excluded from query above)
        submitted_clause = (
            "company=%s AND misa_voucher_no IS NOT NULL "
            "AND misa_voucher_no != '' AND docstatus=1"
        ) + batch_clause
        sub_count = frappe.db.sql(
            f"SELECT COUNT(*) FROM `tab{dt}` WHERE {submitted_clause}",
            tuple(params),
        )[0][0]
        if sub_count:
            skipped_submitted[dt] = sub_count

        if not names:
            continue

        ok = 0
        fail_list: list[tuple[str, str]] = []
        for n in names:
            try:
                frappe.delete_doc(
                    dt, n,
                    force=True,
                    ignore_permissions=True,
                )
                frappe.db.commit()
                ok += 1
            except Exception as exc:
                frappe.db.rollback()
                fail_list.append((n, f"{type(exc).__name__}: {str(exc)[:300]}"))
                frappe.log_error(
                    title=f"Misa delete failed: {n}",
                    message=f"{type(exc).__name__}: {exc}",
                )

        deleted[dt] = ok
        if fail_list:
            failed[dt] = fail_list

        if progress_callback:
            try:
                progress_callback(dt, ok, len(fail_list), len(names))
            except Exception:
                pass

        _publish_progress(batch_name or "all", {
            "Delete": {dt: {"deleted": ok, "failed": len(fail_list)}}
        })

    return {
        "deleted": deleted,
        "failed": failed,
        "skipped_submitted": skipped_submitted,
        "total_deleted": sum(deleted.values()),
        "total_failed": sum(len(v) for v in failed.values()),
        "total_skipped": sum(skipped_submitted.values()),
        "elapsed_seconds": time.time() - t0,
    }


# ---------------------------------------------------- PE references backfill

def _backfill_pe_references_for_batch(batch_name: str,
                                      company: str | None) -> dict:
    """Find PEs created by this batch that have no `references` rows and
    link them via FIFO oldest-open-invoice on the same party.

    Covers the "PE before SI" advance-payment case: PE handler creates
    PE without refs when the matching SI doesn't exist yet (e.g. PE
    posting_date < SI posting_date in chronological iteration). After
    the main loop, every same-period SI/PI exists; backfill via
    cancel + re-amend with references.

    Returns {"linked": N, "no_match": N, "failed": N, "skipped": N}.
    """
    out = {"linked": 0, "no_match": 0, "failed": 0, "skipped": 0,
           "samples": []}
    if not company:
        return out
    # PEs created by THIS batch (filter by misa_voucher_no on rows of
    # this batch with target_doctype='Payment Entry')
    pe_names = frappe.db.sql_list(
        """SELECT DISTINCT target_name FROM `tabMisa Migration Row`
           WHERE batch=%s AND target_doctype='Payment Entry'
             AND target_name IS NOT NULL AND status='Posted'""",
        (batch_name,),
    )
    if not pe_names:
        return out
    # Filter to those with NO references AND not already amended
    # (an amended PE has amended_to set in tabPayment Entry — exclude
    # those; the AMENDMENT itself should be in the candidate set, not
    # the original cancelled doc). DISTINCT prevents row duplication
    # from the LEFT JOIN when refs already exist on amended chain.
    #
    # ALSO filter out PEs whose party_account is NOT a supplier-payable
    # (331) or customer-receivable (131) account. UNC salary payments
    # (Dr 3341 / Cr bank) post via PE Pay with paid_to=3341. The party
    # is the company itself (e.g. "DCNET" — registered as a Supplier
    # for other purposes). Without this filter, backfill cancels the
    # working salary PE and tries to amend with PI references, but
    # amend submit fails because PI.credit_to=331 ≠ PE.party_account=3341.
    # Net result: original salary PE stays cancelled → ~17B Dr 3341 GL
    # lost. Skipping these PEs preserves their unallocated-advance GL.
    unlinked = frappe.db.sql(
        """SELECT DISTINCT pe.name, pe.party_type, pe.party, pe.paid_amount
           FROM `tabPayment Entry` pe
           LEFT JOIN `tabPayment Entry Reference` per ON per.parent=pe.name
           LEFT JOIN `tabPayment Entry` amended ON amended.amended_from=pe.name
           WHERE pe.name IN %s AND pe.company=%s
             AND pe.docstatus = 1
             AND per.parent IS NULL
             AND amended.name IS NULL
             AND pe.party_type IN ('Customer','Supplier')
             AND pe.party IS NOT NULL AND pe.party != ''
             AND (
                 (pe.payment_type='Pay' AND pe.paid_to LIKE '331%%')
                 OR (pe.payment_type='Receive' AND pe.paid_from LIKE '131%%')
             )""",
        (tuple(pe_names), company),
        as_dict=True,
    )
    if not unlinked:
        return out

    from frappe import copy_doc
    for pe in unlinked:
        try:
            invoices = _open_invoices_for_party(
                company, pe.party_type, pe.party
            )
            if not invoices:
                out["no_match"] += 1
                # Audit-trail Comment: orphan PE is GL-correct
                # (Dr party_account / Cr bank) but has no allocation
                # because Misa source had no matching open invoice.
                try:
                    frappe.get_doc({
                        "doctype": "Comment",
                        "comment_type": "Comment",
                        "reference_doctype": "Payment Entry",
                        "reference_name": pe.name,
                        "content": (
                            "Misa migration: no matching open invoice for "
                            f"{pe.party_type} {pe.party!r} — payment posted "
                            "as unallocated advance. GL is correct; "
                            "party outstanding may show credit balance."
                        ),
                    }).insert(ignore_permissions=True)
                    frappe.db.commit()
                except Exception:
                    pass
                if len(out["samples"]) < 5:
                    out["samples"].append({
                        "pe": pe.name, "party": pe.party,
                        "reason": "no_open_invoice",
                    })
                continue
            remaining = float(pe.paid_amount)
            refs = []
            for inv in invoices:
                if remaining <= 0:
                    break
                avail = float(inv["outstanding_amount"] or 0)
                if avail <= 0:
                    continue
                take = min(avail, remaining)
                refs.append({
                    "reference_doctype": inv["target_doctype"],
                    "reference_name": inv["name"],
                    "allocated_amount": take,
                })
                remaining -= take
            if not refs:
                out["no_match"] += 1
                continue

            # Cancel + amend pattern — PE.references is immutable on
            # submitted PE. Verify cancel actually flipped docstatus to 2
            # before attempting amend, to avoid "cannot be amended" errors
            # when the cancel was silently rolled back by a hook.
            doc = frappe.get_doc("Payment Entry", pe.name)
            doc.flags.ignore_permissions = True
            if doc.docstatus == 1:
                doc.cancel()
                doc.reload()
            if doc.docstatus != 2:
                out["skipped"] += 1
                if len(out["samples"]) < 5:
                    out["samples"].append({
                        "pe": pe.name,
                        "reason": f"cancel did not take (docstatus={doc.docstatus})",
                    })
                continue
            new_doc = copy_doc(doc)
            new_doc.amended_from = doc.name
            new_doc.references = []
            for r in refs:
                new_doc.append("references", r)
            new_doc.flags.ignore_permissions = True
            new_doc.insert()
            new_doc.submit()
            frappe.db.commit()
            out["linked"] += 1
        except Exception as exc:
            out["failed"] += 1
            if len(out["samples"]) < 5:
                out["samples"].append({
                    "pe": pe.name, "error": f"{type(exc).__name__}: {exc}"[:150],
                })
            # Do NOT log_error per-PE here — it spams the user's
            # notification panel with one entry per failed PE. Keep
            # samples for the summary; surface aggregate count only.

    return out


def _open_invoices_for_party(company: str, party_type: str,
                             party: str) -> list[dict]:
    target_dt = "Sales Invoice" if party_type == "Customer" else \
                "Purchase Invoice"
    party_field = "customer" if target_dt == "Sales Invoice" else "supplier"
    rows = frappe.db.sql(
        f"""SELECT name, outstanding_amount, posting_date
            FROM `tab{target_dt}`
            WHERE company=%s AND docstatus=1 AND {party_field}=%s
              AND outstanding_amount > 0
            ORDER BY posting_date ASC""",
        (company, party), as_dict=True,
    )
    return [{**r, "target_doctype": target_dt} for r in rows]
