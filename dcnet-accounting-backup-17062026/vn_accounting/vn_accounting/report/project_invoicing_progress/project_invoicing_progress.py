"""Project Invoicing Progress — Bảng tiến độ xuất hóa đơn.

Theo dõi từng stage: ngày dự kiến, trạng thái, days_to_due, giá xuất, SI link.
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import flt, getdate, today, date_diff


_STATUS_INDICATORS = {
    "Đã xuất HĐ": "green",
    "Đã thu tiền": "green",
    "Đã có SI draft": "blue",
    "Chờ xuất HĐ": "orange",
    "Đang thi công": "blue",
    "Dự kiến": "gray",
    "Đã hủy": "red",
}


def execute(filters=None):
    filters = filters or {}
    columns = _columns()
    data = _fetch(filters)
    return columns, data


def _columns():
    return [
        {"fieldname": "parent_costing", "label": _("Công trình"), "fieldtype": "Link", "options": "Project Costing", "width": 160},
        {"fieldname": "stage_order", "label": _("Thứ tự"), "fieldtype": "Int", "width": 70},
        {"fieldname": "stage_name", "label": _("Giai đoạn"), "fieldtype": "Data", "width": 180},
        {"fieldname": "status", "label": _("Trạng thái"), "fieldtype": "Data", "width": 130},
        {"fieldname": "expected_invoice_date", "label": _("Ngày dự kiến"), "fieldtype": "Date", "width": 110},
        {"fieldname": "days_to_due", "label": _("Còn (ngày)"), "fieldtype": "Int", "width": 90},
        {"fieldname": "cost_pinned", "label": _("CP đã pin"), "fieldtype": "Currency", "options": "currency", "width": 130},
        {"fieldname": "price_final", "label": _("Giá xuất HĐ"), "fieldtype": "Currency", "options": "currency", "width": 130},
        {"fieldname": "sales_invoice", "label": _("Hóa đơn"), "fieldtype": "Link", "options": "Sales Invoice", "width": 140},
    ]


def _fetch(filters):
    company = filters.get("company")
    project = filters.get("project")
    status = filters.get("status")
    due_within = filters.get("due_within_days")

    rows = frappe.db.sql("""
        SELECT s.name, s.parent_costing, s.stage_order, s.stage_name, s.status,
               s.expected_invoice_date, s.cost_pinned, s.price_suggested,
               s.price_override, s.sales_invoice
        FROM `tabProject Costing Stage` s
        JOIN `tabProject Costing` pc ON pc.name = s.parent_costing
        WHERE pc.company = %(company)s
          AND (%(project)s = '' OR s.parent_costing = %(project)s)
          AND (%(status)s = '' OR s.status = %(status)s)
        ORDER BY s.expected_invoice_date ASC, s.parent_costing ASC, s.stage_order ASC
    """, {"company": company, "project": project or "", "status": status or ""}, as_dict=True)

    today_d = getdate(today())
    out = []
    for r in rows:
        days = None
        if r.expected_invoice_date:
            days = date_diff(r.expected_invoice_date, today_d)
        # Filter due_within
        if due_within is not None and due_within != "":
            try:
                limit = int(due_within)
                if days is None or days > limit:
                    continue
            except (TypeError, ValueError):
                pass
        out.append({
            "parent_costing": r.parent_costing,
            "stage_order": r.stage_order,
            "stage_name": r.stage_name,
            "status": r.status,
            "expected_invoice_date": r.expected_invoice_date,
            "days_to_due": days,
            "cost_pinned": flt(r.cost_pinned),
            "price_final": flt(r.price_override or r.price_suggested),
            "sales_invoice": r.sales_invoice or "",
            "currency": "VND",
        })
    return out


def get_indicator(row):
    """Used by list view styling (Frappe Script Report supports via JS file)."""
    status = row.get("status")
    color = _STATUS_INDICATORS.get(status, "gray")
    return [status or "", color, f"status,=,{status}"]
