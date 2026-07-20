"""Tests for the Kho section of the VN Accounting workspace sidebar.

These tests assert the JSON fixture state directly — no Frappe DB required.
They validate the INTENDED final state after Phase 2 Tier-1 fixes are applied.
"""
import json
import os
import unittest


def _fixture_path() -> str:
	"""Locate workspace_sidebar/vn_accounting.json relative to this file."""
	here = os.path.dirname(os.path.abspath(__file__))
	return os.path.normpath(
		os.path.join(here, "..", "workspace_sidebar", "vn_accounting.json")
	)


class TestKhoSidebarFixture(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		with open(_fixture_path(), encoding="utf-8") as f:
			cls.data = json.load(f)
		cls.items = cls.data["items"]
		section_start = next(
			i for i, it in enumerate(cls.items)
			if it.get("type") == "Section Break" and it.get("label") == "Kho"
		)
		section_end = next(
			(
				i for i, it in enumerate(cls.items[section_start + 1:], section_start + 1)
				if it.get("type") == "Section Break"
			),
			len(cls.items),
		)
		cls.section_items = cls.items[section_start + 1:section_end]

	def test_kho_section_exists(self):
		labels = [it.get("label") for it in self.items if it.get("type") == "Section Break"]
		self.assertIn("Kho", labels)

	def test_nhap_xuat_kho_is_stock_entry(self):
		item = next(it for it in self.section_items if it["label"] == "Nhập xuất kho")
		self.assertEqual(item["link_type"], "DocType")
		self.assertEqual(item["link_to"], "Stock Entry")

	def test_nhap_xuat_kho_has_stock_entry_type_filter(self):
		"""Stock Entry must filter to only inbound/outbound movement types."""
		item = next(it for it in self.section_items if it["label"] == "Nhập xuất kho")
		ro = item.get("route_options")
		self.assertTrue(ro, "Nhập xuất kho missing route_options")
		parsed = json.loads(ro)
		self.assertIn("stock_entry_type", parsed, "route_options must include stock_entry_type filter")

	def test_nhap_xuat_kho_has_docstatus_filter(self):
		"""Stock Entry must show only submitted records (docstatus=1) in sidebar."""
		item = next(it for it in self.section_items if it["label"] == "Nhập xuất kho")
		ro = item.get("route_options")
		self.assertTrue(ro, "Nhập xuất kho missing route_options")
		parsed = json.loads(ro)
		self.assertIn("docstatus", parsed, "route_options must include docstatus filter")
		self.assertEqual(parsed["docstatus"], ["=", 1])

	def test_kiem_ke_kho_has_docstatus_filter(self):
		"""Stock Reconciliation must show only submitted records in sidebar."""
		item = next(it for it in self.section_items if it["label"] == "Kiểm kê kho")
		self.assertEqual(item["link_type"], "DocType")
		self.assertEqual(item["link_to"], "Stock Reconciliation")
		ro = item.get("route_options")
		self.assertTrue(ro, "Kiểm kê kho missing route_options")
		parsed = json.loads(ro)
		self.assertEqual(parsed.get("docstatus"), ["=", 1])

	def test_so_lo_present(self):
		item = next(it for it in self.section_items if it["label"] == "Số lô")
		self.assertEqual(item["link_type"], "DocType")
		self.assertEqual(item["link_to"], "Batch")

	def test_bc_nhap_xuat_ton_present(self):
		item = next(it for it in self.section_items if it["label"] == "BC nhập xuất tồn")
		self.assertEqual(item["link_type"], "Report")
		self.assertEqual(item["link_to"], "Stock Balance")

	def test_so_chi_tiet_kho_present(self):
		item = next(it for it in self.section_items if it["label"] == "Sổ chi tiết kho")
		self.assertEqual(item["link_type"], "Report")
		self.assertEqual(item["link_to"], "Stock Ledger")


if __name__ == "__main__":
	unittest.main()
