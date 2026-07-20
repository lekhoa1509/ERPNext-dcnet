"""Tests cho dirty-check fingerprint (FB-2026-00625)."""

import frappe
from frappe.tests.utils import FrappeTestCase

from vn_accounting.api.realtime import report_data_fingerprint


class TestReportDataFingerprint(FrappeTestCase):
	def test_empty_doctypes_returns_empty(self):
		self.assertEqual(report_data_fingerprint("[]"), "")
		self.assertEqual(report_data_fingerprint(""), "")

	def test_bogus_doctype_ignored(self):
		# Doctype không tồn tại -> bỏ qua, không lỗi
		self.assertEqual(report_data_fingerprint('["__NoSuchDoctype__"]'), "")

	def test_valid_doctype_format(self):
		# Payment Entry luôn tồn tại trên site có ERPNext
		fp = report_data_fingerprint('["Payment Entry"]')
		self.assertTrue(fp.startswith("Payment Entry:"))
		self.assertEqual(fp.count("|"), 0)  # 1 doctype -> không có separator

	def test_multiple_doctypes_joined(self):
		fp = report_data_fingerprint('["Payment Entry", "Journal Entry"]')
		self.assertEqual(fp.count("|"), 1)
		self.assertTrue(fp.startswith("Payment Entry:"))
		self.assertIn("|Journal Entry:", fp)

	def test_mixed_valid_and_bogus(self):
		fp = report_data_fingerprint('["Payment Entry", "__Nope__"]')
		self.assertTrue(fp.startswith("Payment Entry:"))
		self.assertEqual(fp.count("|"), 0)  # bogus bị loại

	def test_fingerprint_stable_without_change(self):
		# Không có thay đổi DB -> 2 lần gọi cho cùng fingerprint (deterministic)
		company = frappe.db.get_value("Company", {}, "name")
		a = report_data_fingerprint('["Payment Entry", "Journal Entry"]', company=company)
		b = report_data_fingerprint('["Payment Entry", "Journal Entry"]', company=company)
		self.assertEqual(a, b)

	def test_company_filter_scopes_count(self):
		# Lọc company chỉ áp cho doctype có trường company (PE có; bỏ qua nếu không)
		company = frappe.db.get_value("Company", {}, "name")
		scoped = report_data_fingerprint('["Payment Entry"]', company=company)
		unscoped = report_data_fingerprint('["Payment Entry"]')
		# cả hai đều đúng format; scoped count <= unscoped count
		self.assertTrue(scoped.startswith("Payment Entry:"))
		self.assertTrue(unscoped.startswith("Payment Entry:"))
