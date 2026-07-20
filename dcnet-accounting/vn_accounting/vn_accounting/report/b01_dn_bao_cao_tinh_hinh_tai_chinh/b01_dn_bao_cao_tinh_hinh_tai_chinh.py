"""B01-DN Báo cáo tình hình tài chính (Balance Sheet) — TT99/2025."""
import datetime
from decimal import Decimal

import frappe
from frappe import _
from frappe.utils import getdate, today

from vn_accounting.financial_reporting.resolver import resolve_all_lines


def execute(filters=None):
    filters = frappe._dict(filters or {})
    company = filters.company or frappe.defaults.get_user_default("Company")
    as_on_date = getdate(filters.as_on_date or today())

    columns = _get_columns()
    data = _get_data(company, as_on_date)
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
            "label": _("Số cuối kỳ"),
            "fieldtype": "Currency",
            "width": 160,
        },
        {
            "fieldname": "prior_value",
            "label": _("Số đầu năm"),
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


def _get_data(company, as_on_date):
    mapping = _load_bctc_mapping(company, "b01")
    if not mapping:
        return _no_mapping_message()

    # Prior value = end of previous calendar year (Dec 31 of year-1)
    prior_date = datetime.date(as_on_date.year, 1, 1) - datetime.timedelta(days=1)

    # Resolve current and prior values
    current_results = resolve_all_lines(company, mapping, datetime.date(2000, 1, 1), as_on_date)
    prior_results = resolve_all_lines(company, mapping, datetime.date(2000, 1, 1), prior_date)

    # Inject current-fiscal-year unallocated P&L into the equity side. Without
    # this, an interim balance sheet (run before the year's Period Closing
    # Voucher) shows 5xx/7xx revenue and 6xx/8xx expense balances open in GL
    # but never reflected on the equity side via ma 421, so ma 270 != ma 440.
    current_results = _inject_interim_pnl(company, current_results, as_on_date)
    prior_results = _inject_interim_pnl(company, prior_results, prior_date)

    prior_map = {line.get("code"): val for line, val in prior_results}

    rows = []
    for line, current_value in current_results:
        code = line.get("code") or ""
        indent = int(line.get("display_indent") or 0)
        is_subtotal = line.get("is_subtotal")

        indent_str = " " * (indent * 4)  # non-breaking spaces for visual indent
        label = f"{indent_str}{line.get('label') or ''}"

        row = frappe._dict(
            code=code,
            label=label,
            current_value=float(current_value or 0),
            prior_value=float(prior_map.get(code) or 0),
            account_formula=line.get("account_formula") or line.get("line_formula") or "",
        )

        if is_subtotal:
            row["bold"] = 1

        rows.append(row)

    # Check B01 equation: mã_270 == mã_440 (assets = liabilities + equity)
    _append_balance_check(rows, current_results)

    return rows


def _fiscal_year_start(company, as_on_date):
    """Return the start date of the fiscal year covering as_on_date."""
    fy = frappe.db.sql(
        """
        SELECT year_start_date FROM `tabFiscal Year`
        WHERE disabled = 0
          AND year_start_date <= %(d)s AND year_end_date >= %(d)s
        ORDER BY year_start_date DESC LIMIT 1
        """,
        {"d": as_on_date},
        as_dict=True,
    )
    if fy and fy[0].year_start_date:
        return getdate(fy[0].year_start_date)
    return datetime.date(as_on_date.year, 1, 1)


def _interim_unallocated_pnl(company, as_on_date):
    """Current-fiscal-year net profit not yet closed via Period Closing Voucher.

    Formula = (Cr - Dr) of 5xx + 7xx accounts in the FY-to-date period
              - (Dr - Cr) of 6xx + 8xx accounts in the same period
    PCV entries are excluded so closed prior-year P&L doesn't double count
    via TK 4211 (which ma 421% already captures).
    """
    fy_start = _fiscal_year_start(company, as_on_date)
    row = frappe.db.sql(
        """
        SELECT
            SUM(CASE WHEN LEFT(account, 1) IN ('5','7') THEN credit - debit ELSE 0 END) AS revenue_net,
            SUM(CASE WHEN LEFT(account, 1) IN ('6','8') THEN debit - credit ELSE 0 END) AS expense_net
        FROM `tabGL Entry`
        WHERE company = %(company)s
          AND is_cancelled = 0
          AND voucher_type != 'Period Closing Voucher'
          AND posting_date BETWEEN %(fy_start)s AND %(as_on)s
          AND LEFT(account, 1) IN ('5','6','7','8')
        """,
        {"company": company, "fy_start": fy_start, "as_on": as_on_date},
        as_dict=True,
    )
    if not row:
        return Decimal(0)
    revenue_net = Decimal(str(row[0].revenue_net or 0))
    expense_net = Decimal(str(row[0].expense_net or 0))
    return revenue_net - expense_net


def _inject_interim_pnl(company, results, as_on_date):
    """Insert synthetic line 421b after 421 and add its value into 420/400/440.

    The injection mirrors what a Period Closing Voucher would do at year-end:
    move accrued 5xx/6xx/7xx/8xx net to the equity side as undistributed
    earnings of the current period.
    """
    pnl = _interim_unallocated_pnl(company, as_on_date)
    if pnl == 0:
        return results

    insert_at = None
    for i, (line, _val) in enumerate(results):
        if (line.get("code") or "") == "421":
            insert_at = i + 1
            break
    if insert_at is None:
        for i, (line, _val) in enumerate(results):
            if (line.get("code") or "") == "420":
                insert_at = i
                break
    if insert_at is None:
        return results

    synthetic_line = frappe._dict({
        "code": "421b",
        "label": "Lợi nhuận chưa phân phối kỳ này (chưa kết chuyển)",
        "value_type": "synthetic",
        "account_formula": "5xx+7xx − 6xx−8xx (FY-to-date)",
        "line_formula": "",
        "display_indent": 2,
        "is_subtotal": 0,
    })
    new_results = list(results)
    new_results.insert(insert_at, (synthetic_line, pnl))

    bubble_codes = {"420", "400", "440"}
    for i, (line, val) in enumerate(new_results):
        if (line.get("code") or "") in bubble_codes:
            new_results[i] = (line, (val or Decimal(0)) + pnl)

    return new_results


def _load_bctc_mapping(company, report_type):
    """Load BCTC Mapping lines for a given report type (b01/b02/b03)."""
    mapping_name = frappe.db.get_value("BCTC Mapping", {"company": company}, "name")
    if not mapping_name:
        return []

    field_map = {"b01": "b01_lines", "b02": "b02_lines", "b03": "b03_lines"}
    child_field = field_map.get(report_type, "b01_lines")

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


def _append_balance_check(rows, current_results):
    """Append a balance warning row if mã_270 != mã_440."""
    resolved = {line.get("code"): val for line, val in current_results}
    ma_270 = resolved.get("270") or Decimal(0)
    ma_440 = resolved.get("440") or Decimal(0)

    tolerance = Decimal(str(
        frappe.db.get_single_value("VN Accounting Settings", "period_closing_balance_tolerance") or 1
    ))

    diff = abs(ma_270 - ma_440)
    if diff > tolerance:
        rows.append(frappe._dict(
            code="CHK",
            label=f"⚠️ Mất cân đối B01: Mã 270 ({ma_270:,.0f}) ≠ Mã 440 ({ma_440:,.0f}). "
                  f"Chênh lệch {diff:,.0f}. Kiểm tra BCTC Mapping.",
            current_value=0,
            prior_value=0,
            account_formula="",
            bold=1,
        ))
