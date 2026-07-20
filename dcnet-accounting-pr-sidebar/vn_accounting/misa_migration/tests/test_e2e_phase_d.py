"""End-to-end Phase D test: full T1/2026 import.

Skipped by default — gated by env var `MISA_E2E=1`. Requires:

  * Phase 1+2+3 already imported on this site (Account mapping populated,
    Customer/Supplier/Employee/Item masters loaded).
  * Company VND, posting period not locked.
  * NKC + bảng kê BR + bảng kê MV files at
    docs/accounting-requirements/realdata/.

Run with:
  cd <bench> && MISA_E2E=1 ../env/bin/python -m unittest \\
    vn_accounting.misa_migration.tests.test_e2e_phase_d

Expected counts (T1/2026):
  * 303 Sales Invoice (BH prefix)
  * ~531 Purchase Invoice (526 MDV + 5 MH from non-PN paths)
  * ~36 PN → PI with update_stock=1 (NKC count, spec says 40)
  * 544 Payment Entry (236 BC + 220 UNC + 15 PT + 73 PC)
  * ~73 Journal Entry (38 CTNB + 31 NVK + 1 CK + 1 PBDT + 1 PBPTT + 1 KH)
  * 77 Stock Entry (52 PX + 21 PXHN + 4 PNHN)

GL Entry Total Dr = Total Cr per voucher is asserted on a 50-voucher
random sample. AR aging by Customer match Misa within 1k VND/customer
is asserted via the trial balance comparison in test_trial_balance_t1_2026.
"""

from __future__ import annotations

import json
import os
import unittest
from collections import Counter
from pathlib import Path
from typing import Any

import frappe


_REALDATA_DIR = Path(
    "/home/long/long/frappe-bench-dcnet/docs/accounting-requirements/realdata"
)
_NKC_FILE = _REALDATA_DIR / "so_nhat_ky_chung" / "So_nhat_ky_chung_01-2026.xlsx"
_BR_FILE = (
    _REALDATA_DIR / "bang_ke_hoa_don_mua_ban"
    / "Bang_ke_hoa_don_chung_tu_hang_hoa_dich_vu_ban_ra_mau_quan_tri 01-2026.xlsx"
)
_MV_FILE = (
    _REALDATA_DIR / "bang_ke_hoa_don_mua_ban"
    / "Bang_ke_hoa_don_chung_tu_hang_hoa_dich_vu_mua_vao_mau_quan_tri 01-2026.xlsx"
)


# Acceptance thresholds (Spec §12 + session-last summary)
_EXPECTED_PREFIX_COUNTS = {
    "BH": 303,
    "MDV": 526, "MH": 5, "PN": 36,
    "BC": 236, "UNC": 220, "PT": 15, "PC": 73,
    "CTNB": 38, "NVK": 31, "CK": 1,
    "PBDT": 1, "PBPTT": 1, "KH": 1,
    "PX": 52, "PXHN": 21, "PNHN": 4,
}
_EXPECTED_TOTAL = 1564


def _xlsx_to_payloads(xlsx_path: Path) -> list[dict[str, Any]]:
    """Read Misa export xlsx → list of row dicts keyed by Vietnamese header."""
    from openpyxl import load_workbook
    wb = load_workbook(xlsx_path, read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    # Misa exports have title/blank lines; header on row 4 (index 3)
    headers = [str(c).strip() if c else "" for c in rows[3]]
    out: list[dict[str, Any]] = []
    for r in rows[4:]:
        if all(c is None for c in r):
            continue
        d: dict[str, Any] = {}
        for i, val in enumerate(r):
            if i < len(headers) and headers[i]:
                if val is None:
                    continue
                if hasattr(val, "isoformat"):
                    val = val.isoformat()
                d[headers[i]] = val
        if d:
            out.append(d)
    return out


@unittest.skipUnless(
    os.environ.get("MISA_E2E") == "1",
    "Set MISA_E2E=1 to run the full T1/2026 import E2E test. Requires "
    "Phase 1+2+3 imported and Account mapping populated.",
)
class TestE2EPhaseDT1_2026(unittest.TestCase):
    """E2E test posting the full T1/2026 dataset via run_phase_4_post."""

    @classmethod
    def setUpClass(cls):
        cls.nkc_payloads = _xlsx_to_payloads(_NKC_FILE)
        cls.br_payloads = _xlsx_to_payloads(_BR_FILE)
        cls.mv_payloads = _xlsx_to_payloads(_MV_FILE)

    def test_parser_voucher_count_matches_spec(self):
        from vn_accounting.misa_migration.parsers import nkc_parser
        vouchers = nkc_parser.parse_nkc_rows(self.nkc_payloads)
        self.assertGreaterEqual(len(vouchers), _EXPECTED_TOTAL - 5,
            f"Expected ~{_EXPECTED_TOTAL} vouchers, got {len(vouchers)}")
        self.assertLessEqual(len(vouchers), _EXPECTED_TOTAL + 5)

        prefix_counts = Counter(v.get("prefix") for v in vouchers)
        for prefix, expected in _EXPECTED_PREFIX_COUNTS.items():
            actual = prefix_counts.get(prefix, 0)
            self.assertGreaterEqual(
                actual, expected - 2,
                f"Prefix {prefix}: expected ~{expected}, got {actual}"
            )

    def test_nkc_balance_zero_unbalanced(self):
        from vn_accounting.misa_migration.parsers import nkc_parser
        vouchers = nkc_parser.parse_nkc_rows(self.nkc_payloads)
        unbalanced = [v for v in vouchers if v.get("balance_error")]
        self.assertEqual(
            len(unbalanced), 0,
            f"{len(unbalanced)} unbalanced vouchers: "
            f"{[v['voucher_no'] for v in unbalanced[:5]]}"
        )

    def test_full_post_creates_expected_docs(self):
        """The actual E2E: create a synthetic batch, post via run_phase_4_post,
        assert per-DocType counts.

        This test creates real ERPNext docs. Run only on a throwaway site.
        """
        from vn_accounting.misa_migration.importers.phase_4_orchestrator import (
            run_phase_4_post,
        )

        # Create a Misa Migration Batch with Phase 4 rows already 'Ready'
        batch_name = self._create_phase_4_batch()
        try:
            summary = run_phase_4_post(batch_name, chunk_commit=100)
        finally:
            # Cleanup hint for the next run — leave Batch + Rows for debugging
            print(f"E2E batch: {batch_name}")

        self.assertGreater(summary["total_vouchers"], _EXPECTED_TOTAL - 10)

        # Expected by-DocType ranges (tolerances ±5 for rounding/edge cases)
        by_dt = {
            k: v.get("posted", 0) for k, v in summary["by_target_doctype"].items()
        }
        self.assertGreaterEqual(
            by_dt.get("Sales Invoice", 0), 298,
            f"Sales Invoice posted: {by_dt.get('Sales Invoice', 0)}")
        self.assertGreaterEqual(
            by_dt.get("Purchase Invoice", 0), 525,
            f"Purchase Invoice posted: {by_dt.get('Purchase Invoice', 0)}")
        self.assertGreaterEqual(
            by_dt.get("Payment Entry", 0), 540,
            f"Payment Entry posted: {by_dt.get('Payment Entry', 0)}")
        self.assertGreaterEqual(
            by_dt.get("Journal Entry", 0), 70,
            f"Journal Entry posted: {by_dt.get('Journal Entry', 0)}")
        self.assertGreaterEqual(
            by_dt.get("Stock Entry", 0), 75,
            f"Stock Entry posted: {by_dt.get('Stock Entry', 0)}")

    def test_sample_si_exists(self):
        """First sales invoice should have doc.name = BH20260001."""
        # This presumes test_full_post_creates_expected_docs ran first or a
        # prior batch already created the doc. Standalone check.
        if not frappe.db.exists("Sales Invoice", "BH20260001"):
            self.skipTest("Run test_full_post_creates_expected_docs first")
        si = frappe.get_doc("Sales Invoice", "BH20260001")
        self.assertEqual(si.name, "BH20260001")
        self.assertGreater(len(si.items), 0)

    def test_gl_entry_balance_per_voucher_sample(self):
        """Random 50-voucher sample: per-voucher Total Dr = Total Cr."""
        # Pick 50 distinct voucher_no across all 5 target doctypes
        sample = frappe.db.sql(
            """
            SELECT DISTINCT voucher_no
            FROM `tabGL Entry`
            WHERE voucher_no LIKE 'BH%' OR voucher_no LIKE 'MDV%'
               OR voucher_no LIKE 'BC%' OR voucher_no LIKE 'UNC%'
               OR voucher_no LIKE 'NVK%' OR voucher_no LIKE 'PX%'
            ORDER BY RAND() LIMIT 50
            """,
            as_dict=True,
        )
        if not sample:
            self.skipTest("No GL Entries to sample — run full E2E post first")
        for r in sample:
            vno = r["voucher_no"]
            totals = frappe.db.sql(
                """SELECT SUM(debit) dr, SUM(credit) cr FROM `tabGL Entry`
                   WHERE voucher_no=%s AND is_cancelled=0""",
                (vno,), as_dict=True,
            )[0]
            dr = float(totals.get("dr") or 0)
            cr = float(totals.get("cr") or 0)
            self.assertAlmostEqual(
                dr, cr, delta=1.0,
                msg=f"Voucher {vno}: Dr={dr} ≠ Cr={cr}"
            )

    # ------------------------------------------------------- helpers

    def _create_phase_4_batch(self) -> str:
        """Create a Misa Migration Batch with Phase 4 rows inserted directly.

        Returns the batch name. Caller responsible for cleanup; we
        deliberately leave the batch + rows for debugging after run.
        """
        batch = frappe.get_doc({
            "doctype": "Misa Migration Batch",
            "title": "E2E T1/2026",
            "company": (
                frappe.defaults.get_global_default("company")
                or frappe.db.get_value("Company", {}, "name")
            ),
            "status": "REVIEWED",
        })
        batch.flags.ignore_permissions = True
        batch.insert()

        for ft, payloads in (
            ("NKC", self.nkc_payloads),
            ("Bang ke BR", self.br_payloads),
            ("Bang ke MV", self.mv_payloads),
        ):
            for idx, p in enumerate(payloads, 1):
                row = frappe.get_doc({
                    "doctype": "Misa Migration Row",
                    "batch": batch.name,
                    "file_type": ft,
                    "row_index": idx,
                    "status": "Ready",
                    "raw_payload": json.dumps(p, ensure_ascii=False, default=str),
                })
                row.flags.ignore_permissions = True
                row.insert()

        frappe.db.commit()
        return batch.name


class TestE2ESmoke(unittest.TestCase):
    """Always-on smoke tests for the orchestrator (no real-data run)."""

    def test_orchestrator_handles_empty_batch_gracefully(self):
        from vn_accounting.misa_migration.importers.phase_4_orchestrator import (
            run_phase_4_post,
        )
        import unittest.mock as mock
        with mock.patch(
            "vn_accounting.misa_migration.importers.phase_4_orchestrator.frappe"
        ) as mock_frappe:
            mock_frappe.db.sql.return_value = []
            result = run_phase_4_post("BATCH-EMPTY")
            self.assertEqual(result["total_vouchers"], 0)
            self.assertEqual(result["by_target_doctype"], {})
            self.assertEqual(result["errors"], [])
            self.assertIn("elapsed_seconds", result)


if __name__ == "__main__":
    unittest.main()
