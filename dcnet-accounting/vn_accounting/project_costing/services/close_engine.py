"""Close Project Costing per BL §7 + §11.4.

`close_project(costing_doc, writeoff_account, writeoff_amount, force)`:

  1. Validate all stages have submitted SI or are Đã hủy.
  2. Compute remaining 154 balance via GL Entry (Dr - Cr) on TK 154 for project.
  3. Balance ≈ 0 → flip status to "Đã hoàn thành", set closed_on.
  4. Balance > 0 with `force=False` → return {"balance": x, "needs_decision": True}
     (UI dialog asks KTT which write-off account + confirm).
  5. Balance > 0 with `force=True` → post Dr <writeoff> / Cr 154 + flip status.

Marker: [PROJECT_COSTING:<costing>][TYPE:CLOSE_WRITEOFF].
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import flt, today

_MARKER_PREFIX = "PROJECT_COSTING"
_TYPE = "CLOSE_WRITEOFF"


def _marker(costing: str) -> str:
    return f"[{_MARKER_PREFIX}:{costing}][TYPE:{_TYPE}]"


def _load_settings_accounts(company: str) -> dict[str, str | None]:
    from vn_accounting.utils.account_resolver import resolve_account

    return {
        "wip": resolve_account("wip_account_project_costing", company),
        "writeoff": resolve_account("writeoff_account_project_costing", company),
    }


def _validate_all_stages_resolved(costing_name: str):
    """Reject close if any stage is in active (non-terminal) state."""
    UNRESOLVED = ("Dự kiến", "Đang thi công", "Chờ xuất HĐ", "Đã có SI draft")
    rows = frappe.db.get_all(
        "Project Costing Stage",
        filters={"parent_costing": costing_name, "status": ["in", UNRESOLVED]},
        fields=["name", "stage_name", "status"],
    )
    if rows:
        names = ", ".join(f"{r.name} ({r.status})" for r in rows)
        frappe.throw(
            _("Không thể đóng — còn giai đoạn chưa hoàn tất: {0}").format(names)
        )


def compute_wip_balance(project: str, company: str) -> float:
    """Dr - Cr trên TK WIP (Settings) cho project. > 0 = còn cost dư."""
    accounts = _load_settings_accounts(company)
    wip_acc = accounts["wip"]
    if not wip_acc:
        return 0.0
    rows = frappe.db.sql("""
        SELECT IFNULL(SUM(debit), 0) - IFNULL(SUM(credit), 0) AS bal
        FROM `tabGL Entry`
        WHERE account = %s AND project = %s AND company = %s
          AND is_cancelled = 0
    """, (wip_acc, project, company), as_dict=True)
    return flt(rows[0].bal) if rows else 0.0


def close_project(
    costing_doc,
    *,
    writeoff_account: str | None = None,
    writeoff_amount: float = 0,
    force: bool = False,
) -> dict:
    """Close a Project Costing. See module docstring for flow.

    Returns dict:
      {"balance": <float>, "writeoff_je": <name|None>, "needs_decision": <bool>}
    """
    _validate_all_stages_resolved(costing_doc.name)

    balance = compute_wip_balance(costing_doc.project, costing_doc.company)

    if abs(balance) < 0.01:
        # Clean close
        frappe.db.set_value(
            "Project Costing", costing_doc.name,
            {"status": "Đã hoàn thành", "closed_on": today()},
            update_modified=False,
        )
        return {"balance": 0, "writeoff_je": None, "needs_decision": False}

    # Balance non-zero
    if not force:
        return {"balance": balance, "writeoff_je": None, "needs_decision": True}

    # Force write-off
    accounts = _load_settings_accounts(costing_doc.company)
    wo_acc = writeoff_account or accounts["writeoff"]
    wip_acc = accounts["wip"]
    if not (wo_acc and wip_acc):
        frappe.throw(_("Thiếu cấu hình TK Write-off / WIP trong VN Accounting Settings"))

    je = frappe.new_doc("Journal Entry")
    je.posting_date = today()
    je.company = costing_doc.company
    je.voucher_type = "Journal Entry"
    je.user_remark = (
        f"{_marker(costing_doc.name)} "
        + _("Write-off khi đóng công trình {0}").format(costing_doc.project)
    )

    if balance > 0:
        # Cost dư → Dr writeoff / Cr WIP
        je.append("accounts", {
            "account": wo_acc,
            "debit_in_account_currency": flt(balance),
            "project": costing_doc.project,
            "reference_type": "Project Costing",
            "reference_name": costing_doc.name,
            "user_remark": _("Write-off cost còn dư"),
        })
        je.append("accounts", {
            "account": wip_acc,
            "credit_in_account_currency": flt(balance),
            "project": costing_doc.project,
            "reference_type": "Project Costing",
            "reference_name": costing_doc.name,
            "user_remark": _("Đảo WIP công trình"),
        })
    else:
        # Negative balance (cost âm — hiếm): đảo dấu
        amt = abs(balance)
        je.append("accounts", {
            "account": wip_acc,
            "debit_in_account_currency": amt,
            "project": costing_doc.project,
            "reference_type": "Project Costing",
            "reference_name": costing_doc.name,
            "user_remark": _("Cân bằng WIP âm"),
        })
        je.append("accounts", {
            "account": wo_acc,
            "credit_in_account_currency": amt,
            "project": costing_doc.project,
            "reference_type": "Project Costing",
            "reference_name": costing_doc.name,
            "user_remark": _("Ghi vào TK write-off"),
        })

    je.flags.ignore_permissions = True
    je.insert()
    je.submit()

    frappe.db.set_value(
        "Project Costing", costing_doc.name,
        {"status": "Đã hoàn thành", "closed_on": today(), "writeoff_je": je.name},
        update_modified=False,
    )
    return {"balance": balance, "writeoff_je": je.name, "needs_decision": False}


def reopen_project(costing_doc) -> dict:
    """Per BL R7.3: reopen a closed project (e.g. bảo hành cost arrives).

    Does NOT cancel the writeoff JE (would corrupt audit trail) — KTT manually
    handles the bù JE if needed. Just flips status + clears closed_on.
    """
    if costing_doc.status != "Đã hoàn thành":
        frappe.throw(_("Chỉ mở lại công trình đã đóng"))
    frappe.db.set_value(
        "Project Costing", costing_doc.name,
        {"status": "Đang thi công", "closed_on": None},
        update_modified=False,
    )
    return {"status": "Đang thi công"}
