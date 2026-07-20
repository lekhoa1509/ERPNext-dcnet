from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint, flt

from vn_accounting.branch_cash.service import (
	get_user_branch,
	is_privileged_user,
	validate_user_can_manage_branch_cash,
)
from vn_accounting.branch_cash.invoice_loader import parse_invoice_file
from vn_accounting.vn_accounting.report_utils import CASH_PREFIX, get_accounts_by_prefix


class BranchCashEntry(Document):
	def validate(self):
		if not self.branch and not is_privileged_user():
			self.branch = get_user_branch()

		validate_user_can_manage_branch_cash(
			company=self.company,
			branch=self.branch,
			accounting_unit=self.accounting_unit,
		)
		self._validate_amount()
		self._validate_accounting_unit()
		self._validate_official_fields()
		self._validate_linked_invoice()
		self._normalize_invoice_fields()

	def on_submit(self):
		if self.posting_scope != "Official" or self.official_journal_entry:
			return

		journal_entry = self._make_official_journal_entry()
		self.db_set("official_journal_entry", journal_entry.name, update_modified=False)

	def on_cancel(self):
		if not self.official_journal_entry:
			return

		if not frappe.db.exists("Journal Entry", self.official_journal_entry):
			return

		journal_entry = frappe.get_doc("Journal Entry", self.official_journal_entry)
		if journal_entry.docstatus == 1:
			journal_entry.flags.ignore_permissions = True
			journal_entry.cancel()

	def _validate_amount(self):
		if flt(self.amount) <= 0:
			frappe.throw(_("Số tiền phải lớn hơn 0."))

		if self.direction not in {"Receive", "Pay"}:
			frappe.throw(_("Loại phiếu chỉ được là Thu hoặc Chi."))

		if self.posting_scope not in {"Official", "Internal"}:
			frappe.throw(_("Phạm vi ghi nhận chỉ được là Hạch toán sổ cái hoặc Nội bộ chi nhánh."))

	def _validate_accounting_unit(self):
		accounting_unit = frappe.db.get_value(
			"Cost Center",
			self.accounting_unit,
			["company", "is_group"],
			as_dict=True,
		)

		if not accounting_unit:
			frappe.throw(_("Đơn vị hạch toán {0} không tồn tại.").format(self.accounting_unit))

		if accounting_unit.company != self.company:
			frappe.throw(
				_("Đơn vị hạch toán {0} không thuộc công ty {1}.").format(
					self.accounting_unit,
					self.company,
				)
			)

		if cint(accounting_unit.is_group):
			frappe.throw(_("Đơn vị hạch toán phải là Cost Center lá."))

	def _validate_linked_invoice(self):
		"""Linked invoice là tùy chọn. Nếu chọn loại nhưng chưa chọn số → throw;
		hoặc chọn số nhưng chưa chọn loại → cũng throw. Kiểm tra invoice tồn tại."""
		if self.linked_invoice_type and not self.linked_invoice:
			frappe.throw(_("Đã chọn loại hóa đơn {0} — vui lòng chọn hóa đơn cụ thể.").format(self.linked_invoice_type))
		if self.linked_invoice and not self.linked_invoice_type:
			frappe.throw(_("Đã chọn hóa đơn {0} — vui lòng chọn loại hóa đơn trước.").format(self.linked_invoice))
		if self.linked_invoice and self.linked_invoice_type:
			if not frappe.db.exists(self.linked_invoice_type, self.linked_invoice):
				frappe.throw(_("Hóa đơn {0} ({1}) không tồn tại.").format(self.linked_invoice, self.linked_invoice_type))

	def _normalize_invoice_fields(self):
		"""Clear parsed invoice fields when the entry is not marked as having an invoice."""
		if cint(self.get("has_invoice")):
			return

		invoice_fields = (
			"invoice_file",
			"invoice_form_no",
			"invoice_serial",
			"invoice_number",
			"invoice_id",
			"invoice_date",
			"invoice_currency",
			"exchange_rate",
			"seller_name",
			"seller_tax_code",
			"seller_phone",
			"seller_address",
			"buyer_contact_name",
			"buyer_company_name",
			"buyer_tax_code",
			"buyer_warehouse",
			"buyer_address",
			"payment_method",
			"payment_due_date",
			"buyer_bank_account",
			"buyer_bank_name",
			"reference_number",
			"total_before_tax",
			"tax_rate",
			"tax_amount",
			"total_amount",
			"total_in_words",
		)
		for field in invoice_fields:
			self.set(field, None)
		self.set("invoice_items", [])

	def _validate_official_fields(self):
		if self.posting_scope != "Official":
			self.cash_account = None
			self.offset_account = None
			return

		if not self.cash_account or not self.offset_account:
			frappe.throw(_("Tài khoản quỹ và tài khoản đối ứng là bắt buộc khi chọn hạch toán sổ cái."))

		if self.cash_account == self.offset_account:
			frappe.throw(_("Tài khoản quỹ và tài khoản đối ứng phải khác nhau."))

		if not get_accounts_by_prefix(self.company, CASH_PREFIX, self.cash_account):
			frappe.throw(_("Tài khoản quỹ phải là tài khoản lá thuộc nhóm TK 111."))

		self._validate_leaf_account(self.offset_account, _("Offset Account"))

	def _validate_leaf_account(self, account: str, label) -> None:
		account_meta = frappe.db.get_value(
			"Account",
			account,
			["company", "is_group"],
			as_dict=True,
		)
		if not account_meta:
			frappe.throw(_("{0} {1} không tồn tại.").format(label, account))
		if account_meta.company != self.company:
			frappe.throw(_("{0} {1} không thuộc công ty {2}.").format(label, account, self.company))
		if cint(account_meta.is_group):
			frappe.throw(_("{0} phải là tài khoản lá.").format(label))

	def _make_official_journal_entry(self):
		debit_account, credit_account = self._get_gl_accounts()
		remark = self._get_journal_remark()
		company_allows_bs_cost_center = cint(
			frappe.get_cached_value("Company", self.company, "allow_cost_center_in_entry_of_bs_account")
		)

		# Lưu ý: KHÔNG set JE Account row reference_type/reference_name cho SI/PI.
		# ERPNext validate row.account phải khớp với SI.debit_to / PI.credit_to
		# (vd TK 131 + Customer party) — quá chặt cho BCE soft-link. Thông tin hóa
		# đơn liên quan đi qua remark + BCE Dynamic Link → Frappe Connections
		# tự dò + KTT xem được trong Linked Documents.

		journal_entry = frappe.get_doc(
			{
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"company": self.company,
				"posting_date": self.posting_date,
				"user_remark": remark,
				"accounts": [
					self._build_journal_row(
						account=debit_account,
						debit=flt(self.amount),
						credit=0,
						company_allows_bs_cost_center=company_allows_bs_cost_center,
					),
					self._build_journal_row(
						account=credit_account,
						debit=0,
						credit=flt(self.amount),
						company_allows_bs_cost_center=company_allows_bs_cost_center,
					),
				],
			}
		)
		journal_entry.flags.ignore_permissions = True
		journal_entry.insert()
		journal_entry.submit()
		return journal_entry

	def _build_journal_row(self, account: str, debit: float, credit: float, company_allows_bs_cost_center: bool):
		row = {
			"account": account,
			"debit_in_account_currency": debit,
			"credit_in_account_currency": credit,
		}

		if self.accounting_unit and self._account_accepts_cost_center(account, company_allows_bs_cost_center):
			row["cost_center"] = self.accounting_unit

		return row

	def _account_accepts_cost_center(self, account: str, company_allows_bs_cost_center: bool) -> bool:
		report_type = frappe.db.get_value("Account", account, "report_type")
		return report_type == "Profit and Loss" or company_allows_bs_cost_center

	def _get_gl_accounts(self) -> tuple[str, str]:
		if self.direction == "Receive":
			return self.cash_account, self.offset_account
		return self.offset_account, self.cash_account

	def _get_journal_remark(self) -> str:
		scope_label = _("Hạch toán sổ cái")
		invoice_label = ""
		if self.linked_invoice_type and self.linked_invoice:
			invoice_label = _(" | Hóa đơn: {0} ({1})").format(self.linked_invoice, self.linked_invoice_type)
		return _(
			"Phiếu quỹ chi nhánh {0} | Chi nhánh: {1} | Đơn vị hạch toán: {2} | Phạm vi: {3}{4} | {5}"
		).format(
			self.name,
			self.branch,
			self.accounting_unit,
			scope_label,
			invoice_label,
			self.remarks or "",
		)


@frappe.whitelist()
def load_invoice_from_file(file_url: str) -> dict:
	"""Read an uploaded invoice file and return parsed fields for Branch Cash Entry."""
	if not file_url:
		frappe.throw(_("Vui lòng tải lên file hóa đơn trước khi tải dữ liệu."))

	return parse_invoice_file(file_url)
