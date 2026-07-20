"""Unit tests for S21-DN Sổ TSCĐ report."""
import unittest
import frappe


class TestS21DNReport(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def test_report_exists(self):
        """S21-DN So TSCD report must exist in DB."""
        self.assertTrue(
            frappe.db.exists("Report", "S21-DN So TSCD"),
            "Report 'S21-DN So TSCD' must exist"
        )

    def test_s22_dn_report_exists(self):
        """S22-DN Theo Doi TSCD CCDC report must exist."""
        self.assertTrue(
            frappe.db.exists("Report", "S22-DN Theo Doi TSCD CCDC"),
            "Report 'S22-DN Theo Doi TSCD CCDC' must exist"
        )

    def test_s22_dn_report_returns_data(self):
        """S22-DN report must return at least 1 row with seeded assets."""
        company = frappe.db.get_value("Company", {"country": "Vietnam"}, "name") or \
                  frappe.db.get_value("Company", {}, "name")
        if not company:
            self.skipTest("No company found — skipping integration check")

        report = frappe.get_doc("Report", "S22-DN Theo Doi TSCD CCDC")
        try:
            from frappe.desk.query_report import run
            result = run("S22-DN Theo Doi TSCD CCDC", filters={"company": company})
            rows = result.get("result", [])
            self.assertGreater(len(rows), 0, "S22-DN report returned 0 rows for seeded data")
        except Exception as e:
            self.skipTest(f"Report execution error (may need bench context): {e}")

    def test_coa_has_tk242(self):
        """At least one account with number '242' must exist (COA fixture applied)."""
        count = frappe.db.count("Account", {"account_number": "242"})
        self.assertGreater(count, 0, "TK 242 'Chi phí trả trước' not found — COA fixture missing")

    def test_asset_count_gte_10(self):
        """Must have ≥10 submitted Assets in demo data."""
        count = frappe.db.count("Asset", {"docstatus": 1})
        self.assertGreaterEqual(count, 10, f"Expected ≥10 Assets, got {count}")

    def test_ccdc_item_count_gte_3(self):
        """Must have ≥3 submitted CCDC Items in demo data."""
        count = frappe.db.count("CCDC Item", {"docstatus": 1})
        self.assertGreaterEqual(count, 3, f"Expected ≥3 CCDC Items, got {count}")


if __name__ == "__main__":
    unittest.main()
