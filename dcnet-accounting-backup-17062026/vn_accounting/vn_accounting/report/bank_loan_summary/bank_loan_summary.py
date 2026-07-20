"""Bank Loan Summary report.

3 view modes (filter `view_mode`):
  - "Lịch trả nợ trong kỳ" (default): repayment-row-level. 1 row per Bank Loan
    Repayment with due_date BETWEEN from_date AND to_date. Use case: KTT runs
    on the 1st and 15th of each month, sees what's due in the next 15 days.
  - "Đang vay (toàn cảnh)": loan-row-level. All Bank Loans matching status
    filter, no date filter. Use case: full overview of debt portfolio.
  - "Đáo hạn trong kỳ": loan-row-level. Bank Loans whose maturity_date BETWEEN
    from_date AND to_date. Use case: planning final-settlement cash needs.

Per-row computed columns:
  - "Lịch trả nợ" mode: days_to_due (red if past due AND not Booked, orange ≤7)
  - Loan-row modes: days_to_maturity (red if past, orange ≤30)
  - "Lịch trả nợ" mode: paid_periods / total_periods (counts of repayment rows
    by status from the parent's full schedule).

Total row aggregates the relevant amount columns.
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import flt, getdate


def execute(filters=None):
    if not filters:
        return [], []

    _validate_filters(filters)
    view_mode = filters.get("view_mode") or "Lịch trả nợ trong kỳ"
    if view_mode == "Lịch trả nợ trong kỳ":
        return _get_columns_repayment(), _get_data_repayment(filters)
    return _get_columns_loan(view_mode), _get_data_loan(filters, view_mode)


def _validate_filters(filters):
    if not filters.get("company"):
        frappe.throw(_("Vui lòng chọn Công ty."))
    if not filters.get("to_date"):
        frappe.throw(_("'Đến ngày' là bắt buộc."))
    if filters.get("from_date") and filters.get("from_date") > filters.get("to_date"):
        frappe.throw(_("'Từ ngày' phải nhỏ hơn hoặc bằng 'Đến ngày'."))


# ── Mode: Lịch trả nợ trong kỳ ──────────────────────────────────────────────

def _get_columns_repayment():
    return [
        {"label": _("Số phiếu vay"), "fieldname": "loan_name", "fieldtype": "Link", "options": "Bank Loan", "width": 130},
        {"label": _("Ngân hàng"), "fieldname": "bank", "fieldtype": "Link", "options": "Bank", "width": 130},
        {"label": _("Số HĐ vay"), "fieldname": "loan_number", "fieldtype": "Data", "width": 130},
        {"label": _("Ngày đến hạn trả"), "fieldname": "due_date", "fieldtype": "Date", "width": 110},
        {"label": _("Số ngày tới hạn"), "fieldname": "days_to_due", "fieldtype": "Int", "width": 100},
        {"label": _("Gốc kỳ này"), "fieldname": "principal_amount", "fieldtype": "Currency", "width": 120},
        {"label": _("Lãi kỳ này"), "fieldname": "interest_amount", "fieldtype": "Currency", "width": 120},
        {"label": _("Tổng phải trả"), "fieldname": "total_amount", "fieldtype": "Currency", "width": 120},
        {"label": _("Số dư sau trả"), "fieldname": "outstanding_after", "fieldtype": "Currency", "width": 130},
        {"label": _("JE đã hạch toán"), "fieldname": "journal_entry", "fieldtype": "Link", "options": "Journal Entry", "width": 130},
        {"label": _("Trạng thái kỳ"), "fieldname": "repayment_status", "fieldtype": "Data", "width": 110},
        {"label": _("Trạng thái khoản vay"), "fieldname": "loan_status", "fieldtype": "Data", "width": 130},
    ]


def _get_data_repayment(filters):
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    status_list = filters.get("status") or []
    bank = filters.get("bank")

    where = ["bl.docstatus = 1", "bl.company = %(company)s", "br.due_date <= %(to_date)s"]
    params = {"company": company, "from_date": from_date, "to_date": to_date}

    if from_date:
        where.append("br.due_date >= %(from_date)s")
    if status_list:
        where.append("bl.status IN %(status_list)s")
        params["status_list"] = tuple(status_list)
    if bank:
        where.append("bl.bank = %(bank)s")
        params["bank"] = bank

    sql = f"""
        SELECT
            bl.name AS loan_name,
            bl.bank,
            bl.loan_number,
            br.due_date,
            br.principal_amount,
            br.interest_amount,
            br.total_amount,
            br.outstanding_after,
            br.journal_entry,
            br.status AS repayment_status,
            bl.status AS loan_status
        FROM `tabBank Loan Repayment` br
        INNER JOIN `tabBank Loan` bl ON br.parent = bl.name
        WHERE br.parenttype = 'Bank Loan'
          AND {' AND '.join(where)}
        ORDER BY br.due_date ASC, bl.name ASC, br.idx ASC
    """
    rows = frappe.db.sql(sql, params, as_dict=True)
    if not rows:
        return []

    today = getdate()
    for r in rows:
        r["days_to_due"] = (getdate(r["due_date"]) - today).days if r.get("due_date") else None

    # Manual total — Σ Currency only. days_to_due is per-row delta, not summable.
    # outstanding_after is a snapshot per row (= dư nợ sau từng kỳ trả), not summable.
    rows.append({
        "loan_name": _("TỔNG CỘNG ({0} kỳ)").format(len(rows)),
        "days_to_due": None,
        "principal_amount": sum(flt(r["principal_amount"]) for r in rows),
        "interest_amount": sum(flt(r["interest_amount"]) for r in rows),
        "total_amount": sum(flt(r["total_amount"]) for r in rows),
        # outstanding_after is a per-row snapshot (dư nợ sau kỳ trả), not summable.
        # Set None to render blank instead of default "VND 0".
        "outstanding_after": None,
    })
    return rows


# ── Modes: Đang vay (toàn cảnh) + Đáo hạn trong kỳ ─────────────────────────

def _get_columns_loan(view_mode):
    return [
        {"label": _("Số phiếu vay"), "fieldname": "name", "fieldtype": "Link", "options": "Bank Loan", "width": 130},
        {"label": _("Ngân hàng"), "fieldname": "bank", "fieldtype": "Link", "options": "Bank", "width": 130},
        {"label": _("Số HĐ vay"), "fieldname": "loan_number", "fieldtype": "Data", "width": 140},
        {"label": _("TK vay (3411)"), "fieldname": "loan_account", "fieldtype": "Link", "options": "Account", "width": 160},
        {"label": _("Ngày giải ngân"), "fieldname": "start_date", "fieldtype": "Date", "width": 110},
        {"label": _("Ngày đáo hạn"), "fieldname": "maturity_date", "fieldtype": "Date", "width": 110},
        {"label": _("Số ngày tới đáo hạn"), "fieldname": "days_to_maturity", "fieldtype": "Int", "width": 110},
        {"label": _("Số tiền vay"), "fieldname": "loan_amount", "fieldtype": "Currency", "width": 130},
        # NOT _("Outstanding") — vn_translation maps "Outstanding" → "Quá hạn"
        # which is wrong here (Outstanding = số dư, không phải overdue).
        {"label": "Số dư còn lại", "fieldname": "outstanding_amount", "fieldtype": "Currency", "width": 130},
        {"label": _("Lãi suất %"), "fieldname": "interest_rate", "fieldtype": "Percent", "width": 90},
        {"label": _("Loại lãi"), "fieldname": "rate_type", "fieldtype": "Data", "width": 80},
        {"label": _("Hình thức trả"), "fieldname": "repayment_type", "fieldtype": "Data", "width": 110},
        {"label": _("Tần suất"), "fieldname": "repayment_frequency", "fieldtype": "Data", "width": 90},
        {"label": _("Đã trả / Tổng kỳ"), "fieldname": "periods_progress", "fieldtype": "Data", "width": 110},
        {"label": _("Trạng thái"), "fieldname": "status", "fieldtype": "Data", "width": 100},
    ]


def _get_data_loan(filters, view_mode):
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    status_list = filters.get("status") or []
    bank = filters.get("bank")

    where = ["docstatus = 1", "company = %(company)s"]
    params = {"company": company, "from_date": from_date, "to_date": to_date}

    if view_mode == "Đáo hạn trong kỳ":
        if not from_date:
            frappe.throw(_("Chế độ 'Đáo hạn trong kỳ' cần 'Từ ngày'."))
        where.append("maturity_date BETWEEN %(from_date)s AND %(to_date)s")
    # "Đang vay (toàn cảnh)" — no date constraint

    if status_list:
        where.append("status IN %(status_list)s")
        params["status_list"] = tuple(status_list)
    if bank:
        where.append("bank = %(bank)s")
        params["bank"] = bank

    sql = f"""
        SELECT name, bank, loan_number, loan_account, start_date, maturity_date,
               loan_amount, outstanding_amount, interest_rate, rate_type,
               repayment_type, repayment_frequency, status
        FROM `tabBank Loan`
        WHERE {' AND '.join(where)}
        ORDER BY maturity_date ASC, name ASC
    """
    rows = frappe.db.sql(sql, params, as_dict=True)
    if not rows:
        return []

    today = getdate()
    progress_map = _periods_progress([r["name"] for r in rows])
    for r in rows:
        r["days_to_maturity"] = (getdate(r["maturity_date"]) - today).days if r.get("maturity_date") else None
        prog = progress_map.get(r["name"], (0, 0))
        r["periods_progress"] = f"{prog[0]} / {prog[1]}" if prog[1] else ""

    # Manual total — Σ Currency only. days_to_maturity, interest_rate, periods_progress
    # are not meaningful when summed/averaged.
    rows.append({
        "name": _("TỔNG CỘNG ({0} khoản)").format(len(rows)),
        "days_to_maturity": None,
        "interest_rate": None,
        "loan_amount": sum(flt(r["loan_amount"]) for r in rows),
        "outstanding_amount": sum(flt(r["outstanding_amount"]) for r in rows),
    })
    return rows


def _periods_progress(loan_names: list[str]) -> dict[str, tuple[int, int]]:
    if not loan_names:
        return {}
    placeholders = ",".join(["%s"] * len(loan_names))
    rows = frappe.db.sql(
        f"""
        SELECT parent,
               SUM(CASE WHEN status = 'Booked' THEN 1 ELSE 0 END) AS paid,
               COUNT(*) AS total
        FROM `tabBank Loan Repayment`
        WHERE parenttype = 'Bank Loan' AND parent IN ({placeholders})
        GROUP BY parent
        """,
        loan_names,
        as_dict=True,
    )
    return {r["parent"]: (int(r["paid"] or 0), int(r["total"] or 0)) for r in rows}
