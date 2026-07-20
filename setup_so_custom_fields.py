"""
Script tạo Custom Fields cho Sales Order và Sales Order Item.
Chạy: bench --site flow.local execute /workspace/setup_so_custom_fields.py
"""
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

FIELDS = {
    "Sales Order": [
        # ── Thông tin hợp đồng ─────────────────────────────────────
        {
            "fieldname": "custom_hop_dong_section",
            "fieldtype": "Section Break",
            "label": "Thông tin hợp đồng",
            "insert_after": "po_date",
        },
        {
            "fieldname": "custom_contract_duration",
            "fieldtype": "Int",
            "label": "Thời hạn HĐ (tháng)",
            "insert_after": "custom_hop_dong_section",
        },
        {
            "fieldname": "custom_contract_expiry",
            "fieldtype": "Date",
            "label": "Ngày hết hạn Hợp đồng",
            "insert_after": "custom_contract_duration",
            "read_only": 1,
            "description": "Tự tính từ Ngày ký HĐ + Thời hạn HĐ",
        },
        {
            "fieldname": "custom_hop_dong_col_break",
            "fieldtype": "Column Break",
            "insert_after": "custom_contract_expiry",
        },
        {
            "fieldname": "custom_installation_zone",
            "fieldtype": "Select",
            "label": "Khu vực lắp đặt dịch vụ",
            "options": "\nBắc\nTrung\nNam\nToàn Quốc",
            "insert_after": "custom_hop_dong_col_break",
        },
        {
            "fieldname": "custom_opportunity",
            "fieldtype": "Link",
            "label": "Cơ hội",
            "options": "Opportunity",
            "insert_after": "custom_installation_zone",
        },
        {
            "fieldname": "custom_internal_notes",
            "fieldtype": "Small Text",
            "label": "Ghi chú nội bộ",
            "insert_after": "custom_opportunity",
        },
        # ── Tình trạng thực hiện (More Info tab, sau utm_campaign) ──
        {
            "fieldname": "custom_tinh_trang_section",
            "fieldtype": "Section Break",
            "label": "Tình trạng thực hiện",
            "insert_after": "utm_campaign",
        },
        {
            "fieldname": "custom_execution_status",
            "fieldtype": "Select",
            "label": "Tình trạng thực hiện",
            "options": "Chưa thực hiện\nĐang thực hiện\nHoàn thành",
            "default": "Chưa thực hiện",
            "insert_after": "custom_tinh_trang_section",
        },
        {
            "fieldname": "custom_revenue_status",
            "fieldtype": "Select",
            "label": "Tình trạng ghi doanh số",
            "options": "Bản nhập\nĐã ghi\nHủy",
            "default": "Bản nhập",
            "read_only": 1,
            "insert_after": "custom_execution_status",
        },
        {
            "fieldname": "custom_revenue_recognition_date",
            "fieldtype": "Date",
            "label": "Ngày ghi doanh số",
            "insert_after": "custom_revenue_status",
        },
        {
            "fieldname": "custom_tinh_trang_col_break",
            "fieldtype": "Column Break",
            "insert_after": "custom_revenue_recognition_date",
        },
        {
            "fieldname": "custom_payment_due_date",
            "fieldtype": "Date",
            "label": "Hạn thanh toán",
            "insert_after": "custom_tinh_trang_col_break",
        },
        {
            "fieldname": "custom_acceptance_date",
            "fieldtype": "Date",
            "label": "Ngày nghiệm thu tính cước",
            "read_only": 1,
            "insert_after": "custom_payment_due_date",
        },
        # ── Thông tin hóa đơn & giao hàng ──────────────────────────
        {
            "fieldname": "custom_billing_section",
            "fieldtype": "Section Break",
            "label": "Thông tin hóa đơn",
            "insert_after": "custom_acceptance_date",
            "collapsible": 1,
        },
        {
            "fieldname": "custom_billing_customer",
            "fieldtype": "Link",
            "label": "Khách hàng hóa đơn",
            "options": "Customer",
            "insert_after": "custom_billing_section",
        },
        {
            "fieldname": "custom_billing_address",
            "fieldtype": "Small Text",
            "label": "Địa chỉ hóa đơn",
            "insert_after": "custom_billing_customer",
        },
        {
            "fieldname": "custom_billing_col_break",
            "fieldtype": "Column Break",
            "insert_after": "custom_billing_address",
        },
        {
            "fieldname": "custom_shipping_recipient",
            "fieldtype": "Data",
            "label": "Người nhận hàng",
            "insert_after": "custom_billing_col_break",
        },
        {
            "fieldname": "custom_shipping_address",
            "fieldtype": "Small Text",
            "label": "Địa chỉ giao hàng",
            "insert_after": "custom_shipping_recipient",
        },
    ],
    "Sales Order Item": [
        {
            "fieldname": "custom_a_end",
            "fieldtype": "Data",
            "label": "Điểm lắp đặt A-End",
            "insert_after": "description",
        },
        {
            "fieldname": "custom_z_end",
            "fieldtype": "Data",
            "label": "Điểm lắp đặt Z-End",
            "insert_after": "custom_a_end",
        },
    ],
}


def run():
    create_custom_fields(FIELDS, update=True)
    frappe.db.commit()
    print("✅ Custom fields created successfully!")
    for dt, fields in FIELDS.items():
        real_fields = [f for f in fields if f["fieldtype"] not in ("Section Break", "Column Break")]
        print(f"  {dt}: {len(real_fields)} fields")


run()
