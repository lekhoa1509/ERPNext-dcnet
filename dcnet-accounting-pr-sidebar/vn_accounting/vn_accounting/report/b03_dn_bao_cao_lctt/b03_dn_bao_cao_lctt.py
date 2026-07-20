"""B03-DN Báo cáo lưu chuyển tiền tệ (Cash Flow Statement) — TT99/2025."""
from decimal import Decimal

import frappe
from frappe import _
from frappe.utils import getdate, today

from vn_accounting.financial_reporting.resolver import resolve_all_lines


def execute(filters=None):
    filters = frappe._dict(filters or {})
    company = filters.company or frappe.defaults.get_user_default("Company")

    import datetime
    if filters.from_date and filters.to_date:
        period_start = getdate(filters.from_date)
        period_end = getdate(filters.to_date)
    else:
        today_date = getdate(today())
        from frappe.utils import get_first_day, get_last_day
        period_start = get_first_day(today_date)
        period_end = get_last_day(today_date)

    columns = _get_columns()
    data = _get_data(company, period_start, period_end)
    return columns, data


def _get_columns():
    return [
        {
            "fieldname": "code",
            "label": _("Mã"),
            "fieldtype": "Data",
            "width": 70,
        },
        {
            "fieldname": "label",
            "label": _("Tên chỉ tiêu"),
            "fieldtype": "Data",
            "width": 320,
        },
        {
            "fieldname": "current_value",
            "label": _("Kỳ này"),
            "fieldtype": "Currency",
            "width": 160,
        },
        {
            "fieldname": "prior_value",
            "label": _("Kỳ trước"),
            "fieldtype": "Currency",
            "width": 160,
        },
        {
            "fieldname": "account_formula",
            "label": _("Công thức"),
            "fieldtype": "Data",
            "width": 200,
            "hidden": 1,
        },
    ]


def _get_data(company, period_start, period_end):
    mapping_lines = _load_bctc_mapping(company, "b03")
    if not mapping_lines:
        return _no_mapping_message()

    import datetime
    # Prior period = same date range in the previous year
    delta_days = (period_end - period_start).days
    prior_end = datetime.date(period_end.year - 1, period_end.month, period_end.day)
    prior_start = prior_end - datetime.timedelta(days=delta_days)

    current_results = resolve_all_lines(company, mapping_lines, period_start, period_end)
    prior_results = resolve_all_lines(company, mapping_lines, prior_start, prior_end)
    prior_map = {line.get("code"): val for line, val in prior_results}

    rows = []
    for line, current_value in current_results:
        code = line.get("code") or ""
        indent = int(line.get("display_indent") or 0)
        indent_str = " " * (indent * 4)
        label = f"{indent_str}{line.get('label') or ''}"

        row = frappe._dict(
            code=code,
            label=label,
            current_value=float(current_value or 0),
            prior_value=float(prior_map.get(code) or 0),
            account_formula=line.get("account_formula") or line.get("line_formula") or "",
        )
        if line.get("is_subtotal"):
            row["bold"] = 1

        rows.append(row)

    return rows


def _load_bctc_mapping(company, report_type):
    mapping_name = frappe.db.get_value("BCTC Mapping", {"company": company}, "name")
    if not mapping_name:
        return []
    field_map = {"b01": "b01_lines", "b02": "b02_lines", "b03": "b03_lines"}
    child_field = field_map.get(report_type, "b03_lines")
    mapping = frappe.get_doc("BCTC Mapping", mapping_name)
    return mapping.get(child_field) or []


def _no_mapping_message():
    return [
        frappe._dict(
            code="",
            label=_("Chưa có cấu hình BCTC Mapping cho công ty này. "
                     "Mở Cấu hình BCTC để thiết lập."),
            current_value=0,
            prior_value=0,
            account_formula="",
        )
    ]
