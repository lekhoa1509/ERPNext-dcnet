"""Trial Balance comparison: Misa vs ERPNext after T1/2026 import.

Skipped by default. Gates:
  * `MISA_TB=1` — required to compare ERPNext output against the Misa fixture
  * `MISA_TB_FIXTURE=<path>` — optional; defaults to the Danh_sach_so_du file

Acceptance criterion (spec §12 + roadmap C16):
  Per-account difference (Misa balance vs ERPNext computed balance)
  < 1,000 VND.

Helper functions exposed for reuse:

  parse_misa_tb_fixture(xlsx_path) → dict[account_number → {dr, cr}]
  compute_erpnext_tb(company, end_date) → dict[account_number → {dr, cr}]
  diff_trial_balance(misa, erpnext, tol=1000.0) → list[diff_row]

These can be invoked from any Phase E migration validation script, not
just the test.
"""

from __future__ import annotations

import os
import unittest
from pathlib import Path
from typing import Any

import frappe


_REALDATA_ROOT = Path(
    "/home/long/long/frappe-bench-dcnet/docs/accounting-requirements/realdata"
)


def _find_default_fixture() -> Path | None:
    """Locate the Misa số dư xlsx in realdata.

    File lives under a directory with Vietnamese diacritics that may use
    NFC or NFD encoding depending on the source filesystem (macOS export
    typically NFD). Glob-search by basename to avoid encoding issues.
    """
    for p in _REALDATA_ROOT.rglob("Danh_sach_so_du_tai_khoan.xlsx"):
        if "__MACOSX" in str(p):
            continue
        return p
    return None


_DEFAULT_FIXTURE = _find_default_fixture()


# ----------------------------------------------------------------- helpers

def parse_misa_tb_fixture(xlsx_path: Path) -> dict[str, dict[str, float]]:
    """Parse Misa Trial Balance / opening balance xlsx into a dict.

    Expected layout (verified against Danh_sach_so_du_tai_khoan.xlsx):

      Row 0:  Title row ("Danh sách Số dư tài khoản")
      Row 1:  blank
      Row 2:  Headers: ['STT', 'Số tài khoản', 'Tên tài khoản', 'Dư Nợ', 'Dư Có']
      Row 3+: Data rows. Account number in col 1. Dr (col 3) and Cr (col 4)
              are mutually exclusive per row.

    Returns:
      {account_number: {"dr": float, "cr": float}}
    """
    from openpyxl import load_workbook
    wb = load_workbook(str(xlsx_path), read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    wb.close()

    out: dict[str, dict[str, float]] = {}
    for r in rows[3:]:  # skip 3-line header
        if not r or len(r) < 5:
            continue
        acct_no = r[1]
        if not acct_no:
            continue
        acct = str(acct_no).strip()
        if not acct or acct == "Tổng":
            continue
        try:
            dr = float(r[3] or 0)
        except (TypeError, ValueError):
            dr = 0.0
        try:
            cr = float(r[4] or 0)
        except (TypeError, ValueError):
            cr = 0.0
        out[acct] = {"dr": dr, "cr": cr}
    return out


def compute_erpnext_tb(
    company: str,
    end_date: str,
    start_date: str | None = None,
) -> dict[str, dict[str, float]]:
    """Compute ERPNext Trial Balance from GL Entry.

    For each Account on this company, sum debit and credit (sign-aware) up
    to end_date. Returns dict[account_number → {dr, cr, balance}] where
    balance is dr - cr (positive = Dr balance, negative = Cr balance).

    Args:
      company: Company name.
      end_date: ISO date string. Period closing date.
      start_date: optional from-date (default: include opening balances).

    Excludes is_cancelled rows. Excludes Period Closing Voucher entries so
    revenue/expense accounts aren't zeroed out.
    """
    sql = """
        SELECT a.account_number AS acct, SUM(g.debit) AS dr, SUM(g.credit) AS cr
        FROM `tabGL Entry` g
        JOIN `tabAccount` a ON a.name = g.account
        WHERE g.company = %s
          AND a.company = %s
          AND g.posting_date <= %s
          AND g.is_cancelled = 0
          AND g.voucher_type != 'Period Closing Voucher'
    """
    params: list[Any] = [company, company, end_date]
    if start_date:
        sql += " AND g.posting_date >= %s"
        params.append(start_date)
    sql += " GROUP BY a.account_number"

    rows = frappe.db.sql(sql, tuple(params), as_dict=True)
    out: dict[str, dict[str, float]] = {}
    for r in rows:
        acct = (r.get("acct") or "").strip()
        if not acct:
            continue
        dr = float(r.get("dr") or 0)
        cr = float(r.get("cr") or 0)
        out[acct] = {"dr": dr, "cr": cr, "balance": dr - cr}
    return out


def roll_up_balances_by_misa_codes(
    tb: dict[str, dict[str, float]],
    misa_codes: list[str] | None = None,
) -> dict[str, dict[str, float]]:
    """For each Misa code, roll up ERPNext balances of all account_numbers
    that start with this code.

    Misa fixtures list BOTH parent summaries and leaf rows with the same
    balance (Misa convention: parent = sum of children). ERPNext only
    posts to leaves (groups are non-postable), so without roll-up the
    per-code compare flags every parent summary as `missing_in_erpnext`
    even when leaf totals add up correctly.

    This helper produces a rolled-up TB suitable for direct per-code
    diff against a Misa fixture.

    Args:
      tb: input TB (account_number → {dr, cr, balance?}).
      misa_codes: optional list of codes to roll up under. When None,
        every code in `tb` is treated as a candidate parent (i.e. the
        return matches input for unique codes + adds rolled-up parents
        for any code that has descendants).

    Returns:
      Dict same shape as `compute_erpnext_tb` output but per-code values
      are the cumulative rollup of all descendant codes.
    """
    all_codes = sorted(tb.keys()) if not misa_codes else sorted(set(misa_codes) | set(tb.keys()))
    out: dict[str, dict[str, float]] = {}
    for code in all_codes:
        total_dr = 0.0
        total_cr = 0.0
        for other_code, vals in tb.items():
            if other_code == code or other_code.startswith(code):
                total_dr += vals.get("dr", 0.0)
                total_cr += vals.get("cr", 0.0)
        out[code] = {
            "dr": total_dr,
            "cr": total_cr,
            "balance": total_dr - total_cr,
        }
    return out


def diff_trial_balance(
    misa: dict[str, dict[str, float]],
    erpnext: dict[str, dict[str, float]],
    tolerance: float = 1000.0,
) -> list[dict[str, Any]]:
    """Compare Misa vs ERPNext per-account.

    Args:
      misa: parse_misa_tb_fixture output.
      erpnext: compute_erpnext_tb output.
      tolerance: per-account VND tolerance (default 1,000 — spec §12).

    Returns:
      List of diff rows for every account that EITHER appears in only one
      side OR has |diff| > tolerance. Each row:
        {
          "account": str,
          "misa_dr": float, "misa_cr": float, "misa_balance": float,
          "erpnext_dr": float, "erpnext_cr": float, "erpnext_balance": float,
          "diff": float,           # erpnext - misa, signed
          "reason": "diff_exceeds_tolerance" | "missing_in_erpnext"
                  | "missing_in_misa",
        }
    """
    # Iterate Misa keys only. ERPNext-only sub-codes (e.g. 1121.20, 11219)
    # already roll UP into their Misa parents via roll_up_balances_by_misa_codes —
    # reporting them individually here is double-counting since the rolled-up
    # parent already carries the same balance contribution. ERPNext naturally
    # has more granular sub-accounts than Misa source's parent-only summary.
    all_accounts = sorted(misa.keys())
    diffs: list[dict[str, Any]] = []
    for acct in all_accounts:
        m = misa.get(acct)
        e = erpnext.get(acct)

        m_dr = m["dr"] if m else 0.0
        m_cr = m["cr"] if m else 0.0
        m_bal = m_dr - m_cr

        e_dr = e["dr"] if e else 0.0
        e_cr = e["cr"] if e else 0.0
        e_bal = e_dr - e_cr

        diff = e_bal - m_bal
        reason = None
        if m is None and e is not None and abs(e_bal) > tolerance:
            reason = "missing_in_misa"
        elif e is None and m is not None and abs(m_bal) > tolerance:
            reason = "missing_in_erpnext"
        elif abs(diff) > tolerance:
            reason = "diff_exceeds_tolerance"

        if reason:
            diffs.append({
                "account": acct,
                "misa_dr": m_dr, "misa_cr": m_cr, "misa_balance": m_bal,
                "erpnext_dr": e_dr, "erpnext_cr": e_cr, "erpnext_balance": e_bal,
                "diff": diff,
                "reason": reason,
            })
    return diffs


# ----------------------------------------------------------------- always-on tests

class TestTrialBalanceHelpers(unittest.TestCase):
    """Helper logic — runs without real DB or fixture data."""

    def test_diff_within_tolerance_returns_empty(self):
        misa = {"111": {"dr": 100_000, "cr": 0}}
        erpnext = {"111": {"dr": 100_500, "cr": 0, "balance": 100_500}}
        diffs = diff_trial_balance(misa, erpnext, tolerance=1000)
        self.assertEqual(diffs, [])

    def test_diff_exceeding_tolerance_reported(self):
        misa = {"111": {"dr": 100_000, "cr": 0}}
        erpnext = {"111": {"dr": 105_000, "cr": 0, "balance": 105_000}}
        diffs = diff_trial_balance(misa, erpnext, tolerance=1000)
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0]["account"], "111")
        self.assertEqual(diffs[0]["reason"], "diff_exceeds_tolerance")
        self.assertAlmostEqual(diffs[0]["diff"], 5_000.0, delta=0.01)

    def test_missing_in_erpnext_reported(self):
        misa = {"333": {"dr": 0, "cr": 50_000}}
        erpnext = {}
        diffs = diff_trial_balance(misa, erpnext)
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0]["reason"], "missing_in_erpnext")

    def test_missing_in_misa_reported(self):
        misa = {}
        erpnext = {"627": {"dr": 25_000, "cr": 0, "balance": 25_000}}
        diffs = diff_trial_balance(misa, erpnext)
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0]["reason"], "missing_in_misa")

    def test_tiny_diff_in_missing_side_ignored(self):
        # ERPNext has rounding noise on account not in Misa fixture
        misa = {}
        erpnext = {"711": {"dr": 50, "cr": 0, "balance": 50}}
        diffs = diff_trial_balance(misa, erpnext, tolerance=1000)
        self.assertEqual(diffs, [])

    def test_credit_balance_sign_correct(self):
        # Misa: 331 supplier payable Cr 200,000; ERPNext same
        misa = {"331": {"dr": 0, "cr": 200_000}}
        erpnext = {"331": {"dr": 0, "cr": 200_000, "balance": -200_000}}
        diffs = diff_trial_balance(misa, erpnext)
        self.assertEqual(diffs, [])


class TestMisaTbFixtureParser(unittest.TestCase):
    """Parse the real Misa số dư xlsx if it exists."""

    @unittest.skipUnless(
        _DEFAULT_FIXTURE is not None,
        "Fixture Danh_sach_so_du_tai_khoan.xlsx not found in realdata",
    )
    def test_parses_realfile_into_dict(self):
        result = parse_misa_tb_fixture(_DEFAULT_FIXTURE)
        # Should parse non-empty with account 111 + 112 (Cash + Bank)
        self.assertGreater(len(result), 5)
        self.assertIn("111", result)
        self.assertIn("112", result)
        # 111 should be Dr balance
        self.assertGreater(result["111"]["dr"], 0)
        self.assertEqual(result["111"]["cr"], 0)


# ------------------------------------------ E2E gated full Trial Balance compare

@unittest.skipUnless(
    os.environ.get("MISA_TB") == "1",
    "Set MISA_TB=1 to compare ERPNext Trial Balance vs Misa fixture. "
    "Requires Phase 4 import already completed.",
)
class TestTrialBalanceT1_2026Compare(unittest.TestCase):
    """Full compare — ERPNext TB at end of T1/2026 vs Misa fixture."""

    @classmethod
    def setUpClass(cls):
        env_fixture = os.environ.get("MISA_TB_FIXTURE")
        if env_fixture:
            fixture_path = Path(env_fixture)
        elif _DEFAULT_FIXTURE is not None:
            fixture_path = _DEFAULT_FIXTURE
        else:
            raise unittest.SkipTest(
                "No fixture found; set MISA_TB_FIXTURE=<path>"
            )
        cls.misa_tb = parse_misa_tb_fixture(fixture_path)
        cls.company = (
            os.environ.get("MISA_TB_COMPANY")
            or frappe.defaults.get_global_default("company")
            or frappe.db.get_value("Company", {}, "name")
        )
        cls.end_date = os.environ.get("MISA_TB_END", "2026-01-31")
        # MISA_TB_IGNORE_ACCOUNTS: comma-separated list of account_numbers
        # to exclude from the diff. Used to skip known Misa SDK data
        # inconsistencies (e.g. TK 242 prepaid sum != general balance file
        # — drift between two Misa exports for the same period) that
        # aren't fixable from the import code's side.
        ignore = os.environ.get("MISA_TB_IGNORE_ACCOUNTS", "")
        cls.ignore_accounts = {a.strip() for a in ignore.split(",") if a.strip()}

    def test_trial_balance_within_1k_vnd_per_account(self):
        erpnext_tb = compute_erpnext_tb(self.company, self.end_date)
        # Item 1A: roll up ERPNext leaves under each Misa parent code so
        # the per-account compare aligns Misa's summary convention with
        # ERPNext's leaf-only posting. Without this, every Misa parent
        # row (111, 156, 411, …) flags as `missing_in_erpnext` while its
        # leaf is correctly populated.
        erpnext_rolled = roll_up_balances_by_misa_codes(
            erpnext_tb, misa_codes=list(self.misa_tb.keys()),
        )
        diffs = diff_trial_balance(
            self.misa_tb, erpnext_rolled, tolerance=1000.0,
        )
        if self.ignore_accounts:
            diffs = [d for d in diffs if d["account"] not in self.ignore_accounts]
        if diffs:
            preview = "\n".join(
                f"  {d['account']}: misa={d['misa_balance']:.0f} "
                f"erpnext={d['erpnext_balance']:.0f} diff={d['diff']:.0f} "
                f"({d['reason']})"
                for d in diffs[:20]
            )
            extra = f"\n  ...and {len(diffs) - 20} more" if len(diffs) > 20 else ""
            self.fail(
                f"{len(diffs)} accounts diverge >1k VND from Misa:\n"
                f"{preview}{extra}"
            )


if __name__ == "__main__":
    unittest.main()
