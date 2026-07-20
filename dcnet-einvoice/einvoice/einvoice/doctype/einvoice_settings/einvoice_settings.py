import frappe
from frappe.model.document import Document


class EInvoiceSettings(Document):
    """Central settings for E-Invoice Integration."""

    @frappe.whitelist()
    def sync_now(self):
        """Trigger an immediate sync of inward invoices from all active providers."""
        from einvoice.einvoice.services.sync import SyncService

        frappe.enqueue(
            SyncService.run_sync,
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

        from einvoice.einvoice.doctype.einvoice_provider.einvoice_provider import test_connection
        return test_connection(self.default_provider)
