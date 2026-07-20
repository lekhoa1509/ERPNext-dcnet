"""Phase 0 (Opening Balance) post orchestrator.

Phase E commit 13f. Wires the 9 OB file_types into the post pipeline.

Execution order (run AFTER Phase 1+2+3 — masters must be ready):

  1. Load all OB rows from `tabMisa Migration Row` (file_type LIKE 'OB %')
  2. Parse each file_type via PARSER_BY_FILE_TYPE
  3. Dispatch:
     - JE-bound rows (general/bank/customer/supplier/employee/prepaid) →
       single `post_opening_journal` call (one Opening Entry JE per batch)
     - `OB Inventory` → `post_opening_inventory` (N Material Receipt SEs)
     - `OB Fixed Asset` → `post_opening_assets(is_ccdc=False)` (M Assets)
     - `OB CCDC` → `post_opening_assets(is_ccdc=True)` (K Assets)
  4. Update Misa Migration Row status by file_type to Posted/Failed
  5. Return summary envelope

The 5 file_types fed into the single Opening JE share one doc; rows
get a Posted status when the JE inserts successfully. Inventory + Asset
file_types have per-row status tracking.

post_batch order: run_post (Phase 1+2) → run_phase_0_post → run_phase_4_post.
"""

from __future__ import annotations

import json
import time
from typing import Any

import frappe

from vn_accounting.misa_migration.context import (
    clear_active_company,
    set_active_company,
)
from vn_accounting.misa_migration.importers.ob_handlers.opening_asset import (
    post_opening_assets,
)
from vn_accounting.misa_migration.importers.ob_handlers.opening_inventory import (
    post_opening_inventory,
)
from vn_accounting.misa_migration.importers.ob_handlers.opening_journal import (
    post_opening_journal,
)
from vn_accounting.misa_migration.parsers.opening_balance_parser import (
    PARSER_BY_FILE_TYPE,
)


PROGRESS_EVENT = "misa_migration:post_progress"

_JE_FILE_TYPES = (
    "OB Account Balance",
    "OB Bank Balance",
    "OB Customer AR",
    "OB Supplier AP",
    "OB Employee Advance",
    "OB Prepaid Expense",
)

# Item 1B-3: map Misa OB file_type → detail-category label used by
# opening_journal._is_detail_handled. When a file_type has rows in the
# batch, mark its category as "handled" so the general-balance builder
# skips matching TK prefixes (delegated). When EMPTY, the prefix is
# allowed through the general builder so the balance still posts.
_FILE_TYPE_TO_DETAIL_CATEGORY: dict[str, str] = {
    "OB Bank Balance": "bank",
    "OB Customer AR": "customer",
    "OB Supplier AP": "supplier",
    "OB Employee Advance": "employee",
    "OB Inventory": "inventory",
    "OB Fixed Asset": "fixed_asset",
    "OB CCDC": "fixed_asset",   # CCDC overlaps with 21x/214 prefixes
    "OB Prepaid Expense": "prepaid",
}


def _compute_detail_handled_categories(
    parsed: dict[str, list[dict]],
) -> set[str]:
    """Build the set of detail categories whose Misa file produced rows.

    Used by opening_journal._is_detail_handled to decide whether to
    skip a prefix in the general balance builder. Categories whose
    detail file is missing or empty are NOT skipped — their TK prefix
    is allowed through the general builder so the balance still posts
    (default account if unmapped goes to the temp opening account,
    NOT silently lost).
    """
    out: set[str] = set()
    for ft, cat in _FILE_TYPE_TO_DETAIL_CATEGORY.items():
        if parsed.get(ft):
            out.add(cat)
    return out


def _load_phase_0_rows(batch_name: str) -> dict[str, list[tuple[str, dict]]]:
    """Load OB rows from the batch. Returns dict[file_type → list of
    (row_name, parsed_payload)]."""
    rows = frappe.db.sql(
        """
        SELECT name, file_type, raw_payload
        FROM `tabMisa Migration Row`
        WHERE batch=%s
          AND status='Ready'
          AND file_type LIKE 'OB %%'
        """,
        (batch_name,),
        as_dict=True,
    )
    grouped: dict[str, list[tuple[str, dict]]] = {}
    for r in rows:
        try:
            payload = json.loads(r["raw_payload"] or "{}")
        except (TypeError, ValueError):
            continue
        if isinstance(payload, dict):
            grouped.setdefault(r["file_type"], []).append((r["name"], payload))
    return grouped


def _update_rows_status(
    batch_name: str,
    file_type: str,
    new_status: str,
    error_message: str | None = None,
    target_doctype: str | None = None,
    target_name: str | None = None,
) -> None:
    """Update all rows of a file_type to a new status.

    UX Gap 5: also accepts target_name so the batch-level Undo
    (`undo_batch` via `Hoàn tác` button) can walk Misa Migration Row
    .target_name to find docs it needs to cancel. Without this, Phase 0
    OB JE and Material Receipt SEs were silently skipped by Undo
    ("reversed 0 docs" while docs remained docstatus=1).
    """
    update_kwargs = {"status": new_status}
    if target_doctype:
        update_kwargs["target_doctype"] = target_doctype
    if target_name:
        update_kwargs["target_name"] = target_name
    if error_message:
        update_kwargs["error_message"] = (error_message or "")[:240]
    set_clause = ", ".join(f"`{k}`=%s" for k in update_kwargs)
    args = list(update_kwargs.values()) + [batch_name, file_type]
    frappe.db.sql(
        f"UPDATE `tabMisa Migration Row` SET {set_clause} "
        f"WHERE batch=%s AND file_type=%s",
        tuple(args),
    )


def run_phase_0_post(
    batch_name: str,
    max_rows_per_run: int | None = None,
) -> dict[str, Any]:
    """Post all Phase 0 OB rows for a batch.

    Args:
      batch_name: Misa Migration Batch name.
      max_rows_per_run: forwarded to post_opening_assets (FA + CCDC) — caps
        new Assets created per call. None = no cap (legacy, single-pass
        behaviour; the default for every caller except post_job.post_batch,
        which passes 200 to avoid monopolizing a worker on huge asset
        lists). JE and Inventory are unaffected (they always collapse into
        few docs regardless of row count).

    Returns:
      {
        total_rows: int,
        opening_journal: <post_opening_journal result>,
        opening_inventory: <post_opening_inventory result>,
        opening_fa: <post_opening_assets FA result>,
        opening_ccdc: <post_opening_assets CCDC result>,
        complete: bool,
        elapsed_seconds: float,
      }
    """
    t0 = time.time()

    # B2 fix + Item 3: pin batch.company AND auto-run preflight setup
    # so OB handlers resolve against fully-bootstrapped COA.
    batch_company = frappe.db.get_value(
        "Misa Migration Batch", batch_name, "company"
    )
    preflight_summary = None
    if batch_company:
        set_active_company(batch_company)
        # Lazy import to avoid circular dep between the two orchestrators.
        from vn_accounting.misa_migration.importers.phase_4_orchestrator import (
            run_preflight_setup,
        )
        preflight_summary = run_preflight_setup(batch_company)
        try:
            frappe.publish_realtime(PROGRESS_EVENT, {
                "batch": batch_name,
                "phase_0_preflight": True,
                "errors": len(preflight_summary.get("errors", []) or []),
            }, after_commit=False)
        except Exception:
            pass

    grouped = _load_phase_0_rows(batch_name)
    if not grouped:
        clear_active_company()
        return {
            "total_rows": 0,
            "skipped": "no Phase 0 data in batch",
            "complete": True,
            "elapsed_seconds": time.time() - t0,
        }

    # Incremental-month guard: when the Company ALREADY has GL from a prior
    # migration (e.g. full-2025 batch posted, now importing 01-2026), the
    # new batch's "đầu kỳ" files (Bảng cân đối tài khoản Đầu kỳ, Tổng hợp
    # tồn kho Đầu kỳ...) describe balances that ARE ALREADY ON THE BOOKS —
    # posting them again double-counts every account. Detect prior GL not
    # created by this batch's own OB voucher and skip Phase 0 entirely
    # (the files remain useful: validate stage compares Cuối kỳ columns).
    if batch_company:
        own_ob_prefix = f"{batch_name}-OB%"
        prior_gl = frappe.db.sql(
            """SELECT 1 FROM `tabGL Entry`
               WHERE company=%s AND is_cancelled=0
                 AND voucher_no NOT LIKE %s
               LIMIT 1""",
            (batch_company, own_ob_prefix),
        )
        if prior_gl:
            n_rows = sum(len(v) for v in grouped.values())
            for ft in grouped:
                _update_rows_status(
                    batch_name, ft, "Skipped",
                    error_message="Đã có số dư từ đợt migrate trước",
                )
            frappe.db.commit()
            clear_active_company()
            return {
                "total_rows": n_rows,
                "skipped": (
                    "Công ty đã có sổ cái từ đợt migrate trước — bỏ qua "
                    "file số dư đầu kỳ (tránh ghi trùng). Số dư đầu của kỳ "
                    "này chính là số dư cuối đợt trước."
                ),
                "complete": True,
                "elapsed_seconds": time.time() - t0,
            }

    # Parse each file_type's raw payloads
    parsed: dict[str, list[dict]] = {}
    total_rows = 0
    for ft, rows in grouped.items():
        parser = PARSER_BY_FILE_TYPE.get(ft)
        if not parser:
            continue
        # Parser expects xlsx-shaped tuples but we have parsed JSON dicts;
        # convert to tuples by extracting in column order. For now, since
        # rows came from xlsx → JSON via openpyxl, the payload dicts use
        # original Misa column NAMES as keys. We need to construct
        # tuples matching the parser's expected shape.
        # Simpler: store the raw column-ordered tuple-as-list during
        # upload OR accept dict input here. Parsers expect tuples (row
        # 0..N), so we synthesize:
        synth_rows = _dict_payloads_to_xlsx_shape(ft, [p for _n, p in rows])
        try:
            parsed[ft] = parser(synth_rows)
            total_rows += len(parsed[ft])
        except Exception as exc:
            _update_rows_status(batch_name, ft, "Failed",
                                error_message=f"Parse failed: {exc}")
            frappe.log_error(
                title=f"Phase 0 parse failed: {ft}",
                message=f"{type(exc).__name__}: {exc}",
            )
            parsed[ft] = []

    # Item 1B-3: only mark a detail category as "handled" if its file
    # has actual parsed rows. This stops `_build_general_rows` from
    # silently dropping TK 141/152/etc balances when the detail file is
    # missing or empty (e.g. when Phase 3 employee seed wasn't run).
    detail_handled = _compute_detail_handled_categories(parsed)

    # UX Gap fix: read OB posting date from batch (operator must set this
    # via the batch creation form). Misa "đầu kỳ" files don't carry the
    # date — for đầu kỳ 2025 use 2024-12-31, for đầu kỳ 2026 use
    # 2025-12-31. Falls back to handler default if not set (legacy
    # batches that pre-date this field).
    ob_date = frappe.db.get_value(
        "Misa Migration Batch", batch_name, "ob_posting_date"
    )
    je_kwargs = {}
    if ob_date:
        je_kwargs["opening_date"] = str(ob_date)

    # Dispatch JE-bound rows together (single Opening Entry JE)
    je_result = post_opening_journal(
        batch_name,
        general_rows=parsed.get("OB Account Balance", []),
        bank_rows=parsed.get("OB Bank Balance", []),
        customer_rows=parsed.get("OB Customer AR", []),
        supplier_rows=parsed.get("OB Supplier AP", []),
        employee_rows=parsed.get("OB Employee Advance", []),
        prepaid_rows=parsed.get("OB Prepaid Expense", []),
        detail_handled_categories=detail_handled,
        **je_kwargs,
    )
    # Mark all 6 JE-bound file_types as Posted iff JE succeeded.
    # UX Gap 5: also set target_name on each row so batch-level Undo
    # (Hoàn tác) can walk Misa Migration Row.target_name to find the
    # OB JE that needs cancelling. Single JE per batch → all 6 JE-bound
    # file_types share the same target_name.
    if je_result.get("status") == "created":
        ob_target_name = je_result.get("target_name") or f"{batch_name}-OB"
        for ft in _JE_FILE_TYPES:
            _update_rows_status(batch_name, ft, "Posted",
                                target_doctype="Journal Entry",
                                target_name=ob_target_name)
    elif je_result.get("status") == "skipped":
        ob_target_name = je_result.get("target_name") or f"{batch_name}-OB"
        for ft in _JE_FILE_TYPES:
            _update_rows_status(batch_name, ft, "Skipped",
                                target_doctype="Journal Entry",
                                target_name=ob_target_name)
    else:
        for ft in _JE_FILE_TYPES:
            _update_rows_status(batch_name, ft, "Failed",
                                error_message=str(je_result.get("error", ""))[:240])

    # Inventory — Material Receipt SE per warehouse. Pass opening_date
    # via same UX-gap fix as JE handler.
    inv_kwargs = {"opening_date": str(ob_date)} if ob_date else {}
    inv_result = post_opening_inventory(batch_name, parsed.get("OB Inventory", []), **inv_kwargs)
    if inv_result.get("status") in ("created", "partial"):
        _update_rows_status(batch_name, "OB Inventory", "Posted",
                            target_doctype="Stock Entry")
    elif inv_result.get("status") == "skipped":
        _update_rows_status(batch_name, "OB Inventory", "Skipped")
    elif "OB Inventory" in parsed:
        _update_rows_status(batch_name, "OB Inventory", "Failed",
                            error_message=str(inv_result.get("error", ""))[:240])

    # FA Asset docs — server-load cap: post_opening_assets creates at most
    # max_rows_per_run (default 200) new Assets per call. Only mark the
    # file_type's rows Posted once `complete` is True; otherwise leave them
    # "Ready" so post_job.post_batch's re-enqueue-on-incomplete loop resumes
    # this same file_type on the next chunk (already-created Assets are
    # skipped cheaply on re-entry).
    fa_result = post_opening_assets(batch_name, parsed.get("OB Fixed Asset", []),
                                    is_ccdc=False, max_rows_per_run=max_rows_per_run)
    if fa_result.get("status") in ("created", "partial") and fa_result.get("complete", True):
        _update_rows_status(batch_name, "OB Fixed Asset", "Posted",
                            target_doctype="Asset")
    elif fa_result.get("status") == "skipped":
        _update_rows_status(batch_name, "OB Fixed Asset", "Skipped")
    elif "OB Fixed Asset" in parsed and fa_result.get("complete", True):
        _update_rows_status(batch_name, "OB Fixed Asset", "Failed",
                            error_message=str(fa_result.get("error", ""))[:240])

    # CCDC Asset docs — same server-load cap as FA above.
    ccdc_result = post_opening_assets(batch_name, parsed.get("OB CCDC", []),
                                      is_ccdc=True, max_rows_per_run=max_rows_per_run)
    if ccdc_result.get("status") in ("created", "partial") and ccdc_result.get("complete", True):
        _update_rows_status(batch_name, "OB CCDC", "Posted",
                            target_doctype="Asset")
    elif ccdc_result.get("status") == "skipped":
        _update_rows_status(batch_name, "OB CCDC", "Skipped")
    elif "OB CCDC" in parsed and ccdc_result.get("complete", True):
        _update_rows_status(batch_name, "OB CCDC", "Failed",
                            error_message=str(ccdc_result.get("error", ""))[:240])

    frappe.db.commit()
    elapsed = time.time() - t0

    # Only FA/CCDC can span multiple runs (JE = 1 doc, Inventory ≤ N
    # warehouses — both always finish in a single call).
    phase_0_complete = fa_result.get("complete", True) and ccdc_result.get("complete", True)

    summary = {
        "total_rows": total_rows,
        "opening_journal": je_result,
        "opening_inventory": inv_result,
        "opening_fa": fa_result,
        "opening_ccdc": ccdc_result,
        "complete": phase_0_complete,
        "elapsed_seconds": elapsed,
        "preflight": preflight_summary,
    }
    try:
        frappe.publish_realtime(PROGRESS_EVENT, {
            "batch": batch_name, "phase_0": True, "summary": summary,
        }, after_commit=True)
    except Exception:
        pass
    clear_active_company()  # B2: release per-request company override
    return summary


# ---------------------- shape adapter (dict payloads → xlsx tuples)

# Per-file expected column order (matches the xlsx header rows the
# parsers walk; defined here so parsers can stay xlsx-tuple-driven).
_COLUMN_ORDER_BY_FILE_TYPE: dict[str, list[str]] = {
    "OB Account Balance": ["STT", "Số tài khoản", "Tên tài khoản", "Dư Nợ", "Dư Có"],
    "OB Bank Balance": ["STT", "Số TK ngân hàng", "Tên ngân hàng",
                        "Số tài khoản", "Dư Nợ", "Dư Có"],
    "OB Customer AR": ["STT", "Số tài khoản", "Mã khách hàng",
                       "Tên khách hàng", "Dư Nợ", "Dư Có"],
    "OB Supplier AP": ["STT", "Số tài khoản", "Mã nhà cung cấp",
                       "Tên nhà cung cấp", "Dư Nợ", "Dư Có"],
    "OB Employee Advance": ["STT", "Số tài khoản", "Mã nhân viên",
                            "Tên nhân viên", "Dư Nợ", "Dư Có"],
    "OB Inventory": ["STT", "Ngày nhập kho", "Số phiếu nhập", "Mã hàng",
                     "Tên hàng", "Nhóm VTHH", "ĐVT", "Mã kho",
                     "Số lượng tồn", "Đơn giá", "Giá trị tồn", "Số lô"],
    "OB Fixed Asset": ["STT", "Mã tài sản", "Tên tài sản", "Loại tài sản",
                       "Đơn vị sử dụng", "Nguyên giá", "Giá trị tính KH",
                       "Hao mòn lũy kế", "Ngày ghi tăng", "Ngày tính KH",
                       "Thời gian SD (tháng)", "Thời gian SD còn lại (tháng)"],
    "OB CCDC": ["STT", "Mã CCDC", "Tên CCDC", "Ngày ghi tăng", "Số lượng",
                "Giá trị CCDC", "Giá trị còn lại", "Số kỳ phân bổ",
                "Số kỳ PB còn lại", "Số tiền PB hàng kỳ", "TK chờ phân bổ",
                "Ngừng phân bổ"],
    "OB Prepaid Expense": ["STT", "Mã CP trả trước", "Tên CP trả trước",
                           "Ngày ghi nhận", "Số tiền", "Số tiền còn lại",
                           "Số kỳ phân bổ", "Số kỳ phân bổ còn lại",
                           "Số tiền PB hàng kỳ", "Tài khoản chờ phân bổ"],
}


def _dict_payloads_to_xlsx_shape(
    file_type: str,
    dict_rows: list[dict],
) -> list[tuple]:
    """Reconstruct xlsx-shaped tuples for the parser.

    The parsers expect rows in xlsx layout (with title + blank + header
    rows before data). We synthesize:
      row 0: title (we don't have it, use empty)
      row 1: blank
      row 2: header (from _COLUMN_ORDER_BY_FILE_TYPE)
      row 3..N: data rows mapped from dict keys
    """
    cols = _COLUMN_ORDER_BY_FILE_TYPE.get(file_type)
    if not cols:
        return []
    out: list[tuple] = []
    # Header padding to match parser's rows[3:] expectation
    # Inventory parser uses rows[4:] — pad one more for it
    title_pad = 4 if file_type == "OB Inventory" else 3
    out.append(tuple([file_type] + [None] * (len(cols) - 1)))
    for _ in range(title_pad - 2):
        out.append(tuple([None] * len(cols)))
    out.append(tuple(cols))
    # Data rows: extract each dict by column order
    for d in dict_rows:
        out.append(tuple(d.get(c) for c in cols))
    return out
