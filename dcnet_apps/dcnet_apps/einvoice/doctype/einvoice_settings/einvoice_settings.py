import frappe
from frappe.model.document import Document


class EInvoiceSettings(Document):
    """Central settings for E-Invoice Integration."""

    @frappe.whitelist()
    def sync_now(self):
        """Trigger an immediate sync of inward invoices from all active providers."""
        from dcnet_apps.einvoice.tasks.sync_inward_invoices import run_sync

        frappe.enqueue(
            run_sync,
            queue="long",
            timeout=600,
            sync_type="Manual",
        )
        frappe.msgprint("Đã khởi chạy đồng bộ hóa đơn mua vào ở chế độ nền.", alert=True)

    @frappe.whitelist()
    def test_connection(self):
        """Test connection to the default provider."""
        if not self.default_provider:
            frappe.throw("Vui lòng chọn Nhà cung cấp HĐĐT mặc định trước.")

        provider_doc = frappe.get_doc("EInvoice Provider", self.default_provider)
        provider_doc.test_connection()
