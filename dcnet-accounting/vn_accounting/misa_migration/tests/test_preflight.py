"""Unit tests for Phase D pre-flight validation (10 checks)."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestCheckNkcBalance(unittest.TestCase):

    def test_no_balance_errors_passes(self):
        from vn_accounting.misa_migration.importers.preflight import check_nkc_balance
        vouchers = [
            {"voucher_no": "BH20260001", "balance_error": None},
            {"voucher_no": "MDV20260001"},  # no key → ok
        ]
        r = check_nkc_balance(vouchers)
        self.assertTrue(r["passed"])
        self.assertEqual(r["issues"], [])
        self.assertEqual(r["level"], "block")

    def test_balance_errors_collected(self):
        from vn_accounting.misa_migration.importers.preflight import check_nkc_balance
        vouchers = [
            {"voucher_no": "BH20260001", "balance_error": "Dr=100 Cr=99"},
            {"voucher_no": "BH20260002"},
            {"voucher_no": "NVK20260001", "balance_error": "Dr=50 Cr=0"},
        ]
        r = check_nkc_balance(vouchers)
        self.assertFalse(r["passed"])
        self.assertEqual(len(r["issues"]), 2)
        self.assertIn("BH20260001", r["issues"][0])
        self.assertIn("NVK20260001", r["issues"][1])


class TestCheckBhHasBrMatch(unittest.TestCase):

    def test_all_bh_matched_passes(self):
        from vn_accounting.misa_migration.importers.preflight import check_bh_has_br_match
        vouchers = [
            {"voucher_no": "BH20260001", "prefix": "BH"},
            {"voucher_no": "BH20260002", "prefix": "BH"},
            {"voucher_no": "MDV20260001", "prefix": "MDV"},  # not BH, ignored
        ]
        br = {"BH20260001": {}, "BH20260002": {}}
        r = check_bh_has_br_match(vouchers, br)
        self.assertTrue(r["passed"])
        self.assertEqual(r["level"], "warn")

    def test_missing_bh_match_yields_warn(self):
        from vn_accounting.misa_migration.importers.preflight import check_bh_has_br_match
        vouchers = [
            {"voucher_no": "BH20260001", "prefix": "BH"},
            {"voucher_no": "BH20260002", "prefix": "BH"},  # no BR
        ]
        br = {"BH20260001": {}}
        r = check_bh_has_br_match(vouchers, br)
        self.assertFalse(r["passed"])
        self.assertEqual(len(r["issues"]), 1)
        self.assertIn("BH20260002", r["issues"][0])


class TestCheckMvNeededMatch(unittest.TestCase):

    def test_mdv_mh_pn_each_checked(self):
        from vn_accounting.misa_migration.importers.preflight import check_mdv_mh_pn_has_mv_match
        vouchers = [
            {"voucher_no": "MDV1", "prefix": "MDV"},
            {"voucher_no": "MH1", "prefix": "MH"},
            {"voucher_no": "PN1", "prefix": "PN"},
            {"voucher_no": "BC1", "prefix": "BC"},  # not in MV-needed
        ]
        mv = {"MDV1": {}, "MH1": {}}  # PN1 missing
        r = check_mdv_mh_pn_has_mv_match(vouchers, mv)
        self.assertFalse(r["passed"])
        self.assertEqual(len(r["issues"]), 1)
        self.assertIn("PN1", r["issues"][0])


class TestCheckPartyCodeUniqueness(unittest.TestCase):

    def test_unique_party_codes_pass(self):
        from vn_accounting.misa_migration.importers.preflight import check_party_code_uniqueness
        vouchers = [
            {"party_code": "VIETTEL",
             "legs": [{"account": "331"}, {"account": "1121"}]},
            {"party_code": "1986",
             "legs": [{"account": "131"}, {"account": "511"}]},
        ]
        r = check_party_code_uniqueness(vouchers)
        self.assertTrue(r["passed"])

    def test_ambiguous_party_flagged_as_warn(self):
        from vn_accounting.misa_migration.importers.preflight import check_party_code_uniqueness
        vouchers = [
            {"party_code": "MIXED",
             "legs": [{"account": "131"}, {"account": "5111"}]},
            {"party_code": "MIXED",
             "legs": [{"account": "331"}, {"account": "6427"}]},
        ]
        r = check_party_code_uniqueness(vouchers)
        self.assertFalse(r["passed"])
        self.assertEqual(r["level"], "warn")
        self.assertIn("MIXED", r["issues"][0])


class TestCheckTkMapping(unittest.TestCase):

    def test_all_tks_mapped_passes(self):
        from vn_accounting.misa_migration.importers import preflight
        with patch.object(preflight, "frappe") as mock_frappe:
            mock_frappe.db.get_value.return_value = None
            vouchers = [{"legs": [{"account": "111"}, {"account": "131"}]}]
            mapping = {"111": "111 - Cash - DC", "131": "131 - AR - DC"}
            r = preflight.check_tk_mapping(vouchers, "DC", mapping)
            self.assertTrue(r["passed"])

    def test_unmapped_tk_blocks(self):
        from vn_accounting.misa_migration.importers import preflight
        with patch.object(preflight, "frappe") as mock_frappe:
            mock_frappe.db.get_value.return_value = None
            vouchers = [{"legs": [{"account": "999"}, {"account": "131"}]}]
            mapping = {"131": "131 - AR - DC"}
            r = preflight.check_tk_mapping(vouchers, "DC", mapping)
            self.assertFalse(r["passed"])
            self.assertEqual(r["level"], "block")
            self.assertIn("TK 999", r["issues"][0])

    def test_live_lookup_falls_back(self):
        from vn_accounting.misa_migration.importers import preflight
        with patch.object(preflight, "frappe") as mock_frappe:
            mock_frappe.db.get_value.return_value = "511 - Income - DC"
            vouchers = [{"legs": [{"account": "511"}]}]
            r = preflight.check_tk_mapping(vouchers, "DC", {})
            self.assertTrue(r["passed"])


class TestCheckCompanyVndDefault(unittest.TestCase):

    def test_vnd_passes(self):
        from vn_accounting.misa_migration.importers import preflight
        with patch.object(preflight, "frappe") as mock_frappe:
            mock_frappe.db.get_value.return_value = "VND"
            r = preflight.check_company_vnd_default("DC")
            self.assertTrue(r["passed"])

    def test_non_vnd_blocks(self):
        from vn_accounting.misa_migration.importers import preflight
        with patch.object(preflight, "frappe") as mock_frappe:
            mock_frappe.db.get_value.return_value = "USD"
            r = preflight.check_company_vnd_default("DC")
            self.assertFalse(r["passed"])
            self.assertEqual(r["level"], "block")
            self.assertIn("USD", r["issues"][0])


class TestCheckNoExistingPosted(unittest.TestCase):

    def test_no_existing_passes(self):
        from vn_accounting.misa_migration.importers import preflight
        with patch.object(preflight, "frappe") as mock_frappe:
            mock_frappe.db.sql.return_value = []
            vouchers = [{"voucher_no": "BH20260001"},
                        {"voucher_no": "MDV20260001"}]
            r = preflight.check_no_existing_posted(vouchers)
            self.assertTrue(r["passed"])

    def test_existing_si_blocks(self):
        from vn_accounting.misa_migration.importers import preflight
        with patch.object(preflight, "frappe") as mock_frappe:
            def sql_side_effect(query, args, as_dict=False):
                # First call (Sales Invoice) returns 1 hit; others empty
                if "tabSales Invoice" in query:
                    return [{"name": "BH20260001", "docstatus": 1}]
                return []
            mock_frappe.db.sql = sql_side_effect
            vouchers = [{"voucher_no": "BH20260001"}]
            r = preflight.check_no_existing_posted(vouchers)
            self.assertFalse(r["passed"])
            self.assertEqual(r["level"], "block")
            self.assertIn("Sales Invoice BH20260001", r["issues"][0])


class TestCheckSupplierMasterPresent(unittest.TestCase):

    def test_all_masters_present_passes(self):
        from vn_accounting.misa_migration.importers import preflight
        with patch.object(preflight, "frappe") as mock_frappe:
            mock_frappe.db.exists.return_value = True
            vouchers = [
                {"prefix": "MDV", "party_code": "VIETTEL"},
                {"prefix": "BH", "party_code": "1986"},
            ]
            r = preflight.check_supplier_master_present(vouchers)
            self.assertTrue(r["passed"])

    def test_missing_supplier_blocks(self):
        from vn_accounting.misa_migration.importers import preflight
        with patch.object(preflight, "frappe") as mock_frappe:
            existence = {
                ("Supplier", "VIETTEL"): True,
                ("Customer", "1986"): True,
            }
            mock_frappe.db.exists.side_effect = lambda dt, name: \
                existence.get((dt, name), False)
            vouchers = [
                {"prefix": "MDV", "party_code": "VIETTEL"},  # ok
                {"prefix": "MDV", "party_code": "GHOST_SUP"},  # missing
                {"prefix": "BH", "party_code": "1986"},  # ok
                {"prefix": "BH", "party_code": "GHOST_CUS"},  # missing
            ]
            r = preflight.check_supplier_master_present(vouchers)
            self.assertFalse(r["passed"])
            self.assertEqual(r["level"], "block")
            # 1 supplier + 1 customer missing
            self.assertEqual(len(r["issues"]), 2)


class TestRunPreflightOrchestrator(unittest.TestCase):
    """Smoke-test the orchestrator aggregates correctly."""

    def test_all_ok_status(self):
        from vn_accounting.misa_migration.importers import preflight
        with patch.object(preflight, "frappe") as mock_frappe:
            mock_frappe.defaults.get_global_default.return_value = "DC"
            mock_frappe.db.get_value.return_value = "VND"
            mock_frappe.db.get_single = MagicMock(
                return_value=type("X", (), {"mappings": '{"111":"111-Cash"}'})()
            )
            mock_frappe.db.sql.return_value = []
            mock_frappe.db.exists.return_value = True

            r = preflight.run_preflight(
                vouchers=[],
                br_invoices={},
                mv_invoices={},
                company="DC",
            )
            self.assertEqual(r["status"], "ok")
            self.assertEqual(r["block_count"], 0)
            self.assertEqual(r["warn_count"], 0)
            # At least 9 checks ran (10 with company-conditional ones)
            self.assertGreaterEqual(len(r["checks"]), 9)

    def test_block_status_when_balance_fails(self):
        from vn_accounting.misa_migration.importers import preflight
        with patch.object(preflight, "frappe") as mock_frappe:
            mock_frappe.defaults.get_global_default.return_value = "DC"
            mock_frappe.db.get_value.return_value = "VND"
            mock_frappe.db.get_single = MagicMock(
                return_value=type("X", (), {"mappings": "{}"})()
            )
            mock_frappe.db.sql.return_value = []
            mock_frappe.db.exists.return_value = True

            vouchers = [
                {"voucher_no": "BH1", "prefix": "BH",
                 "balance_error": "Dr=100 Cr=99", "legs": [], "party_code": ""},
            ]
            r = preflight.run_preflight(
                vouchers=vouchers, br_invoices={"BH1": {}},
                mv_invoices={}, company="DC",
            )
            self.assertEqual(r["status"], "block")
            self.assertGreaterEqual(r["block_count"], 1)

    def test_warn_status_when_only_warn_fails(self):
        from vn_accounting.misa_migration.importers import preflight
        with patch.object(preflight, "frappe") as mock_frappe:
            mock_frappe.defaults.get_global_default.return_value = "DC"
            mock_frappe.db.get_value.return_value = "VND"
            mock_frappe.db.get_single = MagicMock(
                return_value=type("X", (), {"mappings": "{}"})()
            )
            mock_frappe.db.sql.return_value = []
            mock_frappe.db.exists.return_value = True

            vouchers = [
                {"voucher_no": "BH1", "prefix": "BH",
                 "legs": [], "party_code": ""},  # BR missing → warn
            ]
            r = preflight.run_preflight(
                vouchers=vouchers, br_invoices={},  # no BR for BH1
                mv_invoices={}, company="DC",
            )
            self.assertEqual(r["status"], "warn")
            self.assertEqual(r["block_count"], 0)
            self.assertGreaterEqual(r["warn_count"], 1)

    def test_check_order_stable(self):
        """Cosmetic: same order of checks every call."""
        from vn_accounting.misa_migration.importers import preflight
        with patch.object(preflight, "frappe") as mock_frappe:
            mock_frappe.defaults.get_global_default.return_value = "DC"
            mock_frappe.db.get_value.return_value = "VND"
            mock_frappe.db.get_single = MagicMock(
                return_value=type("X", (), {"mappings": "{}"})()
            )
            mock_frappe.db.sql.return_value = []
            mock_frappe.db.exists.return_value = True

            r1 = preflight.run_preflight([], {}, {}, "DC")
            r2 = preflight.run_preflight([], {}, {}, "DC")
            names1 = [c["name"] for c in r1["checks"]]
            names2 = [c["name"] for c in r2["checks"]]
            self.assertEqual(names1, names2)
            # nkc_balance first
            self.assertEqual(names1[0], "nkc_balance")


if __name__ == "__main__":
    unittest.main()
