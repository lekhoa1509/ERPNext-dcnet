"""Unit tests for importers/voucher_router.py.

Tests the registry + dispatcher independently of handler implementations.
"""

from __future__ import annotations

import unittest

from vn_accounting.misa_migration.importers.voucher_router import (
    HANDLER_TARGET_DOCTYPE,
    PREFIX_HANDLERS,
    get_handler_spec,
    get_target_doctype,
    is_supported_prefix,
    list_handler_modules,
    list_supported_prefixes,
    route_voucher,
)


class TestRegistry(unittest.TestCase):
    def test_all_17_prefixes_registered(self):
        # Spec §2.2 — 17 prefixes
        expected = {
            "BH", "MDV", "MH", "PN", "PNHN", "PX", "PXHN",
            "BC", "UNC", "PT", "PC",
            "CTNB", "NVK", "PBDT", "PBPTT", "KH", "CK",
        }
        self.assertEqual(set(PREFIX_HANDLERS.keys()), expected)

    def test_handler_modules_are_6(self):
        # 6 modules cover 17 prefixes (PI split into purchase_invoice + purchase_receipt)
        mods = set(m for m, _ in PREFIX_HANDLERS.values())
        self.assertEqual(mods, {
            "sales_invoice", "purchase_invoice", "purchase_receipt",
            "stock_entry", "payment_entry", "journal_entry",
        })

    def test_payment_prefixes_share_module(self):
        for p in ["BC", "UNC", "PT", "PC"]:
            self.assertEqual(PREFIX_HANDLERS[p][0], "payment_entry")

    def test_je_prefixes_share_module(self):
        for p in ["CTNB", "NVK", "PBDT", "PBPTT", "KH", "CK"]:
            self.assertEqual(PREFIX_HANDLERS[p][0], "journal_entry")

    def test_stock_prefixes(self):
        for p in ["PX", "PXHN", "PNHN"]:
            self.assertEqual(PREFIX_HANDLERS[p][0], "stock_entry")

    def test_pi_split(self):
        # MDV/MH → purchase_invoice; PN → purchase_receipt (separate handler)
        self.assertEqual(PREFIX_HANDLERS["MDV"][0], "purchase_invoice")
        self.assertEqual(PREFIX_HANDLERS["MH"][0], "purchase_invoice")
        self.assertEqual(PREFIX_HANDLERS["PN"][0], "purchase_receipt")

    def test_target_doctype_map_covers_modules(self):
        # Every handler module must have a target doctype
        mods = set(m for m, _ in PREFIX_HANDLERS.values())
        self.assertEqual(mods, set(HANDLER_TARGET_DOCTYPE.keys()))


class TestQueryAPI(unittest.TestCase):
    def test_is_supported_prefix(self):
        self.assertTrue(is_supported_prefix("BH"))
        self.assertTrue(is_supported_prefix("PBPTT"))
        self.assertFalse(is_supported_prefix("XYZ"))
        self.assertFalse(is_supported_prefix(""))

    def test_get_handler_spec(self):
        self.assertEqual(get_handler_spec("UNC"), ("payment_entry", "create_pe_from_unc"))
        self.assertIsNone(get_handler_spec("XYZ"))

    def test_get_target_doctype(self):
        self.assertEqual(get_target_doctype("BH"), "Sales Invoice")
        self.assertEqual(get_target_doctype("MDV"), "Purchase Invoice")
        self.assertEqual(get_target_doctype("PN"), "Purchase Invoice")  # PR is a sibling
        self.assertEqual(get_target_doctype("PXHN"), "Stock Entry")
        self.assertEqual(get_target_doctype("UNC"), "Payment Entry")
        self.assertEqual(get_target_doctype("PBDT"), "Journal Entry")
        self.assertIsNone(get_target_doctype("XYZ"))

    def test_list_supported_prefixes_sorted(self):
        prefixes = list_supported_prefixes()
        self.assertEqual(len(prefixes), 17)
        self.assertEqual(prefixes, sorted(prefixes))

    def test_list_handler_modules(self):
        # 6 distinct module names
        mods = list_handler_modules()
        self.assertEqual(len(mods), 6)
        self.assertIn("sales_invoice", mods)
        self.assertIn("journal_entry", mods)


class TestDispatch(unittest.TestCase):
    def test_unsupported_prefix(self):
        v = {"voucher_no": "ZZZ123", "prefix": "ZZZ"}
        r = route_voucher(v)
        self.assertEqual(r["status"], "unsupported_prefix")
        self.assertEqual(r["voucher_no"], "ZZZ123")
        self.assertIn("ZZZ", r["error"])
        self.assertIsNone(r["target_doctype"])

    def test_blank_prefix(self):
        v = {"voucher_no": "12345", "prefix": ""}
        r = route_voucher(v)
        self.assertEqual(r["status"], "unsupported_prefix")

    def test_dry_run_doesnt_invoke_handler(self):
        # Handler modules don't exist yet — dry_run must still succeed for all known prefixes.
        for prefix in list_supported_prefixes():
            v = {"voucher_no": f"{prefix}20260001", "prefix": prefix}
            r = route_voucher(v, dry_run=True)
            self.assertEqual(r["status"], "would_dispatch",
                             f"dry_run for {prefix} got {r}")
            self.assertEqual(r["prefix"], prefix)
            self.assertIsNotNone(r["target_doctype"])
            self.assertIn(".", r["handler"])

    def test_all_handlers_resolve_post_c12(self):
        # Post-C12: every prefix in PREFIX_HANDLERS has its module +
        # function on disk. dry_run reports 'would_dispatch' for each;
        # no prefix should return 'handler_missing' anymore.
        from vn_accounting.misa_migration.importers.voucher_router import (
            PREFIX_HANDLERS,
            _resolve_handler,
        )
        for prefix, (module_name, func_name) in PREFIX_HANDLERS.items():
            fn = _resolve_handler(module_name, func_name)
            self.assertIsNotNone(
                fn,
                f"Prefix {prefix!r} → {module_name}.{func_name} did not resolve",
            )

    def test_target_doctype_populated_on_supported_prefix(self):
        v = {"voucher_no": "BC20260001", "prefix": "BC"}
        r = route_voucher(v, dry_run=True)
        self.assertEqual(r["target_doctype"], "Payment Entry")


if __name__ == "__main__":
    unittest.main()
