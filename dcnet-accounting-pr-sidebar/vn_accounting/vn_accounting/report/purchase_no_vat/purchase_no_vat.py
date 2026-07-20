"""Purchase No VAT report (FB-2026-00840).

Lists Purchase Invoices that don't have a linked EInvoice Inward record —
the proxy for "không có hóa đơn VAT" (chưa nhận được hóa đơn điện tử từ NCC).

Use case: KTT cuối tháng / quý cần soát lại các khoản mua chưa có hóa đơn VAT
để chủ động đòi hóa đơn từ NCC, hoặc kiểm tra phòng ban nào đề xuất mua mà
chưa hoàn thiện chứng từ.

Filters:
  - company (required)
  - view_mode: "Không có HĐ VAT" (default) / "Có HĐ VAT" (toggle để verify)
  - from_date / to_date (required) — posting_date range
  - department (multi-select on PI.custom_proposed_department field)
  - supplier (single Link)

Columns: số phiếu, ngày, NCC, tổng tiền, phòng ban đề xuất, mã hóa đơn VAT
(nếu có), tên file hóa đơn (nếu có), trạng thái.

Manual total row sums Currency only (Σ Tổng tiền).
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
    if not filters.get("from_date") or not filters.get("to_date"):
        frappe.throw(_("'Từ ngày' và 'Đến ngày' là bắt buộc."))
    if getdate(filters.get("from_date")) > getdate(filters.get("to_date")):
        frappe.throw(_("'Từ ngày' phải nhỏ hơn hoặc bằng 'Đến ngày'."))


def _get_columns():
    return [
        {"label": _("Số phiếu"), "fieldname": "name", "fieldtype": "Link", "options": "Purchase Invoice", "width": 160},
        {"label": _("Ngày"), "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        {"label": _("Nhà cung cấp"), "fieldname": "supplier", "fieldtype": "Link", "options": "Supplier", "width": 220},
        {"label": _("Tổng tiền"), "fieldname": "grand_total", "fieldtype": "Currency", "width": 140},
        {"label": _("Phòng ban đề xuất"), "fieldname": "custom_proposed_department", "fieldtype": "Link", "options": "Department", "width": 180},
        {"label": _("Mã HĐ VAT"), "fieldname": "einvoice_lookup_code", "fieldtype": "Data", "width": 140},
        {"label": _("EInvoice Inward"), "fieldname": "einvoice_inward", "fieldtype": "Link", "options": "EInvoice Inward", "width": 160},
        {"label": _("Trạng thái"), "fieldname": "status", "fieldtype": "Data", "width": 100},
    ]


def _get_data(filters):
    view_mode = filters.get("view_mode") or "Không có HĐ VAT"
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    departments = filters.get("department") or []
    supplier = filters.get("supplier")

    where = ["pi.docstatus = 1", "pi.company = %(company)s",
             "pi.posting_date BETWEEN %(from_date)s AND %(to_date)s"]
    params = {"company": company, "from_date": from_date, "to_date": to_date}

    # NOT EXISTS / EXISTS toggle on linked EInvoice Inward
    op = "NOT EXISTS" if view_mode == "Không có HĐ VAT" else "EXISTS"
    where.append(
        f"{op} (SELECT 1 FROM `tabEInvoice Inward` ei WHERE ei.linked_purchase_invoice = pi.name)"
    )

    if departments:
        where.append("pi.custom_proposed_department IN %(departments)s")
        params["departments"] = tuple(departments)
    if supplier:
        where.append("pi.supplier = %(supplier)s")
        params["supplier"] = supplier

    sql = f"""
        SELECT
            pi.name,
            pi.posting_date,
            pi.supplier,
            pi.grand_total,
            pi.custom_proposed_department,
            pi.status,
            (SELECT ei.lookup_code FROM `tabEInvoice Inward` ei
             WHERE ei.linked_purchase_invoice = pi.name LIMIT 1) AS einvoice_lookup_code,
            (SELECT ei.name FROM `tabEInvoice Inward` ei
             WHERE ei.linked_purchase_invoice = pi.name LIMIT 1) AS einvoice_inward
        FROM `tabPurchase Invoice` pi
        WHERE {' AND '.join(where)}
        ORDER BY pi.posting_date DESC, pi.name DESC
    """
    rows = frappe.db.sql(sql, params, as_dict=True)
    if not rows:
        return []

    # Manual total — Σ Currency only
    rows.append({
        "name": _("TỔNG CỘNG ({0} hóa đơn)").format(len(rows)),
        "grand_total": sum(flt(r["grand_total"]) for r in rows),
    })
    return rows
