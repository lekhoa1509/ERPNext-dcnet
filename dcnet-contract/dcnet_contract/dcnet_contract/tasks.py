"""Daily scheduler tasks for DCNet Contract billing lifecycle."""

import frappe
from frappe import _
from frappe.utils import today, getdate, add_days

from dcnet_contract.dcnet_contract.utils.state_machine import assert_transition


def run_auto_invoice():
    """Create *draft* Sales Invoices for billing_schedule rows where state=Projected and due_date <= today.

    Invoices are left as drafts (docstatus=0) — the accountant reviews and
    "ghi sổ" (submits) them manually, then issues the official VAT e-invoice.
    The draft worklist surfaces in the "Invoices to Post" report. Billing
    schedule rows are still flipped to state=Invoiced at draft creation so the
    next scheduler run does not produce duplicates.
    """
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
    # v0.2.0: stamp SI with contract + PAKD + earliest billing period idx (FB-D5)
    si.dcnet_contract = contract.name
    si.billing_period_idx = min(int(r.month_index or 0) for r in schedule_rows)
    # 1 HD = 1 PAKD per D3 — resolve the Approved PAKD (fallback to any non-cancelled)
    si.dcnet_pakd = (
        frappe.db.get_value("Phuong An Kinh Doanh",
                             {"contract_ref": contract.name, "workflow_state": "Approved"},
                             "name")
        or frappe.db.get_value("Phuong An Kinh Doanh",
                                {"contract_ref": contract.name, "workflow_state": ["!=", "Cancelled"]},
                                "name")
    )

    if settings.default_payment_terms:
        si.payment_terms_template = settings.default_payment_terms

    # Resolve item_code for the SI lines. Prefer the Item that the contract
    # already links to via DCNet Contract Item.erpnext_item; fall back to a
    # service_type → Item map so the grid never shows a blank Sản phẩm cell.
    item_code = _resolve_si_item_code(contract)

    # Build SI items — one row per billing schedule row
    for bs_row in schedule_rows:
        description = _build_item_description(contract, bs_row)
        row = {
            "qty": 1,
            "rate": bs_row.amount,
            "cost_center": cost_center,
            "income_account": income_account,
            "description": description,
        }
        if item_code:
            row["item_code"] = item_code
            # Keep the period-aware label as item_name; Frappe will not overwrite
            # if explicitly set after item_code resolution.
            row["item_name"] = description
        else:
            row["item_name"] = description
        si.append("items", row)

    # Apply Sales Tax Template (VAT) if configured
    tax_template = settings.default_sales_tax_template or _get_default_tax_template(contract.company)
    if tax_template:
        si.taxes_and_charges = tax_template
        si.set_taxes()

    si.flags.ignore_permissions = True
    si.insert()
    # Left as draft — accountant submits ("ghi sổ") after review. See run_auto_invoice docstring.

    # Register as auto-generated for the central worklist
    try:
        from vn_accounting.auto_source import register
        register("Sales Invoice", si.name, "dcnet_contract.auto_invoice",
                 registered_by="dcnet_contract.tasks.run_auto_invoice")
    except ImportError:
        pass  # vn_accounting not installed — silently skip

    # Update billing schedule rows
    for bs_row in schedule_rows:
        frappe.db.set_value(
            "DCNet Contract Billing Schedule",
            bs_row.bs_name,
            {"state": "Invoiced", "sales_invoice": si.name},
            update_modified=False,
        )


_SERVICE_TYPE_FALLBACK_ITEM = {
    "FTTH DN": "FTTH-BIZ",
    "FTTH HGD": "FTTH-HOME",
    "ILL": "LL-100M",
    "MPLS": "MPLS-L3",
    "P2P": "P2P",
    "Colocation": "COLO-RACK",
}


def _resolve_si_item_code(contract) -> str | None:
    """Pick an Item for SI lines generated from the billing schedule.

    Priority: first contract item with `erpnext_item` set → service_type fallback
    map → None. None lets the line fall back to legacy item_name-only behavior.
    """
    for ci in contract.get("items") or []:
        if ci.get("erpnext_item") and frappe.db.exists("Item", ci.erpnext_item):
            return ci.erpnext_item
    fallback = _SERVICE_TYPE_FALLBACK_ITEM.get(contract.get("service_type"))
    if fallback and frappe.db.exists("Item", fallback):
        return fallback
    return None


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
