"""Unit tests for the Phase 0 Opening Journal handler."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestIsDetailHandled(unittest.TestCase):
    """Verify the prefix-skip table covers expected detail-handled TKs."""

    def test_ar_ap_prefixes_skipped(self):
        """Item 1B-3: only 131 (AR), 331 (AP) detail handlers post to
        matching TKs. 141 was REMOVED from the skip list because the
        employee detail handler silently drops rows when the employee
        master isn't seeded — letting general balance post avoids the
        silent-balance-loss bug."""
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        f = opening_journal._is_detail_handled
        self.assertTrue(f("131"))
        self.assertTrue(f("1311"))
        self.assertTrue(f("331"))

    def test_employee_NOT_skipped(self):
        """Item 1B-3: 141 employee general balance MUST post via general
        because the per-employee detail handler silently drops rows when
        the employee master isn't seeded."""
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        f = opening_journal._is_detail_handled
        self.assertFalse(f("141"))
        self.assertFalse(f("1411"))

    def test_bank_subaccounts_skipped(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        f = opening_journal._is_detail_handled
        self.assertTrue(f("1121"))
        self.assertTrue(f("1121.20"))
        self.assertTrue(f("11210"))

    def test_inventory_NOT_skipped(self):
        """Item 1B-3: Material Receipt SE detail handler posts to the
        item's default stock account via valuation_rate, NOT to the Misa
        TK 1561/1531/etc directly — general balance row IS the source
        of truth for the TB."""
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        f = opening_journal._is_detail_handled
        for tk in ("152", "1521", "153", "155", "156", "1561"):
            with self.subTest(tk=tk):
                self.assertFalse(f(tk))

    def test_fixed_asset_NOT_skipped(self):
        """Item 1B-3: Asset record creation does NOT post GL — opening
        Asset balance requires a separate Manual JE that ERPNext does
        NOT generate automatically. General balance MUST post."""
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        f = opening_journal._is_detail_handled
        for tk in ("211", "213", "2113", "214", "2141"):
            with self.subTest(tk=tk):
                self.assertFalse(f(tk))

    def test_prepaid_skipped(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        f = opening_journal._is_detail_handled
        self.assertTrue(f("242"))
        self.assertTrue(f("2421"))

    def test_cash_general_NOT_skipped(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        f = opening_journal._is_detail_handled
        self.assertFalse(f("111"))   # Cash on hand
        self.assertFalse(f("1111"))
        self.assertFalse(f("411"))   # Equity
        self.assertFalse(f("4211"))
        self.assertFalse(f("334"))   # Salary payable

    def test_empty_returns_false(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        f = opening_journal._is_detail_handled
        self.assertFalse(f(""))
        self.assertFalse(f(None))


class TestBuildGeneralRows(unittest.TestCase):

    def test_skips_group_account_via_account_is_leaf(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        with patch.object(opening_journal, "frappe") as mock_frappe:
            # All TKs resolve to "TK X - DC" but 111 is a group (is_group=1)
            mock_frappe.db.get_value.side_effect = (
                lambda dt, kw, *a, **kw2:
                    "111 - Cash group" if (isinstance(kw, dict) and
                                            kw.get("account_number") == "111")
                    else "1111 - Cash VND" if (isinstance(kw, dict) and
                                                kw.get("account_number") == "1111")
                    else None
            )
            # Override _account_is_leaf to say 111 is group, 1111 is leaf
            with patch.object(opening_journal, "_account_is_leaf",
                              side_effect=lambda n: "group" not in n):
                rows = [
                    {"account_number": "111", "account_name": "Tiền mặt",
                     "dr": 971401947.0, "cr": 0.0},
                    {"account_number": "1111", "account_name": "Tiền VND",
                     "dr": 971401947.0, "cr": 0.0},
                ]
                result = opening_journal._build_general_rows(rows, {}, "DC")
                self.assertEqual(len(result), 1)
                self.assertEqual(result[0]["account"], "1111 - Cash VND")

    def test_skips_detail_handled_prefixes(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        with patch.object(opening_journal, "frappe"), \
             patch.object(opening_journal, "_account_is_leaf", return_value=True):
            rows = [
                {"account_number": "131", "dr": 4_089_355_020, "cr": 1_564_004_140},
                {"account_number": "331", "dr": 0, "cr": 500_000_000},
                {"account_number": "1111", "dr": 100_000_000, "cr": 0},
                {"account_number": "1121.20", "dr": 50_000_000, "cr": 0},
            ]
            with patch.object(opening_journal, "_resolve_account",
                              return_value="ANY"):
                result = opening_journal._build_general_rows(rows, {}, "DC")
                # Only 1111 should remain (131/331/1121.20 are detail-handled)
                self.assertEqual(len(result), 1)
                self.assertEqual(result[0]["debit_in_account_currency"], 100_000_000)

    def test_skips_zero_amount_rows(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        with patch.object(opening_journal, "frappe"), \
             patch.object(opening_journal, "_account_is_leaf", return_value=True), \
             patch.object(opening_journal, "_resolve_account", return_value="X"):
            rows = [{"account_number": "1111", "dr": 0, "cr": 0}]
            self.assertEqual(opening_journal._build_general_rows(rows, {}, "DC"), [])


class TestBuildPartyRows(unittest.TestCase):

    def test_customer_row_carries_party_fields(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        with patch.object(opening_journal, "_resolve_account",
                          return_value="131 - AR - DC"), \
             patch.object(opening_journal, "frappe") as mock_frappe:
            mock_frappe.db.exists.return_value = True
            rows = [{"account_number": "131", "party_code": "BIDVCNCT",
                     "party_name": "Bank BIDV", "dr": 35_200_000, "cr": 0}]
            result = opening_journal._build_party_rows(
                rows, {}, "DC", "Customer", "Customer")
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["party_type"], "Customer")
            self.assertEqual(result[0]["party"], "BIDVCNCT")
            self.assertEqual(result[0]["debit_in_account_currency"], 35_200_000)
            self.assertEqual(result[0]["account"], "131 - AR - DC")

    def test_skips_when_party_master_missing(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        with patch.object(opening_journal, "_resolve_account",
                          return_value="331 - AP - DC"), \
             patch.object(opening_journal, "frappe") as mock_frappe:
            mock_frappe.db.exists.return_value = False  # supplier missing
            rows = [{"account_number": "331", "party_code": "GHOST",
                     "party_name": "Ghost", "dr": 0, "cr": 100_000}]
            self.assertEqual(opening_journal._build_party_rows(
                rows, {}, "DC", "Supplier", "Supplier"), [])

    def test_supplier_credit_row(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        with patch.object(opening_journal, "_resolve_account",
                          return_value="331 - AP - DC"), \
             patch.object(opening_journal, "frappe") as mock_frappe:
            mock_frappe.db.exists.return_value = True
            rows = [{"account_number": "331", "party_code": "VIETTEL",
                     "party_name": "Viettel", "dr": 0, "cr": 50_000_000}]
            result = opening_journal._build_party_rows(
                rows, {}, "DC", "Supplier", "Supplier")
            self.assertEqual(result[0]["credit_in_account_currency"], 50_000_000)
            self.assertEqual(result[0]["debit_in_account_currency"], 0)
            self.assertEqual(result[0]["party_type"], "Supplier")


class TestBuildBankRows(unittest.TestCase):

    def test_each_bank_account_resolved_independently(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        resolved = {"11214": "11214 - SEABANK - DC", "11218": "11218 - VPBANK - DC"}
        # Item 1B-2: _build_bank_rows also calls _account_is_leaf to
        # ensure mapping didn't sneak in a group account. Mock both.
        with patch.object(opening_journal, "_resolve_account",
                          side_effect=lambda tk, m, c: resolved.get(tk)), \
             patch.object(opening_journal, "_account_is_leaf",
                          return_value=True):
            rows = [
                {"bank_no": "000008004970", "bank_name": "SEABANK",
                 "account_number": "11214", "dr": 11_339_937, "cr": 0},
                {"bank_no": "262086313", "bank_name": "VPBANK",
                 "account_number": "11218", "dr": 38_792_955, "cr": 0},
            ]
            result = opening_journal._build_bank_rows(rows, {}, "DC")
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["account"], "11214 - SEABANK - DC")
            self.assertEqual(result[1]["account"], "11218 - VPBANK - DC")


class TestNetAndAggregate(unittest.TestCase):
    """B5 fix: per-row netting + same-(account,party) aggregation."""

    def test_per_row_dr_cr_netted(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        # TK 131 in general file shows BOTH Dr 4089M AND Cr 1564M on same row
        rows = [{
            "account": "131", "debit_in_account_currency": 4_089_355_020,
            "credit_in_account_currency": 1_564_004_140,
            "user_remark": "OB AR 131",
        }]
        out = opening_journal._net_and_aggregate(rows)
        self.assertEqual(len(out), 1)
        # Net Dr = 4089M - 1564M = 2525M
        self.assertEqual(out[0]["debit_in_account_currency"],
                         4_089_355_020 - 1_564_004_140)
        self.assertEqual(out[0]["credit_in_account_currency"], 0.0)

    def test_per_row_cr_larger_than_dr_nets_to_cr(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        rows = [{
            "account": "331", "debit_in_account_currency": 100_000,
            "credit_in_account_currency": 500_000,
        }]
        out = opening_journal._net_and_aggregate(rows)
        self.assertEqual(out[0]["credit_in_account_currency"], 400_000)
        self.assertEqual(out[0]["debit_in_account_currency"], 0.0)

    def test_zero_net_row_dropped(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        rows = [{"account": "X", "debit_in_account_currency": 100,
                 "credit_in_account_currency": 100}]
        out = opening_journal._net_and_aggregate(rows)
        self.assertEqual(out, [])

    def test_aggregates_same_account_no_party(self):
        """TK-collapse fallback: 5111+5112+51131 all → 511. Aggregate net."""
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        rows = [
            {"account": "511 - Doanh thu - DCT",
             "debit_in_account_currency": 0, "credit_in_account_currency": 1_000_000,
             "user_remark": "from 5111"},
            {"account": "511 - Doanh thu - DCT",
             "debit_in_account_currency": 0, "credit_in_account_currency": 500_000,
             "user_remark": "from 5112"},
            {"account": "511 - Doanh thu - DCT",
             "debit_in_account_currency": 200_000, "credit_in_account_currency": 0,
             "user_remark": "from 51131 (returns)"},
        ]
        out = opening_journal._net_and_aggregate(rows)
        self.assertEqual(len(out), 1)
        # Net: Cr 1.5M − Dr 0.2M = Cr 1.3M
        self.assertEqual(out[0]["credit_in_account_currency"], 1_300_000)
        self.assertEqual(out[0]["debit_in_account_currency"], 0.0)
        # User remark merged
        self.assertIn("more", out[0]["user_remark"])

    def test_same_account_different_party_NOT_aggregated(self):
        """Customer/Supplier with same TK 131 but different party stay separate."""
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        rows = [
            {"account": "131 - AR - DCT", "debit_in_account_currency": 100_000,
             "credit_in_account_currency": 0, "party_type": "Customer", "party": "C1"},
            {"account": "131 - AR - DCT", "debit_in_account_currency": 200_000,
             "credit_in_account_currency": 0, "party_type": "Customer", "party": "C2"},
        ]
        out = opening_journal._net_and_aggregate(rows)
        self.assertEqual(len(out), 2)
        parties = {r["party"] for r in out}
        self.assertEqual(parties, {"C1", "C2"})

    def test_combined_per_row_net_then_aggregate(self):
        """Real-world scenario: per-row netting THEN aggregation."""
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        rows = [
            # Row 1: 131 with Dr=Cr=both → nets to Dr 600k
            {"account": "131", "debit_in_account_currency": 1_000_000,
             "credit_in_account_currency": 400_000},
            # Row 2: 131 with Cr 500k
            {"account": "131", "debit_in_account_currency": 0,
             "credit_in_account_currency": 500_000},
        ]
        out = opening_journal._net_and_aggregate(rows)
        self.assertEqual(len(out), 1)
        # Aggregated: Dr 600k (from row 1 after netting) + Cr 500k (row 2)
        # → final net Dr 100k
        self.assertEqual(out[0]["debit_in_account_currency"], 100_000)
        self.assertEqual(out[0]["credit_in_account_currency"], 0.0)


class TestPostOpeningJournal(unittest.TestCase):
    """Top-level post_opening_journal — verifies aggregate JE payload."""

    def test_creates_balanced_je_from_party_rows(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        captured = []

        class MockDoc:
            def __init__(self, payload):
                self.payload = payload
                self.name = payload.get("misa_voucher_no")
                self.flags = type("F", (), {"ignore_permissions": False})()
            def insert(self, set_name=None):
                self.name = set_name or self.name

        def mock_get_doc(payload):
            captured.append(payload)
            return MockDoc(payload)

        with patch.object(opening_journal, "frappe") as mock_frappe, \
             patch.object(opening_journal, "_resolve_account",
                          return_value="131 - AR - DC"), \
             patch.object(opening_journal, "_account_is_leaf", return_value=True), \
             patch.object(opening_journal, "_load_account_mapping", return_value={}):
            mock_frappe.db.exists.return_value = True
            mock_frappe.defaults.get_global_default.return_value = "DC"
            mock_frappe.db.get_value.return_value = None
            mock_frappe.get_doc = mock_get_doc

            customer_rows = [{
                "account_number": "131", "party_code": "C001",
                "party_name": "Cust1", "dr": 100_000, "cr": 0,
            }]
            supplier_rows = [{
                "account_number": "331", "party_code": "S001",
                "party_name": "Sup1", "dr": 0, "cr": 100_000,
            }]
            # Make sure existence check returns True for the JE name check
            mock_frappe.db.exists.side_effect = lambda dt, name: \
                dt != "Journal Entry"
            r = opening_journal.post_opening_journal(
                batch_name="BATCH-X",
                customer_rows=customer_rows,
                supplier_rows=supplier_rows,
            )
            self.assertEqual(r["status"], "created")
            self.assertEqual(r["target_name"], "BATCH-X-OB")
            self.assertEqual(r["row_count"], 2)
            self.assertEqual(r["total_dr"], 100_000)
            self.assertEqual(r["total_cr"], 100_000)

            pl = captured[0]
            self.assertEqual(pl["voucher_type"], "Opening Entry")
            self.assertEqual(pl["is_opening"], "Yes")
            self.assertEqual(pl["posting_date"], "2025-12-31")
            self.assertEqual(len(pl["accounts"]), 2)

    def test_residual_balanced_via_temporary_account(self):
        """Slight Dr/Cr mismatch should land in Temporary Opening or
        TK 4211 fallback."""
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        captured = []
        class MockDoc:
            def __init__(self, payload):
                self.payload = payload
                self.name = payload.get("misa_voucher_no")
                self.flags = type("F", (), {"ignore_permissions": False})()
            def insert(self, set_name=None):
                self.name = set_name or self.name
        with patch.object(opening_journal, "frappe") as mock_frappe, \
             patch.object(opening_journal, "_resolve_account",
                          return_value="X - DC"), \
             patch.object(opening_journal, "_account_is_leaf", return_value=True), \
             patch.object(opening_journal, "_load_account_mapping", return_value={}), \
             patch.object(opening_journal, "_temporary_opening_account",
                          return_value="4211 - LN - DC"):
            mock_frappe.db.exists.side_effect = lambda dt, name: dt != "Journal Entry"
            mock_frappe.defaults.get_global_default.return_value = "DC"
            mock_frappe.get_doc = lambda payload: captured.append(payload) or MockDoc(payload)

            # Dr 100,000 / Cr 99,500 → 500 residual goes to 4211 Cr
            # B5: both rows resolve to "X - DC" via _resolve_account stub,
            # then aggregation nets them → Dr 500. Plus 4211 balancing
            # Cr 500 to balance → total_dr=500, total_cr=500.
            general_rows = [
                {"account_number": "111", "dr": 100_000, "cr": 0},
                {"account_number": "338", "dr": 0, "cr": 99_500},
            ]
            r = opening_journal.post_opening_journal(
                batch_name="BATCH-Y", general_rows=general_rows,
            )
            self.assertEqual(r["status"], "created")
            self.assertEqual(r["total_dr"], 500)
            self.assertEqual(r["total_cr"], 500)
            # Last row is the residual on 4211
            last = captured[0]["accounts"][-1]
            self.assertEqual(last["account"], "4211 - LN - DC")
            self.assertEqual(last["credit_in_account_currency"], 500)

    def test_no_rows_returns_failed(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        with patch.object(opening_journal, "frappe") as mock_frappe:
            mock_frappe.db.exists.return_value = False
            mock_frappe.defaults.get_global_default.return_value = "DC"
            r = opening_journal.post_opening_journal(batch_name="BATCH-Z")
            self.assertEqual(r["status"], "failed")
            self.assertIn("No postable", r["error"])

    def test_idempotency_skipped(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        with patch.object(opening_journal, "frappe") as mock_frappe:
            mock_frappe.db.exists.return_value = True  # JE already exists
            r = opening_journal.post_opening_journal(batch_name="BATCH-X")
            self.assertEqual(r["status"], "skipped")
            self.assertEqual(r["target_name"], "BATCH-X-OB")


if __name__ == "__main__":
    unittest.main()
