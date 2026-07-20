import frappe
from frappe.model.document import Document


class AssetStocktake(Document):
    @frappe.whitelist()
    def load_items(self):
        """Populate stocktake_items from location/department."""
        doctype_map = {"TSCĐ": "Asset", "CCDC": "CCDC Item"}
        target_dt = doctype_map.get(self.scope)
        if not target_dt:
            frappe.throw("Chọn phạm vi kiểm kê (TSCĐ / CCDC) trước")
        filters = {"docstatus": 1}
        if self.location:
            filters["location"] = self.location
        if self.department and target_dt == "Asset":
            filters["department"] = self.department
        if target_dt == "Asset":
            records = frappe.get_all(target_dt, filters=filters,
                                     fields=["name", "asset_name", "purchase_amount", "total_asset_cost"])
        else:
            records = frappe.get_all(target_dt, filters=filters,
                                     fields=["name", "item_name", "cost"])
        self.set("stocktake_items", [])
        for r in records:
            name_label = r.get("asset_name") or r.get("item_name") or r.get("name")
            book_val = r.get("total_asset_cost") or r.get("purchase_amount") or r.get("cost") or 0
            self.append("stocktake_items", {
                "target_doctype": target_dt,
                "target_name": r.get("name"),
                "book_value": book_val,
            })
        self.save()
        return len(records)

    @frappe.whitelist()
    def approve(self):
        """Process approved stocktake — create GL Entries for lost/damaged."""
        company = self.company or frappe.defaults.get_defaults().get("company")
        for item in self.stocktake_items or []:
            if item.physical_status == "Mất":
                self._create_loss_je(item, company)
            elif item.physical_status == "Hỏng":
                if item.target_doctype and item.target_name:
                    frappe.db.set_value(item.target_doctype, item.target_name, "status", "Out of Order")
        self.status = "Approved"
        self.save()

    def _create_loss_je(self, item, company):
        debit_acct = frappe.db.get_value(
            "Account",
            {"account_number": "1381", "company": company},
            "name"
        )
        if not debit_acct:
            debit_acct = frappe.db.get_value(
                "Account",
                {"account_name": ["like", "1381%"], "company": company},
                "name"
            )
        if item.target_doctype == "Asset":
            credit_acct = frappe.db.get_value(
                "Account",
                {"account_number": "211", "company": company, "is_group": 0},
                "name"
            )
            if not credit_acct:
                credit_acct = frappe.db.get_value(
                    "Account",
                    {"account_name": ["like", "211%"], "company": company, "is_group": 0},
                    "name"
                )
        else:
            credit_acct = frappe.db.get_value(
                "Account",
                {"account_number": "153", "company": company, "is_group": 0},
                "name"
            )
            if not credit_acct:
                credit_acct = frappe.db.get_value(
                    "Account",
                    {"account_name": ["like", "153%"], "company": company, "is_group": 0},
                    "name"
                )
        if not debit_acct or not credit_acct:
            frappe.log_error(
                f"Accounts not found for loss JE: debit={debit_acct} credit={credit_acct} item={item.target_name}",
                "Asset Stocktake"
            )
            return
        je = frappe.new_doc("Journal Entry")
        je.posting_date = self.stocktake_date
        je.company = company
        je.voucher_type = "Journal Entry"
        je.user_remark = f"Kiểm kê — mất tài sản: {item.target_name}"
        amount = item.book_value or 0
        je.append("accounts", {"account": debit_acct, "debit_in_account_currency": amount})
        je.append("accounts", {"account": credit_acct, "credit_in_account_currency": amount})
        je.insert(ignore_permissions=True)
        je.submit()
