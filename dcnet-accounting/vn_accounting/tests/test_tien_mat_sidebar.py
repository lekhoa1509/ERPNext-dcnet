"""Tests for the Tiền mặt section of the VN Accounting workspace sidebar.

These tests assert the JSON fixture state directly — no Frappe DB required.
"""
import json
import os
import unittest


def _fixture_path() -> str:
	"""Locate workspace_sidebar/vn_accounting.json relative to this file."""
	here = os.path.dirname(os.path.abspath(__file__))
	# vn_accounting/tests/test_*.py → vn_accounting/workspace_sidebar/vn_accounting.json
	return os.path.normpath(
		os.path.join(here, "..", "workspace_sidebar", "vn_accounting.json")
	)


class TestTienMatSidebarFixture(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		with open(_fixture_path(), encoding="utf-8") as f:
			cls.data = json.load(f)
		cls.items = cls.data["items"]
		# Slice Tiền mặt section: between its Section Break and the next Section Break
		section_start = next(
			i for i, it in enumerate(cls.items)
			if it.get("type") == "Section Break" and it.get("label") == "Tiền mặt"
		)
		section_end = next(
			(
				i for i, it in enumerate(cls.items[section_start + 1:], section_start + 1)
				if it.get("type") == "Section Break"
			),
			len(cls.items),
		)
		cls.section_items = cls.items[section_start + 1:section_end]

	def test_section_label_renamed(self):
		labels = [it.get("label") for it in self.items if it.get("type") == "Section Break"]
		self.assertIn("Tiền mặt", labels)
		self.assertNotIn("Quỹ tiền mặt", labels)

	def test_section_has_6_items(self):
		self.assertEqual(
			len(self.section_items),
			6,
			f"Expected 6 items, got {len(self.section_items)}: "
			f"{[it.get('label') for it in self.section_items]}",
		)

	def test_phieu_thu_is_report(self):
		"""Phiếu thu now points to Cash Receipts report (captures both JE and PE)."""
		item = next(it for it in self.section_items if it["label"] == "Phiếu thu")
		self.assertEqual(item["link_type"], "Report")
		self.assertEqual(item["link_to"], "Cash Receipts")
		self.assertIn(item.get("route_options"), (None, "", "null"))

	def test_phieu_chi_is_report(self):
		"""Phiếu chi now points to Cash Payments report (captures both JE and PE)."""
		item = next(it for it in self.section_items if it["label"] == "Phiếu chi")
		self.assertEqual(item["link_type"], "Report")
		self.assertEqual(item["link_to"], "Cash Payments")
		self.assertIn(item.get("route_options"), (None, "", "null"))

	def test_kiem_ke_quy_list_present(self):
		item = next(it for it in self.section_items if it["label"] == "Kiểm kê quỹ")
		self.assertEqual(item["link_type"], "DocType")
		self.assertEqual(item["link_to"], "Cash Count")

	def test_branch_cash_entry_has_docstatus_filter(self):
		item = next(
			it for it in self.section_items if it["label"] == "Phiếu quỹ chi nhánh"
		)
		ro = item.get("route_options")
		self.assertTrue(ro, "Phiếu quỹ chi nhánh missing route_options")
		parsed = json.loads(ro)
		self.assertEqual(parsed, {"docstatus": ["=", 1]})

	def test_so_noi_bo_report_present(self):
		item = next(it for it in self.section_items if it["label"] == "Sổ quỹ chi nhánh")
		self.assertEqual(item["link_type"], "Report")
		self.assertEqual(item["link_to"], "So Noi Bo")

	def test_so_quy_tien_mat_present(self):
		item = next(it for it in self.section_items if it["label"] == "Sổ quỹ tiền mặt")
		self.assertEqual(item["link_type"], "Report")
		self.assertEqual(item["link_to"], "Cash Book")

	def test_no_removed_items(self):
		labels = [it.get("label") for it in self.items]
		# Items removed across the redesign — must not reappear.
		removed = [
			# Earlier-round folded creation entries
			"Thu tiền mặt",
			"Chi tiền mặt",
			"Tạo bút toán tiền mặt",
			"+ Rút/nộp tiền",
			"+ Tạo biên bản kiểm kê",
			# Reports + PE round — consolidated into Phiếu thu/chi
			"BC thu tiền mặt",
			"BC chi tiền mặt",
			# Reports + PE round — useless URL link, replaced by boot.py ownership
			"Phiếu kế toán",
		]
		for lbl in removed:
			self.assertNotIn(lbl, labels, f"{lbl!r} should have been removed")

	def test_no_duplicate_du_bao_dong_tien(self):
		count = sum(1 for it in self.items if it.get("label") == "Dự báo dòng tiền")
		self.assertEqual(
			count,
			1,
			f"'Dự báo dòng tiền' should appear exactly once, found {count}",
		)

	def test_no_je_pe_doctype_links_in_fixture(self):
		"""JE/PE ownership is now boot.py-driven, NOT fixture-driven.

		After the Reports + PE round, no sidebar item anywhere in the fixture
		should claim Journal Entry or Payment Entry via link_type=DocType. The
		previous Phiếu thu / Phiếu chi DocType links have been replaced with
		Report links to Cash Receipts / Cash Payments. Cross-workspace sidebar
		context preservation is handled in vn_accounting/boot.py via the
		`workspace_sidebar_item` bootinfo override.
		"""
		offenders = [
			(it.get("label"), it.get("link_to")) for it in self.items
			if it.get("link_type") == "DocType"
			and it.get("link_to") in ("Journal Entry", "Payment Entry")
		]
		self.assertEqual(
			offenders,
			[],
			f"unexpected JE/PE DocType links in fixture: {offenders}. "
			"Cross-workspace ownership should be claimed via boot.py, not fixture.",
		)

	def test_phieu_thu_chi_section_order(self):
		"""Phiếu thu must come before Phiếu chi (UX convention: thu before chi)."""
		labels = [it.get("label") for it in self.section_items]
		idx_thu = labels.index("Phiếu thu")
		idx_chi = labels.index("Phiếu chi")
		self.assertLess(idx_thu, idx_chi, "Phiếu thu must precede Phiếu chi")


if __name__ == "__main__":
	unittest.main()
