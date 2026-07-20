"""Term Deposit Summary report.

3 view modes (filter `view_mode`):
  - "Đang gửi tại ngày": snapshot — shows TDs that were Active at to_date
    (start_date <= to_date AND (maturity_date >= to_date OR status NOT IN
    ('Settled', 'Early Settled', 'Cancelled'))). Date range from_date is
    advisory only in this mode; to_date drives the snapshot.
  - "Phát sinh trong kỳ": TDs whose start_date BETWEEN from_date AND to_date.
  - "Đáo hạn trong kỳ": TDs whose maturity_date BETWEEN from_date AND to_date.

Per-row computed columns:
  - days_to_maturity: maturity_date - today (negative if past, formatter
    highlights orange ≤30, red <0).
  - booked_interest: Σ Term Deposit Interest.interest_amount WHERE status='Booked'
    AND due_date <= to_date.
  - unbooked_interest: total_interest - booked_interest.

Total row aggregates principal_amount, total_interest, booked_interest,
unbooked_interest.
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import flt, getdate


def execute(filters=None):
    if not filters:
        return [], []

    _validate_filters(filters)
    columns = _get_columns()
    data = _get_data(filters)
    return columns, data


def _validate_filters(filters):
    if not filters.get("company"):
        frappe.throw(_("Vui lòng chọn Công ty."))
    if not filters.get("to_date"):
        frappe.throw(_("'Đến ngày' là bắt buộc."))
    if filters.get("from_date") and filters.get("from_date") > filters.get("to_date"):
        frappe.throw(_("'Từ ngày' phải nhỏ hơn hoặc bằng 'Đến ngày'."))


def _get_columns():
    return [
        {"label": _("Số phiếu"), "fieldname": "name", "fieldtype": "Link", "options": "Term Deposit", "width": 130},
        {"label": _("Số sổ TK"), "fieldname": "deposit_number", "fieldtype": "Data", "width": 130},
        {"label": _("Ngân hàng"), "fieldname": "bank", "fieldtype": "Link", "options": "Bank", "width": 130},
        {"label": _("TK 1281"), "fieldname": "deposit_account", "fieldtype": "Link", "options": "Account", "width": 160},
        {"label": _("Gốc"), "fieldname": "principal_amount", "fieldtype": "Currency", "width": 130},
        {"label": _("Lãi suất %"), "fieldname": "interest_rate", "fieldtype": "Percent", "width": 90},
        {"label": _("Kỳ hạn (tháng)"), "fieldname": "term_months", "fieldtype": "Int", "width": 100},
        {"label": _("Ngày gửi"), "fieldname": "start_date", "fieldtype": "Date", "width": 100},
        {"label": _("Ngày đáo hạn"), "fieldname": "maturity_date", "fieldtype": "Date", "width": 100},
        {"label": _("Số ngày tới đáo hạn"), "fieldname": "days_to_maturity", "fieldtype": "Int", "width": 110},
        {"label": _("Hình thức trả lãi"), "fieldname": "interest_type", "fieldtype": "Data", "width": 110},
        {"label": _("Tổng lãi dự kiến"), "fieldname": "total_interest", "fieldtype": "Currency", "width": 130},
        {"label": _("Lãi đã hạch toán"), "fieldname": "booked_interest", "fieldtype": "Currency", "width": 130},
        {"label": _("Lãi còn phải hạch toán"), "fieldname": "unbooked_interest", "fieldtype": "Currency", "width": 140},
        {"label": _("Trạng thái"), "fieldname": "status", "fieldtype": "Data", "width": 110},
    ]


def _get_data(filters):
    view_mode = filters.get("view_mode") or "Đang gửi tại ngày"
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    status_list = filters.get("status") or []
    bank = filters.get("bank")

    where = ["docstatus = 1", "company = %(company)s"]
    params = {"company": company, "from_date": from_date, "to_date": to_date}

    if view_mode == "Đang gửi tại ngày":
        # Snapshot: started on/before to_date AND not yet fully settled by to_date.
        where.append("start_date <= %(to_date)s")
        # status filter (default Active+Matured) controls what counts as "still open"
    elif view_mode == "Phát sinh trong kỳ":
        if not from_date:
            frappe.throw(_("Chế độ 'Phát sinh trong kỳ' cần 'Từ ngày'."))
        where.append("start_date BETWEEN %(from_date)s AND %(to_date)s")
    elif view_mode == "Đáo hạn trong kỳ":
        if not from_date:
            frappe.throw(_("Chế độ 'Đáo hạn trong kỳ' cần 'Từ ngày'."))
        where.append("maturity_date BETWEEN %(from_date)s AND %(to_date)s")

    if status_list:
        # MultiSelectList yields a Python list — bind as IN clause
        where.append("status IN %(status_list)s")
        params["status_list"] = tuple(status_list)
    if bank:
        where.append("bank = %(bank)s")
        params["bank"] = bank

    sql = f"""
        SELECT name, deposit_number, bank, deposit_account, principal_amount,
               interest_rate, term_months, start_date, maturity_date,
               interest_type, total_interest, status
        FROM `tabTerm Deposit`
        WHERE {' AND '.join(where)}
        ORDER BY maturity_date ASC, name ASC
    """
    rows = frappe.db.sql(sql, params, as_dict=True)
    if not rows:
        return []

    # Compute days_to_maturity + booked/unbooked interest in Python (small N expected)
    today = getdate(filters.get("to_date"))
    booked_map = _booked_interest_by_parent([r["name"] for r in rows], to_date)
    out = []
    for r in rows:
        booked = flt(booked_map.get(r["name"], 0))
        total = flt(r.get("total_interest"))
        out.append({
            **r,
            "days_to_maturity": (getdate(r["maturity_date"]) - today).days if r.get("maturity_date") else None,
            "booked_interest": booked,
            "unbooked_interest": max(total - booked, 0),
        })

    # Manual total row — only sums Currency columns. Skips Int (kỳ hạn months,
    # days_to_maturity) and Percent (interest_rate) which are not meaningful when
    # summed/averaged. add_total_row in JSON is 0 to disable Frappe's auto-sum.
    if out:
        out.append({
            "name": _("TỔNG CỘNG ({0} phiếu)").format(len(rows)),
            "principal_amount": sum(flt(r["principal_amount"]) for r in out),
            "interest_rate": None,
            "term_months": None,
            "days_to_maturity": None,
            "total_interest": sum(flt(r["total_interest"]) for r in out),
            "booked_interest": sum(flt(r["booked_interest"]) for r in out),
            "unbooked_interest": sum(flt(r["unbooked_interest"]) for r in out),
        })
    return out


def _booked_interest_by_parent(parent_names: list[str], to_date) -> dict[str, float]:
    if not parent_names:
        return {}
    placeholders = ",".join(["%s"] * len(parent_names))
    rows = frappe.db.sql(
        f"""
        SELECT parent, SUM(interest_amount) AS booked
        FROM `tabTerm Deposit Interest`
        WHERE parenttype = 'Term Deposit'
          AND status = 'Booked'
          AND due_date <= %s
          AND parent IN ({placeholders})
        GROUP BY parent
        """,
        [to_date, *parent_names],
        as_dict=True,
    )
    return {r["parent"]: flt(r["booked"]) for r in rows}
