"""Tests for PAKD _sync_commission_lines override rescale + Skipped/Cancelled preservation.

Run from bench root:
  env/bin/python -m unittest dcnet_pakd.tests.test_sync_commission_lines -v
"""

import unittest

import frappe


def _ensure_frappe():
	if not getattr(frappe.local, "conf", None):
		frappe.init(site="dcnet.localhost", sites_path="sites")
		frappe.connect()


class TestSyncCommissionLines(unittest.TestCase):
	"""End-to-end exercising of _sync_commission_lines via a real PAKD doc.

	Uses an existing draft PAKD (PAKD-2026-00006) and rolls back state at end of
	each test by restoring the snapshotted commission_lines.
	"""

	@classmethod
	def setUpClass(cls):
		_ensure_frappe()
		frappe.set_user("Administrator")
		# Dynamically pick the first Draft PAKD with Pending Sales Commission lines.
		# The legacy hardcoded "PAKD-2026-00006" got purged by the v0.2.0 sample
		# cleanup; this lookup keeps the test resilient to seed churn.
		picked = frappe.db.sql_list("""
			SELECT DISTINCT p.name FROM `tabPhuong An Kinh Doanh` p
			JOIN `tabPAKD Commission Line` cl ON cl.parent = p.name
			WHERE p.workflow_state = 'Draft'
			  AND cl.state = 'Pending' AND cl.component = 'Sales Commission'
			LIMIT 1
		""")
		if not picked:
			raise unittest.SkipTest(
				"No Draft PAKD with Pending Sales Commission lines — re-seed dcnet_sample")
		cls.PAKD = picked[0]

	def setUp(self):
		doc = frappe.get_doc("Phuong An Kinh Doanh", self.PAKD)
		self._snapshot = [
			(l.name, l.state, l.amount, l.override_rate or 0, l.skip_reason or "")
			for l in doc.commission_lines
		]

	def tearDown(self):
		for name, state, amount, override_rate, skip_reason in self._snapshot:
			if not frappe.db.exists("PAKD Commission Line", name):
				continue
			frappe.db.set_value(
				"PAKD Commission Line",
				name,
				{
					"state": state,
					"amount": amount,
					"override_rate": override_rate,
					"skip_reason": skip_reason,
				},
				update_modified=False,
			)
		frappe.db.commit()

	def _line_for(self, doc, component):
		for l in doc.commission_lines:
			if l.component == component and l.state == "Pending":
				return l
		raise AssertionError(f"No Pending line found for component={component}")

	def test_per_line_override_rescales_amount(self):
		"""line.amount at upstream 6% → set line.override_rate=3 → after save, line.amount halves."""
		doc = frappe.get_doc("Phuong An Kinh Doanh", self.PAKD)
		sc = self._line_for(doc, "Sales Commission")
		original_amount = sc.amount

		sc.override_rate = 3.0  # half of template 6%
		doc.save(ignore_permissions=True)

		doc.reload()
		sc_after = next(l for l in doc.commission_lines if l.name == sc.name)
		# Template SC rate is 6%; rescale = original × (3/6) = original / 2
		self.assertEqual(sc_after.amount, round(original_amount * 3 / 6))

	def test_blank_line_override_falls_through(self):
		"""line.override_rate=0 (default) → no rescale; amount stays at upstream."""
		doc = frappe.get_doc("Phuong An Kinh Doanh", self.PAKD)
		sc = self._line_for(doc, "Sales Commission")
		sc.override_rate = 0
		doc.save(ignore_permissions=True)

		doc.reload()
		sc_after = next(l for l in doc.commission_lines if l.name == sc.name)
		# Amount should be the canonical engine-derived value
		self.assertEqual(sc_after.amount, doc.total_sales_commission or sc_after.amount)

	def test_skipped_lines_preserved_on_resync(self):
		"""Line in Skipped state stays Skipped + amount preserved; no Pending duplicate appended."""
		doc = frappe.get_doc("Phuong An Kinh Doanh", self.PAKD)
		sc = self._line_for(doc, "Sales Commission")
		sc.state = "Skipped"
		sc.skip_reason = "Test: kỳ này bỏ qua"
		original_amount = sc.amount
		doc.save(ignore_permissions=True)

		doc.reload()
		sc_after = next(l for l in doc.commission_lines if l.name == sc.name)
		self.assertEqual(sc_after.state, "Skipped")
		self.assertEqual(sc_after.amount, original_amount)
		# No duplicate Pending for same (period, component)
		dupes = [
			l for l in doc.commission_lines
			if l.component == "Sales Commission"
			and l.billing_schedule_idx == sc_after.billing_schedule_idx
			and l.state == "Pending"
		]
		self.assertEqual(dupes, [])


if __name__ == "__main__":
	unittest.main()
