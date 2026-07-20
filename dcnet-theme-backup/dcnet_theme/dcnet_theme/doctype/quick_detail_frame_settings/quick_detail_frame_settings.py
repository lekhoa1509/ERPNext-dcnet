import frappe
from frappe.model.document import Document


class QuickDetailFrameSettings(Document):
    def on_update(self):
        frappe.cache.delete_value("dcnet_qdf_overrides")
