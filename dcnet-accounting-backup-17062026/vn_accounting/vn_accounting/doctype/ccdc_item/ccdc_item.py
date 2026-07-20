import frappe
from frappe import _
from frappe.model.document import Document


class CCDCItem(Document):
    def before_save(self):
        if not self.accounting_entries:
            self._autofill_entries()

    def validate(self):
        if self.cost <= 0:
            frappe.throw("Cost must be greater than 0")
        if self.useful_period_months <= 0:
            frappe.throw("Useful period must be greater than 0")
        if self.allocation_periods < 1:
            frappe.throw("Allocation periods must be at least 1")
        self._validate_entries_balance()

    def on_submit(self):
        self._post_je()
        self._create_allocation_schedule()
        self.db_set("status", "Đang sử dụng")

    def on_cancel(self):
        if self.posted_je:
            try:
                je = frappe.get_doc("Journal Entry", self.posted_je)
                if je.docstatus == 1:
                    je.cancel()
            except frappe.DoesNotExistError:
                pass
        self.db_set("status", "Mới mua")
        # Reverse GL entries created by JE cancellation inherit reference_type/reference_name
        # which triggers Frappe's back-link check. Skip it — the JE is already cancelled.
        self.flags.ignore_links = True

    def _autofill_entries(self):
        from vn_accounting.utils.accounting_posting import build_default_entries
        company = self.company or frappe.defaults.get_user_default("Company")
        if not company:
            return
        rows = build_default_entries(
            "CCDC Item Purchase",
            None,
            self.cost or 0,
            bool(self.has_vat),
            float(self.vat_rate or 10),
            company,
        )
        self.accounting_entries = []
        for r in rows:
            self.append("accounting_entries", r)

    def _validate_entries_balance(self):
        if not self.accounting_entries:
            return
        total = sum(float(r.amount or 0) for r in self.accounting_entries)
        cost = float(self.cost or 0)
        vat = float(cost * float(self.vat_rate or 0) / 100) if self.has_vat else 0
        expected = round(cost + vat)
        if abs(total - expected) > 1:
            frappe.throw(
                _("Tổng dòng hạch toán ({0}) không khớp với giá trị + VAT ({1})").format(
                    total, expected
                )
            )

    def _post_je(self):
        from vn_accounting.utils.accounting_posting import (
            build_default_entries,
            post_je_from_entries,
            resolve_cost_center,
        )
        company = self.company
        if not self.accounting_entries:
            rows = build_default_entries(
                "CCDC Item Purchase",
                None,
                self.cost or 0,
                bool(self.has_vat),
                float(self.vat_rate or 10),
                company,
            )
        else:
            rows = self.accounting_entries

        posting_date = self.available_for_use_date or frappe.utils.today()
        remark = "CCDC ghi nhận 242: {0} — {1}".format(
            self.name, self.item_name or self.item_code or ""
        )
        cost_center = resolve_cost_center(self, company)
        je_name = post_je_from_entries(
            rows, company, posting_date, remark,
            "CCDC Item", self.name,
            submit=True,
            cost_center=cost_center,
            source_key="vn_accounting.ccdc.purchase",
        )
        self.db_set("posted_je", je_name, update_modified=False)

    def _create_allocation_schedule(self):
        from vn_accounting.asset.ccdc_allocation import create_allocation_schedule
        create_allocation_schedule(self)
