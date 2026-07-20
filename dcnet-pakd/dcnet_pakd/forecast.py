"""Cash flow forecast provider for PAKD commission payments.

Returns pending commission lines as outflow entries. Confidence is mapped
from PAKD workflow_state: Approved → committed, Pending* → probable.
"""
import frappe


def get_pakd_forecast(filters):
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if not company or not from_date or not to_date:
        return []

    rows = frappe.db.sql("""
        SELECT cl.component, cl.amount, cl.name as line_name,
               p.name as pakd_name, p.workflow_state, p.sales_person,
               bs.due_date
        FROM `tabPAKD Commission Line` cl
        JOIN `tabPhuong An Kinh Doanh` p ON p.name = cl.parent
        JOIN `tabDCNet Contract` c ON c.name = p.contract_ref
        JOIN `tabDCNet Contract Billing Schedule` bs
            ON bs.parent = c.name AND bs.idx = cl.billing_schedule_idx
        WHERE cl.state = 'Pending'
          AND c.company = %(company)s
          AND bs.due_date BETWEEN %(from_date)s AND %(to_date)s
    """, {"company": company, "from_date": from_date, "to_date": to_date}, as_dict=True)

    entries = []
    for r in rows:
        if not r.amount or float(r.amount) <= 0:
            continue

        if r.workflow_state == "Approved":
            confidence = "committed"
        elif r.workflow_state and "Pending" in r.workflow_state:
            confidence = "probable"
        else:
            continue

        entries.append({
            "expected_date": str(r.due_date),
            "amount": float(r.amount),
            "direction": "outflow",
            "category": f"PAKD {r.component}" if r.component else "PAKD Commission",
            "confidence": confidence,
            "party_type": "Employee",
            "party": r.sales_person,
            "source_doctype": "Phuong An Kinh Doanh",
            "source_name": r.pakd_name,
            "description": f"{r.component or 'Commission'} - {r.pakd_name}",
        })
    return entries
