"""E2E test for Phase C — Customer import on real Misa file.

Exercises the full pipeline: upload → parse → preview → skip Invalid →
mark_reviewed → post → verify Mã='1986' created → undo → verify gone.

Run via env/bin/python (DO NOT use bench run-tests on dev sites with
sample data — fails per ~/.claude/rules memory).
"""

from __future__ import annotations

import os
import shutil
import unittest

import frappe

from vn_accounting.misa_migration import state as st


class TestPhaseCEndToEnd(unittest.TestCase):
    """Customer file E2E. Item file (2,705 rows) deferred to a slower test."""

    @classmethod
    def setUpClass(cls):
        # Locate real Customer file (deal with trailing-space dir name)
        ROOT = "/home/long/long/frappe-bench-dcnet/docs/accounting-requirements/realdata"
        outer = next(os.path.join(ROOT, d) for d in os.listdir(ROOT)
                     if "danh" in d.lower() and "import" in d.lower())
        inner = next(os.path.join(outer, d) for d in os.listdir(outer)
                     if "danh" in d.lower())
        date_dir = next(os.path.join(inner, d) for d in os.listdir(inner)
                        if d[:5].replace(".", "").isdigit())
        cls._src = os.path.join(date_dir, "Danh_sach_khach_hang.xlsx")
        cls._dst = "/home/long/long/frappe-bench-dcnet/sites/dcnet.localhost/public/files/_test_e2e_phase_c.xlsx"
        shutil.copy(cls._src, cls._dst)

        # Clean prior active batch
        active = st.find_active_batch("DCNET")
        if active:
            frappe.db.set_value("Misa Migration Batch", active, "status", "REVERSED",
                                update_modified=False)
            frappe.db.commit()

        # Ensure target Customer '1986' doesn't pre-exist
        if frappe.db.exists("Customer", "1986"):
            frappe.delete_doc("Customer", "1986", force=True, ignore_permissions=True)
            frappe.db.commit()

    @classmethod
    def tearDownClass(cls):
        if cls._dst and os.path.exists(cls._dst):
            os.unlink(cls._dst)

    def test_full_phase_c_customer_flow(self):
        from vn_accounting.misa_migration.api.upload import create_batch, attach_file
        from vn_accounting.misa_migration.api.parse import start_parse
        from vn_accounting.misa_migration.api.review import mark_reviewed, resolve_row
        from vn_accounting.misa_migration.api.post import start_post
        from vn_accounting.misa_migration.api.undo import start_undo

        b = create_batch(company="DCNET", batch_title="_E2E_PHASE_C_TEST_")
        b = attach_file(batch_name=b["name"], file_url="/files/_test_e2e_phase_c.xlsx",
                        file_type="Customer", original_filename="Danh_sach_khach_hang.xlsx",
                        size_bytes=os.path.getsize(self._dst))
        self.assertEqual(b["status"], "UPLOADED")

        try:
            r = start_parse(batch_name=b["name"], sync=True)
            self.assertEqual(r["status"], "PARSED")
            self.assertGreater(r["total_rows"], 50)  # ~104 customers in file

            # Skip any Invalid rows (Misa file usually has 1 trailing 'Tổng' row)
            invalid_rows = frappe.db.sql_list(
                "SELECT name FROM `tabMisa Migration Row` WHERE batch=%s AND status='Invalid'",
                (b["name"],),
            )
            for row_name in invalid_rows:
                resolve_row(b["name"], row_name, "skip")

            rv = mark_reviewed(b["name"])
            self.assertEqual(rv["status"], "REVIEWED")

            rp = start_post(b["name"], sync=True)
            self.assertEqual(rp["status"], "POSTED")
            self.assertGreater(rp["posted"], 50)

            # Verify '1986' exists with correct fields
            self.assertTrue(frappe.db.exists("Customer", "1986"),
                           "Customer '1986' should be created with doc.name = Misa Mã")
            cust = frappe.db.get_value("Customer", "1986",
                                       ["customer_name", "tax_id"], as_dict=True)
            self.assertIn("1986", cust["customer_name"])
            self.assertEqual(cust["tax_id"], "0108316915")

            # Undo
            ru = start_undo(b["name"], sync=True)
            self.assertEqual(ru["status"], "REVERSED")
            self.assertGreater(ru["reversed"], 50)
            self.assertFalse(frappe.db.exists("Customer", "1986"),
                            "Customer '1986' should be deleted by undo")
        finally:
            frappe.db.set_value("Misa Migration Batch", b["name"], "status", "REVERSED",
                                update_modified=False)
            frappe.db.sql("DELETE FROM `tabMisa Migration Row` WHERE batch=%s", (b["name"],))
            frappe.delete_doc("Misa Migration Batch", b["name"], force=True, ignore_permissions=True)
            frappe.db.commit()


if __name__ == "__main__":
    unittest.main()
