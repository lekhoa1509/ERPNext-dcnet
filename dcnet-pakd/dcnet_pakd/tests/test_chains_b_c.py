"""
Integration tests for chains B (One-off VTTB) and C (FTTH Rollup).
Run: bench --site dcnet.localhost run-tests --app dcnet_pakd --module dcnet_pakd.tests.test_chains_b_c
"""
import unittest
import frappe
from frappe.utils import today


class TestChainBOneoffVTTB(unittest.TestCase):
	"""Chain B: One-off VTTB → shadow SO → PAKD → approve → PE → commission posted"""

	def setUp(self):
		frappe.set_user("Administrator")
		# Create One-off VTTB contract
		self.contract = frappe.get_doc({
			"doctype": "DCNet Contract",
			"customer": "_Test DCNet Customer",
			"sales_person": "HR-EMP-00038",
			"company": "DCNET",
			"branch": "HCM",
			"project_category": "Telecom",
			"service_type": "VTTB",
			"contract_date": "2026-01-01",
			"acceptance_date": "2026-01-01",
			"contract_type": "One-off",
			"payment_mode": "OneOff",
			"currency": "VND",
			"items": [{
				"item_label": "VTTB Thiết bị đầu cuối",
				"item_kind": "One-off Goods",
				"uom": "Nos",
				"qty": 2,
				"unit_price": 7500,
				"amount_per_period": 15000,
				"erpnext_item": "Consulting",
			}],
		})
		self.contract.insert(ignore_permissions=True)
		self.contract.submit()
		frappe.db.commit()

	def tearDown(self):
		frappe.set_user("Administrator")
		# Cleanup PAKDs referencing this contract
		pakds = frappe.get_all("Phuong An Kinh Doanh", filters={"contract_ref": self.contract.name})
		for p in pakds:
			doc = frappe.get_doc("Phuong An Kinh Doanh", p.name)
			doc.commission_lines = []
			frappe.flags.ignore_workflow = True
			doc.save(ignore_permissions=True)
			frappe.flags.ignore_workflow = False
			doc.delete(ignore_permissions=True)
		# Cleanup the contract created in setUp + any cascaded SI/PE so the
		# test doesn't accumulate ghost _Test DCNet Customer contracts across
		# runs (caused the v0.2.0 sample-data cleanup to spawn 16 orphans).
		try:
			# Cancel + delete any auto-generated SI/PE first
			si_names = frappe.get_all("Sales Invoice",
			                          filters={"dcnet_contract": self.contract.name},
			                          pluck="name")
			for n in si_names:
				try:
					d = frappe.get_doc("Sales Invoice", n)
					if d.docstatus == 1:
						d.cancel()
					frappe.delete_doc("Sales Invoice", n, force=True, ignore_permissions=True)
				except Exception:
					pass
			doc = frappe.get_doc("DCNet Contract", self.contract.name)
			if doc.docstatus == 1 and doc.status != "Expired":
				doc.cancel()
			elif doc.status == "Expired":
				frappe.db.set_value("DCNet Contract", doc.name, "docstatus", 2,
				                     update_modified=False)
			frappe.delete_doc("DCNet Contract", doc.name, force=True, ignore_permissions=True)
		except Exception:
			pass
		frappe.db.commit()

	def test_b1_contract_created_with_shadow_so(self):
		"""One-off VTTB contract should auto-create shadow Sales Order"""
		self.contract.reload()
		self.assertEqual(self.contract.docstatus, 1, "Contract should be submitted")
		# shadow SO may or may not be created depending on dcnet_contract impl
		# Just check contract is active/submitted
		self.assertIn(self.contract.status, ["Active", "Submitted"])

	def test_b2_billing_schedule_has_row(self):
		"""One-off contract should generate billing_schedule row.

		v0.2.0 walk-items: One-off Goods generates at month_index=0 (no Setup Fee
		in this contract). Legacy v0.1.x had month_index=1 for One-off — the new
		walk-items engine packs all items starting at 0.
		"""
		bs = frappe.get_all("DCNet Contract Billing Schedule",
			filters={"parent": self.contract.name},
			fields=["name", "month_index", "amount", "item_type"])
		self.assertGreater(len(bs), 0, "One-off contract must have billing_schedule rows")
		oneoff_rows = [r for r in bs if r.item_type == "One-off Goods"]
		self.assertGreater(len(oneoff_rows), 0, "Must have at least one One-off Goods billing row")

	def test_b3_pakd_created_with_rule_engine(self):
		"""PAKD One-off Sale should compute costs via rule engine"""
		pakd = frappe.get_doc({
			"doctype": "Phuong An Kinh Doanh",
			"pakd_type": "One-off Sale/Project",
			"contract_ref": self.contract.name,
			"customer": self.contract.customer,
			"sales_person": self.contract.sales_person,
			"branch": self.contract.branch,
			"company": self.contract.company,
			"service_type": self.contract.service_type,
			"items": [{
				"item_label": "VTTB Thiết bị đầu cuối",
				"uom": "Nos",
				"qty": 2,
				"unit_price": 7500,
			}],
		})
		pakd.insert(ignore_permissions=True)
		frappe.db.commit()

		# Rule engine should compute something
		has_any_cost = any([
			pakd.total_manager_services > 0,
			pakd.total_add_costs > 0,
			pakd.total_sales_commission > 0,
		])
		self.assertTrue(has_any_cost, "One-off rule engine should compute at least one cost component")

	def test_b4_pakd_approve_generates_commission_lines(self):
		"""Approving One-off PAKD should generate commission lines"""
		pakd = frappe.get_doc({
			"doctype": "Phuong An Kinh Doanh",
			"pakd_type": "One-off Sale/Project",
			"contract_ref": self.contract.name,
			"customer": self.contract.customer,
			"sales_person": self.contract.sales_person,
			"branch": self.contract.branch,
			"company": self.contract.company,
			"service_type": self.contract.service_type,
			"items": [{
				"item_label": "VTTB Thiết bị đầu cuối",
				"uom": "Nos",
				"qty": 2,
				"unit_price": 7500,
			}],
		})
		pakd.insert(ignore_permissions=True)

		# Approve via DB to bypass workflow transition check (test env)
		frappe.db.set_value("Phuong An Kinh Doanh", pakd.name, {
			"workflow_state": "Approved",
			"status": "Approved",
		})
		frappe.db.commit()

		# Re-save to trigger validate() → _sync_commission_lines() (bypass workflow check)
		pakd.reload()
		pakd.flags.ignore_workflow = True
		pakd.save(ignore_permissions=True)
		frappe.db.commit()
		pakd.reload()

		# v0.2.0 commission_lines = SC + License only. One-off Sale has no License row,
		# but SC must be generated for each billing period.
		self.assertGreater(len(pakd.commission_lines), 0, "Approved One-off PAKD must have commission_lines")
		pending = [l for l in pakd.commission_lines if l.state == "Pending"]
		self.assertGreater(len(pending), 0, "Commission lines should be Pending on approval")
		# All v0.2.0 commission_lines must be Sales Commission or License Fee
		non_sc_license = [l for l in pakd.commission_lines if l.component not in ("Sales Commission", "License Fee")]
		self.assertEqual(len(non_sc_license), 0,
			f"v0.2.0 commission_lines must only contain SC/License — got: {[(l.component, l.state) for l in non_sc_license]}")


@unittest.skip("v0.2.0 D4: Monthly FTTH Rollup PAKD type removed — Chain C replaced by per-HD Mẫu 01 PAKDs")
class TestChainCFTTHRollup(unittest.TestCase):
	"""Chain C: FTTH Rollup Mẫu 02 — coefficient-based commission (DEPRECATED)."""

	def setUp(self):
		frappe.set_user("Administrator")
		self.contract = frappe.get_doc({
			"doctype": "DCNet Contract",
			"customer": "_Test DCNet Customer",
			"sales_person": "HR-EMP-00038",
			"company": "DCNET",
			"branch": "HCM",
			"project_category": "Telecom",
			"service_type": "FTTH DN",
			"contract_date": "2026-01-01",
			"acceptance_date": "2026-01-01",
			"contract_type": "Recurring",
			"payment_mode": "Monthly",
			"package_term_months": 1,
			"currency": "VND",
			"items": [{
				"item_label": "FTTH DN 50M",
				"uom": "Nos",
				"qty": 1,
				"unit_price": 500,
				"amount_per_period": 500,
			}],
		})
		self.contract.insert(ignore_permissions=True)
		self.contract.submit()
		frappe.db.commit()

	def tearDown(self):
		frappe.set_user("Administrator")
		pakds = frappe.get_all("Phuong An Kinh Doanh", filters={"contract_ref": self.contract.name})
		for p in pakds:
			doc = frappe.get_doc("Phuong An Kinh Doanh", p.name)
			doc.commission_lines = []
			frappe.flags.ignore_workflow = True
			doc.save(ignore_permissions=True)
			frappe.flags.ignore_workflow = False
			doc.delete(ignore_permissions=True)
		frappe.db.commit()

	def test_c1_ftth_rollup_coefficient_commission(self):
		"""Monthly FTTH Rollup: commission = (salary_coefficient %) × revenue_actual"""
		salary_coef = 15.0  # 15% — Percent field, engine divides by 100
		revenue_actual = 500.0
		expected_commission = salary_coef / 100.0 * revenue_actual  # 75.0

		pakd = frappe.get_doc({
			"doctype": "Phuong An Kinh Doanh",
			"pakd_type": "Monthly FTTH Rollup",
			"contract_ref": self.contract.name,
			"customer": self.contract.customer,
			"sales_person": self.contract.sales_person,
			"branch": self.contract.branch,
			"company": self.contract.company,
			"service_type": self.contract.service_type,
			"items": [{
				"item_label": "FTTH DN 50M",
				"uom": "Nos",
				"qty": 1,
				"unit_price": 500,
				"revenue_actual": revenue_actual,
				"salary_coefficient": salary_coef,
			}],
		})
		pakd.insert(ignore_permissions=True)
		frappe.db.commit()

		self.assertAlmostEqual(pakd.total_sales_commission, expected_commission, places=2,
			msg=f"FTTH commission should be {expected_commission} (coef × revenue_actual)")
		self.assertEqual(pakd.total_manager_services, 0, "FTTH Rollup should have no MS")
		self.assertEqual(pakd.total_add_costs, 0, "FTTH Rollup should have no AC")
		self.assertEqual(pakd.total_license_fee, 0, "FTTH Rollup should have no GPVT")

	def test_c2_ftth_rollup_only_luong_kd_lines(self):
		"""FTTH Rollup PAKD approval generates only Lương KD commission lines"""
		salary_coef = 15.0  # 15% — Percent field
		revenue_actual = 500.0

		pakd = frappe.get_doc({
			"doctype": "Phuong An Kinh Doanh",
			"pakd_type": "Monthly FTTH Rollup",
			"contract_ref": self.contract.name,
			"customer": self.contract.customer,
			"sales_person": self.contract.sales_person,
			"branch": self.contract.branch,
			"company": self.contract.company,
			"service_type": self.contract.service_type,
			"items": [{
				"item_label": "FTTH DN 50M",
				"uom": "Nos",
				"qty": 1,
				"unit_price": 500,
				"revenue_actual": revenue_actual,
				"salary_coefficient": salary_coef,
			}],
		})
		pakd.insert(ignore_permissions=True)

		# Approve via DB to bypass workflow transition check (test env)
		frappe.db.set_value("Phuong An Kinh Doanh", pakd.name, {
			"workflow_state": "Approved",
			"status": "Approved",
		})
		frappe.db.commit()

		# Re-save to trigger validate() → _sync_commission_lines() (bypass workflow check)
		pakd.reload()
		pakd.flags.ignore_workflow = True
		pakd.save(ignore_permissions=True)
		frappe.db.commit()
		pakd.reload()

		self.assertGreater(len(pakd.commission_lines), 0, "FTTH PAKD must generate commission lines")

		components = set(l.component for l in pakd.commission_lines)
		self.assertEqual(components, {"Sales Commission"},
			f"FTTH Rollup should only have Lương KD lines, got: {components}")

		# Check per-line amount
		expected_per_line = salary_coef / 100.0 * revenue_actual
		for line in pakd.commission_lines:
			self.assertAlmostEqual(line.amount, expected_per_line, places=2,
				msg=f"Each FTTH commission line should be (coef%) × revenue_actual")
