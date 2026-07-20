import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

from einvoice.einvoice.exceptions import (
    EInvoiceProviderError,
    EInvoiceProviderNotReady,
)


class EInvoiceProvider(Document):
    """Represents a single E-Invoice provider configuration."""

    def get_provider_instance(self):
        """Return the appropriate provider class instance based on provider_type."""
        from einvoice.einvoice.providers import get_provider_class

        klass = get_provider_class(self.provider_type)
        return klass(self)


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
        return {"success": True, "message": "Kết nối thành công!"}
    except EInvoiceProviderNotReady as e:
        doc.connection_status = "Failed"
        doc.last_tested = now_datetime()
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"success": False, "message": e.message}
    except EInvoiceProviderError as e:
        doc.connection_status = "Failed"
        doc.last_tested = now_datetime()
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"success": False, "message": f"Kết nối thất bại: {e.message}"}
    except Exception as e:
        doc.connection_status = "Failed"
        doc.last_tested = now_datetime()
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"success": False, "message": f"Kết nối thất bại: {str(e)}"}


@frappe.whitelist()
def refresh_templates(docname):
    """Fetch latest invoice templates from the provider."""
    doc = frappe.get_doc("EInvoice Provider", docname)
    try:
        provider = doc.get_provider_instance()
        provider.authenticate()
        return provider.get_invoice_templates()
    except EInvoiceProviderNotReady as e:
        frappe.msgprint(e.message)
        return []
    except EInvoiceProviderError as e:
        frappe.msgprint(f"Lỗi: {e.message}")
        return []
