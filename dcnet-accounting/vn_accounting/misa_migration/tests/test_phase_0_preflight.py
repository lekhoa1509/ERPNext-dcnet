"""Unit tests for Phase 0 prerequisite checker (UX Gap 7).

Each check verifies a specific dependency that must be in place BEFORE
running Phase 0 OB import, so the operator gets actionable feedback
instead of silent balance drops or mid-stream handler failures.
"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestPhase0Prerequisites(unittest.TestCase):

    def _patch_frappe_for_check(
        self, file_type, payload_rows, master_existing=None, **extras,
    ):
        """Set up frappe mocks: tabMisa Migration Row + master existence."""
        master_existing = master_existing or []

        def sql(query, params=(), as_dict=False):
            if "raw_payload" in query:
                import json
                return [{"raw_payload": json.dumps(p)} for p in payload_rows]
            return []

        def sql_list(query, params=()):
            if "SELECT DISTINCT file_type" in query:
                return [file_type]
            if "SELECT name FROM" in query:
                # Bulk existence check — return whichever masters exist
                return list(master_existing)
            return []

        m = MagicMock()
        m.db.sql = sql
        m.db.sql_list = sql_list
        m.db.get_value.return_value = extras.get("company", "DCNET TEST")
        m.db.count.return_value = extras.get("count", 0)
        m.db.exists.return_value = extras.get("exists", False)
        m.defaults.get_global_default.return_value = "DCNET TEST"
        return m

    def test_customer_ar_all_resolve_passes(self):
        from vn_accounting.misa_migration.importers import phase_0_preflight as p
        mock_frappe = self._patch_frappe_for_check(
            "OB Customer AR",
            payload_rows=[
                {"Mã khách hàng": "KH001"},
                {"Mã khách hàng": "KH002"},
            ],
            master_existing=["KH001", "KH002"],
        )
        with patch.object(p, "frappe", mock_frappe):
            r = p.check_phase_0_prerequisites("MM-X", company="DCNET TEST")
        self.assertEqual(r["status"], "ok")
        self.assertEqual(r["block_count"], 0)
        cust_check = [c for c in r["checks"] if c["label"] == "Customer master"][0]
        self.assertTrue(cust_check["passed"])
        self.assertEqual(cust_check["found"], 2)
        self.assertEqual(cust_check["expected"], 2)

    def test_customer_ar_missing_master_blocks(self):
        from vn_accounting.misa_migration.importers import phase_0_preflight as p
        mock_frappe = self._patch_frappe_for_check(
            "OB Customer AR",
            payload_rows=[
                {"Mã khách hàng": "KH001"},
                {"Mã khách hàng": "KH002"},
                {"Mã khách hàng": "KH003"},
            ],
            master_existing=["KH001"],
        )
        with patch.object(p, "frappe", mock_frappe):
            r = p.check_phase_0_prerequisites("MM-X", company="DCNET TEST")
        self.assertEqual(r["status"], "block")
        self.assertEqual(r["block_count"], 1)
        cust_check = [c for c in r["checks"] if c["label"] == "Customer master"][0]
        self.assertFalse(cust_check["passed"])
        self.assertEqual(cust_check["found"], 1)
        self.assertEqual(cust_check["expected"], 3)
        self.assertIn("KH002", cust_check["issues"][0])
        self.assertIn("KH003", cust_check["issues"][0])
        self.assertIn("Phase 3", cust_check["hint"])

    def test_inventory_warehouse_missing_blocks(self):
        from vn_accounting.misa_migration.importers import phase_0_preflight as p
        mock_frappe = self._patch_frappe_for_check(
            "OB Inventory",
            payload_rows=[
                {"Mã hàng": "ITEM01", "Mã kho": "KHOHN"},
                {"Mã hàng": "ITEM02", "Mã kho": "KHOCANTHO"},
            ],
            master_existing=["ITEM01", "ITEM02"],  # items exist
        )
        # Override sql_list to distinguish DISTINCT vs item vs warehouse
        def sql_list(query, params=()):
            if "SELECT DISTINCT file_type" in query:
                return ["OB Inventory"]
            if "tabItem" in query:
                return ["ITEM01", "ITEM02"]
            if "tabWarehouse" in query:
                return []   # no warehouses exist
            return []
        mock_frappe.db.sql_list = sql_list
        from vn_accounting.misa_migration.importers import phase_0_preflight as p
        with patch.object(p, "frappe", mock_frappe):
            r = p.check_phase_0_prerequisites("MM-X", company="DCNET TEST")
        self.assertEqual(r["status"], "block")
        # Two checks for OB Inventory: item + warehouse
        wh_check = [c for c in r["checks"] if c["label"] == "Warehouse master"][0]
        self.assertFalse(wh_check["passed"])
        self.assertEqual(wh_check["expected"], 2)
        self.assertEqual(wh_check["found"], 0)
        item_check = [c for c in r["checks"]
                      if c["label"] == "Item master (stock items)"][0]
        self.assertTrue(item_check["passed"])

    def test_fixed_asset_item_missing_blocks(self):
        from vn_accounting.misa_migration.importers import phase_0_preflight as p
        mock_frappe = self._patch_frappe_for_check(
            "OB Fixed Asset",
            payload_rows=[
                {"Mã tài sản": "AS001"},
                {"Mã tài sản": "AS002"},
            ],
            master_existing=[],  # no items
        )
        def sql_list(query, params=()):
            if "SELECT DISTINCT file_type" in query:
                return ["OB Fixed Asset"]
            if "tabItem" in query and "is_fixed_asset" in query:
                return []   # no items with is_fixed_asset=1
            return []
        mock_frappe.db.sql_list = sql_list
        # Asset Category count = 1 (warn passes)
        mock_frappe.db.count.return_value = 1
        with patch.object(p, "frappe", mock_frappe):
            r = p.check_phase_0_prerequisites("MM-X", company="DCNET TEST")
        self.assertEqual(r["status"], "block")
        item_check = [c for c in r["checks"]
                      if c["label"] == "Item master (fixed assets)"][0]
        self.assertFalse(item_check["passed"])
        self.assertIn("is_fixed_asset", item_check["issues"][0])
        self.assertIn("Phase 3", item_check["hint"])

    def test_prepaid_no_tk_242_leaf_blocks(self):
        from vn_accounting.misa_migration.importers import phase_0_preflight as p
        mock_frappe = self._patch_frappe_for_check(
            "OB Prepaid Expense",
            payload_rows=[{"Mã CP trả trước": "PP01"}],
            exists=False,  # no TK 242 leaf
        )
        with patch.object(p, "frappe", mock_frappe):
            r = p.check_phase_0_prerequisites("MM-X", company="DCNET TEST")
        self.assertEqual(r["status"], "block")
        chk = [c for c in r["checks"]
               if c["label"] == "TK 242 leaf account"][0]
        self.assertFalse(chk["passed"])
        self.assertIn("coa_leaves bootstrap", chk["hint"])

    def test_prepaid_with_tk_242_leaf_passes(self):
        from vn_accounting.misa_migration.importers import phase_0_preflight as p
        mock_frappe = self._patch_frappe_for_check(
            "OB Prepaid Expense",
            payload_rows=[{"Mã CP trả trước": "PP01"}],
            exists="242 - Chi phí trả trước - DCT",
        )
        with patch.object(p, "frappe", mock_frappe):
            r = p.check_phase_0_prerequisites("MM-X", company="DCNET TEST")
        self.assertEqual(r["status"], "ok")
        chk = [c for c in r["checks"]
               if c["label"] == "TK 242 leaf account"][0]
        self.assertTrue(chk["passed"])

    def test_ccdc_default_category_missing_only_warns(self):
        """CCDC default category missing is WARN not BLOCK because the
        handler auto-creates it."""
        from vn_accounting.misa_migration.importers import phase_0_preflight as p
        mock_frappe = self._patch_frappe_for_check(
            "OB CCDC",
            payload_rows=[{"Mã CCDC": "CC001"}],
            exists=False,
        )
        with patch.object(p, "frappe", mock_frappe):
            r = p.check_phase_0_prerequisites("MM-X", company="DCNET TEST")
        # warn, not block
        self.assertEqual(r["status"], "warn")
        self.assertEqual(r["block_count"], 0)
        chk = r["checks"][0]
        self.assertEqual(chk["level"], "warn")
        self.assertFalse(chk["passed"])

    def test_bank_balance_no_subaccounts_warns(self):
        from vn_accounting.misa_migration.importers import phase_0_preflight as p
        mock_frappe = self._patch_frappe_for_check(
            "OB Bank Balance",
            payload_rows=[{"Số tài khoản": "1121"}],
            count=0,  # no bank sub-accounts
        )
        with patch.object(p, "frappe", mock_frappe):
            r = p.check_phase_0_prerequisites("MM-X", company="DCNET TEST")
        self.assertEqual(r["status"], "warn")
        chk = r["checks"][0]
        self.assertEqual(chk["level"], "warn")
        self.assertFalse(chk["passed"])
        self.assertIn("collapse vào parent", chk["issues"][0])

    def test_employee_advance_missing_is_warn_not_block(self):
        """Employee master missing for TK 141 is WARN — general balance
        fallback can still post the balance even without per-employee
        detail rows."""
        from vn_accounting.misa_migration.importers import phase_0_preflight as p
        mock_frappe = self._patch_frappe_for_check(
            "OB Employee Advance",
            payload_rows=[{"Mã nhân viên": "NV01"}, {"Mã nhân viên": "NV02"}],
            master_existing=[],
        )
        with patch.object(p, "frappe", mock_frappe):
            r = p.check_phase_0_prerequisites("MM-X", company="DCNET TEST")
        # warn, not block
        self.assertEqual(r["status"], "warn")
        chk = [c for c in r["checks"]
               if c["label"] == "Employee master"][0]
        self.assertEqual(chk["level"], "warn")

    def test_no_ob_rows_present_returns_ok(self):
        """When batch has no OB rows at all, checker returns ok with empty list."""
        from vn_accounting.misa_migration.importers import phase_0_preflight as p
        mock_frappe = MagicMock()
        mock_frappe.db.sql_list.return_value = []
        # No file_types present → no checks
        def sql(q, p=(), as_dict=False): return []
        mock_frappe.db.sql = sql
        with patch.object(p, "frappe", mock_frappe):
            r = p.check_phase_0_prerequisites("MM-X", company="DCNET TEST")
        self.assertEqual(r["status"], "ok")
        self.assertEqual(r["checks"], [])
        self.assertEqual(r["block_count"], 0)


if __name__ == "__main__":
    unittest.main()
