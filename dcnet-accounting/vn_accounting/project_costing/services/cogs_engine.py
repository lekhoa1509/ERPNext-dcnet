"""COGS Recognition engine per BL §11.3.

When Sales Invoice for a Project Costing Stage is submitted, post:
    Dr <cogs_account> / Cr <wip_account> (project=X)   amount = stage.cost_pinned

Marker: [PROJECT_COSTING:<costing>][TYPE:STAGE_COGS][SI:<si>] — used for cancel
lookup. Stage.cogs_je stores the JE ref. EC2 (stage cost = 0) → no JE, SI
submits cleanly.

Stage status flow on this engine:
    SI submit       → Stage.status = "Đã xuất HĐ", Stage.cogs_je = <je>
    SI cancel       → Stage.status = "Chờ xuất HĐ", Stage.cogs_je = None
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import flt

_MARKER_PREFIX = "PROJECT_COSTING"
_TYPE = "STAGE_COGS"


def _marker(costing: str, si_name: str) -> str:
    return f"[{_MARKER_PREFIX}:{costing}][TYPE:{_TYPE}][SI:{si_name}]"


def _load_settings_accounts(company: str) -> dict[str, str | None]:
    """Return COGS + WIP accounts from Settings, company-scoped."""
    from vn_accounting.utils.account_resolver import resolve_account
    return {
        "cogs": resolve_account("cogs_account_project_costing", company),
        "wip": resolve_account("wip_account_project_costing", company),
    }


def _find_existing_je(costing: str, si_name: str, *, include_cancelled: bool = False) -> str | None:
    marker = _marker(costing, si_name)
    filters = {"user_remark": ["like", f"%{marker}%"]}
    if not include_cancelled:
        filters["docstatus"] = 1
    return frappe.db.get_value("Journal Entry", filters, "name")


def on_sales_invoice_submit(doc, method=None):
    """Recognize COGS on SI with project_costing_stage link.

    Skips silently when:
      - frappe.flags.misa_migration_active (Misa NKC already has COGS legs)
      - SI not docstatus=1
      - SI has no project_costing_stage Custom Field value
      - Stage cost_pinned = 0 (EC2 — tạm ứng, no JE needed)
      - JE already exists for this (costing, si) pair (idempotent)
    """
    if getattr(frappe.flags, "misa_migration_active", False):
        return
    if doc.docstatus != 1:
        return
    stage_name = doc.get("project_costing_stage")
    if not stage_name:
        return
    stage = frappe.db.get_value(
        "Project Costing Stage", stage_name,
        ["name", "parent_costing", "cost_pinned"], as_dict=True
    )
    if not stage:
        return

    cost = flt(stage.cost_pinned)
    if cost <= 0:
        # EC2: stage cost = 0 (e.g. tạm ứng đầu) → SI submits, no COGS JE.
        # Still flip stage status.
        frappe.db.set_value(
            "Project Costing Stage", stage_name,
            {"status": "Đã xuất HĐ"},
            update_modified=False,
        )
        return

    parent = stage.parent_costing
    if _find_existing_je(parent, doc.name):
        return  # idempotent

    accounts = _load_settings_accounts(doc.company)
    cogs_acc, wip_acc = accounts["cogs"], accounts["wip"]
    if not (cogs_acc and wip_acc):
        frappe.log_error(
            title="Project Costing COGS skipped",
            message=f"Missing TK config: cogs={cogs_acc} wip={wip_acc} for SI {doc.name}",
        )
        return

    # Resolve project from Project Costing (= same as project name due to autoname)
    project = parent

    je = frappe.new_doc("Journal Entry")
    je.posting_date = doc.posting_date
    je.company = doc.company
    je.voucher_type = "Journal Entry"
    je.user_remark = (
        f"{_marker(parent, doc.name)} "
        + _("Ghi nhận giá vốn công trình {0} từ hóa đơn {1}").format(project, doc.name)
    )
    je.append("accounts", {
        "account": cogs_acc,
        "debit_in_account_currency": cost,
        "project": project,
        "reference_type": "Project Costing",
        "reference_name": parent,
        "user_remark": _("Giá vốn stage {0}").format(stage_name),
    })
    je.append("accounts", {
        "account": wip_acc,
        "credit_in_account_currency": cost,
        "project": project,
        "reference_type": "Project Costing",
        "reference_name": parent,
        "user_remark": _("Đảo WIP công trình"),
    })
    je.flags.ignore_permissions = True
    je.insert()
    je.submit()

    # Update stage atomically (db.set_value to avoid recursive validate)
    frappe.db.set_value(
        "Project Costing Stage", stage_name,
        {"status": "Đã xuất HĐ", "cogs_je": je.name},
        update_modified=False,
    )


def on_sales_invoice_cancel(doc, method=None):
    stage_name = doc.get("project_costing_stage")
    if not stage_name:
        return
    parent = frappe.db.get_value("Project Costing Stage", stage_name, "parent_costing")
    if not parent:
        return
    je_name = _find_existing_je(parent, doc.name)
    if je_name:
        je = frappe.get_doc("Journal Entry", je_name)
        je.flags.ignore_permissions = True
        je.cancel()

    frappe.db.set_value(
        "Project Costing Stage", stage_name,
        {"status": "Chờ xuất HĐ", "cogs_je": None},
        update_modified=False,
    )
