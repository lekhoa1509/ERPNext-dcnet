# Sổ Nhật Ký Chung (S03a-DN) theo Phụ lục IV TT99/2025/TT-BTC
import frappe
from frappe import _
from frappe.utils import flt, getdate


def execute(filters=None):
    if not filters:
        return [], []
    _validate(filters)
    cols = _columns()
    data, totals = _data(filters)
    if data:
        data.append({
            "posting_date": None,
            "voucher_no": "",
            "voucher_date": None,
            "remarks": _("Cộng phát sinh kỳ"),
            "ghi_so_cai": 0,
            "stt_dong": "",
            "against": "",
            "debit": totals["debit"],
            "credit": totals["credit"],
            "bold": 1,
        })
    return cols, data


def _validate(filters):
    if not filters.get("company"):
        frappe.throw(_("Công ty là bắt buộc"))
    if not filters.get("from_date") or not filters.get("to_date"):
        frappe.throw(_("Từ ngày và Đến ngày là bắt buộc"))
    if getdate(filters["from_date"]) > getdate(filters["to_date"]):
        frappe.throw(_("Từ ngày phải trước Đến ngày"))


def _columns():
    # Đúng thứ tự cột Phụ lục IV TT99/2025 — Mẫu S03a-DN
    return [
        {"fieldname": "posting_date", "label": _("Ngày ghi sổ"), "fieldtype": "Date", "width": 100,
         "description": _("Ngày ghi sổ kế toán (= ngày hạch toán chứng từ)")},
        {"fieldname": "voucher_no", "label": _("Số CT"), "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 150,
         "description": _("Số hiệu chứng từ kế toán")},
        {"fieldname": "voucher_date", "label": _("Ngày CT"), "fieldtype": "Date", "width": 100,
         "description": _("Ngày của chứng từ gốc")},
        {"fieldname": "remarks", "label": _("Diễn giải"), "fieldtype": "Data", "width": 240,
         "description": _("Nội dung nghiệp vụ kinh tế phát sinh")},
        {"fieldname": "ghi_so_cai", "label": _("Đã ghi SC"), "fieldtype": "Check", "width": 70,
         "description": _("Đã ghi Sổ Cái — luôn = ✓ vì GL Entry tồn tại")},
        {"fieldname": "stt_dong", "label": _("STT dòng"), "fieldtype": "Int", "width": 70,
         "description": _("Số thứ tự dòng trong cùng một bút toán")},
        {"fieldname": "account", "label": _("Tài khoản"), "fieldtype": "Link", "options": "Account", "width": 180,
         "description": _("Tài khoản kế toán của dòng này")},
        {"fieldname": "against", "label": _("TK đối ứng"), "fieldtype": "Data", "width": 200,
         "description": _("Tài khoản đối ứng của bút toán (theo Phụ lục IV TT99/2025)")},
        {"fieldname": "debit", "label": _("PS Nợ"), "fieldtype": "Currency", "width": 130,
         "description": _("Số phát sinh bên Nợ")},
        {"fieldname": "credit", "label": _("PS Có"), "fieldtype": "Currency", "width": 130,
         "description": _("Số phát sinh bên Có")},
    ]


def _data(filters):
    rows = frappe.db.sql(
        """
        SELECT gle.posting_date,
               gle.voucher_no,
               gle.voucher_type,
               gle.transaction_date AS voucher_date,
               gle.remarks,
               gle.account,
               gle.against,
               gle.debit,
               gle.credit,
               gle.creation
        FROM `tabGL Entry` gle
        WHERE gle.company = %(company)s
          AND gle.posting_date BETWEEN %(from_date)s AND %(to_date)s
          AND gle.is_cancelled = 0
        ORDER BY gle.posting_date ASC, gle.creation ASC
        """,
        filters,
        as_dict=True,
    )

    result = []
    totals = {"debit": 0.0, "credit": 0.0}
    last_voucher = None
    stt = 0
    for r in rows:
        key = (r.posting_date, r.voucher_no)
        if key != last_voucher:
            stt = 1
            last_voucher = key
        else:
            stt += 1
        debit = flt(r.debit)
        credit = flt(r.credit)
        totals["debit"] += debit
        totals["credit"] += credit
        result.append({
            "posting_date": r.posting_date if stt == 1 else None,
            "voucher_no": r.voucher_no if stt == 1 else "",
            "voucher_type": r.voucher_type,
            "voucher_date": r.voucher_date if stt == 1 else None,
            "remarks": r.remarks if stt == 1 else "",
            "ghi_so_cai": 1,
            "stt_dong": stt,
            "account": r.account,
            "against": r.against or "",
            "debit": debit,
            "credit": credit,
        })

    return result, totals
