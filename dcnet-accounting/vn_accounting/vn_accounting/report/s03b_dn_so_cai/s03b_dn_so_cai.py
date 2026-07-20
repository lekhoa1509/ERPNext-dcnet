# Sổ Cái (S03b-DN) theo Phụ lục IV TT99/2025/TT-BTC
import frappe
from frappe import _
from frappe.utils import flt, getdate

from vn_accounting.vn_accounting.report_utils import (
    build_summary_cards,
    build_summary_rows,
    split_balance,
)


def execute(filters=None):
    if not filters:
        return [], []
    _validate(filters)
    cols = _columns()

    opening_debit, opening_credit = _opening_balance(filters)
    txn_rows, period_debit, period_credit = _transactions(filters)

    opening_net = opening_debit - opening_credit
    closing_net = opening_net + period_debit - period_credit
    opening_dr, opening_cr = split_balance(opening_net)
    closing_dr, closing_cr = split_balance(closing_net)

    # 3 dòng tóm tắt PIN ở ĐẦU data table (KTT quét nhanh không cần scroll).
    summary_rows = build_summary_rows(
        opening_dr, opening_cr, period_debit, period_credit,
        closing_dr, closing_cr,
        from_date=filters["from_date"], to_date=filters["to_date"],
    )
    data = [*summary_rows, *txn_rows]

    # 4 cards lơ lửng trên data table (Frappe native report_summary widget).
    summary_cards = build_summary_cards(opening_net, period_debit, period_credit, closing_net)

    return cols, data, None, None, summary_cards


def _validate(filters):
    if not filters.get("company"):
        frappe.throw(_("Công ty là bắt buộc"))
    if not filters.get("account"):
        frappe.throw(_("Tài khoản là bắt buộc"))
    if not filters.get("from_date") or not filters.get("to_date"):
        frappe.throw(_("Từ ngày và Đến ngày là bắt buộc"))
    if getdate(filters["from_date"]) > getdate(filters["to_date"]):
        frappe.throw(_("Từ ngày phải trước Đến ngày"))


def _columns():
    return [
        {"fieldname": "posting_date", "label": _("Ngày ghi sổ"), "fieldtype": "Date", "width": 100,
         "description": _("Ngày ghi sổ kế toán")},
        {"fieldname": "voucher_no", "label": _("Số CT"), "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 150,
         "description": _("Số hiệu chứng từ")},
        {"fieldname": "voucher_date", "label": _("Ngày CT"), "fieldtype": "Date", "width": 100,
         "description": _("Ngày chứng từ gốc")},
        {"fieldname": "remarks", "label": _("Diễn giải"), "fieldtype": "Data", "width": 260,
         "description": _("Nội dung nghiệp vụ phát sinh")},
        {"fieldname": "against", "label": _("TK đối ứng"), "fieldtype": "Data", "width": 220,
         "description": _("Tài khoản đối ứng của bút toán")},
        {"fieldname": "debit", "label": _("PS Nợ"), "fieldtype": "Currency", "width": 130,
         "description": _("Số phát sinh bên Nợ")},
        {"fieldname": "credit", "label": _("PS Có"), "fieldtype": "Currency", "width": 130,
         "description": _("Số phát sinh bên Có")},
    ]


def _opening_balance(filters):
    r = frappe.db.sql(
        """
        SELECT IFNULL(SUM(debit),0) AS d, IFNULL(SUM(credit),0) AS c
        FROM `tabGL Entry`
        WHERE company = %(company)s
          AND account = %(account)s
          AND posting_date < %(from_date)s
          AND is_cancelled = 0
        """,
        filters,
        as_dict=True,
    )[0]
    return flt(r.d), flt(r.c)


def _transactions(filters):
    rows = frappe.db.sql(
        """
        SELECT posting_date, voucher_no, voucher_type, transaction_date AS voucher_date,
               remarks, against, debit, credit, creation
        FROM `tabGL Entry`
        WHERE company = %(company)s
          AND account = %(account)s
          AND posting_date BETWEEN %(from_date)s AND %(to_date)s
          AND is_cancelled = 0
        ORDER BY posting_date ASC, creation ASC
        """,
        filters,
        as_dict=True,
    )
    result = []
    period_debit = 0.0
    period_credit = 0.0
    for r in rows:
        debit = flt(r.debit)
        credit = flt(r.credit)
        period_debit += debit
        period_credit += credit
        result.append({
            "posting_date": r.posting_date,
            "voucher_no": r.voucher_no,
            "voucher_type": r.voucher_type,
            "voucher_date": r.voucher_date,
            "remarks": r.remarks or "",
            "against": r.against or "",
            "debit": debit,
            "credit": credit,
        })
    return result, period_debit, period_credit
