"""BC hoa hồng theo NVKD — Commission Register by Sales Person.

Shows all commission lines across PAKDs, grouped/filterable by NVKD.
Covers both JE path (draft + submitted) and Additional Salary (HRMS) path.
Includes PAKD + Contract context for full traceability.

Filter modes:
- only_payable=1 (default): all lines where billing period is Paid
  (both Pending and Posted — shows full commission picture for paid invoices)
- only_payable=0: full register including unpaid periods
"""

import frappe
from frappe import _


def execute(filters=None):
    filters = filters or {}
    if "only_payable" not in filters:
        filters["only_payable"] = 1
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"fieldname": "sales_person_name", "label": _("NVKD"), "fieldtype": "Data", "width": 150},
        {"fieldname": "pakd", "label": _("PAKD"), "fieldtype": "Link",
         "options": "Phuong An Kinh Doanh", "width": 130},
        {"fieldname": "contract", "label": _("Hợp đồng"), "fieldtype": "Link",
         "options": "DCNet Contract", "width": 130},
        {"fieldname": "customer", "label": _("Khách hàng"), "fieldtype": "Data", "width": 160},
        {"fieldname": "billing_idx", "label": _("Kỳ"), "fieldtype": "Int", "width": 50},
        {"fieldname": "component", "label": _("Khoản"), "fieldtype": "Data", "width": 120},
        {"fieldname": "amount", "label": _("Số tiền"), "fieldtype": "Currency", "width": 120},
        {"fieldname": "state", "label": _("Trạng thái"), "fieldtype": "Data", "width": 90},
        {"fieldname": "posting_method", "label": _("Phương thức"), "fieldtype": "Data", "width": 100},
        {"fieldname": "je_status", "label": _("GL"), "fieldtype": "Data", "width": 80},
        {"fieldname": "sales_invoice", "label": _("Hóa đơn"), "fieldtype": "Link",
         "options": "Sales Invoice", "width": 140},
        {"fieldname": "paid_date", "label": _("Ngày thu"), "fieldtype": "Date", "width": 95},
        {"fieldname": "payroll_month", "label": _("Tháng lương"), "fieldtype": "Data", "width": 90},
        {"fieldname": "payment_entry", "label": _("Phiếu thu"), "fieldtype": "Link",
         "options": "Payment Entry", "width": 130},
        {"fieldname": "additional_salary", "label": _("Lương bổ sung"), "fieldtype": "Link",
         "options": "Additional Salary", "width": 130},
        {"fieldname": "journal_entry", "label": _("Bút toán"), "fieldtype": "Link",
         "options": "Journal Entry", "width": 130},
    ]


def get_data(filters):
    conditions = []
    values = {}

    only_payable = int(filters.get("only_payable") or 0)
    if only_payable:
        # Show ALL commission lines where billing period is Paid (customer paid)
        # — includes both Pending (not yet posted) AND Posted (already processed)
        conditions.append("bs.state = 'Paid'")
    else:
        if filters.get("state"):
            conditions.append("cl.state = %(state)s")
            values["state"] = filters["state"]

    if filters.get("payroll_month"):
        conditions.append("cl.payroll_month = %(payroll_month)s")
        values["payroll_month"] = filters["payroll_month"]
    if filters.get("pakd"):
        conditions.append("cl.parent = %(pakd)s")
        values["pakd"] = filters["pakd"]
    if filters.get("sales_person"):
        conditions.append("p.sales_person = %(sales_person)s")
        values["sales_person"] = filters["sales_person"]
    if filters.get("component"):
        conditions.append("cl.component = %(component)s")
        values["component"] = filters["component"]

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    bs_join = "JOIN" if only_payable else "LEFT JOIN"

    rows = frappe.db.sql(
        f"""
        SELECT
            cl.parent AS pakd,
            p.workflow_state AS pakd_state,
            p.contract_ref AS contract,
            p.customer,
            p.sales_person,
            COALESCE(emp.employee_name, p.sales_person) AS sales_person_name,
            cl.billing_schedule_idx AS billing_idx,
            cl.component,
            cl.amount,
            cl.state,
            bs.sales_invoice,
            pe.posting_date AS paid_date,
            cl.payroll_month,
            cl.payment_entry,
            cl.additional_salary,
            cl.journal_entry
        FROM `tabPAKD Commission Line` cl
        JOIN `tabPhuong An Kinh Doanh` p ON p.name = cl.parent
        LEFT JOIN `tabEmployee` emp ON emp.name = p.sales_person
        {bs_join} `tabDCNet Contract Billing Schedule` bs
          ON bs.parent = p.contract_ref AND bs.month_index = cl.billing_schedule_idx
        LEFT JOIN `tabPayment Entry` pe
          ON pe.name = bs.payment_entry AND pe.docstatus = 1
        {where}
        ORDER BY sales_person_name, pe.posting_date DESC, cl.parent, cl.billing_schedule_idx
        """,
        values,
        as_dict=True,
    )

    # Enrich with posting method + JE status
    for row in rows:
        if row.additional_salary:
            row["posting_method"] = "HRMS"
            row["je_status"] = "Lương bổ sung"
        elif row.journal_entry:
            je_status = frappe.db.get_value("Journal Entry", row.journal_entry, "docstatus")
            row["posting_method"] = "Bút toán"
            row["je_status"] = "Đã ghi sổ" if je_status == 1 else "Nháp" if je_status == 0 else "Đã hủy"
        else:
            row["posting_method"] = "—"
            row["je_status"] = "Chưa đăng"

    return rows
