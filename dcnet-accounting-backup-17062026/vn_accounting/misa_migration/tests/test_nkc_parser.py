"""Unit tests for parsers/nkc_parser.py.

Pure-function tests — no Frappe DB. Tests construct row dicts directly in
the shape parse_job._row_to_dict emits.
"""

from __future__ import annotations

import unittest

from vn_accounting.misa_migration.parsers.nkc_parser import (
    BalanceError,
    extract_prefix,
    parse_nkc_rows,
)


def _row(voucher_no, account, debit, credit, **kw):
    """Build an NKC row dict with sensible defaults."""
    d = {
        "Ngày hạch toán": "2026-01-01",
        "Ngày chứng từ": "2026-01-01",
        "Số chứng từ": voucher_no,
        "Ngày hóa đơn": "",
        "Số hóa đơn": "",
        "Mã đối tượng": "",
        "Tên đối tượng": "",
        "Diễn giải chung": "",
        "Diễn giải": "",
        "Tài khoản": account,
        "TK đối ứng": "",
        "Phát sinh Nợ": debit,
        "Phát sinh Có": credit,
    }
    d.update(kw)
    return d


class TestExtractPrefix(unittest.TestCase):
    def test_simple_prefixes(self):
        self.assertEqual(extract_prefix("BC20260001"), "BC")
        self.assertEqual(extract_prefix("BH20260033"), "BH")
        self.assertEqual(extract_prefix("MH20260005"), "MH")
        self.assertEqual(extract_prefix("PN20260002"), "PN")
        self.assertEqual(extract_prefix("PT20260009"), "PT")
        self.assertEqual(extract_prefix("PC20260012"), "PC")
        self.assertEqual(extract_prefix("PX20260007"), "PX")
        self.assertEqual(extract_prefix("KH20260001"), "KH")
        self.assertEqual(extract_prefix("CK20260002"), "CK")

    def test_3char_prefixes(self):
        self.assertEqual(extract_prefix("MDV20260015"), "MDV")
        self.assertEqual(extract_prefix("NVK20260001"), "NVK")
        self.assertEqual(extract_prefix("UNC20260012"), "UNC")

    def test_4char_prefixes_beat_2char(self):
        # PXHN must NOT collapse to PX
        self.assertEqual(extract_prefix("PXHN20260005"), "PXHN")
        # PNHN must NOT collapse to PN
        self.assertEqual(extract_prefix("PNHN20260004"), "PNHN")
        # CTNB must NOT collapse to CT (which doesn't exist anyway)
        self.assertEqual(extract_prefix("CTNB20260008"), "CTNB")
        # PBDT must NOT collapse to PB or PT
        self.assertEqual(extract_prefix("PBDT2026001"), "PBDT")

    def test_5char_prefix(self):
        # PBPTT must NOT collapse to PBPT (not known) or PBP
        self.assertEqual(extract_prefix("PBPTT2026001"), "PBPTT")

    def test_blank_returns_empty(self):
        self.assertEqual(extract_prefix(""), "")
        self.assertEqual(extract_prefix(None), "")
        self.assertEqual(extract_prefix("   "), "")

    def test_unknown_prefix_falls_back_to_alpha_run(self):
        # XYZ is not in KNOWN_PREFIXES but regex fallback extracts "XYZ"
        self.assertEqual(extract_prefix("XYZ123456"), "XYZ")


class TestParseNkcRows(unittest.TestCase):
    def test_two_row_voucher_groups_correctly(self):
        # Real NKC sample: BC20260001 = 2 legs (Dr 11215 / Cr 131)
        rows = [
            _row("BC20260001", "11215", 209000, 0,
                 **{"Mã đối tượng": "PTE.A.1206.1121",
                    "Tên đối tượng": "LÊ THỊ BÍCH TRÂN",
                    "Diễn giải chung": "Thu tiền"}),
            _row("BC20260001", "131", 0, 209000,
                 **{"Mã đối tượng": "PTE.A.1206.1121",
                    "Tên đối tượng": "LÊ THỊ BÍCH TRÂN",
                    "Diễn giải chung": "Thu tiền"}),
        ]
        vouchers = parse_nkc_rows(rows)
        self.assertEqual(len(vouchers), 1)
        v = vouchers[0]
        self.assertEqual(v["voucher_no"], "BC20260001")
        self.assertEqual(v["prefix"], "BC")
        self.assertEqual(v["party_code"], "PTE.A.1206.1121")
        self.assertEqual(v["party_name"], "LÊ THỊ BÍCH TRÂN")
        self.assertEqual(len(v["legs"]), 2)
        self.assertEqual(v["total_dr"], 209000.0)
        self.assertEqual(v["total_cr"], 209000.0)
        self.assertNotIn("balance_error", v)

    def test_groups_two_distinct_vouchers(self):
        rows = [
            _row("BC20260001", "11215", 209000, 0),
            _row("BC20260001", "131", 0, 209000),
            _row("BC20260002", "11215", 1470000, 0),
            _row("BC20260002", "131", 0, 1470000),
        ]
        vouchers = parse_nkc_rows(rows)
        self.assertEqual([v["voucher_no"] for v in vouchers],
                         ["BC20260001", "BC20260002"])
        for v in vouchers:
            self.assertEqual(len(v["legs"]), 2)
            self.assertEqual(v["total_dr"], v["total_cr"])

    def test_8_row_mdv_voucher_keeps_all_legs(self):
        # Real NKC sample: MDV20260002 has 8 rows (4 services × 2 legs)
        rows = [
            _row("MDV20260002", "6322", 18991974, 0),
            _row("MDV20260002", "331", 0, 18991974),
            _row("MDV20260002", "6323", 37983948, 0),
            _row("MDV20260002", "331", 0, 37983948),
            _row("MDV20260002", "6323", 32286356, 0),
            _row("MDV20260002", "331", 0, 32286356),
            _row("MDV20260002", "6323", 50000000, 0),
            _row("MDV20260002", "331", 0, 50000000),
        ]
        vouchers = parse_nkc_rows(rows)
        self.assertEqual(len(vouchers), 1)
        v = vouchers[0]
        self.assertEqual(len(v["legs"]), 8)
        # All Dr 6322/6323, all Cr 331 — no consolidation
        accounts = [l["account"] for l in v["legs"]]
        self.assertEqual(accounts.count("6322"), 1)
        self.assertEqual(accounts.count("6323"), 3)
        self.assertEqual(accounts.count("331"), 4)
        # Balance check passes
        self.assertEqual(v["total_dr"], v["total_cr"])

    def test_tk_doi_ung_column_ignored(self):
        # Spec §5: "TK đối ứng" column is Misa display-only and must be ignored.
        # Even if absurd values are present, output must reflect Tài khoản only.
        rows = [
            _row("BC20260001", "11215", 209000, 0,
                 **{"TK đối ứng": "999999_BOGUS"}),
            _row("BC20260001", "131", 0, 209000,
                 **{"TK đối ứng": "ANOTHER_BOGUS"}),
        ]
        vouchers = parse_nkc_rows(rows)
        accounts = [l["account"] for l in vouchers[0]["legs"]]
        self.assertEqual(accounts, ["11215", "131"])
        # No leg picked up the bogus contra account
        for leg in vouchers[0]["legs"]:
            self.assertNotIn("BOGUS", leg["account"])

    def test_unbalanced_voucher_tags_error_by_default(self):
        rows = [
            _row("BC20260001", "11215", 209000, 0),
            _row("BC20260001", "131", 0, 100000),  # Cr off by 109000
        ]
        vouchers = parse_nkc_rows(rows)
        self.assertEqual(len(vouchers), 1)
        v = vouchers[0]
        self.assertIn("balance_error", v)
        self.assertAlmostEqual(v["total_dr"] - v["total_cr"], 109000.0)

    def test_unbalanced_voucher_raises_when_strict(self):
        rows = [
            _row("BC20260001", "11215", 209000, 0),
            _row("BC20260001", "131", 0, 100000),
        ]
        with self.assertRaises(BalanceError) as cm:
            parse_nkc_rows(rows, raise_on_unbalanced=True)
        self.assertEqual(cm.exception.voucher_no, "BC20260001")

    def test_tolerance_allows_sub_cent_drift(self):
        # 0.001 < 0.01 tolerance — must NOT flag balance_error
        rows = [
            _row("BC20260001", "11215", 209000.005, 0),
            _row("BC20260001", "131", 0, 209000.0),
        ]
        vouchers = parse_nkc_rows(rows)
        self.assertNotIn("balance_error", vouchers[0])

    def test_voucher_remark_and_invoice_metadata(self):
        rows = [
            _row("MDV20260001", "6322", 7649330, 0,
                 **{"Ngày hóa đơn": "2026-01-01",
                    "Số hóa đơn": "3777-HK",
                    "Mã đối tượng": "HE_HURRICANE ELECTRIC",
                    "Tên đối tượng": "HURRICANE ELECTRIC",
                    "Diễn giải chung": "Transit Service Monthly Fee",
                    "Diễn giải": "Transit Service Monthly Fee leg 1"}),
            _row("MDV20260001", "331", 0, 7649330,
                 **{"Ngày hóa đơn": "2026-01-01",
                    "Số hóa đơn": "3777-HK",
                    "Mã đối tượng": "HE_HURRICANE ELECTRIC",
                    "Tên đối tượng": "HURRICANE ELECTRIC",
                    "Diễn giải chung": "Transit Service Monthly Fee",
                    "Diễn giải": "Transit Service Monthly Fee leg 2"}),
        ]
        vouchers = parse_nkc_rows(rows)
        v = vouchers[0]
        self.assertEqual(v["invoice_no"], "3777-HK")
        self.assertEqual(v["invoice_date"], "2026-01-01")
        self.assertEqual(v["voucher_remark"], "Transit Service Monthly Fee")
        self.assertEqual(v["legs"][0]["leg_desc"], "Transit Service Monthly Fee leg 1")
        self.assertEqual(v["legs"][1]["leg_desc"], "Transit Service Monthly Fee leg 2")

    def test_blank_voucher_no_skipped(self):
        rows = [
            _row("BC20260001", "11215", 209000, 0),
            _row("", "999", 100, 100),                    # missing voucher_no
            _row(None, "999", 100, 100),                  # None voucher_no
            _row("BC20260001", "131", 0, 209000),
        ]
        vouchers = parse_nkc_rows(rows)
        self.assertEqual(len(vouchers), 1)
        self.assertEqual(len(vouchers[0]["legs"]), 2)

    def test_numeric_string_amounts(self):
        # parse_job emits strings sometimes; ensure _to_float coerces
        rows = [
            _row("BC20260001", "11215", "209000", "0"),
            _row("BC20260001", "131", "0", "209000"),
        ]
        vouchers = parse_nkc_rows(rows)
        self.assertEqual(vouchers[0]["total_dr"], 209000.0)
        self.assertEqual(vouchers[0]["total_cr"], 209000.0)

    def test_comma_separator_amounts(self):
        # Some Misa exports may have "1,234,567" — strip
        rows = [
            _row("BC20260001", "11215", "1,470,000", "0"),
            _row("BC20260001", "131", "0", "1,470,000"),
        ]
        vouchers = parse_nkc_rows(rows)
        self.assertEqual(vouchers[0]["total_dr"], 1470000.0)

    def test_row_indices_preserved(self):
        rows = [
            _row("BC20260001", "11215", 209000, 0),
            _row("BC20260002", "11215", 100000, 0),
            _row("BC20260001", "131", 0, 209000),
            _row("BC20260002", "131", 0, 100000),
        ]
        vouchers = parse_nkc_rows(rows)
        # Order of first-seen
        self.assertEqual(vouchers[0]["voucher_no"], "BC20260001")
        self.assertEqual(vouchers[0]["row_indices"], [1, 3])
        self.assertEqual(vouchers[1]["voucher_no"], "BC20260002")
        self.assertEqual(vouchers[1]["row_indices"], [2, 4])


if __name__ == "__main__":
    unittest.main()
