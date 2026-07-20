import frappe
from frappe.model.document import Document
from frappe.utils import today, flt


class EInvoiceInward(Document):
    """Staging record for an inward invoice fetched from an E-Invoice provider."""

    def validate(self):
        if self.linked_purchase_invoice and self.status == "New":
            self.status = "Matched"

        # Auto-calculate tax rate if not set
        if not self.tax_rate and self.total_before_tax:
            self.tax_rate = round((self.tax_amount or 0) / self.total_before_tax * 100, 0)

    @frappe.whitelist()
    def match_purchase_invoice(self, purchase_invoice):
        """Manually match this staging record to an existing Purchase Invoice."""
        self.linked_purchase_invoice = purchase_invoice
        self.status = "Matched"
        self.save(ignore_permissions=True)

        frappe.db.set_value(
            "Purchase Invoice",
            purchase_invoice,
            {
                "einvoice_inward": self.name,
                "einvoice_lookup_code": self.lookup_code,
            },
        )
        frappe.msgprint(f"Đã ghép nối với {purchase_invoice}", alert=True)

    @frappe.whitelist()
    def create_purchase_invoice(self):
        """Create a new Purchase Invoice from this staging record's data."""
        supplier = self._get_or_create_supplier()
        tax_template = self._resolve_tax_template()

        pi = frappe.new_doc("Purchase Invoice")
        pi.supplier = supplier
        pi.company = self.company
        pi.posting_date = self.invoice_date or today()
        pi.bill_no = self.invoice_number
        pi.bill_date = self.invoice_date
        pi.einvoice_inward = self.name
        pi.einvoice_lookup_code = self.lookup_code

        pi.append("items", {
            "item_name": f"Hóa đơn {self.invoice_number} từ {self.supplier_name}",
            "description": f"Nhập từ HĐĐT - Mã tra cứu: {self.lookup_code}",
            "qty": 1,
            "rate": self.total_before_tax or 0,
            "expense_account": frappe.get_cached_value(
                "Company", pi.company, "default_expense_account"
            ),
        })

        # Apply tax template
        if tax_template:
            pi.taxes_and_charges = tax_template.name
            pi.set_taxes()

            # Compare calculated tax with HĐĐT tax
            calculated_tax = flt(pi.total_taxes_and_charges)
            expected_tax = flt(self.tax_amount)
            if expected_tax and calculated_tax:
                diff_pct = abs(calculated_tax - expected_tax) / expected_tax * 100
                if diff_pct > 1:
                    frappe.msgprint(
                        f"Thuế tính theo mẫu ({frappe.format_value(calculated_tax, 'Currency')}) "
                        f"chênh lệch với thuế trên HĐĐT ({frappe.format_value(expected_tax, 'Currency')}). "
                        f"Vui lòng kiểm tra.",
                        alert=True,
                    )

        pi.insert(ignore_permissions=True)

        self.linked_purchase_invoice = pi.name
        self.status = "PI Created"
        self.save(ignore_permissions=True)

        frappe.msgprint(f"Đã tạo {pi.name} (Draft). Vui lòng kiểm tra và submit.", alert=True)
        return pi.name

    def _resolve_tax_template(self):
        """
        Find the best matching Purchase Taxes and Charges Template by tax rate.

        Logic:
        1. Calculate actual_rate from inward invoice
        2. Find templates for this company
        3. Match by tax rate (On Net Total)
        4. Fallback to is_default if no rate match
        5. Throw if no template exists at all
        """
        actual_rate = round(self.tax_rate or 0, 0)

        templates = frappe.get_all(
            "Purchase Taxes and Charges Template",
            filters={"company": self.company},
            fields=["name", "is_default"],
        )

        if not templates:
            frappe.throw(
                f"Công ty {self.company} chưa có Purchase Taxes and Charges Template. "
                f"Vui lòng tạo tại: /app/purchase-taxes-and-charges-template/new"
            )

        # Try to match by tax rate
        matched = []
        for tmpl in templates:
            taxes = frappe.get_all(
                "Purchase Taxes and Charges",
                filters={
                    "parent": tmpl.name,
                    "charge_type": "On Net Total",
                },
                fields=["rate"],
                limit=1,
            )
            if taxes and round(flt(taxes[0].rate), 0) == actual_rate:
                matched.append(tmpl)

        if len(matched) == 1:
            return frappe.get_doc("Purchase Taxes and Charges Template", matched[0].name)

        if len(matched) > 1:
            # Prefer is_default
            for m in matched:
                if m.is_default:
                    return frappe.get_doc("Purchase Taxes and Charges Template", m.name)
            return frappe.get_doc("Purchase Taxes and Charges Template", matched[0].name)

        # No rate match — fallback to default
        for tmpl in templates:
            if tmpl.is_default:
                frappe.msgprint(
                    f"Không tìm thấy mẫu thuế {actual_rate}%. "
                    f"Đang dùng mẫu mặc định. Vui lòng kiểm tra.",
                    alert=True,
                )
                return frappe.get_doc("Purchase Taxes and Charges Template", tmpl.name)

        # No default either — throw with guidance
        frappe.throw(
            f"Công ty {self.company} chưa có Purchase Taxes and Charges Template mặc định. "
            f"Vui lòng tạo tại: /app/purchase-taxes-and-charges-template/new"
        )

    def _get_or_create_supplier(self):
        """Find an existing supplier by tax code, or create a new one."""
        if self.supplier_tax_code:
            existing = frappe.db.get_value(
                "Supplier", {"tax_id": self.supplier_tax_code}, "name"
            )
            if existing:
                return existing

        supplier = frappe.new_doc("Supplier")
        supplier.supplier_name = self.supplier_name or "Nhà cung cấp không xác định"
        supplier.supplier_group = frappe.db.get_single_value(
            "Buying Settings", "supplier_group"
        ) or "All Supplier Groups"
        supplier.tax_id = self.supplier_tax_code
        supplier.insert(ignore_permissions=True)
        return supplier.name

    @frappe.whitelist()
    def ignore_invoice(self):
        """Mark this invoice as ignored."""
        self.status = "Ignored"
        self.save(ignore_permissions=True)
        frappe.msgprint("Đã bỏ qua hóa đơn này.", alert=True)
