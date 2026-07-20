"""Scheduled task — sync trạng thái HĐ đầu ra (EasyInvoice) mỗi 15min."""
import frappe
from einvoice.einvoice.services.state_sync import sync_pending_invoices


def run_if_frequency_match():
    """Gate: chỉ chạy nếu auto_sync được bật trên EInvoice Settings."""
    settings = frappe.get_single("EInvoice Settings")
    if not settings.get("enable_auto_sync"):
        return
    try:
        result = sync_pending_invoices()
        frappe.logger().info(f"[EInvoice] Outward state sync: {result}")
    except Exception as e:
        frappe.log_error(
            title="[EInvoice] Outward sync error",
            message=str(e),
        )
