"""ERPNext pipeline forecast providers.

5 providers covering the Quotation → SO → SI → PE lifecycle (inflow)
and PO → PI → PE lifecycle (outflow). Each provider only returns documents
at their CURRENT lifecycle stage to avoid double-counting.
"""
import frappe
from datetime import date, timedelta

from vn_accounting.forecast.payment_delay import adjust_expected_date


def get_quotation_forecast(filters):
    """Open quotations not yet ordered → possible inflow."""
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if not company or not from_date or not to_date:
        return []

    rows = frappe.db.sql("""
        SELECT q.name, q.grand_total, q.valid_till, q.transaction_date,
               q.party_name as customer
        FROM `tabQuotation` q
        WHERE q.company = %(company)s
          AND q.docstatus = 1
          AND q.status = 'Open'
          AND q.order_type = 'Sales'
    """, {"company": company}, as_dict=True)

    entries = []
    for r in rows:
        exp_date = str(r.valid_till) if r.valid_till else str(r.transaction_date + timedelta(days=30))
        if exp_date < from_date or exp_date > to_date:
            continue
        entries.append({
            "expected_date": exp_date,
            "amount": float(r.grand_total),
            "direction": "inflow",
            "category": "Quotation",
            "confidence": "possible",
            "party_type": "Customer",
            "party": r.customer,
            "source_doctype": "Quotation",
            "source_name": r.name,
            "description": f"Quotation {r.name}",
        })
    return entries


def get_sales_order_forecast(filters):
    """Submitted SOs not fully billed → probable inflow."""
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if not company or not from_date or not to_date:
        return []

    rows = frappe.db.sql("""
        SELECT so.name, so.grand_total, so.per_billed, so.transaction_date,
               so.customer
        FROM `tabSales Order` so
        WHERE so.company = %(company)s
          AND so.docstatus = 1
          AND so.per_billed < 100
          AND so.status NOT IN ('Closed', 'Cancelled')
    """, {"company": company}, as_dict=True)

    entries = []
    for r in rows:
        remaining = float(r.grand_total) * (100 - float(r.per_billed)) / 100
        if remaining <= 0:
            continue

        # Try Payment Schedule for due_date
        exp_date = _get_payment_schedule_date(r.name, "Sales Order")
        if not exp_date:
            exp_date = str(r.transaction_date + timedelta(days=30))

        if exp_date < from_date or exp_date > to_date:
            continue

        entries.append({
            "expected_date": exp_date,
            "amount": remaining,
            "direction": "inflow",
            "category": "Sales Order",
            "confidence": "probable",
            "party_type": "Customer",
            "party": r.customer,
            "source_doctype": "Sales Order",
            "source_name": r.name,
            "description": f"SO {r.name} ({100 - float(r.per_billed):.0f}% unbilled)",
        })
    return entries


def get_purchase_order_forecast(filters):
    """Submitted POs not fully billed → probable outflow."""
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if not company or not from_date or not to_date:
        return []

    rows = frappe.db.sql("""
        SELECT po.name, po.grand_total, po.per_billed, po.schedule_date,
               po.transaction_date, po.supplier
        FROM `tabPurchase Order` po
        WHERE po.company = %(company)s
          AND po.docstatus = 1
          AND po.per_billed < 100
          AND po.status NOT IN ('Closed', 'Cancelled')
    """, {"company": company}, as_dict=True)

    entries = []
    for r in rows:
        remaining = float(r.grand_total) * (100 - float(r.per_billed)) / 100
        if remaining <= 0:
            continue

        exp_date = _get_payment_schedule_date(r.name, "Purchase Order")
        if not exp_date:
            base = r.schedule_date or r.transaction_date
            exp_date = str(base + timedelta(days=30))

        if exp_date < from_date or exp_date > to_date:
            continue

        entries.append({
            "expected_date": exp_date,
            "amount": remaining,
            "direction": "outflow",
            "category": "Purchase Order",
            "confidence": "probable",
            "party_type": "Supplier",
            "party": r.supplier,
            "source_doctype": "Purchase Order",
            "source_name": r.name,
            "description": f"PO {r.name} ({100 - float(r.per_billed):.0f}% unbilled)",
        })
    return entries


def get_unpaid_si_forecast(filters):
    """Submitted SIs with outstanding > 0 → committed/overdue inflow."""
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if not company or not from_date or not to_date:
        return []

    today_str = str(date.today())

    rows = frappe.db.sql("""
        SELECT si.name, si.outstanding_amount, si.due_date, si.customer
        FROM `tabSales Invoice` si
        WHERE si.company = %(company)s
          AND si.docstatus = 1
          AND si.outstanding_amount > 0
          AND si.is_return = 0
    """, {"company": company}, as_dict=True)

    entries = []
    for r in rows:
        due = str(r.due_date) if r.due_date else today_str
        is_overdue = due < today_str

        if is_overdue:
            confidence = "overdue"
            exp_date = today_str
        else:
            confidence = "committed"
            exp_date = adjust_expected_date(due, r.customer, company)

        if exp_date < from_date or exp_date > to_date:
            continue

        entries.append({
            "expected_date": exp_date,
            "amount": float(r.outstanding_amount),
            "direction": "inflow",
            "category": "Sales Invoice",
            "confidence": confidence,
            "party_type": "Customer",
            "party": r.customer,
            "source_doctype": "Sales Invoice",
            "source_name": r.name,
            "description": f"SI {r.name} - {'Overdue' if is_overdue else 'Due ' + due}",
        })
    return entries


def get_unpaid_pi_forecast(filters):
    """Submitted PIs with outstanding > 0 → committed/overdue outflow."""
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if not company or not from_date or not to_date:
        return []

    today_str = str(date.today())

    rows = frappe.db.sql("""
        SELECT pi.name, pi.outstanding_amount, pi.due_date, pi.supplier
        FROM `tabPurchase Invoice` pi
        WHERE pi.company = %(company)s
          AND pi.docstatus = 1
          AND pi.outstanding_amount > 0
          AND pi.is_return = 0
    """, {"company": company}, as_dict=True)

    entries = []
    for r in rows:
        due = str(r.due_date) if r.due_date else today_str
        is_overdue = due < today_str

        confidence = "overdue" if is_overdue else "committed"
        exp_date = today_str if is_overdue else due

        if exp_date < from_date or exp_date > to_date:
            continue

        entries.append({
            "expected_date": exp_date,
            "amount": float(r.outstanding_amount),
            "direction": "outflow",
            "category": "Purchase Invoice",
            "confidence": confidence,
            "party_type": "Supplier",
            "party": r.supplier,
            "source_doctype": "Purchase Invoice",
            "source_name": r.name,
            "description": f"PI {r.name} - {'Overdue' if is_overdue else 'Due ' + due}",
        })
    return entries


def _get_payment_schedule_date(docname, doctype):
    """Get earliest unpaid Payment Schedule due_date for a document."""
    ps = frappe.db.sql("""
        SELECT due_date FROM `tabPayment Schedule`
        WHERE parent = %(name)s AND parenttype = %(doctype)s
          AND outstanding > 0
        ORDER BY due_date ASC LIMIT 1
    """, {"name": docname, "doctype": doctype}, as_dict=True)
    return str(ps[0].due_date) if ps else None
