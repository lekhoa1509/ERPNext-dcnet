"""Unit tests for the Phase 0 orchestrator (OB dispatch)."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestDictPayloadsToXlsxShape(unittest.TestCase):

    def test_account_balance_shape(self):
        from vn_accounting.misa_migration.importers.phase_0_orchestrator \
            import _dict_payloads_to_xlsx_shape
        dicts = [
            {"STT": "1", "Số tài khoản": "111", "Tên tài khoản": "Cash",
             "Dư Nợ": 100, "Dư Có": 0},
        ]
        out = _dict_payloads_to_xlsx_shape("OB Account Balance", dicts)
        # row 0 = title, row 1 = blank, row 2 = header, row 3+ = data
        self.assertEqual(out[0][0], "OB Account Balance")
        self.assertEqual(out[2][1], "Số tài khoản")
        self.assertEqual(out[3][1], "111")
        self.assertEqual(out[3][3], 100)

    def test_inventory_uses_4_row_header_padding(self):
        from vn_accounting.misa_migration.importers.phase_0_orchestrator \
            import _dict_payloads_to_xlsx_shape
        dicts = [{"Mã hàng": "X", "Số lượng tồn": 5}]
        out = _dict_payloads_to_xlsx_shape("OB Inventory", dicts)
        # Inventory parser walks rows[4:] → need 4 pre-data rows
        # row 0 title, row 1 blank, row 2 blank, row 3 header, row 4 data
        self.assertEqual(out[3][3], "Mã hàng")  # header at row 3
        self.assertEqual(out[4][3], "X")  # first data row

    def test_unknown_file_type_returns_empty(self):
        from vn_accounting.misa_migration.importers.phase_0_orchestrator \
            import _dict_payloads_to_xlsx_shape
        self.assertEqual(_dict_payloads_to_xlsx_shape("UNKNOWN", [{}]), [])


class TestLoadPhase0Rows(unittest.TestCase):

    def test_loads_and_groups_by_file_type(self):
        from vn_accounting.misa_migration.importers import phase_0_orchestrator
        with patch.object(phase_0_orchestrator, "frappe") as mock_frappe:
            mock_frappe.db.sql.return_value = [
                {"name": "R1", "file_type": "OB Account Balance",
                 "raw_payload": '{"Số tài khoản": "111", "Dư Nợ": 100}'},
                {"name": "R2", "file_type": "OB Account Balance",
                 "raw_payload": '{"Số tài khoản": "112", "Dư Nợ": 200}'},
                {"name": "R3", "file_type": "OB Customer AR",
                 "raw_payload": '{"Mã khách hàng": "C1", "Dư Nợ": 50}'},
            ]
            result = phase_0_orchestrator._load_phase_0_rows("BATCH-X")
            self.assertEqual(set(result.keys()),
                             {"OB Account Balance", "OB Customer AR"})
            self.assertEqual(len(result["OB Account Balance"]), 2)
            self.assertEqual(result["OB Customer AR"][0][1]["Mã khách hàng"], "C1")

    def test_invalid_json_row_skipped(self):
        from vn_accounting.misa_migration.importers import phase_0_orchestrator
        with patch.object(phase_0_orchestrator, "frappe") as mock_frappe:
            mock_frappe.db.sql.return_value = [
                {"name": "R1", "file_type": "OB Account Balance",
                 "raw_payload": "not valid json{"},
                {"name": "R2", "file_type": "OB Account Balance",
                 "raw_payload": '{"Số tài khoản": "111"}'},
            ]
            result = phase_0_orchestrator._load_phase_0_rows("BATCH-X")
            self.assertEqual(len(result["OB Account Balance"]), 1)


class TestRunPhase0Post(unittest.TestCase):

    def test_no_phase_0_data_returns_zero(self):
        from vn_accounting.misa_migration.importers import phase_0_orchestrator
        with patch.object(phase_0_orchestrator, "_load_phase_0_rows", return_value={}):
            r = phase_0_orchestrator.run_phase_0_post("BATCH-X")
            self.assertEqual(r["total_rows"], 0)
            self.assertIn("no Phase 0 data", r["skipped"])

    def test_dispatches_all_4_handler_categories(self):
        from vn_accounting.misa_migration.importers import phase_0_orchestrator
        with patch.object(phase_0_orchestrator, "_load_phase_0_rows") as mock_load, \
             patch.object(phase_0_orchestrator, "frappe") as mock_frappe, \
             patch.object(phase_0_orchestrator, "post_opening_journal") as mock_je, \
             patch.object(phase_0_orchestrator, "post_opening_inventory") as mock_inv, \
             patch.object(phase_0_orchestrator, "post_opening_assets") as mock_assets:
            # 3 file_types: 1 JE-bound, 1 inventory, 1 FA
            mock_load.return_value = {
                "OB Account Balance": [("R1", {"STT": "1", "Số tài khoản": "111",
                                                "Tên tài khoản": "Cash",
                                                "Dư Nợ": 100, "Dư Có": 0})],
                "OB Inventory": [("R2", {"STT": "1", "Mã hàng": "X",
                                          "Số lượng tồn": 5, "Đơn giá": 100,
                                          "Mã kho": "KHO"})],
                "OB Fixed Asset": [("R3", {"STT": "1", "Mã tài sản": "A1",
                                            "Tên tài sản": "Asset 1",
                                            "Nguyên giá": 1000,
                                            "Thời gian SD (tháng)": 36})],
            }
            mock_je.return_value = {"status": "created", "target_name": "X-OB"}
            mock_inv.return_value = {"status": "created", "created_names": ["X-OB-INV"]}
            mock_assets.return_value = {"status": "created", "created_names": ["A1"]}

            r = phase_0_orchestrator.run_phase_0_post("BATCH-X")
            self.assertEqual(r["total_rows"], 3)
            self.assertEqual(r["opening_journal"]["status"], "created")
            self.assertEqual(r["opening_inventory"]["status"], "created")
            self.assertEqual(r["opening_fa"]["status"], "created")
            # post_opening_assets called for FA (is_ccdc=False)
            args_list = mock_assets.call_args_list
            # 2 calls: once for FA, once for CCDC (empty rows for CCDC)
            self.assertEqual(len(args_list), 2)
            # Verify first call is_ccdc=False
            self.assertFalse(args_list[0].kwargs.get("is_ccdc", False))
            self.assertTrue(args_list[1].kwargs.get("is_ccdc", False))

    def test_updates_row_status_on_je_success(self):
        from vn_accounting.misa_migration.importers import phase_0_orchestrator
        with patch.object(phase_0_orchestrator, "_load_phase_0_rows") as mock_load, \
             patch.object(phase_0_orchestrator, "frappe") as mock_frappe, \
             patch.object(phase_0_orchestrator, "post_opening_journal") as mock_je, \
             patch.object(phase_0_orchestrator, "post_opening_inventory",
                          return_value={"status": "failed"}), \
             patch.object(phase_0_orchestrator, "post_opening_assets",
                          return_value={"status": "failed"}):
            mock_load.return_value = {
                "OB Customer AR": [("R1", {"STT": "1", "Số tài khoản": "131",
                                            "Mã khách hàng": "C1",
                                            "Tên khách hàng": "Cust 1",
                                            "Dư Nợ": 100, "Dư Có": 0})],
            }
            mock_je.return_value = {"status": "created", "target_name": "X-OB"}

            phase_0_orchestrator.run_phase_0_post("BATCH-X")
            # SQL UPDATE called for each JE-bound file_type with Posted status
            update_calls = [c for c in mock_frappe.db.sql.call_args_list
                            if "UPDATE" in str(c[0][0]).upper()]
            self.assertGreaterEqual(len(update_calls), 1)
            # First arg of one of the calls should have "Posted" in args
            posted_calls = [
                c for c in update_calls
                if any("Posted" in str(a) for a in c[0][1])
            ]
            self.assertGreater(len(posted_calls), 0)


if __name__ == "__main__":
    unittest.main()
