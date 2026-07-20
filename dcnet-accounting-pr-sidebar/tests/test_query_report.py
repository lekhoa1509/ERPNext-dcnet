from pathlib import Path
import sys
import types
import unittest

APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
	sys.path.insert(0, str(APP_ROOT))


def install_frappe_stub():
	for module_name in list(sys.modules):
		if module_name == "frappe" or module_name.startswith("frappe."):
			sys.modules.pop(module_name, None)
		if module_name == "vn_accounting.branch_cash.service":
			sys.modules.pop(module_name, None)

	frappe = types.ModuleType("frappe")
	frappe.session = types.SimpleNamespace(user="branch.user@example.com")
	frappe._dict = lambda value=None: dict(value or {})
	frappe.whitelist = lambda *args, **kwargs: (lambda fn: fn)
	frappe.read_only = lambda *args, **kwargs: (lambda fn: fn)
	frappe.db = types.SimpleNamespace(
		has_column=lambda doctype, fieldname: doctype == "Branch" and fieldname == "accounting_unit",
		get_value=lambda doctype, name, fieldname: "HN - DCNET" if doctype == "Branch" else None,
	)
	sys.modules["frappe"] = frappe

	frappe_desk = types.ModuleType("frappe.desk")
	sys.modules["frappe.desk"] = frappe_desk

	query_report_module = types.ModuleType("frappe.desk.query_report")
	query_report_module.run = lambda *args, **kwargs: {"ok": True, "kwargs": kwargs}
	sys.modules["frappe.desk.query_report"] = query_report_module

	service = types.ModuleType("vn_accounting.branch_cash.service")
	service.get_allowed_accounting_units = lambda company=None, user=None: ["HCM - DCNET"] if user == "multi.user@example.com" else []
	service.get_user_branch = lambda user=None: "DCNET Hanoi Branch"
	service.has_company_wide_access = lambda company, user=None: False
	service.is_privileged_user = lambda user=None: user == "manager@example.com"
	sys.modules["vn_accounting.branch_cash.service"] = service


install_frappe_stub()
from vn_accounting.query_report import apply_general_ledger_branch_restriction, get_allowed_general_ledger_cost_centers


class TestQueryReportRestriction(unittest.TestCase):
	def test_branch_mapping_is_used_when_user_is_restricted(self):
		allowed = get_allowed_general_ledger_cost_centers(company="DCNET", user="branch.user@example.com")
		self.assertEqual(allowed, ["HN - DCNET"])

	def test_existing_cost_centers_are_intersected_with_allowed_values(self):
		filters = apply_general_ledger_branch_restriction(
			"General Ledger",
			filters={"company": "DCNET", "cost_center": ["HN - DCNET", "Other - DCNET"]},
			user="branch.user@example.com",
		)
		self.assertEqual(filters["cost_center"], ["HN - DCNET"])

	def test_unrestricted_user_keeps_original_filters(self):
		filters = apply_general_ledger_branch_restriction(
			"General Ledger",
			filters={"company": "DCNET"},
			user="manager@example.com",
		)
		self.assertEqual(filters, {"company": "DCNET"})


if __name__ == "__main__":
	unittest.main()
