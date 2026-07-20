import frappe
from frappe import _
from frappe.model.document import Document


class ImportAutoSettings(Document):
    """Central AI connection settings for Import Auto."""

    def validate(self):
        if not self.timeout_seconds:
            self.timeout_seconds = 60

    @frappe.whitelist()
    def test_ai_connection(self):
        self.check_permission("write")
        from dcnet_migrate.import_auto.services.ai_client import test_connection

        result = test_connection(self)
        frappe.db.set_single_value(self.doctype, "last_test_result", _("Connected"))
        frappe.msgprint(_("AI connection is working."), alert=True)
        return result


@frappe.whitelist()
def test_ai_connection():
    settings = frappe.get_single("Import Auto Settings")
    settings.check_permission("write")
    from dcnet_migrate.import_auto.services.ai_client import test_connection

    result = test_connection(settings)
    frappe.db.set_single_value("Import Auto Settings", "last_test_result", _("Connected"))
    frappe.msgprint(_("AI connection is working."), alert=True)
    return result
