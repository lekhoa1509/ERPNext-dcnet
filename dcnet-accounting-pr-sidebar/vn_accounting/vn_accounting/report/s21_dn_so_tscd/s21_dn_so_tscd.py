"""Sổ TSCĐ S21-DN — Fixed Asset Register per TT99/2025 format.

Columns match official form 01-TSCĐ: nguyên giá, số kỳ KH, tỷ lệ KH năm,
giá trị khấu hao năm, KH luỹ kế, giá trị còn lại.
"""
from __future__ import annotations

import frappe
from frappe import _


def execute(filters=None):
    filters = filters or {}
    columns = _get_columns()
    data = _get_data(filters)
    return columns, data


def _get_columns():
    return [
        {
            "label": _("Mã TS"),
            "fieldname": "asset_code",
            "fieldtype": "Link",
            "options": "Asset",
            "width": 120,
        },
        {
            "label": _("Tên tài sản"),
            "fieldname": "asset_name",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": _("Ngày đưa vào SD"),
            "fieldname": "available_for_use_date",
            "fieldtype": "Date",
            "width": 110,
        },
        {
            "label": _("Nguyên giá"),
            "fieldname": "gross_purchase_amount",
            "fieldtype": "Currency",
            "width": 140,
        },
        {
            "label": _("Số kỳ KH"),
            "fieldname": "num_periods",
            "fieldtype": "Int",
            "width": 80,
        },
        {
            "label": _("% KH năm"),
            "fieldname": "rate_pct",
            "fieldtype": "Float",
            "precision": 2,
            "width": 90,
        },
        {
            "label": _("GTKH năm"),
            "fieldname": "annual_depreciation",
            "fieldtype": "Currency",
            "width": 140,
        },
        {
            "label": _("KH luỹ kế"),
            "fieldname": "accumulated_depreciation_amount",
            "fieldtype": "Currency",
            "width": 140,
        },
        {
            "label": _("Giá trị còn lại"),
            "fieldname": "book_value",
            "fieldtype": "Currency",
            "width": 140,
        },
        {
            "label": _("Ghi chú"),
            "fieldname": "notes",
            "fieldtype": "Data",
            "width": 150,
        },
    ]


def _get_data(filters):
    company = filters.get("company")
    if not company:
        frappe.throw(_("Vui lòng chọn công ty"))

    conditions = ["a.docstatus = 1", "a.status != 'Scrapped'", "a.company = %(company)s"]
    params = {"company": company}

    if filters.get("asset_category"):
        conditions.append("a.asset_category = %(asset_category)s")
        params["asset_category"] = filters["asset_category"]

    if filters.get("location"):
        conditions.append("a.location = %(location)s")
        params["location"] = filters["location"]

    if filters.get("status"):
        conditions.append("a.status = %(status)s")
        params["status"] = filters["status"]

    where_sql = " AND ".join(conditions)

    rows = frappe.db.sql(
        """
        SELECT
            a.name AS asset_code,
            a.asset_name,
            a.available_for_use_date,
            a.total_asset_cost AS gross_purchase_amount,
            COALESCE(fb.total_number_of_depreciations, 0) AS num_periods,
            COALESCE(fb.rate_of_depreciation, 0) AS rate_pct,
            (a.total_asset_cost - a.value_after_depreciation) AS accumulated_depreciation_amount,
            a.value_after_depreciation AS book_value,
            NULL AS notes
        FROM `tabAsset` a
        LEFT JOIN `tabAsset Finance Book` fb ON fb.parent = a.name AND fb.idx = 1
        WHERE {where_sql}
        ORDER BY a.name
        """.format(where_sql=where_sql),
        params,
        as_dict=True,
    )

    for row in rows:
        rate = row.get("rate_pct") or 0
        gross = row.get("gross_purchase_amount") or 0
        row["annual_depreciation"] = round(gross * rate / 100, 0) if rate else 0

    return rows
