import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class EInvoiceProvider(Document):
    """Represents a single E-Invoice provider configuration."""

    def get_provider_instance(self):
        """Return the appropriate provider class instance based on provider_type."""
        from dcnet_apps.einvoice.providers import get_provider_class

        klass = get_provider_class(self.provider_type)
        return klass(self)


# ---------------------------------------------------------------------------
# Module-level whitelist functions (required for frm.call() resolution)
# ---------------------------------------------------------------------------

@frappe.whitelist()
def test_connection(docname):
    """Test the API connection for a provider and update its status."""
    doc = frappe.get_doc("EInvoice Provider", docname)
    try:
        provider = doc.get_provider_instance()
        provider.authenticate()
        doc.connection_status = "Connected"
        doc.last_tested = now_datetime()
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"success": True, "message": "✅ Kết nối thành công!"}
    except Exception as e:
        doc.connection_status = "Failed"
        doc.last_tested = now_datetime()
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.throw(f"❌ Kết nối thất bại: {str(e)}")


@frappe.whitelist()
def refresh_templates(docname):
    """Fetch latest invoice templates from the provider."""
    doc = frappe.get_doc("EInvoice Provider", docname)
    provider = doc.get_provider_instance()
    provider.authenticate()
    templates = provider.get_invoice_templates()
    return templates
