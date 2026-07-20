"""Auto-source registry — central, app-distributed metadata for auto-generated docs.

Architecture:
  - Each app declares its auto-gen sources in `hooks.py` via the
    `auto_generated_doc_sources` dict. Source metadata: label, doctype,
    needs_approval, action_draft/submitted/cancelled, description.
  - Each app's auto-gen code path calls `register(target_dt, target_name, source_key)`
    immediately after insert. The registry table (Auto Generated Doc Registry)
    records the linkage; no Custom Field on SI/JE is needed.
  - For ERPNext core code we cannot modify (Asset Depreciation, Subscription,
    Deferred, ERR), an `after_insert` doc_event classifies & registers via
    voucher_type / link field inspection.
  - The "Auto Generated Docs Pending" report queries the registry via dynamic
    LEFT JOIN to all target DocTypes — no SQL predicates per source needed.

Adding a new auto-gen source:
  1. Declare in `<your_app>/hooks.py`:
       auto_generated_doc_sources = {
           "your_app.flow_name": {
               "label": "...", "doctype": "...", "needs_approval": True/False,
               "action_draft": "...", "description": "...",
           }
       }
  2. Call `register(target_doctype, target_name, source_key,
                    registered_by="your_app.module.func")` after the insert.
"""
from __future__ import annotations

import inspect

import frappe
from frappe import _
from frappe.utils import now, today


# --------------------------------------------------------------------------- #
# Public API — call from any app
# --------------------------------------------------------------------------- #

def register(
    target_doctype: str,
    target_name: str,
    source_key: str,
    registered_by: str | None = None,
) -> str | None:
    """Idempotent registration. Returns the registry row name (or existing if dupe).

    Returns None if the target doc is missing or source_key is unregistered.
    """
    sources = get_sources_registry()
    if source_key not in sources:
        # Soft-fail: log + return. Never block the parent transaction.
        frappe.log_error(
            f"register() called with unregistered source_key '{source_key}' "
            f"for {target_doctype} {target_name}",
            "auto_source.register",
        )
        return None

    existing = frappe.db.get_value(
        "Auto Generated Doc Registry",
        {"target_doctype": target_doctype, "target_name": target_name},
        "name",
    )
    if existing:
        return existing

    company, posting_date = _fetch_target_meta(target_doctype, target_name)
    if not company or not posting_date:
        # Target deleted between insert + register, or fields missing
        return None

    if not registered_by:
        registered_by = _infer_caller()

    doc = frappe.get_doc({
        "doctype": "Auto Generated Doc Registry",
        "source_key": source_key,
        "target_doctype": target_doctype,
        "target_name": target_name,
        "company": company,
        "posting_date": posting_date,
        "registered_at": now(),
        "registered_by": registered_by[:140] if registered_by else None,
    })
    doc.flags.ignore_permissions = True
    doc.insert()
    return doc.name


def get_sources_registry() -> dict:
    """Merge auto_generated_doc_sources hook entries from all installed apps.

    Returns: { source_key: {label, doctype, needs_approval, action_draft,
                            action_submitted, action_cancelled, description, ...} }
    """
    cache_key = "vn_accounting:auto_sources_registry"
    cached = frappe.cache.get_value(cache_key)
    if cached is not None:
        return cached

    merged: dict = {}
    # frappe.get_hooks returns a list of dicts (one per app); merge them.
    hooks_value = frappe.get_hooks("auto_generated_doc_sources", default=None)
    if hooks_value:
        # hooks_value can be either a dict (single source) or list of dicts (multi-app)
        if isinstance(hooks_value, dict):
            merged.update(hooks_value)
        else:
            for entry in hooks_value:
                if isinstance(entry, dict):
                    merged.update(entry)

    # Frappe's hook merge wraps EVERY inner scalar value in a list — even
    # strings and bools — so a custom-app hook entry's "label" comes through
    # as ["X"] not "X". Peel single-element lists back to their scalar.
    def _unwrap(v):
        if isinstance(v, list) and len(v) == 1:
            return v[0]
        return v

    merged = {
        key: ({k: _unwrap(v) for k, v in (meta or {}).items()} if isinstance(meta, dict) else meta)
        for key, meta in merged.items()
    }

    # Fill defaults
    for key, meta in merged.items():
        if not isinstance(meta, dict):
            continue
        meta.setdefault("action_submitted", "Đã hoàn tất — xem lại khi cần")
        meta.setdefault("action_cancelled", "Đã hủy — kiểm tra lý do")
        meta.setdefault("needs_approval", True)
        meta.setdefault("description", "")
        meta.setdefault("doctype", "Journal Entry")

    frappe.cache.set_value(cache_key, merged)
    return merged


# --------------------------------------------------------------------------- #
# ERPNext-core classifier — after_insert hook
# --------------------------------------------------------------------------- #

def classify_and_register_je(doc, method=None):
    """Register ERPNext-core auto-generated JEs we cannot stamp at call site.

    Idempotent: skips if registry row already exists. Light per-insert cost.
    """
    try:
        # Already registered (caller stamped explicitly)?
        if frappe.db.exists("Auto Generated Doc Registry",
                            {"target_doctype": "Journal Entry", "target_name": doc.name}):
            return

        source_key = None
        vt = doc.get("voucher_type") or ""
        remark = (doc.get("user_remark") or "")

        if vt == "Depreciation Entry":
            source_key = "erp.asset_depreciation"
        elif vt == "Deferred Revenue":
            source_key = "erp.deferred_revenue"
        elif vt == "Deferred Expense":
            source_key = "erp.deferred_expense"
        elif vt == "Exchange Rate Revaluation":
            source_key = "erp.exchange_rate_revaluation"

        if not source_key:
            return

        register("Journal Entry", doc.name, source_key,
                 registered_by="vn_accounting.auto_source.classify_and_register_je")
    except Exception:
        # Never let registry hiccup break the parent JE insert.
        frappe.log_error(frappe.get_traceback(), "auto_source.classify_and_register_je")


def classify_and_register_si(doc, method=None):
    """Register ERPNext-core auto-generated SIs (Subscription)."""
    try:
        if frappe.db.exists("Auto Generated Doc Registry",
                            {"target_doctype": "Sales Invoice", "target_name": doc.name}):
            return

        source_key = None
        if doc.get("subscription"):
            source_key = "erp.subscription_invoice"

        if not source_key:
            return

        register("Sales Invoice", doc.name, source_key,
                 registered_by="vn_accounting.auto_source.classify_and_register_si")
    except Exception:
        frappe.log_error(frappe.get_traceback(), "auto_source.classify_and_register_si")


# --------------------------------------------------------------------------- #
# Cleanup on delete — keep registry clean
# --------------------------------------------------------------------------- #

def cleanup_orphan_on_delete(doc, method=None):
    """When the target doc is deleted, drop its registry row."""
    try:
        frappe.db.delete("Auto Generated Doc Registry", {
            "target_doctype": doc.doctype,
            "target_name": doc.name,
        })
    except Exception:
        frappe.log_error(frappe.get_traceback(), "auto_source.cleanup_orphan_on_delete")


# --------------------------------------------------------------------------- #
# One-off backfill — for existing data on sites pre-refactor
# --------------------------------------------------------------------------- #

def backfill_existing_docs():
    """Scan existing SI + JE and register any that match known auto-gen patterns.

    Run via `bench --site X execute vn_accounting.auto_source.backfill_existing_docs`.
    Idempotent — register() skips dupes.
    """
    counts: dict[str, int] = {}

    def _bump(key):
        counts[key] = counts.get(key, 0) + 1

    # SI — dcnet_contract.auto_invoice (custom field present?) or subscription
    if frappe.db.has_column("Sales Invoice", "dcnet_contract"):
        sis = frappe.db.sql(
            """SELECT name FROM `tabSales Invoice`
               WHERE dcnet_contract IS NOT NULL AND dcnet_contract != ''
                 AND docstatus IN (0, 1, 2)""",
            as_dict=True,
        )
        for r in sis:
            if register("Sales Invoice", r.name, "dcnet_contract.auto_invoice",
                        registered_by="backfill"):
                _bump("dcnet_contract.auto_invoice")

    if frappe.db.has_column("Sales Invoice", "subscription"):
        sis = frappe.db.sql(
            """SELECT name FROM `tabSales Invoice`
               WHERE subscription IS NOT NULL AND subscription != ''
                 AND docstatus IN (0, 1, 2)""",
            as_dict=True,
        )
        for r in sis:
            if register("Sales Invoice", r.name, "erp.subscription_invoice",
                        registered_by="backfill"):
                _bump("erp.subscription_invoice")

    # JE — by voucher_type
    je_classifiers = [
        ("Depreciation Entry", "erp.asset_depreciation"),
        ("Deferred Revenue", "erp.deferred_revenue"),
        ("Deferred Expense", "erp.deferred_expense"),
        ("Exchange Rate Revaluation", "erp.exchange_rate_revaluation"),
    ]
    for vt, key in je_classifiers:
        jes = frappe.db.sql(
            """SELECT name FROM `tabJournal Entry`
               WHERE voucher_type = %s AND docstatus IN (0, 1, 2)""",
            (vt,),
            as_dict=True,
        )
        for r in jes:
            if register("Journal Entry", r.name, key, registered_by="backfill"):
                _bump(key)

    # JE — by user_remark patterns (Treasury, LCV VAT)
    remark_patterns = [
        ("%VAT NK khấu trừ%", "vn_accounting.lcv_vat_deductible"),
        ("Term Deposit % - Interest period %", "vn_accounting.treasury.deposit_interest"),
        ("Bank Loan % - Repayment %", "vn_accounting.treasury.loan_repayment"),
        ("Term Deposit % - Settlement %", "vn_accounting.treasury.deposit_settlement"),
        ("Term Deposit % - New deposit%", "vn_accounting.treasury.deposit_creation"),
        ("Bank Loan % - Disbursement%", "vn_accounting.treasury.loan_disbursement"),
        ("Term Deposit % - Accrual%", "vn_accounting.treasury.deposit_accrual"),
        ("Bank Loan % - Accrual%", "vn_accounting.treasury.loan_accrual"),
    ]
    for pattern, key in remark_patterns:
        jes = frappe.db.sql(
            """SELECT name FROM `tabJournal Entry`
               WHERE user_remark LIKE %s AND docstatus IN (0, 1, 2)""",
            (pattern,),
            as_dict=True,
        )
        for r in jes:
            if register("Journal Entry", r.name, key, registered_by="backfill"):
                _bump(key)

    frappe.db.commit()
    frappe.cache.delete_value("vn_accounting:auto_sources_registry")
    print("Backfill complete:")
    for key, n in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {n:6d}  {key}")
    return counts


# --------------------------------------------------------------------------- #
# Internal helpers
# --------------------------------------------------------------------------- #

def _fetch_target_meta(target_doctype: str, target_name: str) -> tuple[str | None, str | None]:
    """Return (company, posting_date) from the target doc."""
    if not frappe.db.exists(target_doctype, target_name):
        return None, None

    # Most accounting docs have these two fields directly.
    val = frappe.db.get_value(
        target_doctype, target_name, ["company", "posting_date"], as_dict=True
    )
    if not val:
        return None, None
    return val.get("company"), val.get("posting_date") or today()


def _infer_caller() -> str:
    """Best-effort caller identification for forensics."""
    try:
        # 2 frames up: skip register() and _infer_caller() itself
        frame = inspect.stack()[2]
        mod = inspect.getmodule(frame[0])
        mod_name = mod.__name__ if mod else "?"
        return f"{mod_name}.{frame.function}"
    except Exception:
        return "unknown"


# Cache invalidation when hooks change (e.g., after install/migrate)
def clear_sources_cache():
    frappe.cache.delete_value("vn_accounting:auto_sources_registry")


@frappe.whitelist()
def get_source_labels_for_filter() -> list[str]:
    """Trả về danh sách nhãn (label) đã được đăng ký — dùng cho bộ lọc
    'Loại tài liệu' trên báo cáo. Tự cập nhật khi có nguồn mới."""
    sources = get_sources_registry()
    return sorted({m.get("label") for m in sources.values() if isinstance(m, dict) and m.get("label")})
