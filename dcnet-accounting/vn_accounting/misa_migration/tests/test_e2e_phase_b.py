"""End-to-end test of Phase B pipeline on real Misa master files.

Run via:
  cd <bench>/sites && ../env/bin/python -m unittest \
      apps.vn_accounting.vn_accounting.misa_migration.tests.test_e2e_phase_b -v

OR inline via env/bin/python with frappe.init() (preferred — bench
run-tests fails on dev sites with sample data per memory rule).

This test exercises the full Phase B flow on a small subset (UOM only)
so it stays under 5 seconds. The larger 3-file run is documented in
session-last as a one-shot manual smoke.
"""

from __future__ import annotations

import os
import shutil
import unittest

import frappe

from vn_accounting.misa_migration import state as st


class TestPhaseBEndToEnd(unittest.TestCase):
    """Single-file UOM E2E: upload → parse → preview → review → post → undo."""

    @classmethod
    def setUpClass(cls):
        # Clean up any active DCNet batch from prior runs
        active = st.find_active_batch("DCNET")
        if active:
            frappe.db.set_value("Misa Migration Batch", active, "status", "REVERSED",
                                update_modified=False)
            frappe.db.commit()

        # Copy real UOM file into site public/files
        ROOT = "/home/long/long/frappe-bench-dcnet/docs/accounting-requirements/realdata"
        outer = next(os.path.join(ROOT, d) for d in os.listdir(ROOT)
                     if "danh" in d.lower() and "import" in d.lower())
        inner = next(os.path.join(outer, d) for d in os.listdir(outer)
                     if "danh" in d.lower())
        date_dir = next(os.path.join(inner, d) for d in os.listdir(inner)
                        if d[:5].replace(".", "").isdigit())
        cls._src = os.path.join(date_dir, "Danh_sach_don_vi_tinh.xlsx")
        public_files = "/home/long/long/frappe-bench-dcnet/sites/dcnet.localhost/public/files"
        os.makedirs(public_files, exist_ok=True)
        cls._dst = os.path.join(public_files, "_test_e2e_phase_b_uom.xlsx")
        shutil.copy(cls._src, cls._dst)

    @classmethod
    def tearDownClass(cls):
        if cls._dst and os.path.exists(cls._dst):
            os.unlink(cls._dst)

    def test_full_flow(self):
        from vn_accounting.misa_migration.api.upload import create_batch, attach_file
        from vn_accounting.misa_migration.api.parse import start_parse
        from vn_accounting.misa_migration.api.review import aggregate_counts, mark_reviewed
        from vn_accounting.misa_migration.api.post import preflight, start_post
        from vn_accounting.misa_migration.api.undo import start_undo

        b = create_batch(company="DCNET", batch_title="_E2E_TEST_UOM_")
        self.assertEqual(b["status"], "DRAFT")
        b = attach_file(batch_name=b["name"], file_url="/files/" + os.path.basename(self._dst),
                        file_type="UOM", original_filename=os.path.basename(self._dst),
                        size_bytes=os.path.getsize(self._dst))
        self.assertEqual(b["status"], "UPLOADED")
        try:
            r = start_parse(batch_name=b["name"], sync=True)
            self.assertEqual(r["status"], "PARSED")
            self.assertGreater(r["total_rows"], 0)

            counts = aggregate_counts(b["name"])
            self.assertIn("UOM", counts["counts"])

            r = mark_reviewed(b["name"])
            self.assertEqual(r["status"], "REVIEWED")

            pre = preflight(b["name"])
            self.assertEqual(pre["blocked"], [])
            self.assertGreater(pre["n_ready"], 0)

            r = start_post(b["name"], sync=True)
            self.assertEqual(r["status"], "POSTED")
            self.assertGreater(r["posted"], 0)

            r = start_undo(b["name"], sync=True)
            self.assertEqual(r["status"], "REVERSED")
        finally:
            # cleanup
            frappe.db.set_value("Misa Migration Batch", b["name"], "status", "REVERSED",
                                update_modified=False)
            frappe.db.sql("DELETE FROM `tabMisa Migration Row` WHERE batch=%s", (b["name"],))
            frappe.delete_doc("Misa Migration Batch", b["name"], force=True, ignore_permissions=True)
            frappe.db.commit()


if __name__ == "__main__":
    unittest.main()
