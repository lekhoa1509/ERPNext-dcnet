import frappe
from frappe.model.document import Document


class EInvoiceInward(Document):
    """Staging record for an inward invoice fetched from an E-Invoice provider."""

    def validate(self):
        if self.linked_purchase_invoice and self.status == "New":
            self.status = "Matched"

    @frappe.whitelist()
    def match_purchase_invoice(self, purchase_invoice):
        """Manually match this staging record to an existing Purchase Invoice."""
        self.linked_purchase_invoice = purchase_invoice
        self.status = "Matched"
        self.save(ignore_permissions=True)

        # Update the Purchase Invoice with back-reference
        frappe.db.set_value(
            "Purchase Invoice",
            purchase_invoice,
            {
                "einvoice_inward": self.name,
                "einvoice_lookup_code": self.lookup_code,
            },
        )
        # Frappe auto-commits after request, no need for explicit commit
        frappe.msgprint(f"✅ Đã ghép nối với {purchase_invoice}", alert=True)

    @frappe.whitelist()
    def create_purchase_invoice(self):
        """Create a new Purchase Invoice from this staging record's data."""
        # Find or create supplier
        supplier = self._get_or_create_supplier()

        pi = frappe.new_doc("Purchase Invoice")
        pi.supplier = supplier
        pi.posting_date = self.invoice_date
        pi.bill_no = self.invoice_number
        pi.bill_date = self.invoice_date
        pi.einvoice_inward = self.name
        pi.einvoice_lookup_code = self.lookup_code

        # Add a single line item with totals (user will edit details)
        pi.append("items", {
            "item_name": f"Hóa đơn {self.invoice_number} từ {self.supplier_name}",
            "description": f"Nhập từ HĐĐT - Mã tra cứu: {self.lookup_code}",
            "qty": 1,
            "rate": self.total_before_tax or 0,
            "expense_account": frappe.get_cached_value(
                "Company", pi.company, "default_expense_account"
            ),
        })

        pi.insert(ignore_permissions=True)

        self.linked_purchase_invoice = pi.name
        self.status = "PI Created"
        self.save(ignore_permissions=True)
        # Frappe auto-commits after request, no need for explicit commit

        frappe.msgprint(f"✅ Đã tạo {pi.name} (Draft). Vui lòng kiểm tra và submit.", alert=True)
        return pi.name

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
        # Frappe auto-commits after request, no need for explicit commit
        frappe.msgprint("Đã bỏ qua hóa đơn này.", alert=True)
