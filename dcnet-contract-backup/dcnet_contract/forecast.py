"""Cash flow forecast provider for DCNet Contract billing schedule.

Returns projected billing schedule rows (state='Projected') from active
contracts as committed inflow entries.
"""
import frappe
from vn_accounting.forecast.payment_delay import adjust_expected_date


def get_contract_forecast(filters):
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if not company or not from_date or not to_date:
        return []

    rows = frappe.db.sql("""
        SELECT bs.due_date, bs.amount, bs.item_type,
               c.name as contract_name, c.customer
        FROM `tabDCNet Contract Billing Schedule` bs
        JOIN `tabDCNet Contract` c ON c.name = bs.parent
        WHERE c.company = %(company)s
          AND c.docstatus = 1
          AND c.status IN ('Active', 'Suspended')
          AND bs.state = 'Projected'
          AND bs.due_date BETWEEN %(from_date)s AND %(to_date)s
    """, {"company": company, "from_date": from_date, "to_date": to_date}, as_dict=True)

    entries = []
    for r in rows:
        if not r.amount or float(r.amount) <= 0:
            continue
        adjusted_date = adjust_expected_date(str(r.due_date), r.customer, company)
        category = f"Contract {r.item_type}" if r.item_type else "Contract Service"
        entries.append({
            "expected_date": adjusted_date,
            "amount": float(r.amount),
            "direction": "inflow",
            "category": category,
            "confidence": "committed",
            "party_type": "Customer",
            "party": r.customer,
            "source_doctype": "DCNet Contract",
            "source_name": r.contract_name,
            "description": f"{category} - {r.contract_name}",
        })
    return entries
