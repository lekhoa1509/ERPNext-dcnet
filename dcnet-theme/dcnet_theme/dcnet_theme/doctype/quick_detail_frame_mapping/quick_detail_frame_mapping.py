import frappe
from frappe.model.document import Document


class QuickDetailFrameMapping(Document):
    def validate(self):
        if self.parent_doctype and self.child_field:
            self._validate_child_field_exists()

    def _validate_child_field_exists(self):
        try:
            meta = frappe.get_meta(self.parent_doctype)
        except Exception:
            frappe.throw(f"DocType '{self.parent_doctype}' không tồn tại")

        field = meta.get_field(self.child_field)
        if not field:
            frappe.throw(
                f"DocType '{self.parent_doctype}' không có field '{self.child_field}'"
            )
        if field.fieldtype != "Table":
            frappe.throw(
                f"Field '{self.child_field}' phải là Table type (hiện tại: {field.fieldtype})"
            )
