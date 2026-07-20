"""Misa Migration post API — Phase B + Phase D preflight integration."""

from __future__ import annotations

import json

import frappe
from frappe import _

from vn_accounting.misa_migration import state as st
from vn_accounting.misa_migration.importers import preflight as _phase_d_preflight
from vn_accounting.misa_migration.importers.orchestrator import get_counts
from vn_accounting.misa_migration.jobs import post_job
from vn_accounting.misa_migration.parsers import (
    invoice_list_parser,
    nkc_parser,
)


_PHASE_4_FILE_TYPES = ("NKC", "Bang ke BR", "Bang ke MV")


def _collect_phase_4_payloads(batch_name: str) -> dict[str, list[dict]]:
    """Pull NKC/BR/MV raw_payload rows for a batch and return them grouped by
    file_type. Each row's raw_payload is decoded; malformed rows are skipped.
    """
    rows = frappe.db.sql(
        """
        SELECT file_type, raw_payload
        FROM `tabMisa Migration Row`
        WHERE batch=%s
          AND file_type IN ('NKC', 'Bang ke BR', 'Bang ke MV')
        """,
        (batch_name,),
        as_dict=True,
    )
    grouped: dict[str, list[dict]] = {ft: [] for ft in _PHASE_4_FILE_TYPES}
    for r in rows:
        ft = r["file_type"]
        try:
            payload = json.loads(r["raw_payload"] or "{}")
        except (TypeError, ValueError):
            continue
        if isinstance(payload, dict):
            grouped.setdefault(ft, []).append(payload)
    return grouped


def _run_phase_d_preflight(batch_name: str) -> dict | None:
    """Parse Phase 4 raw payloads → run the 10-check pipeline.

    Returns None if the batch has no NKC/BR/MV rows (Phase 1+2-only batch).
    """
    grouped = _collect_phase_4_payloads(batch_name)
    if not any(grouped.get(ft) for ft in _PHASE_4_FILE_TYPES):
        return None

    vouchers = nkc_parser.parse_nkc_rows(grouped.get("NKC") or [])
    br_list = invoice_list_parser.parse_invoice_list(
        grouped.get("Bang ke BR") or [], kind="BR"
    )
    mv_list = invoice_list_parser.parse_invoice_list(
        grouped.get("Bang ke MV") or [], kind="MV"
    )
    # Preflight checks need a dual-key lookup (voucher_no + invoice_no)
    # so warning checks resolve Misa's 1-invoice-N-vouchers chain via
    # Số hóa đơn fallback. InvoiceLookup is dict-compatible for legacy
    # callers + adds .find()/.has() for the new fallback path.
    from vn_accounting.misa_migration.importers.phase_4_orchestrator import InvoiceLookup
    br_invoices = InvoiceLookup(br_list)
    mv_invoices = InvoiceLookup(mv_list)

    company = (
        frappe.db.get_value("Misa Migration Batch", batch_name, "company")
        or frappe.defaults.get_global_default("company")
        or frappe.db.get_value("Company", {}, "name")
    )
    return _phase_d_preflight.run_preflight(
        vouchers=vouchers,
        br_invoices=br_invoices,
        mv_invoices=mv_invoices,
        company=company,
    )


@frappe.whitelist()
def preflight(batch_name: str) -> dict:
    """Aggregate Phase B (row-status counts) + Phase D (10-check pipeline).

    Backward-compatible: existing fields (blocked/warnings/n_invalid/...)
    retained for Phase 1+2-only batches. When Phase 4 rows exist the
    'checks' field carries the structured C13 envelope and any block-level
    issues from those checks are also appended to 'blocked' for the
    legacy UI path.
    """
    counts = get_counts(batch_name)
    blocked = []
    warnings = []
    n_invalid = sum(c.get("Invalid", 0) for c in counts.values())
    n_conflict = sum(c.get("Conflict", 0) for c in counts.values())
    n_ready = sum(c.get("Ready", 0) for c in counts.values())

    if n_invalid > 0:
        blocked.append(_("Có {0} dòng Invalid — sửa hoặc skip trước khi post.").format(n_invalid))
    if n_conflict > 0:
        warnings.append(_("Có {0} dòng Conflict cần resolve.").format(n_conflict))
    if n_ready == 0 and not warnings and not blocked:
        warnings.append(_("Không có dòng nào ở trạng thái Ready để post."))

    phase_d_envelope = None
    try:
        phase_d_envelope = _run_phase_d_preflight(batch_name)
    except Exception as exc:
        warnings.append(
            _("Pre-flight Phase 4 lỗi: {0}").format(str(exc)[:200])
        )

    if phase_d_envelope:
        for c in phase_d_envelope["checks"]:
            if c["level"] == "block" and not c["passed"]:
                for issue in c["issues"]:
                    blocked.append(f"[{c['label']}] {issue}")
            elif c["level"] == "warn" and not c["passed"]:
                for issue in c["issues"]:
                    warnings.append(f"[{c['label']}] {issue}")

    # UX Gap 7 — Phase 0 prerequisite checks. Detects missing
    # master data (Customer / Supplier / Employee / Item / Warehouse /
    # Asset Category / bank-leaf accounts) that would cause OB import
    # to silently drop balances or fail mid-stream.
    phase_0_envelope = None
    try:
        from vn_accounting.misa_migration.importers.phase_0_preflight import (
            check_phase_0_prerequisites,
        )
        phase_0_envelope = check_phase_0_prerequisites(batch_name)
    except Exception as exc:
        warnings.append(
            _("Pre-flight Phase 0 lỗi: {0}").format(str(exc)[:200])
        )

    if phase_0_envelope:
        for c in phase_0_envelope["checks"]:
            label_with_phase = f"Phase 0 / {c['file_type']} — {c['label']}"
            if c["level"] == "block" and not c["passed"]:
                for issue in c["issues"]:
                    blocked.append(f"[{label_with_phase}] {issue} → {c['hint']}")
            elif c["level"] == "warn" and not c["passed"]:
                for issue in c["issues"]:
                    warnings.append(f"[{label_with_phase}] {issue} → {c['hint']}")

    return {
        "batch": batch_name, "counts": counts,
        "blocked": blocked, "warnings": warnings,
        "n_invalid": n_invalid, "n_conflict": n_conflict, "n_ready": n_ready,
        "checks": (phase_d_envelope or {}).get("checks", []),
        "phase_d_status": (phase_d_envelope or {}).get("status"),
        # UX Gap 7 — surface structured Phase 0 prerequisite check
        # results for richer UI display (label / level / hint / counts).
        "phase_0_checks": (phase_0_envelope or {}).get("checks", []),
        "phase_0_status": (phase_0_envelope or {}).get("status"),
    }


@frappe.whitelist()
def prewarm_masters(company: str) -> dict:
    """Pre-create COA leaves, Company defaults, and Party accounts BEFORE
    launching parallel shards.

    Two shards posting concurrently both call ``run_preflight_setup`` at
    worker start; while the underlying ensure_* helpers are idempotent,
    concurrent writes to Company defaults and Party Account child rows
    can briefly contend on row-level locks. Running this once before
    dispatch eliminates the contention window AND avoids 2× the wall
    time inside the workers.

    Also pre-warms the in-memory Account cache that handlers rely on for
    fast Misa TK → leaf-account resolution.

    Acquires the company-wide lock (NOT shard-scoped) for the duration so
    a concurrent batch-create or sharded prewarm can't run in parallel
    with the master mutations.

    Args:
        company: Company name (required).

    Returns:
        {
            "company": str,
            "preflight": <preflight setup summary>,
            "account_cache_size": int,  # entries pre-warmed
            "elapsed_seconds": float,
        }
    """
    import time as _time
    if not company:
        frappe.throw(_("Phải chọn Company."))
    if not frappe.db.exists("Company", company):
        frappe.throw(_("Company không tồn tại: {0}").format(company))

    from vn_accounting.misa_migration.context import set_active_company
    from vn_accounting.misa_migration.importers.phase_4_orchestrator import (
        run_preflight_setup,
    )
    from vn_accounting.misa_migration.importers.nkc_handlers.payment_entry import (
        _warm_account_cache_for_company, reset_perf_caches,
        _ACCOUNT_BY_NUMBER_CACHE,
    )

    t0 = _time.time()
    # Company-wide lock (no shard token) — serializes against any other
    # prewarm or create_batch call for this Company.
    with st.lock_for_company(company, timeout=30):
        set_active_company(company)
        preflight_summary = run_preflight_setup(company)
        reset_perf_caches()
        _warm_account_cache_for_company(company)
        cache_size = len(_ACCOUNT_BY_NUMBER_CACHE)

    # PERF (Tier 1.1): Redis-cached flag so workers can short-circuit
    # the per-shard run_preflight_setup. ~1hr TTL covers a long parallel
    # run; refresh on every prewarm call so back-to-back runs keep the
    # contract alive.
    frappe.cache().set_value(
        prewarm_flag_key(company), 1, expires_in_sec=3600
    )

    return {
        "company": company,
        "preflight": preflight_summary,
        "account_cache_size": cache_size,
        "elapsed_seconds": _time.time() - t0,
        "prewarmed_flag_set": True,
    }


# PERF (Tier 1.1): cache key contract for the prewarm-done flag.
# Workers in run_phase_4_post check this; prewarm_masters sets it after
# the company-wide lock has serialized the master-data mutations. When
# this is set, parallel shards skip their own preflight setup and avoid
# racing on Company / Party Account row-level locks.
def prewarm_flag_key(company: str) -> str:
    return f"misa:masters_prewarmed:{company}"


@frappe.whitelist()
def install_misa_coa(batch_name: str) -> dict:
    """Bootstrap Phase 1 (master refs) + Phase 2 (CoA) + Phase 3 (party masters).

    Fresh-wipe scenarios (no baseline CoA, no Customer/Supplier/Item masters)
    cause Misa Account importer to throw "must be a group" because root
    accounts and short-prefix candidates don't exist. Fix: call
    ``bootstrap_coa`` FIRST to install vn_accounting TT99/2025 baseline,
    then iterate Phase 1+2+3 file types. Brings preflight from BLOCK → OK
    so the operator can click ``Đăng vào ERPNext`` or
    ``⚡ Đăng chế độ nhanh (SQL)`` without manual SQL prep.

    Safe to re-run — bootstrap_coa is idempotent (no-op when
    ``Account count > 5``), and each importer.lookup_existing guards
    against duplicate inserts.
    """
    if not batch_name:
        frappe.throw(_("Phải chọn batch."))

    company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")
    if not company:
        frappe.throw(_("Batch không có Company."))

    from vn_accounting.misa_migration.importers.orchestrator import (
        importer_for_file_type,
    )
    from vn_accounting.misa_migration.bulk_pump.coa_bootstrap import (
        bootstrap_coa,
    )

    # Step 0: ensure base CoA exists. bootstrap_coa is idempotent — skips if
    # Company already has accounts. Without this step, fresh sites (post-wipe,
    # post-install) have 0 accounts and Phase 1/2 Misa row loop below does
    # nothing useful — leaving the user with no CoA + downstream bulk_pump
    # failing on missing receivable / cash / income default accounts.
    company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")
    bootstrap_result = None
    if company:
        try:
            bootstrap_result = bootstrap_coa(company)
        except Exception as exc:
            frappe.log_error(
                title=f"bootstrap_coa failed during install_misa_coa: {company}",
                message=str(exc),
            )
            bootstrap_result = {"error": str(exc)}

    # When Standard CoA detected (non-VN), bail out before running Phase 1/2
    # importers — they'd attach Misa rows to wrong account tree. UI handles
    # the 'non_vn_coa_detected' branch by prompting user for force-overwrite.
    if bootstrap_result and bootstrap_result.get("action") == "non_vn_coa_detected":
        return {
            "batch": batch_name,
            "bootstrap_coa": bootstrap_result,
            "phase_2_summary": {},
            "skipped_reason": "non_vn_coa_detected",
        }

    # Step 0: baseline VAS CoA — required before Misa Account importer runs.
    # vn_accounting's TT99/2025 template installs ~185 accounts incl. roots
    # (Asset/Liability/...) + 111/112/131/242/333/... leaves. Misa Account
    # importer then promotes those leaves to groups as needed to host
    # Misa-specific Tier-5 sub-accounts (1111, 1121.81, 1311, ...).
    from vn_accounting.misa_migration.bulk_pump.coa_bootstrap import bootstrap_coa
    bootstrap_summary = bootstrap_coa(company)

    # Phase 1 (reference masters) + Phase 2 (chart of accounts + defaults) +
    # Phase 3 (party masters). Order matches PHASE_1_2_3_IMPORTERS declared
    # order; party masters last so Customer/Supplier/Item have all the
    # parent group + account refs they depend on.
    _BOOTSTRAP_FILE_TYPES = (
        # Phase 1
        "UOM",
        "Bank",
        "Department",
        "Warehouse",
        "Item Group",
        "Customer Group",
        "Supplier Group",
        "Cost Center",
        "Project",
        "Asset Category",
        "CCDC Category",
        # Phase 2
        "Account",
        "Misa Default Account",
        # Phase 3 — party masters (depend on Phase 1+2 above)
        "Customer",
        "Supplier",
        "Item",
        "Employee",
        "Bank Account",
    )

    summary: dict[str, dict] = {}
    for ft in _BOOTSTRAP_FILE_TYPES:
        importer = importer_for_file_type(ft, batch_name)
        if not importer:
            continue

        # Step 1: preview any unfinished rows so status flips to
        # Ready/Conflict/Invalid/Exists. Include 'Failed' so rows that
        # erred in a prior run (e.g. before bootstrap_coa was added)
        # get re-classified against current DB state — they may now be
        # Exists if a peer call created the parent, or Ready if the
        # blocker has been resolved (e.g. parent group auto-promoted).
        new_names = frappe.db.sql_list(
            """SELECT name FROM `tabMisa Migration Row`
               WHERE batch=%s AND file_type=%s AND status IN ('New','Failed')
               ORDER BY
                 CASE WHEN file_type='Account'
                      THEN CHAR_LENGTH(COALESCE(JSON_UNQUOTE(JSON_EXTRACT(parsed_payload, '$._tk')), ''))
                      ELSE 0
                 END, row_index""",
            (batch_name, ft),
        )
        for n in new_names:
            importer.preview_row(frappe.get_doc("Misa Migration Row", n))

        # Step 2: post Ready rows.
        ready_names = frappe.db.sql_list(
            """SELECT name FROM `tabMisa Migration Row`
               WHERE batch=%s AND file_type=%s AND status='Ready'
               ORDER BY
                 CASE WHEN file_type='Account'
                      THEN CHAR_LENGTH(COALESCE(JSON_UNQUOTE(JSON_EXTRACT(parsed_payload, '$._tk')), ''))
                      ELSE 0
                 END, row_index""",
            (batch_name, ft),
        )
        for n in ready_names:
            importer.post_row(frappe.get_doc("Misa Migration Row", n))

        finalize = getattr(importer, "finalize", None)
        if callable(finalize):
            try:
                fin = finalize()
                if fin:
                    importer.counts["finalize"] = fin
            except Exception as exc:
                frappe.log_error(
                    title=f"Misa finalize failed during install_misa_coa: {ft}",
                    message=str(exc),
                )

        summary[ft] = dict(importer.counts)
        frappe.db.commit()

    return {
        "batch": batch_name,
        "company": company,
        "bootstrap_coa": bootstrap_summary,
        "phase_2_summary": summary,
    }


@frappe.whitelist()
def clear_prewarm_flag(company: str) -> dict:
    """Operator helper: drop the prewarm flag so the next post forces
    a fresh preflight run. Use after Company defaults / COA changes."""
    if not company:
        frappe.throw(_("Phải chọn Company."))
    frappe.cache().delete_value(prewarm_flag_key(company))
    return {"company": company, "cleared": True}


_SHARD_QUEUE_MAP = {
    # Sharded batches route to dedicated queues so two shards run on
    # separate worker pools. Mapping is deterministic by shard_token
    # first character (case-insensitive) — keeps a stable assignment
    # across restarts without needing a registry. Unmapped tokens
    # fall back to "default".
    "A": "long",
    "B": "default",
    "1": "long",
    "2": "default",
    "L": "long",
    "D": "default",
}


def _resolve_post_queue(shard_token: str | None) -> str:
    """Return RQ queue name for a shard_token.

    No shard / empty token → "default" (legacy). Sharded tokens map by
    first-char so callers using "A"/"B" or "1"/"2" get reliable routing.
    Unknown sharded tokens land on "default" — operator can always pin
    explicitly by editing the map.
    """
    token = (shard_token or "").strip()
    if not token:
        return "default"
    return _SHARD_QUEUE_MAP.get(token[:1].upper(), "default")


@frappe.whitelist()
def start_post(batch_name: str, sync: bool = False,
               queue: str | None = None) -> dict:
    """Enqueue post_batch after preflight passes.

    Queue selection (in order):
      1. Explicit ``queue`` arg if provided (operator override).
      2. Shard-derived queue via ``_resolve_post_queue(batch.shard_token)``
         so two-shard parallel posts land on different queues (typically
         long + default, served by separate worker pools).
      3. ``"default"`` as final fallback.
    """
    batch_row = frappe.db.get_value(
        "Misa Migration Batch", batch_name,
        ["status", "shard_token"], as_dict=True,
    ) or {}
    status = batch_row.get("status")
    shard_token = (batch_row.get("shard_token") or "").strip() or None

    if status != st.REVIEWED:
        frappe.throw(_("Không thể post ở trạng thái {0} — phải là REVIEWED.").format(status))

    pre = preflight(batch_name)
    if pre["blocked"]:
        frappe.throw("<br>".join(pre["blocked"]))

    if sync:
        return post_job.post_batch(batch_name)

    rq_queue = (queue or "").strip() or _resolve_post_queue(shard_token)

    job = frappe.enqueue(
        "vn_accounting.misa_migration.jobs.post_job.post_batch",
        batch_name=batch_name, queue=rq_queue, timeout=14400,
    )
    frappe.db.set_value("Misa Migration Batch", batch_name, "job_id", job.id, update_modified=False)
    frappe.db.commit()
    return {
        "batch": batch_name, "queued": True, "job_id": job.id,
        "queue": rq_queue, "shard_token": shard_token,
    }


@frappe.whitelist()
def start_post_bulk_full(batch_name: str, skip_bootstrap: bool = False) -> dict:
    """SQL-pump bulk-INSERT path for ALL doctypes (SI+PI+PE+JE+SE+Asset).

    Sequential ordering on a fresh-wipe Company:
      1. ``install_misa_coa`` — bootstrap baseline CoA + Phase 1/2/3 masters
         (Warehouse, UOM, Customer, Supplier, Item, ...) via ORM. Idempotent.
      2. ``run_bulk_pump_full`` — bulk-INSERT Phase 0 (OB JE + Inventory +
         Assets) + Phase 4 (SI/PI/PE/JE/SE) via SQL pump.

    Pass ``skip_bootstrap=True`` to skip step 1 if masters are known to
    exist (e.g. operator already clicked "Cài đặt CoA Misa" or the Company
    has a pre-existing CoA + master set).

    Target: 10-15x faster than ORM submit path for Phase 4. See
    bulk_pump/__init__.py.
    """
    from vn_accounting.misa_migration.bulk_pump.orchestrator import (
        run_bulk_pump_full,
    )
    from vn_accounting.misa_migration.bulk_pump.coa_bootstrap import (
        refresh_company_default_accounts,
    )
    company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")
    if not company:
        frappe.throw(_("Batch missing company"))

    bootstrap_summary = None
    if not skip_bootstrap:
        bootstrap_summary = install_misa_coa(batch_name)

    bulk_summary = run_bulk_pump_full(batch_name, company)
    return {
        "batch": batch_name,
        "company": company,
        "bootstrap": bootstrap_summary,
        "bulk_pump": bulk_summary,
    }


@frappe.whitelist()
def start_post_bulk_si(batch_name: str) -> dict:
    """SQL-pump bulk-INSERT path for Sales Invoice (proof-of-concept).

    Bypasses ERPNext ORM submit cycle. Pre-computes all SI/Items/Taxes/
    Payment Schedule/GL Entry rows in memory, bulk-INSERTs via executemany.
    Target: 10-15x faster than ORM submit path for SI only.

    SCOPE: SI only. PI/PE/JE/SE/Asset bulk-pump pending.
    """
    from vn_accounting.misa_migration.bulk_pump.orchestrator import (
        run_bulk_pump_si_only,
    )
    company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")
    if not company:
        frappe.throw(_("Batch missing company"))
    return run_bulk_pump_si_only(batch_name, company)


@frappe.whitelist()
def get_post_progress(batch_name: str) -> dict:
    counts = get_counts(batch_name)
    batch_status = frappe.db.get_value("Misa Migration Batch", batch_name, "status")
    n_posted = sum(c.get("Posted", 0) for c in counts.values())
    n_failed = sum(c.get("Failed", 0) for c in counts.values())
    return {
        "batch": batch_name, "status": batch_status,
        "counts": counts, "posted": n_posted, "failed": n_failed,
    }


# ---------- pipeline recovery — cancel + delete Phase 4 drafts (Item 2)

def _resolve_batch_company(batch_name: str) -> str:
    """Resolve Company for a batch. Falls back to global default."""
    company = (
        frappe.db.get_value("Misa Migration Batch", batch_name, "company")
        or frappe.defaults.get_global_default("company")
        or frappe.db.get_value("Company", {}, "name")
    )
    if not company:
        frappe.throw(_("Không tìm thấy Company cho batch {0}.").format(batch_name))
    return company


@frappe.whitelist()
def cancel_phase_4(batch_name: str, confirm_token: str = "") -> dict:
    """Cancel docstatus=1 Misa-imported Phase 4 docs for this batch.

    Operator-recovery tool — distinct from `start_undo` which works at
    Misa Migration Row level. This walks the pipeline (REVERSE order
    PE → PI → SI → JE → SE) cancelling every Misa-imported submitted doc.

    The operator MUST type the batch name exactly into `confirm_token`
    (UI dialog passes it). Prevents fat-finger destruction.
    """
    if confirm_token != batch_name:
        frappe.throw(_(
            "Vui lòng gõ chính xác mã batch ({0}) vào ô xác nhận."
        ).format(batch_name))

    company = _resolve_batch_company(batch_name)
    from vn_accounting.misa_migration.context import set_active_company
    from vn_accounting.misa_migration.importers.phase_4_orchestrator import (
        cancel_phase_4_drafts,
    )
    set_active_company(company)
    try:
        result = cancel_phase_4_drafts(batch_name=batch_name, company=company)
    finally:
        from vn_accounting.misa_migration.context import clear_active_company
        clear_active_company()
    result["batch"] = batch_name
    return result


@frappe.whitelist()
def delete_phase_4(batch_name: str, confirm_token: str = "") -> dict:
    """Delete docstatus=0/2 Misa-imported Phase 4 docs for this batch.

    docstatus=1 docs are SKIPPED (caller must `cancel_phase_4` first).
    The operator MUST type the batch name exactly into `confirm_token`.
    """
    if confirm_token != batch_name:
        frappe.throw(_(
            "Vui lòng gõ chính xác mã batch ({0}) vào ô xác nhận."
        ).format(batch_name))

    company = _resolve_batch_company(batch_name)
    from vn_accounting.misa_migration.context import set_active_company
    from vn_accounting.misa_migration.importers.phase_4_orchestrator import (
        delete_phase_4_drafts,
    )
    set_active_company(company)
    try:
        result = delete_phase_4_drafts(batch_name=batch_name, company=company)
    finally:
        from vn_accounting.misa_migration.context import clear_active_company
        clear_active_company()
    result["batch"] = batch_name
    return result
