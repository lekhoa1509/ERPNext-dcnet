import frappe
from frappe.model.document import Document


class CRMCareCard(Document):
    def validate(self):
        # Backfill snapshot fields from the linked Customer so list/filter queries
        # work even when fetch_from did not run (e.g. programmatic inserts).
        if self.customer:
            for target, source in (
                ("customer_name", "customer_name"),
                ("tax_id", "tax_id"),
                ("mobile_no", "mobile_no"),
                ("email_id", "email_id"),
            ):
                if not self.get(target):
                    value = frappe.db.get_value("Customer", self.customer, source)
                    if value:
                        self.set(target, value)
