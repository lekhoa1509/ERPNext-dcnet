from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime


class BCTCMapping(Document):

    @frappe.whitelist()
    def copy_from_company(self, source_company: str) -> dict:
        """Copy B01/B02/B03 lines from another company's BCTC Mapping."""
        if source_company == self.company:
            frappe.throw(_("Cannot copy from the same company."))

        source_name = f"BCTC Mapping {source_company}"
        if not frappe.db.exists("BCTC Mapping", source_name):
            frappe.throw(_("No BCTC Mapping found for company {0}.").format(source_company))

        source = frappe.get_doc("BCTC Mapping", source_name)

        for table_field in ("b01_lines", "b02_lines", "b03_lines"):
            self.set(table_field, [])
            for row in source.get(table_field) or []:
                self.append(table_field, row.as_dict())

        self.save(ignore_permissions=True)
        return {"status": "ok", "source_company": source_company}

    @frappe.whitelist()
    def restore_from_template(self, report: str, line_codes: list | None = None) -> dict:
        """Restore B01/B02/B03 lines from the seeded template.
        report: 'b01' | 'b02' | 'b03'
        line_codes: list of codes to restore (None = restore all)
        """
        coa = self.coa_template or "vn_large_enterprise"
        template_name = f"{coa}_{report}"

        if not frappe.db.exists("BCTC Mapping Template", template_name):
            frappe.throw(
                _("Template '{0}' not found. Run bench migrate to seed templates.").format(
                    template_name
                )
            )

        template = frappe.get_doc("BCTC Mapping Template", template_name)
        table_field = f"{report}_lines"
        template_lines = {row.code: row for row in template.get(table_field) or []}

        if line_codes is None:
            self.set(table_field, [])
            for row in template.get(table_field) or []:
                self.append(table_field, row.as_dict())
        else:
            existing = {row.code: row for row in self.get(table_field) or []}
            for code in line_codes:
                if code in template_lines and code in existing:
                    trow = template_lines[code].as_dict()
                    erow = existing[code]
                    for fld in (
                        "value_type", "account_formula", "line_formula",
                        "sign_multiplier", "is_subtotal",
                    ):
                        erow.set(fld, trow.get(fld))

        self.last_restored_from_default = now_datetime()
        self.save(ignore_permissions=True)
        return {"status": "ok", "report": report, "restored_codes": line_codes or "all"}
