"""CCDC allocation schedule creation and per-period posting (TT99/2025 §4)."""
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import getdate, today, now


# --------------------------------------------------------------------------- #
# Account resolution helpers — pure functions, testable without DB
# --------------------------------------------------------------------------- #

def _resolve_debit_account(row_debit, item_expense, company):
    """Return debit account: row override > item.expense_account > lookup 6423."""
    if row_debit:
        return row_debit
    if item_expense:
        return item_expense
    from vn_accounting.utils.accounting_posting import lookup_account_by_number
    return lookup_account_by_number(company, "6423")


def _resolve_credit_account(row_credit, item_prepayment, company):
    """Return credit account: row override > item.prepayment_account > lookup 242."""
    if row_credit:
        return row_credit
    if item_prepayment:
        return item_prepayment
    from vn_accounting.utils.accounting_posting import lookup_account_by_number
    return lookup_account_by_number(company, "242")


# --------------------------------------------------------------------------- #
# Schedule creation
# --------------------------------------------------------------------------- #

def create_allocation_schedule(ccdc_item_doc) -> str:
    """Create CCDC Allocation Schedule with N child entries.

    Called from CCDCItem.on_submit. Populates debit_account / credit_account
    on each row from ccdc_item_doc fields (fallback to 6423/242 lookup).
    """
    n = int(ccdc_item_doc.allocation_periods or 1)
    cost = float(ccdc_item_doc.cost or 0)
    per_period = round(cost / n, 2)
    last_amount = round(cost - per_period * (n - 1), 2)

    from dateutil.relativedelta import relativedelta
    start = getdate(ccdc_item_doc.available_for_use_date or today())

    company = ccdc_item_doc.company
    debit_acc = _resolve_debit_account(None, ccdc_item_doc.expense_account, company)
    credit_acc = _resolve_credit_account(None, ccdc_item_doc.prepayment_account, company)

    schedule = frappe.get_doc({
        "doctype": "CCDC Allocation Schedule",
        "ccdc_item": ccdc_item_doc.name,
        "start_date": start,
        "total_amount": cost,
        "periods": n,
        "frequency": "Monthly",
        "status": "Active",
    })

    for i in range(1, n + 1):
        period_start = start + relativedelta(months=i - 1)
        amount = per_period if i < n else last_amount
        schedule.append("allocation_entries", {
            "period_no": i,
            "period_start_date": period_start,
            "allocation_amount": amount,
            "status": "Pending",
            "debit_account": debit_acc,
            "credit_account": credit_acc,
        })

    schedule.flags.ignore_permissions = True
    schedule.insert()
    frappe.db.commit()
    return schedule.name


# --------------------------------------------------------------------------- #
# Scheduler: daily auto-posting
# --------------------------------------------------------------------------- #

def allocate_ccdc_monthly():
    """Post Pending allocation entries where period_start_date <= today.

    Called by daily scheduler. Safe to run multiple times (idempotent by status=Posted check).
    """
    today_date = today()
    pending = frappe.get_all(
        "CCDC Allocation Entry",
        filters={"status": "Pending", "period_start_date": ["<=", today_date]},
        fields=[
            "name", "parent", "parenttype", "allocation_amount", "period_start_date",
            "period_no", "debit_account", "credit_account",
        ],
    )

    for entry in pending:
        try:
            schedule = frappe.get_doc("CCDC Allocation Schedule", entry.parent)
            if schedule.status == "Cancelled":
                continue
            ccdc_item = frappe.get_doc("CCDC Item", schedule.ccdc_item)
            _post_entry(ccdc_item, entry, entry.period_start_date, entry.parent)
        except Exception:
            frappe.log_error(frappe.get_traceback(), "CCDC allocate_ccdc_monthly error")


# --------------------------------------------------------------------------- #
# Whitelisted API — UI button handler
# --------------------------------------------------------------------------- #

@frappe.whitelist()
def post_allocation_period(schedule_name, period_idx):
    """Post a specific allocation period. Idempotent.

    Returns dict: {status: 'posted'|'already_posted', je_name, period_idx}.
    """
    period_idx = int(period_idx)
    schedule = frappe.get_doc("CCDC Allocation Schedule", schedule_name)

    entry = next(
        (r for r in schedule.allocation_entries if r.period_no == period_idx),
        None,
    )
    if not entry:
        frappe.throw(
            _("Kỳ {0} không tồn tại trong lịch phân bổ {1}").format(
                period_idx, schedule_name
            )
        )

    if entry.journal_entry:
        return {
            "status": "already_posted",
            "je_name": entry.journal_entry,
            "period_idx": period_idx,
        }

    ccdc_item = frappe.get_doc("CCDC Item", schedule.ccdc_item)
    _post_entry(ccdc_item, entry, entry.period_start_date, schedule_name)
    frappe.db.commit()

    je_name = frappe.db.get_value("CCDC Allocation Entry", entry.name, "journal_entry")
    return {"status": "posted", "je_name": je_name, "period_idx": period_idx}


# --------------------------------------------------------------------------- #
# Internal posting — supports both dict (scheduler) and DocumentRow (API)
# --------------------------------------------------------------------------- #

def _post_entry(ccdc_item_doc, entry, posting_date, schedule_name: str):
    """Post a single allocation entry via post_je_from_entries."""
    from vn_accounting.utils.accounting_posting import (
        post_je_from_entries,
        resolve_cost_center,
    )

    def _get(key):
        return entry.get(key) if isinstance(entry, dict) else getattr(entry, key, None)

    company = ccdc_item_doc.company
    debit_acc = _resolve_debit_account(
        _get("debit_account"), ccdc_item_doc.expense_account, company
    )
    credit_acc = _resolve_credit_account(
        _get("credit_account"), ccdc_item_doc.prepayment_account, company
    )

    amount = float(_get("allocation_amount") or 0)
    period_no = _get("period_no")

    entries = [{
        "account_debit": debit_acc,
        "account_credit": credit_acc,
        "amount": amount,
        "description": _("Phân bổ CCDC kỳ {0}: {1}").format(period_no, ccdc_item_doc.name),
        "is_vat": 0,
    }]

    remark = "Phân bổ CCDC {0} kỳ {1}".format(ccdc_item_doc.name, period_no)
    cost_center = resolve_cost_center(ccdc_item_doc, company)

    je_name = post_je_from_entries(
        entries, company, posting_date, remark,
        "CCDC Allocation Schedule", schedule_name,
        submit=True, cost_center=cost_center,
        source_key="vn_accounting.ccdc.allocation",
    )

    entry_name = _get("name")
    frappe.db.set_value(
        "CCDC Allocation Entry",
        entry_name,
        {"status": "Posted", "journal_entry": je_name, "posted_at": now()},
        update_modified=False,
    )
    _maybe_complete_schedule(schedule_name, ccdc_item_doc.name)


def _maybe_complete_schedule(schedule_name: str, ccdc_item_name: str):
    """Mark schedule Completed when all entries are Posted."""
    remaining = frappe.get_all(
        "CCDC Allocation Entry",
        filters={"parent": schedule_name, "status": "Pending"},
        fields=["name"],
    )
    if not remaining:
        frappe.db.set_value(
            "CCDC Allocation Schedule", schedule_name, "status", "Completed",
            update_modified=False,
        )
        frappe.db.set_value(
            "CCDC Item", ccdc_item_name, "status", "Hết phân bổ",
            update_modified=False,
        )
