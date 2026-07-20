from datetime import date, timedelta
from decimal import Decimal

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, today

from dcnet_contract.dcnet_contract.utils.billing_schedule import (
	ScheduleInput,
	_add_months,
	generate_schedule,
)
from dcnet_contract.dcnet_contract.shadow_so import cancel_shadow_so, create_shadow_so
from dcnet_contract.dcnet_contract.utils.state_machine import assert_transition

RECURRING_SERVICES = {"P2P", "MPLS", "ILL", "FTTH DN", "FTTH HGD", "IT Managed"}
ONEOFF_SERVICES = {"VTTB", "Thi công"}


class DCNetContract(Document):
	def validate(self):
		self._validate_items_not_empty()
		self._validate_item_values()
		self._validate_contract_type_matches_service()
		self._validate_one_off_vttb_needs_item()
		self._compute_totals()
		self._compute_end_date()

	def before_print(self, settings=None):
		if self.contract_html:
			# Template-based contract: use stored HTML (may include sales edits)
			self.contract_html_rendered = self.contract_html
		else:
			# Backward compat: old contracts without template
			from dcnet_contract.dcnet_contract.utils.docx_generator import (
				generate_appendix_html_for_print,
				generate_html_for_print,
			)
			self.contract_html_rendered = generate_html_for_print(self.name)
			self.appendix_html = generate_appendix_html_for_print(self.name)

	def before_submit(self):
		if not self.acceptance_date:
			frappe.throw(_("Acceptance date is required before submitting a contract"))

	def on_submit(self):
		assert_transition("Draft", "Active")
		self.status = "Active"
		self._generate_billing_schedule()
		create_shadow_so(self)
		self._sync_customer_data()
		if self.amended_from:
			self._revise_old_contract()

	def on_cancel(self):
		assert_transition(self.status, "Cancelled")
		self._cancel_billing_schedule_rows()
		cancel_shadow_so(self)
		self.status = "Cancelled"
		self.db_set("status", "Cancelled")

	def _validate_items_not_empty(self):
		if not self.items:
			frappe.throw(_("Contract must have at least 1 item"))

	def _validate_item_values(self):
		for row in self.items:
			if (row.unit_price or 0) <= 0:
				frappe.throw(_("Unit price must be greater than 0 for item '{0}'").format(row.item_label))
			if (row.qty or 0) < 1:
				frappe.throw(_("Quantity must be >= 1 for item '{0}'").format(row.item_label))

	def _validate_contract_type_matches_service(self):
		if self.service_type in RECURRING_SERVICES and self.contract_type != "Recurring":
			frappe.throw(
				_("Service {0} requires Recurring contract type").format(self.service_type)
			)
		if self.service_type in ONEOFF_SERVICES and self.contract_type != "One-off":
			frappe.throw(
				_("Service {0} requires One-off contract type").format(self.service_type)
			)

	def _validate_one_off_vttb_needs_item(self):
		if self.contract_type == "One-off" and self.service_type == "VTTB":
			for row in self.items:
				if not row.erpnext_item:
					frappe.throw(
						_("VTTB contract: item '{0}' must link to an ERPNext Item").format(row.item_label)
					)

	def _compute_totals(self):
		self.unit_price_total = sum(
			(row.qty or 0) * (row.unit_price or 0) for row in self.items
		)
		for row in self.items:
			row.amount_per_period = (row.qty or 0) * (row.unit_price or 0)

		if self.contract_type == "Recurring" and self.package_term_months:
			self.grand_total = self.unit_price_total * self.package_term_months + (self.setup_fee or 0)
		else:
			self.grand_total = self.unit_price_total + (self.setup_fee or 0)

	def _compute_end_date(self):
		if not self.acceptance_date:
			return
		acc_date = getdate(self.acceptance_date)
		if self.contract_type == "Recurring" and self.package_term_months:
			self.end_date = _add_months(acc_date, self.package_term_months) - timedelta(days=1)
		else:
			self.end_date = acc_date

	def _revise_old_contract(self):
		"""When this contract is an amendment, mark the old contract as Revised.
		Frappe requires cancel before amend, so old doc is already Cancelled.
		We upgrade its status to Revised to distinguish revision from pure cancellation.
		Billing schedule rows are already Cancelled by on_cancel."""
		old_doc = frappe.get_doc("DCNet Contract", self.amended_from)
		assert_transition(old_doc.status, "Revised")
		frappe.db.set_value("DCNet Contract", old_doc.name, "status", "Revised")

		# Add comment on old contract
		old_doc.add_comment(
			"Comment",
			_("Contract revised. New contract: {0}").format(self.name),
		)

	def _cancel_billing_schedule_rows(self):
		"""Cancel future billing schedule rows on mid-term cancellation.
		Projected → Cancelled, Invoiced → create Return SI (credit note),
		Paid rows → warning only (no auto-refund)."""
		invoiced_rows = []
		paid_periods = []
		cancelled_periods = []

		for row in self.billing_schedule:
			if row.state in ("Projected", "Invoiced", "Overdue"):
				if row.state in ("Invoiced", "Overdue") and row.sales_invoice:
					invoiced_rows.append(row)
				cancelled_periods.append(f"{row.period_start} – {row.period_end}")
				frappe.db.set_value(
					"DCNet Contract Billing Schedule", row.name, "state", "Cancelled"
				)
			elif row.state == "Paid":
				paid_periods.append(f"{row.period_start} – {row.period_end}")

		if cancelled_periods:
			self.add_comment(
				"Comment",
				_("Cancelled periods: {0}").format(", ".join(cancelled_periods)),
			)

		# Auto-create credit notes for invoiced rows
		if invoiced_rows:
			credit_notes = self._create_credit_notes(invoiced_rows)
			if credit_notes:
				frappe.msgprint(
					_("Credit Notes created: {0}").format(", ".join(credit_notes)),
					title=_("Credit Notes"),
					indicator="green",
				)

		# Warn about paid rows — no auto-refund
		if paid_periods:
			msg = _("Periods {0} were already paid. Manual refund Payment Entry may be needed.").format(
				", ".join(paid_periods)
			)
			frappe.msgprint(msg, title=_("Paid Periods Warning"), indicator="orange")
			self.add_comment("Comment", msg)

	def _create_credit_notes(self, invoiced_rows):
		"""Create Return Sales Invoices for invoiced billing schedule rows."""
		# Group rows by sales_invoice
		si_to_rows: dict[str, list] = {}
		for row in invoiced_rows:
			si_to_rows.setdefault(row.sales_invoice, []).append(row)

		credit_note_names = []
		for si_name, rows in si_to_rows.items():
			original_si = frappe.get_doc("Sales Invoice", si_name)
			if original_si.docstatus != 1:
				continue

			return_si = frappe.copy_doc(original_si)
			return_si.is_return = 1
			return_si.return_against = si_name
			return_si.posting_date = today()
			return_si.set_posting_time = 1

			# Negate quantities on all items
			for item in return_si.items:
				item.qty = -abs(item.qty)

			# Clear workflow_state so new Return SI starts from initial state
			# (copy_doc copies the original's workflow_state which fails insert validation)
			return_si.workflow_state = None
			return_si.flags.ignore_permissions = True
			return_si.insert()
			return_si.submit()

			credit_note_names.append(return_si.name)

			# Link credit note back to billing schedule rows
			for row in rows:
				frappe.db.set_value(
					"DCNet Contract Billing Schedule", row.name,
					"credit_note", return_si.name,
				)

		return credit_note_names

	def _sync_customer_data(self):
		"""Sync contract customer fields back to master data on submit.
		Only updates if contract field has a value (gentle sync)."""
		if not self.customer:
			return

		# Update Customer.tax_id
		if self.customer_tax_id:
			frappe.db.set_value("Customer", self.customer, "tax_id", self.customer_tax_id)

		# Update or create Address
		addr_name = frappe.db.get_value(
			"Dynamic Link",
			{"link_doctype": "Customer", "link_name": self.customer, "parenttype": "Address"},
			"parent",
		)
		addr_fields = {}
		if self.customer_address:
			addr_fields["address_line1"] = self.customer_address
		if self.customer_phone:
			addr_fields["phone"] = self.customer_phone
		if self.customer_fax:
			addr_fields["fax"] = self.customer_fax
		if self.customer_email:
			addr_fields["email_id"] = self.customer_email

		if addr_fields:
			if addr_name:
				for field, val in addr_fields.items():
					frappe.db.set_value("Address", addr_name, field, val)
			else:
				addr = frappe.new_doc("Address")
				addr.address_title = self.customer_name or self.customer
				addr.address_type = "Billing"
				addr.address_line1 = addr_fields.get("address_line1", "")
				addr.phone = addr_fields.get("phone", "")
				addr.fax = addr_fields.get("fax", "")
				addr.email_id = addr_fields.get("email_id", "")
				addr.append("links", {"link_doctype": "Customer", "link_name": self.customer})
				addr.flags.ignore_permissions = True
				addr.insert()

		# Update or create Contact
		contact_link = frappe.db.get_value(
			"Dynamic Link",
			{"link_doctype": "Customer", "link_name": self.customer, "parenttype": "Contact"},
			"parent",
		)
		if self.customer_representative:
			parts = self.customer_representative.strip().split(" ", 1)
			first_name = parts[0]
			last_name = parts[1] if len(parts) > 1 else ""

			if contact_link:
				frappe.db.set_value("Contact", contact_link, "first_name", first_name)
				if last_name:
					frappe.db.set_value("Contact", contact_link, "last_name", last_name)
				if self.customer_representative_title:
					frappe.db.set_value("Contact", contact_link, "designation", self.customer_representative_title)
			else:
				contact = frappe.new_doc("Contact")
				contact.first_name = first_name
				contact.last_name = last_name
				contact.designation = self.customer_representative_title or ""
				contact.append("links", {"link_doctype": "Customer", "link_name": self.customer})
				contact.flags.ignore_permissions = True
				contact.insert()

		# Sync CMND custom fields back to Customer (for FTTH HGD individual contracts)
		cmnd_fields = {
			"customer_id_number": self.customer_id_number,
			"customer_id_date": self.customer_id_date,
			"customer_id_place": self.customer_id_place,
			"customer_dob": self.customer_dob,
		}
		for cf_field, val in cmnd_fields.items():
			if val and frappe.db.exists("Custom Field", {"dt": "Customer", "fieldname": cf_field}):
				frappe.db.set_value("Customer", self.customer, cf_field, val)

		# Update or create Bank Account
		if self.customer_bank_account:
			ba_name = frappe.db.get_value(
				"Bank Account", {"party_type": "Customer", "party": self.customer}, "name"
			)
			if ba_name:
				frappe.db.set_value("Bank Account", ba_name, "bank_account_no", self.customer_bank_account)
			else:
				ba = frappe.new_doc("Bank Account")
				ba.account_name = f"{self.customer_name or self.customer} - Bank"
				ba.bank_account_no = self.customer_bank_account
				ba.party_type = "Customer"
				ba.party = self.customer
				ba.flags.ignore_permissions = True
				ba.insert()

	def _generate_billing_schedule(self):
		settings = frappe.get_cached_doc("DCNet Contract Settings")
		inp = ScheduleInput(
			contract_type=self.contract_type,
			payment_mode=self.payment_mode,
			package_term_months=self.package_term_months,
			acceptance_date=getdate(self.acceptance_date),
			unit_price_total=Decimal(str(self.unit_price_total or 0)),
			setup_fee=Decimal(str(self.setup_fee or 0)),
			rounding_mode=settings.default_rounding_mode or "Half-up",
		)
		rows = generate_schedule(inp)
		# Delete existing child rows from DB (important for amended docs)
		frappe.db.delete("DCNet Contract Billing Schedule", {"parent": self.name})
		self.set("billing_schedule", [])
		for r in rows:
			self.append("billing_schedule", {
				"month_index": r.month_index,
				"period_start": r.period_start,
				"period_end": r.period_end,
				"due_date": r.due_date,
				"item_type": r.item_type,
				"amount": float(r.amount),
				"is_prorated": 1 if r.is_prorated else 0,
				"state": r.state,
			})
		self.db_update_all()


@frappe.whitelist()
def generate_contract_document(contract_name, template_name=None, output_format="docx"):
	"""Generate filled contract document. Returns file URL."""
	from dcnet_contract.dcnet_contract.utils.docx_generator import generate_document
	return generate_document(contract_name, template_name, output_format)


@frappe.whitelist()
def suspend_contract(name, reason=None):
	doc = frappe.get_doc("DCNet Contract", name)
	assert_transition(doc.status, "Suspended")
	frappe.db.set_value("DCNet Contract", name, "status", "Suspended")
	if reason:
		doc.add_comment("Comment", reason)
	frappe.db.commit()


@frappe.whitelist()
def resume_contract(name):
	doc = frappe.get_doc("DCNet Contract", name)
	assert_transition(doc.status, "Active")
	frappe.db.set_value("DCNet Contract", name, "status", "Active")
	frappe.db.commit()


@frappe.whitelist()
def get_customer_info(customer):
	"""Look up Customer → Address → Contact → Bank Account and return auto-fill dict."""
	info = {}
	if not customer or not frappe.db.exists("Customer", customer):
		return info

	cust = frappe.get_doc("Customer", customer)
	info["customer_tax_id"] = cust.tax_id or ""

	# Primary address
	addr_name = frappe.db.get_value(
		"Dynamic Link",
		{"link_doctype": "Customer", "link_name": customer, "parenttype": "Address"},
		"parent",
	)
	if addr_name:
		addr = frappe.get_doc("Address", addr_name)
		addr_parts = [addr.address_line1 or ""]
		if addr.city:
			addr_parts.append(addr.city)
		info["customer_address"] = ", ".join(p for p in addr_parts if p)
		info["customer_phone"] = addr.phone or ""
		info["customer_fax"] = addr.fax or ""
		info["customer_email"] = addr.email_id or ""

	# Primary contact
	contact_link = frappe.db.get_value(
		"Dynamic Link",
		{"link_doctype": "Customer", "link_name": customer, "parenttype": "Contact"},
		"parent",
	)
	if contact_link:
		contact = frappe.get_doc("Contact", contact_link)
		full_name = ((contact.first_name or "") + " " + (contact.last_name or "")).strip()
		info["customer_representative"] = full_name
		info["customer_representative_title"] = contact.designation or ""

	# Bank account
	bank_acc = frappe.db.get_value(
		"Bank Account", {"party_type": "Customer", "party": customer}, "bank_account_no"
	)
	if bank_acc:
		info["customer_bank_account"] = bank_acc

	return info
