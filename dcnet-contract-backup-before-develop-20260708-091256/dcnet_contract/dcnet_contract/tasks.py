"""Daily scheduler tasks for DCNet Contract billing lifecycle."""

import frappe
from frappe import _
from frappe.utils import today, getdate, add_days

from dcnet_contract.dcnet_contract.utils.state_machine import assert_transition


def run_auto_invoice():
    """Create Sales Invoices for billing_schedule rows where state=Projected and due_date <= today."""
    rows = frappe.db.sql(
        """
        SELECT bs.name AS bs_name, bs.parent AS contract_name,
               bs.period_start, bs.period_end, bs.due_date,
               bs.amount, bs.item_type, bs.month_index
        FROM `tabDCNet Contract Billing Schedule` bs
        JOIN `tabDCNet Contract` c ON c.name = bs.parent
        WHERE bs.state = 'Projected'
          AND bs.due_date <= %s
          AND c.docstatus = 1
          AND c.status = 'Active'
        ORDER BY bs.parent, bs.month_index
        """,
        (today(),),
        as_dict=True,
    )

    # Group by contract
    by_contract: dict[str, list] = {}
    for r in rows:
        by_contract.setdefault(r.contract_name, []).append(r)

    for contract_name, schedule_rows in by_contract.items():
        _create_invoice_for_rows(contract_name, schedule_rows)

    if by_contract:
        frappe.db.commit()


def _create_invoice_for_rows(contract_name: str, schedule_rows: list[dict]):
    """Create a single Sales Invoice covering the given billing schedule rows."""
    contract = frappe.get_cached_doc("DCNet Contract", contract_name)
    settings = frappe.get_cached_doc("DCNet Contract Settings")

    cost_center = _get_cost_center(contract.branch, settings)
    income_account = settings.default_income_account or _get_default_income_account(contract.company)

    if not income_account:
        frappe.throw(
            _("Income account not configured for company {0}").format(contract.company)
        )
    if not cost_center:
        frappe.throw(
            _("Cost center not configured for branch {0}").format(contract.branch or _("(empty)"))
        )

    # Use earliest period_start as posting_date
    posting_date = min(r.period_start for r in schedule_rows)

    si = frappe.new_doc("Sales Invoice")
    si.customer = contract.customer
    si.company = contract.company
    si.posting_date = posting_date
    si.due_date = max(r.due_date for r in schedule_rows)
    si.currency = contract.currency or "VND"
    si.set_posting_time = 1

    if settings.default_payment_terms:
        si.payment_terms_template = settings.default_payment_terms

    # Build SI items — one row per billing schedule row
    for bs_row in schedule_rows:
        description = _build_item_description(contract, bs_row)
        si.append("items", {
            "item_name": description,
            "description": description,
            "qty": 1,
            "rate": bs_row.amount,
            "cost_center": cost_center,
            "income_account": income_account,
        })

    # Apply Sales Tax Template (VAT) if configured
    tax_template = settings.default_sales_tax_template or _get_default_tax_template(contract.company)
    if tax_template:
        si.taxes_and_charges = tax_template
        si.set_taxes()

    si.flags.ignore_permissions = True
    si.insert()
    si.submit()

    # Update billing schedule rows
    for bs_row in schedule_rows:
        frappe.db.set_value(
            "DCNet Contract Billing Schedule",
            bs_row.bs_name,
            {"state": "Invoiced", "sales_invoice": si.name},
            update_modified=False,
        )


def _build_item_description(contract, bs_row: dict) -> str:
    """Build SI item description from contract items and billing period."""
    item_labels = ", ".join(r.item_label for r in contract.items)
    if bs_row.item_type == "Setup Fee":
        return f"{item_labels} - Setup Fee"
    return f"{item_labels} ({bs_row.period_start} - {bs_row.period_end})"


def _get_cost_center(branch: str, settings) -> str | None:
    """Look up cost_center from Settings branch_cost_center_map."""
    if not branch or not settings.get("branch_cost_center_map"):
        return None
    for row in settings.branch_cost_center_map:
        if row.branch == branch:
            return row.cost_center
    return None


def _get_default_income_account(company: str) -> str | None:
    """Get default income account for the company."""
    return frappe.db.get_value("Company", company, "default_income_account")


def _get_default_tax_template(company: str) -> str | None:
    """Get the default Sales Taxes and Charges Template for the company."""
    return frappe.db.get_value(
        "Sales Taxes and Charges Template",
        {"company": company, "is_default": 1},
        "name",
    )


def run_overdue_check():
    """Mark Invoiced billing_schedule rows as Overdue if past grace period."""
    settings = frappe.get_cached_doc("DCNet Contract Settings")
    grace_days = settings.overdue_grace_period_days or 15
    cutoff_date = add_days(today(), -grace_days)

    rows = frappe.db.sql(
        """
        SELECT bs.name AS bs_name
        FROM `tabDCNet Contract Billing Schedule` bs
        JOIN `tabDCNet Contract` c ON c.name = bs.parent
        WHERE bs.state = 'Invoiced'
          AND bs.due_date < %s
          AND c.docstatus = 1
          AND c.status = 'Active'
        """,
        (cutoff_date,),
        as_dict=True,
    )

    for r in rows:
        frappe.db.set_value(
            "DCNet Contract Billing Schedule",
            r.bs_name,
            "state",
            "Overdue",
            update_modified=False,
        )

    if rows:
        frappe.db.commit()


def run_expire_contracts():
    """Expire active contracts whose end_date has passed."""
    contracts = frappe.get_all(
        "DCNet Contract",
        filters={
            "docstatus": 1,
            "status": ["in", ["Active", "Suspended"]],
            "end_date": ["<", today()],
        },
        pluck="name",
    )

    for name in contracts:
        doc = frappe.get_doc("DCNet Contract", name)
        try:
            assert_transition(doc.status, "Expired")
        except ValueError:
            continue
        frappe.db.set_value("DCNet Contract", name, "status", "Expired")

    if contracts:
        frappe.db.commit()
