"""Tests for the PAKD section of the VN Accounting workspace sidebar (Phase D)."""
import json
import os
import unittest


def _fixture_path(rel: str) -> str:
	here = os.path.dirname(os.path.abspath(__file__))
	return os.path.normpath(os.path.join(here, "..", rel))


class TestPakdSection(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		with open(_fixture_path("workspace_sidebar/vn_accounting.json"), encoding="utf-8") as f:
			cls.data = json.load(f)
		cls.items = cls.data["items"]
		start = next(
			i for i, it in enumerate(cls.items)
			if it.get("type") == "Section Break" and it.get("label") == "PAKD"
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
		self.assertIn("PAKD", labels)

	def test_section_position_after_hopdong_before_kho(self):
		labels = [it.get("label") for it in self.items if it.get("type") == "Section Break"]
		self.assertEqual(labels.index("PAKD"), labels.index("Hợp đồng") + 1)
		self.assertEqual(labels.index("PAKD"), labels.index("Kho") - 1)

	def test_all_5_items_present(self):
		expected = {
			"Phương án kinh doanh": ("DocType", "Phuong An Kinh Doanh"),
			"Bảng tính hoa hồng": ("DocType", "PAKD Commission Rule Template"),
			"Sổ chi tiết hoa hồng": ("Report", "Commission Register"),
			"PAKD chờ xử lý": ("Report", "Pending PAKD Aging"),
			"Lợi nhuận theo dịch vụ": ("Report", "Profitability by Service"),
		}
		labels = {it["label"]: (it["link_type"], it["link_to"]) for it in self.section_items}
		for label, expected_pair in expected.items():
			self.assertIn(label, labels, f"missing item: {label}")
			self.assertEqual(labels[label], expected_pair)

	def test_pakd_main_has_no_route_options(self):
		"""Phuong An Kinh Doanh is_submittable=0 — must NOT have docstatus filter."""
		item = next(it for it in self.section_items if it["label"] == "Phương án kinh doanh")
		self.assertNotIn("route_options", item)

	def test_boot_claims_phuong_an_kinh_doanh(self):
		boot_path = os.path.normpath(
			os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "boot.py")
		)
		with open(boot_path, encoding="utf-8") as f:
			src = f.read()
		self.assertIn('"Phuong An Kinh Doanh"', src)

	def test_section_icon_briefcase(self):
		self.assertEqual(self.section_break.get("icon"), "briefcase")


if __name__ == "__main__":
	unittest.main()
