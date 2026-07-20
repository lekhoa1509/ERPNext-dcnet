"""P1.6: Tests for Phase 1 — Foundation Settings DocTypes.

Run via:
    bench --site dcnet.localhost run-tests --app vn_accounting \
        --module vn_accounting.tests.test_phase1_settings
"""
from __future__ import annotations

import unittest

import frappe


class TestSettingsSeed(unittest.TestCase):
    """Idempotency of all 4 seed functions."""

    def test_seed_lcv_allocation_settings_idempotent(self):
        from vn_accounting.landed_cost.seed import seed_lcv_allocation_settings

        seed_lcv_allocation_settings()
        count1 = frappe.db.count("LCV Expense Type Setting", {"parent": "LCV Allocation Settings"})
        seed_lcv_allocation_settings()  # second call must not duplicate
        count2 = frappe.db.count("LCV Expense Type Setting", {"parent": "LCV Allocation Settings"})
        self.assertEqual(count1, count2, "Seed must be idempotent — no duplicates on 2nd call")
        self.assertGreaterEqual(count1, 12, "Must seed at least 12 expense types")

    def test_seed_period_closing_idempotent(self):
        from vn_accounting.period_closing.seed import seed_period_closing_account_settings

        seed_period_closing_account_settings()
        seed_period_closing_account_settings()

    def test_bctc_template_seed_idempotent(self):
        from vn_accounting.financial_reporting.bctc_template_seed import seed_bctc_mapping_templates

        seed_bctc_mapping_templates()
        count1 = frappe.db.count("BCTC Mapping Template")
        seed_bctc_mapping_templates()
        count2 = frappe.db.count("BCTC Mapping Template")
        self.assertEqual(count1, count2, "Template seed must not create duplicates")
        self.assertGreaterEqual(count1, 3, "Must have at least 3 templates (B01/B02/B03 large)")


class TestBCTCTemplateContent(unittest.TestCase):
    """BCTC Mapping Template content correctness."""

    def setUp(self):
        # Ensure templates are seeded before each test
        from vn_accounting.financial_reporting.bctc_template_seed import seed_bctc_mapping_templates
        seed_bctc_mapping_templates()

    def test_bctc_mapping_templates_seeded(self):
        for tmpl in ["vn_large_enterprise_b01", "vn_large_enterprise_b02", "vn_large_enterprise_b03"]:
            self.assertTrue(
                frappe.db.exists("BCTC Mapping Template", tmpl),
                f"Template {tmpl} must exist",
            )

    def test_b01_has_mã_270_and_440(self):
        b01 = frappe.get_doc("BCTC Mapping Template", "vn_large_enterprise_b01")
        codes = [r.code for r in b01.b01_lines]
        self.assertIn("270", codes, "B01 must have mã 270 (Tổng tài sản)")
        self.assertIn("440", codes, "B01 must have mã 440 (Tổng nguồn vốn)")

    def test_b01_has_enough_lines(self):
        b01 = frappe.get_doc("BCTC Mapping Template", "vn_large_enterprise_b01")
        self.assertGreaterEqual(len(b01.b01_lines), 20, "B01 must have ≥20 line mappings")

    def test_b02_has_lines(self):
        b02 = frappe.get_doc("BCTC Mapping Template", "vn_large_enterprise_b02")
        self.assertGreaterEqual(len(b02.b02_lines), 5, "B02 must have ≥5 line mappings")

    def test_b03_has_lines(self):
        b03 = frappe.get_doc("BCTC Mapping Template", "vn_large_enterprise_b03")
        self.assertGreaterEqual(len(b03.b03_lines), 5, "B03 must have ≥5 line mappings")


class TestDocTypeFieldDescriptions(unittest.TestCase):
    """All reqd=1 fields + Link/Select/Currency/Float/Percent must have description ≥10 chars."""

    NEW_DOCTYPES = [
        "LCV Allocation Settings",
        "LCV Expense Type Setting",
        "Manufacturing Costing Settings",
        "BCTC Mapping",
        "BCTC Mapping Template",
        "BCTC Line",
        "Account List Item",
    ]
    TYPES_REQUIRING_DESCRIPTION = {"Link", "Select", "Currency", "Float", "Percent"}

    def test_field_descriptions(self):
        missing = []
        for doctype in self.NEW_DOCTYPES:
            try:
                meta = frappe.get_meta(doctype)
            except Exception as e:
                missing.append(f"{doctype}: could not load meta — {e}")
                continue
            for f in meta.fields:
                needs_desc = f.reqd or f.fieldtype in self.TYPES_REQUIRING_DESCRIPTION
                if needs_desc and f.fieldtype not in ("Section Break", "Column Break", "HTML", "Heading"):
                    if not f.description or len(f.description.strip()) < 10:
                        missing.append(
                            f"{doctype}.{f.fieldname} (reqd={f.reqd}, type={f.fieldtype})"
                        )
        self.assertEqual(
            missing,
            [],
            "Fields missing description (≥10 chars):\n" + "\n".join(missing),
        )


class TestVNAccountingSettingsExtension(unittest.TestCase):
    """VN Accounting Settings extended with Period Closing fields."""

    EXPECTED_FIELDS = [
        "pnl_account_911",
        "retained_earnings_current_year",
        "retained_earnings_prior_year",
        "corporate_income_tax_account",
        "revenue_accounts_to_close",
        "expense_accounts_to_close_periodic",
    ]

    def test_period_closing_fields_exist(self):
        meta = frappe.get_meta("VN Accounting Settings")
        existing = {f.fieldname for f in meta.fields}
        for fieldname in self.EXPECTED_FIELDS:
            self.assertIn(
                fieldname,
                existing,
                f"VN Accounting Settings must have field '{fieldname}'",
            )


if __name__ == "__main__":
    unittest.main()
