"""Profitability by Service — PAKD revenue vs cost breakdown by service type."""

import frappe
from frappe import _


def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"fieldname": "pakd_type", "label": _("Loại PAKD"), "fieldtype": "Data", "width": 140},
        {"fieldname": "service_type", "label": _("Loại DV"), "fieldtype": "Data", "width": 100},
        {"fieldname": "name", "label": _("PAKD"), "fieldtype": "Link", "options": "Phuong An Kinh Doanh", "width": 140},
        {"fieldname": "customer", "label": _("Khách hàng"), "fieldtype": "Data", "width": 160},
        {"fieldname": "revenue", "label": _("Doanh thu"), "fieldtype": "Currency", "width": 120},
        {"fieldname": "cost_ms", "label": _("MS"), "fieldtype": "Currency", "width": 100},
        {"fieldname": "cost_gpvt", "label": _("GPVT"), "fieldtype": "Currency", "width": 100},
        {"fieldname": "cost_add", "label": _("Chi phí ngoài"), "fieldtype": "Currency", "width": 120},
        {"fieldname": "commission", "label": _("Hoa hồng"), "fieldtype": "Currency", "width": 110},
        {"fieldname": "gross_profit", "label": _("Lợi nhuận gộp"), "fieldtype": "Currency", "width": 130},
    ]


def get_data(filters):
    conditions = []
    values = {}
    joins = ""

    if filters.get("company"):
        conditions.append("p.company = %(company)s")
        values["company"] = filters["company"]
    if filters.get("pakd_type"):
        conditions.append("p.pakd_type = %(pakd_type)s")
        values["pakd_type"] = filters["pakd_type"]
    if filters.get("service_type"):
        conditions.append("p.service_type = %(service_type)s")
        values["service_type"] = filters["service_type"]
    if filters.get("customer"):
        conditions.append("p.customer = %(customer)s")
        values["customer"] = filters["customer"]
    if filters.get("contract_ref"):
        conditions.append("p.contract_ref = %(contract_ref)s")
        values["contract_ref"] = filters["contract_ref"]
    if filters.get("status"):
        conditions.append("p.status = %(status)s")
        values["status"] = filters["status"]
    if filters.get("from_date"):
        conditions.append("DATE(p.creation) >= %(from_date)s")
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions.append("DATE(p.creation) <= %(to_date)s")
        values["to_date"] = filters["to_date"]
    if filters.get("customer_group"):
        # customer_group lives on Customer, JOIN to filter
        joins = "LEFT JOIN `tabCustomer` c ON c.name = p.customer"
        conditions.append("c.customer_group = %(customer_group)s")
        values["customer_group"] = filters["customer_group"]

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    rows = frappe.db.sql(
        f"""
        SELECT
            p.pakd_type,
            p.service_type,
            p.name,
            p.customer,
            COALESCE(p.total_revenue_contract, 0)  AS revenue,
            COALESCE(p.total_manager_services, 0)  AS cost_ms,
            COALESCE(p.total_license_fee, 0)       AS cost_gpvt,
            COALESCE(p.total_add_costs, 0)         AS cost_add,
            COALESCE(p.total_sales_commission, 0)  AS commission
        FROM `tabPhuong An Kinh Doanh` p
        {joins}
        {where}
        ORDER BY p.pakd_type, p.service_type, p.name
        """,
        values,
        as_dict=True,
    )

    for r in rows:
        r["gross_profit"] = (
            r["revenue"] - r["cost_ms"] - r["cost_gpvt"] - r["cost_add"] - r["commission"]
        )

    return rows
