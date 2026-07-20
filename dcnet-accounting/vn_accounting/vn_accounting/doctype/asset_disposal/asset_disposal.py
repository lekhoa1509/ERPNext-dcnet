from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, today


class AssetDisposal(Document):

    def validate(self):
        self._validate_asset()
        self._validate_dates()
        if self.disposal_type == "Sell":
            self._validate_sell_fields()

    def _validate_asset(self):
        asset = frappe.get_doc("Asset", self.asset)
        if asset.docstatus != 1:
            frappe.throw(_("Asset {0} must be submitted").format(self.asset))
        if asset.status in ("Sold", "Scrapped", "Capitalized"):
            frappe.throw(
                _("Asset {0} is already {1}").format(self.asset, asset.status)
            )

    def _validate_dates(self):
        if getdate(self.disposal_date) > getdate(today()):
            frappe.throw(_("Disposal date cannot be in the future"))
        asset_purchase_date = frappe.db.get_value("Asset", self.asset, "purchase_date")
        if getdate(self.disposal_date) < getdate(asset_purchase_date):
            frappe.throw(_("Disposal date cannot be before purchase date"))

    def _validate_sell_fields(self):
        if not self.selling_amount or self.selling_amount <= 0:
            frappe.throw(_("Selling amount must be greater than 0"))
        if not self.buyer:
            frappe.throw(_("Buyer is required for Sell disposal"))

    @frappe.whitelist()
    def execute(self):
        if self.status != "Draft":
            frappe.throw(_("Only Draft disposals can be executed"))

        self.validate()
        asset_doc = frappe.get_doc("Asset", self.asset)

        # Pro-rata depreciation up to disposal date (only for partially depreciated assets)
        if asset_doc.status not in ("Fully Depreciated",) and asset_doc.value_after_depreciation > 0:
            from erpnext.assets.doctype.asset.depreciation import depreciate_asset
            try:
                depreciate_asset(asset_doc, getdate(self.disposal_date), _("Asset disposed via Asset Disposal"))
            except Exception:
                frappe.log_error(title=_("Pro-rata depreciation skipped for {0}").format(self.asset))
        asset_doc.reload()

        # Update values after pro-rata depreciation
        self.gross_purchase_amount = asset_doc.total_asset_cost
        self.accumulated_depreciation = (
            asset_doc.total_asset_cost - asset_doc.value_after_depreciation
        )
        self.book_value = asset_doc.value_after_depreciation

        # Create writeoff Journal Entry
        je = self._create_writeoff_je(asset_doc)

        # Update Asset
        asset_doc.db_set("disposal_date", self.disposal_date)
        asset_doc.db_set("journal_entry_for_scrap", je.name)

        if self.disposal_type == "Sell":
            asset_doc.db_set("status", "Sold")
            si = self._create_sales_invoice(asset_doc)
            self.db_set("sales_invoice", si.name, update_modified=False)
        else:
            asset_doc.db_set("status", "Scrapped")

        # Use db_set to avoid re-running validate() which checks asset status
        # (asset is already Scrapped/Sold at this point — validate would reject it)
        self.db_set("journal_entry", je.name, update_modified=False)
        self.db_set("status", "Executed")

        frappe.msgprint(
            _("Asset disposed successfully. Journal Entry: {0}").format(
                frappe.utils.get_link_to_form("Journal Entry", je.name)
            ),
            indicator="green",
        )

    def _create_writeoff_je(self, asset_doc):
        depreciation_series = frappe.get_cached_value(
            "Company", asset_doc.company, "series_for_depreciation_entry"
        )

        je = frappe.new_doc("Journal Entry")
        je.voucher_type = "Journal Entry"
        je.naming_series = depreciation_series or "JV-.YYYY.-"
        je.posting_date = self.disposal_date
        je.company = asset_doc.company
        je.remark = _("Asset Disposal writeoff for {0} ({1})").format(
            asset_doc.name, asset_doc.asset_name
        )

        # Debit: Accumulated Depreciation Account
        if self.accumulated_depreciation > 0:
            je.append("accounts", {
                "account": self.accumulated_depreciation_account,
                "debit_in_account_currency": self.accumulated_depreciation,
                "reference_type": "Asset",
                "reference_name": asset_doc.name,
            })

        # Debit: Disposal Loss Account (book value remaining)
        if self.book_value > 0:
            je.append("accounts", {
                "account": self.disposal_loss_account,
                "debit_in_account_currency": self.book_value,
                "reference_type": "Asset",
                "reference_name": asset_doc.name,
            })

        # Credit: Fixed Asset Account (full original cost = total_asset_cost)
        je.append("accounts", {
            "account": self.fixed_asset_account,
            "credit_in_account_currency": self.gross_purchase_amount,  # stored from total_asset_cost
            "reference_type": "Asset",
            "reference_name": asset_doc.name,
        })

        je.flags.ignore_permissions = True
        je.save()
        je.submit()

        return je

    def _create_sales_invoice(self, asset_doc):
        si = frappe.new_doc("Sales Invoice")
        si.customer = self.buyer
        si.company = asset_doc.company
        si.posting_date = self.disposal_date

        # Always use generic disposal item (not asset item_code which has is_fixed_asset=1
        # and would require an Asset link in the SI row)
        item_code = self._get_or_create_disposal_item(asset_doc.company)

        si.append("items", {
            "item_code": item_code,
            "item_name": _("Asset Disposal: {0}").format(asset_doc.asset_name),
            "qty": 1,
            "rate": self.selling_amount,
            "income_account": self.disposal_income_account,
        })

        si.flags.ignore_permissions = True
        si.save()

        return si

    def _get_or_create_disposal_item(self, company):
        item_name = "Asset Disposal Income"
        if not frappe.db.exists("Item", item_name):
            item = frappe.new_doc("Item")
            item.item_code = item_name
            item.item_name = item_name
            item.item_group = "Services"
            item.is_stock_item = 0
            item.flags.ignore_permissions = True
            item.save()
        return item_name

    @frappe.whitelist()
    def cancel_disposal(self):
        if self.status != "Executed":
            frappe.throw(_("Only Executed disposals can be cancelled"))

        # For Sell: validate SI is cancelled first
        if self.disposal_type == "Sell" and self.sales_invoice:
            si_docstatus = frappe.db.get_value(
                "Sales Invoice", self.sales_invoice, "docstatus"
            )
            if si_docstatus == 1:
                frappe.throw(
                    _("Please cancel Sales Invoice {0} before cancelling this disposal").format(
                        self.sales_invoice
                    )
                )

        # Restore asset status BEFORE cancelling the JE
        # ERPNext blocks JE cancel when asset is still "Scrapped" or "Sold"
        asset_doc = frappe.get_doc("Asset", self.asset)
        asset_doc.db_set("disposal_date", None)
        asset_doc.db_set("journal_entry_for_scrap", None)

        restored_status = "Fully Depreciated" if asset_doc.value_after_depreciation == 0 else "Partially Depreciated"
        asset_doc.db_set("status", restored_status)

        # Cancel writeoff JE (asset is now un-scrapped, so ERPNext allows this)
        if self.journal_entry:
            je = frappe.get_doc("Journal Entry", self.journal_entry)
            je.flags.ignore_permissions = True
            je.cancel()

        # Restore depreciation schedule
        asset_doc.reload()
        from erpnext.assets.doctype.asset.depreciation import (
            reverse_depreciation_entry_made_on_disposal,
            reset_depreciation_schedule,
        )
        try:
            reverse_depreciation_entry_made_on_disposal(asset_doc)
        except Exception:
            frappe.log_error(title=_("Reverse depreciation skipped for {0}").format(self.asset))
        try:
            reset_depreciation_schedule(
                asset_doc, _("Asset restored via Asset Disposal cancellation")
            )
        except Exception:
            frappe.log_error(title=_("Reset depreciation schedule skipped for {0}").format(self.asset))

        self.db_set("status", "Cancelled")

        frappe.msgprint(
            _("Asset Disposal cancelled and asset restored"),
            indicator="green",
        )
