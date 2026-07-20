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
	frappe._ = lambda value, *args, **kwargs: value
	frappe.throw = lambda message: (_ for _ in ()).throw(Exception(message))
	frappe._dict = lambda value=None: value or {}
	frappe.utils = types.SimpleNamespace(flt=lambda value, precision=2: round(float(value or 0), precision))
	sys.modules["frappe"] = frappe

	service = types.ModuleType("vn_accounting.branch_cash.service")
	service.build_branch_cash_entry_permission_query = lambda table_alias="`tabBranch Cash Entry`", user=None: f"{table_alias}.branch = 'CN-HCM'"
	service.validate_report_filters = lambda filters, user=None: None
	sys.modules["vn_accounting.branch_cash.service"] = service


install_frappe_stub()
from vn_accounting.vn_accounting.report.so_noi_bo.so_noi_bo import build_ledger_rows, get_conditions


class TestSoNoiBoReport(unittest.TestCase):
	def test_build_ledger_rows_generates_running_balance(self):
		rows = [
			{
				"name": "BCE-0001",
				"posting_date": "2026-04-13",
				"branch": "CN-HCM",
				"accounting_unit": "HCM - DCNET",
				"direction": "Receive",
				"amount": 500000,
				"remarks": "Thu nội bộ",
			},
			{
				"name": "BCE-0002",
				"posting_date": "2026-04-14",
				"branch": "CN-HCM",
				"accounting_unit": "HCM - DCNET",
				"direction": "Pay",
				"amount": 125000,
				"remarks": "Chi nội bộ",
			},
		]

		data = build_ledger_rows(rows, 100000)

		self.assertEqual(data[0]["remarks"], "Số dư đầu kỳ")
		self.assertEqual(data[1]["debit"], 500000)
		self.assertEqual(data[1]["credit"], 0)
		self.assertEqual(data[1]["balance"], 600000)
		self.assertEqual(data[2]["debit"], 0)
		self.assertEqual(data[2]["credit"], 125000)
		self.assertEqual(data[2]["balance"], 475000)
		self.assertEqual(data[3]["remarks"], "Cộng phát sinh")
		self.assertEqual(data[3]["debit"], 500000)
		self.assertEqual(data[3]["credit"], 125000)
		self.assertEqual(data[4]["remarks"], "Số dư cuối kỳ")
		self.assertEqual(data[4]["balance"], 475000)

	def test_get_conditions_forces_internal_scope_and_permission_filter(self):
		conditions, params = get_conditions(
			{
				"company": "DCNET",
				"from_date": "2026-04-01",
				"to_date": "2026-04-30",
				"branch": "CN-HCM",
			}
		)

		self.assertIn("bce.posting_scope = 'Internal'", conditions)
		self.assertIn("bce.branch = %(branch)s", conditions)
		self.assertIn("(bce.branch = 'CN-HCM')", conditions)
		self.assertEqual(params["company"], "DCNET")
		self.assertEqual(params["branch"], "CN-HCM")


if __name__ == "__main__":
	unittest.main()
