from frappe.model.document import Document


class BankStatementImport(Document):
    def validate(self):
        if self.source_type == "excel_upload" and self.status == "Draft" and not self.file:
            # only enforce file for excel_upload AFTER it moves past draft; allow saving draft without file
            pass
