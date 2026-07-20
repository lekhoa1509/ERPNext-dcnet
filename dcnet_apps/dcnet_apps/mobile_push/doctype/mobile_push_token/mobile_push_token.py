import frappe
from frappe.model.document import Document


class MobilePushToken(Document):
    def before_save(self):
        if not self.user:
            self.user = frappe.session.user
        if not self.last_seen:
            self.last_seen = frappe.utils.now()
