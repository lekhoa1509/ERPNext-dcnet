"""Frappe doc_event hooks for Asset Repair — VN classification + inline JE (TT99/2025)."""
from __future__ import annotations

import frappe
from frappe import _

from vn_accounting.utils.accounting_posting import (
    build_default_entries,
    post_je_from_entries,
    resolve_cost_center,
)


def on_validate(doc, method):
    """Auto-fill downtime; warn on large Chi phí cost; validate accounting entries balance."""
    _autofill_downtime(doc)
    _warn_large_chi_phi(doc)
    _validate_entries_balance(doc)


def on_submit(doc, method):
    """Post inline accounting_entries as one JE; set posted_je + backward-compat alias."""
    if not doc.accounting_entries:
        _autofill_entries(doc)

    company = frappe.db.get_value("Asset", doc.asset, "company") or frappe.defaults.get_user_default("Company")
    cost_center = resolve_cost_center(doc, company)
    remark = _("Sửa chữa TSCĐ {0} — {1} [{2}]").format(doc.asset or doc.name, doc.repair_classification or "", doc.name)

    je_name = post_je_from_entries(
        entries=doc.accounting_entries,
        company=company,
        posting_date=doc.completion_date or frappe.utils.today(),
        user_remark=remark,
        ref_doctype="Asset Repair",
        ref_name=doc.name,
        submit=True,
        cost_center=cost_center,
        source_key="vn_accounting.asset.repair",
    )
    frappe.db.set_value("Asset Repair", doc.name, "posted_je", je_name, update_modified=False)
    # Backward-compat alias — capitalization_je points to the same JE
    frappe.db.set_value("Asset Repair", doc.name, "capitalization_je", je_name, update_modified=False)


def on_cancel(doc, method):
    """Cancel the linked JE when Asset Repair is cancelled."""
    je_name = doc.posted_je or doc.capitalization_je
    if not je_name:
        return
    try:
        je = frappe.get_doc("Journal Entry", je_name)
        if je.docstatus == 1:
            je.cancel()
    except frappe.DoesNotExistError:
        pass
    # Reverse GL entries created by JE cancellation inherit reference_type/reference_name,
    # which triggers Frappe's back-link check. Skip it — the JE is already cancelled.
    doc.flags.ignore_links = True


# --------------------------------------------------------------------------- #
# Private helpers
# --------------------------------------------------------------------------- #

def _autofill_downtime(doc):
    if doc.failure_date and doc.completion_date and not doc.get("downtime"):
        try:
            from erpnext.assets.doctype.asset_repair.asset_repair import get_downtime
            doc.downtime = get_downtime(str(doc.failure_date), str(doc.completion_date))
        except Exception:
            pass


def _warn_large_chi_phi(doc):
    if doc.repair_classification != "Chi phí":
        return
    if not doc.asset:
        return
    gross = frappe.db.get_value("Asset", doc.asset, "gross_purchase_amount") or 0
    if gross > 0 and (doc.repair_cost or 0) >= 0.1 * gross:
        frappe.msgprint(
            _("Chi phí sửa chữa ≥ 10% nguyên giá. Cân nhắc chọn 'Sửa chữa lớn vốn hóa'."),
            indicator="orange",
            alert=True,
        )


def _validate_entries_balance(doc):
    if not doc.accounting_entries:
        return
    if not doc.repair_cost:
        return

    total = sum(float(row.amount or 0) for row in doc.accounting_entries)
    vat_amt = 0.0
    if doc.has_vat and doc.vat_rate:
        vat_amt = round(float(doc.repair_cost) * float(doc.vat_rate) / 100)
    expected = round(float(doc.repair_cost)) + vat_amt

    if abs(total - expected) > 1:
        frappe.throw(
            _("Tổng bút toán ({0}) không khớp với chi phí sửa chữa + VAT ({1})").format(total, expected)
        )


def _autofill_entries(doc):
    """Build default entries when accounting_entries is empty at submit time."""
    if not doc.repair_classification:
        frappe.throw(_("Chưa chọn Phân loại sửa chữa"))
    if not doc.repair_cost:
        frappe.throw(_("Chi phí sửa chữa phải > 0"))

    company = frappe.db.get_value("Asset", doc.asset, "company") or frappe.defaults.get_user_default("Company")
    rows = build_default_entries(
        event_type="Asset Repair",
        classification=doc.repair_classification,
        amount=doc.repair_cost,
        has_vat=bool(doc.has_vat),
        vat_rate=float(doc.vat_rate or 10),
        company=company,
        asset_name=doc.asset,
    )
    doc.accounting_entries = []
    for r in rows:
        doc.append("accounting_entries", r)
