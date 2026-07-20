"""Tests for the Hợp đồng section of the VN Accounting workspace sidebar (Phase C)."""
import json
import os
import unittest


def _fixture_path(rel: str) -> str:
	here = os.path.dirname(os.path.abspath(__file__))
	return os.path.normpath(os.path.join(here, "..", rel))


class TestContractSection(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		with open(_fixture_path("workspace_sidebar/vn_accounting.json"), encoding="utf-8") as f:
			cls.data = json.load(f)
		cls.items = cls.data["items"]
		# Find Hợp đồng section + its child range
		start = next(
			i for i, it in enumerate(cls.items)
			if it.get("type") == "Section Break" and it.get("label") == "Hợp đồng"
		)
		end = next(
			(i for i, it in enumerate(cls.items[start + 1:], start + 1)
			 if it.get("type") == "Section Break"),
			len(cls.items),
		)
		cls.section_break = cls.items[start]
		cls.section_items = cls.items[start + 1:end]

	def test_section_present(self):
		labels = [it.get("label") for it in self.items if it.get("type") == "Section Break"]
		self.assertIn("Hợp đồng", labels)

	def test_section_position_after_banhang(self):
		# Hợp đồng comes immediately after Bán hàng. PAKD (Phase D) sits between
		# Hợp đồng and Kho, so don't assert Hợp đồng is directly before Kho.
		labels = [it.get("label") for it in self.items if it.get("type") == "Section Break"]
		self.assertEqual(labels.index("Hợp đồng"), labels.index("Bán hàng") + 1)
		self.assertLess(labels.index("Hợp đồng"), labels.index("Kho"))

	def test_all_4_items_present(self):
		expected = {
			"Danh sách hợp đồng": ("DocType", "DCNet Contract"),
			"Mẫu hợp đồng": ("DocType", "DCNet Contract Template"),
			"Công nợ theo hợp đồng": ("Report", "Outstanding Receivables by Contract"),
			"Hợp đồng sắp hết hạn": ("Report", "Contract Expiry Report"),
		}
		labels = {it["label"]: (it["link_type"], it["link_to"]) for it in self.section_items}
		for label, expected_pair in expected.items():
			self.assertIn(label, labels, f"missing item: {label}")
			self.assertEqual(labels[label], expected_pair)

	def test_main_list_has_docstatus_filter(self):
		item = next(it for it in self.section_items if it["label"] == "Danh sách hợp đồng")
		ro = item.get("route_options") or ""
		self.assertIn("docstatus", ro)

	def test_boot_claims_dcnet_contract(self):
		# Read boot.py source — string-search for the DocType
		boot_path = os.path.normpath(
			os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "boot.py")
		)
		with open(boot_path, encoding="utf-8") as f:
			src = f.read()
		self.assertIn('"DCNet Contract"', src)

	def test_section_icon_file_text(self):
		self.assertEqual(self.section_break.get("icon"), "file-text")


if __name__ == "__main__":
	unittest.main()
