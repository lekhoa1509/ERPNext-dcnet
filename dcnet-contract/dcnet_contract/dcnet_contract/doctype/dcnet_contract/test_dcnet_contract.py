import frappe
from frappe.tests.utils import FrappeTestCase

from dcnet_contract.tests.helpers import (
	ensure_branch,
	ensure_customer,
	ensure_employee,
	ensure_item,
	make_active_contract,
)


class TestDCNetContract(FrappeTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.customer = ensure_customer()
		cls.sales_person = ensure_employee()
		ensure_branch("HCM")
		cls.test_item = ensure_item()

	def test_draft_to_active_generates_schedule(self):
		doc = frappe.get_doc({
			"doctype": "DCNet Contract",
			"customer": self.customer,
			"sales_person": self.sales_person,
			"branch": "HCM",
			"contract_type": "Recurring",
			"service_type": "P2P",
			"project_category": "Telecom",
			"payment_mode": "Monthly",
			"package_term_months": 12,
			"contract_date": "2026-01-01",
			"acceptance_date": "2026-01-01",
			"items": [{"item_label": "P2P HCM-HN 100M", "qty": 1, "unit_price": 10500}],
		}).insert(ignore_permissions=True)

		self.assertEqual(doc.status, "Draft")
		self.assertEqual(doc.unit_price_total, 10500)
		self.assertEqual(len(doc.billing_schedule), 0)

		doc.submit()
		doc.reload()
		self.assertEqual(doc.status, "Active")
		self.assertEqual(len(doc.billing_schedule), 12)
		self.assertTrue(all(r.state == "Projected" for r in doc.billing_schedule))

	def test_cancel_from_active(self):
		doc = make_active_contract(self.customer, self.sales_person)
		doc.cancel()
		doc.reload()
		self.assertEqual(doc.status, "Cancelled")
		self.assertEqual(doc.docstatus, 2)

	def test_vttb_without_item_link_fails(self):
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc({
				"doctype": "DCNet Contract",
				"customer": self.customer,
				"sales_person": self.sales_person,
				"branch": "HCM",
				"contract_type": "One-off",
				"service_type": "VTTB",
				"project_category": "Equipment",
				"payment_mode": "OneOff",
				"contract_date": "2026-01-01",
				"acceptance_date": "2026-01-01",
				"items": [{"item_label": "Router Cisco", "qty": 1, "unit_price": 50000}],
			}).insert(ignore_permissions=True)

	def test_grand_total_computation(self):
		doc = frappe.get_doc({
			"doctype": "DCNet Contract",
			"customer": self.customer,
			"sales_person": self.sales_person,
			"branch": "HCM",
			"contract_type": "Recurring",
			"service_type": "MPLS",
			"project_category": "Telecom",
			"payment_mode": "Monthly",
			"package_term_months": 6,
			"contract_date": "2026-01-01",
			"acceptance_date": "2026-01-01",
			"setup_fee": 5000,
			"items": [{"item_label": "MPLS 50M", "qty": 1, "unit_price": 8000}],
		}).insert(ignore_permissions=True)

		self.assertEqual(doc.unit_price_total, 8000)
		self.assertEqual(doc.grand_total, 8000 * 6 + 5000)

	def test_one_off_contract(self):
		doc = frappe.get_doc({
			"doctype": "DCNet Contract",
			"customer": self.customer,
			"sales_person": self.sales_person,
			"branch": "HCM",
			"contract_type": "One-off",
			"service_type": "Thi công",
			"project_category": "Construction",
			"payment_mode": "OneOff",
			"contract_date": "2026-03-01",
			"acceptance_date": "2026-03-01",
			"items": [{"item_label": "Thi công hạ tầng", "qty": 1, "unit_price": 150000}],
		}).insert(ignore_permissions=True)

		doc.submit()
		doc.reload()
		self.assertEqual(doc.status, "Active")
		self.assertEqual(len(doc.billing_schedule), 1)
		self.assertEqual(float(doc.billing_schedule[0].amount), 150000.0)

	def test_vttb_submit_creates_shadow_so(self):
		"""VTTB contract submit creates a shadow Sales Order with correct items."""
		doc = frappe.get_doc({
			"doctype": "DCNet Contract",
			"customer": self.customer,
			"sales_person": self.sales_person,
			"branch": "HCM",
			"contract_type": "One-off",
			"service_type": "VTTB",
			"project_category": "Equipment",
			"payment_mode": "OneOff",
			"contract_date": "2026-03-01",
			"acceptance_date": "2026-03-15",
			"items": [
				{"item_label": "Router Cisco", "qty": 2, "unit_price": 50000, "erpnext_item": self.test_item},
			],
		}).insert(ignore_permissions=True)

		doc.submit()
		doc.reload()

		# shadow_sales_order field should be set
		self.assertTrue(doc.shadow_sales_order)

		# Verify the SO
		so = frappe.get_doc("Sales Order", doc.shadow_sales_order)
		self.assertEqual(so.customer, self.customer)
		self.assertEqual(so.is_shadow_contract, 1)
		self.assertEqual(so.docstatus, 1)
		self.assertEqual(len(so.items), 1)
		self.assertEqual(so.items[0].item_code, self.test_item)
		self.assertEqual(so.items[0].qty, 2)

	def test_vttb_cancel_cascades_to_shadow_so(self):
		"""Cancelling a VTTB contract also cancels the shadow SO."""
		doc = frappe.get_doc({
			"doctype": "DCNet Contract",
			"customer": self.customer,
			"sales_person": self.sales_person,
			"branch": "HCM",
			"contract_type": "One-off",
			"service_type": "VTTB",
			"project_category": "Equipment",
			"payment_mode": "OneOff",
			"contract_date": "2026-03-01",
			"acceptance_date": "2026-03-15",
			"items": [
				{"item_label": "Switch HP", "qty": 1, "unit_price": 30000, "erpnext_item": self.test_item},
			],
		}).insert(ignore_permissions=True)

		doc.submit()
		doc.reload()
		so_name = doc.shadow_sales_order
		self.assertTrue(so_name)

		doc.cancel()

		# SO should be cancelled
		so = frappe.get_doc("Sales Order", so_name)
		self.assertEqual(so.docstatus, 2)

	def test_recurring_no_shadow_so(self):
		"""Recurring contracts should NOT create shadow SOs."""
		doc = make_active_contract(self.customer, self.sales_person)
		self.assertFalse(doc.shadow_sales_order)

	def test_thi_cong_no_shadow_so(self):
		"""Thi cong one-off contracts should NOT create shadow SOs."""
		doc = frappe.get_doc({
			"doctype": "DCNet Contract",
			"customer": self.customer,
			"sales_person": self.sales_person,
			"branch": "HCM",
			"contract_type": "One-off",
			"service_type": "Thi công",
			"project_category": "Construction",
			"payment_mode": "OneOff",
			"contract_date": "2026-03-01",
			"acceptance_date": "2026-03-01",
			"items": [{"item_label": "Thi công hạ tầng", "qty": 1, "unit_price": 150000}],
		}).insert(ignore_permissions=True)

		doc.submit()
		doc.reload()
		self.assertFalse(doc.shadow_sales_order)

	def test_shadow_so_permission_query(self):
		"""Non-admin users cannot see shadow SOs via permission query."""
		from dcnet_contract.dcnet_contract.permissions import so_permission_query

		# Admin/System Manager gets empty string (no filter)
		result = so_permission_query("Administrator")
		self.assertEqual(result, "")

		# Non-admin gets filter to exclude shadow SOs
		# Create a test user scenario
		condition = so_permission_query("test_non_admin@example.com")
		self.assertIn("is_shadow_contract", condition)

	def test_amend_active_contract_creates_revision(self):
		"""Amending an active contract: old→Revised, future schedule cancelled, new→Active.
		Frappe requires cancelling before amending. Our on_cancel sets status to Cancelled,
		then on_submit of the amended doc detects amended_from and sets old to Revised."""
		old_doc = make_active_contract(self.customer, self.sales_person)
		self.assertEqual(old_doc.status, "Active")
		self.assertEqual(len(old_doc.billing_schedule), 12)

		# Frappe amend pattern: cancel first, then amend
		old_doc.cancel()
		old_doc.reload()
		self.assertEqual(old_doc.status, "Cancelled")

		# Amend: Frappe creates a copy with amended_from set
		new_doc = frappe.copy_doc(old_doc)
		new_doc.amended_from = old_doc.name
		new_doc.docstatus = 0
		# Change terms for the revision (e.g., new price)
		new_doc.items[0].unit_price = 12000
		new_doc.insert(ignore_permissions=True)
		new_doc.submit()
		new_doc.reload()

		# New contract should be Active with fresh schedule
		self.assertEqual(new_doc.status, "Active")
		self.assertEqual(len(new_doc.billing_schedule), 12)
		self.assertTrue(all(r.state == "Projected" for r in new_doc.billing_schedule))

		# Old contract should be Revised (upgraded from Cancelled by the amend)
		old_doc.reload()
		self.assertEqual(old_doc.status, "Revised")

		# All old schedule rows should be Cancelled
		self.assertTrue(all(r.state == "Cancelled" for r in old_doc.billing_schedule))

	def test_cancel_midterm_future_rows_cancelled_paid_untouched(self):
		"""Cancel mid-term: future Projected→Cancelled, Paid rows stay."""
		doc = make_active_contract(self.customer, self.sales_person)
		self.assertEqual(len(doc.billing_schedule), 12)

		# Simulate: mark first 2 rows as Paid (as if invoiced and paid)
		for i, row in enumerate(doc.billing_schedule):
			if i < 2:
				frappe.db.set_value(
					"DCNet Contract Billing Schedule", row.name, "state", "Paid"
				)

		doc.reload()
		self.assertEqual(doc.billing_schedule[0].state, "Paid")
		self.assertEqual(doc.billing_schedule[1].state, "Paid")

		doc.cancel()
		doc.reload()

		self.assertEqual(doc.status, "Cancelled")
		# First 2 rows should still be Paid
		self.assertEqual(doc.billing_schedule[0].state, "Paid")
		self.assertEqual(doc.billing_schedule[1].state, "Paid")
		# Remaining 10 rows should be Cancelled
		for row in doc.billing_schedule[2:]:
			self.assertEqual(row.state, "Cancelled")

	def test_cancel_midterm_invoiced_row_with_invalid_si(self):
		"""Cancel mid-term with Invoiced row pointing to non-existent/cancelled SI.
		_create_credit_notes skips rows whose SI is not docstatus=1. No crash."""
		doc = make_active_contract(self.customer, self.sales_person)

		# Simulate: mark row 3 as Invoiced with a fake SI name (not docstatus=1)
		frappe.db.set_value(
			"DCNet Contract Billing Schedule", doc.billing_schedule[2].name,
			{"state": "Invoiced", "sales_invoice": "SI-TEST-INVALID"},
		)

		doc.reload()
		# Cancel should work — credit note skipped because SI is invalid (no error)
		doc.cancel()
		doc.reload()

		self.assertEqual(doc.status, "Cancelled")
		# The invoiced row should now be Cancelled
		self.assertEqual(doc.billing_schedule[2].state, "Cancelled")
		# No credit_note linked because the SI was invalid
		credit_note = frappe.db.get_value(
			"DCNet Contract Billing Schedule", doc.billing_schedule[2].name, "credit_note"
		)
		self.assertFalse(credit_note)

	def test_state_machine_revised_transition(self):
		"""State machine allows Active → Revised."""
		from dcnet_contract.dcnet_contract.utils.state_machine import assert_transition
		assert_transition("Active", "Revised")  # Should not raise

	# ─── Edge case validation tests (Phase 1 guards) ────────────────────

	def test_empty_items_raises_validation(self):
		"""Contract with no items → validation error."""
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc({
				"doctype": "DCNet Contract",
				"customer": self.customer,
				"sales_person": self.sales_person,
				"branch": "HCM",
				"contract_type": "Recurring",
				"service_type": "P2P",
				"project_category": "Telecom",
				"payment_mode": "Monthly",
				"package_term_months": 12,
				"contract_date": "2026-01-01",
				"acceptance_date": "2026-01-01",
				"items": [],
			}).insert(ignore_permissions=True)

	def test_zero_unit_price_raises_validation(self):
		"""Item with unit_price=0 → validation error."""
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc({
				"doctype": "DCNet Contract",
				"customer": self.customer,
				"sales_person": self.sales_person,
				"branch": "HCM",
				"contract_type": "Recurring",
				"service_type": "P2P",
				"project_category": "Telecom",
				"payment_mode": "Monthly",
				"package_term_months": 12,
				"contract_date": "2026-01-01",
				"acceptance_date": "2026-01-01",
				"items": [{"item_label": "P2P", "qty": 1, "unit_price": 0}],
			}).insert(ignore_permissions=True)

	def test_zero_qty_raises_validation(self):
		"""Item with qty=0 → validation error."""
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc({
				"doctype": "DCNet Contract",
				"customer": self.customer,
				"sales_person": self.sales_person,
				"branch": "HCM",
				"contract_type": "Recurring",
				"service_type": "P2P",
				"project_category": "Telecom",
				"payment_mode": "Monthly",
				"package_term_months": 12,
				"contract_date": "2026-01-01",
				"acceptance_date": "2026-01-01",
				"items": [{"item_label": "P2P", "qty": 0, "unit_price": 10500}],
			}).insert(ignore_permissions=True)

	def test_submit_without_acceptance_date_raises(self):
		"""Submit without acceptance_date → before_submit error."""
		doc = frappe.get_doc({
			"doctype": "DCNet Contract",
			"customer": self.customer,
			"sales_person": self.sales_person,
			"branch": "HCM",
			"contract_type": "Recurring",
			"service_type": "P2P",
			"project_category": "Telecom",
			"payment_mode": "Monthly",
			"package_term_months": 12,
			"contract_date": "2026-01-01",
			"acceptance_date": "2026-01-01",
			"items": [{"item_label": "P2P", "qty": 1, "unit_price": 10500}],
		}).insert(ignore_permissions=True)

		# Remove acceptance_date after insert (bypassing validate)
		frappe.db.set_value("DCNet Contract", doc.name, "acceptance_date", None)
		doc.reload()

		with self.assertRaises(frappe.ValidationError):
			doc.submit()
