"""Unit tests for accounting_posting.build_default_entries (pure function).

Run: cd /home/long/long/frappe-bench-dcnet/apps/vn_accounting
     python -m pytest vn_accounting/utils/test_accounting_posting.py -v

These tests run without a Frappe site by passing company=None so the helper
returns raw account-number strings instead of resolving via DB. The real
DB-coupled tests (resolve_cost_center, post_je_from_entries balance) live
in tests/test_accounting_posting_helper.py and run under bench.
"""
from __future__ import annotations

import pytest

from vn_accounting.utils.accounting_posting import build_default_entries


# --- Asset Repair --- #

def test_asset_repair_chi_phi_no_vat():
    rows = build_default_entries("Asset Repair", "Chi phí", 5_000_000, has_vat=False)
    assert len(rows) == 1
    r = rows[0]
    assert r["account_debit"] == "6427"
    assert r["account_credit"] == "111"
    assert r["amount"] == 5_000_000
    assert r["is_vat"] == 0


def test_asset_repair_chi_phi_with_vat_10():
    rows = build_default_entries("Asset Repair", "Chi phí", 5_000_000, has_vat=True, vat_rate=10)
    assert len(rows) == 2
    main, vat = rows
    assert main["account_debit"] == "6427"
    assert main["account_credit"] == "111"
    assert main["amount"] == 5_000_000
    assert vat["account_debit"] == "1331"
    assert vat["account_credit"] == "111"
    assert vat["amount"] == 500_000
    assert vat["is_vat"] == 1


def test_asset_repair_capitalized_no_vat():
    rows = build_default_entries(
        "Asset Repair", "Sửa chữa lớn vốn hóa", 18_000_000, has_vat=False
    )
    assert len(rows) == 1
    assert rows[0]["account_debit"] == "2413"
    assert rows[0]["account_credit"] == "331"
    assert rows[0]["amount"] == 18_000_000


def test_asset_repair_upgrade_with_vat():
    rows = build_default_entries(
        "Asset Repair", "Nâng cấp cải tạo", 20_000_000, has_vat=True, vat_rate=10
    )
    assert len(rows) == 2
    assert rows[0]["account_debit"] == "2412"
    assert rows[0]["account_credit"] == "331"
    assert rows[1]["account_debit"] == "1331"
    assert rows[1]["account_credit"] == "331"
    assert rows[1]["amount"] == 2_000_000


def test_asset_repair_invalid_classification_raises():
    with pytest.raises(Exception):
        build_default_entries("Asset Repair", "Bogus", 1_000_000)


# --- CCDC Item Purchase --- #

def test_ccdc_purchase_no_vat():
    # VAS-correct flow: two rows model receive-into-warehouse + issue-for-amortization.
    rows = build_default_entries("CCDC Item Purchase", None, 4_000_000, has_vat=False)
    assert len(rows) == 2
    # Row 1: Dr 153 / Cr 331 — supplies received, payable created
    assert rows[0]["account_debit"] == "153"
    assert rows[0]["account_credit"] == "331"
    assert rows[0]["amount"] == 4_000_000
    # Row 2: Dr 242 / Cr 153 — issued for amortization, cost moved to prepaid
    assert rows[1]["account_debit"] == "242"
    assert rows[1]["account_credit"] == "153"
    assert rows[1]["amount"] == 4_000_000


def test_ccdc_purchase_with_vat():
    rows = build_default_entries("CCDC Item Purchase", None, 4_000_000, has_vat=True, vat_rate=10)
    assert len(rows) == 3
    # First two rows = cost movement (153, 242, 331 — see no_vat test)
    # Row 3: Dr 1331 / Cr 331 — VAT input credit, same payable as the cost row
    assert rows[2]["account_debit"] == "1331"
    assert rows[2]["account_credit"] == "331"
    assert rows[2]["amount"] == 400_000


# --- CCDC Writeoff --- #

def test_ccdc_writeoff_only_remaining_242():
    rows = build_default_entries(
        "CCDC Writeoff", None, 0, remaining_242=4_000_000, remaining_153=0, compensation_amount=0
    )
    assert len(rows) == 1
    assert rows[0]["account_debit"] == "6423"
    assert rows[0]["account_credit"] == "242"
    assert rows[0]["amount"] == 4_000_000


def test_ccdc_writeoff_all_three_rows():
    rows = build_default_entries(
        "CCDC Writeoff", None, 0,
        remaining_242=4_000_000, remaining_153=2_000_000, compensation_amount=1_000_000,
    )
    assert len(rows) == 3
    assert rows[0]["account_debit"] == "6423" and rows[0]["account_credit"] == "242"
    assert rows[1]["account_debit"] == "632" and rows[1]["account_credit"] == "153"
    assert rows[2]["account_debit"] == "1388" and rows[2]["account_credit"] == "711"


def test_ccdc_writeoff_skips_zero_amounts():
    rows = build_default_entries(
        "CCDC Writeoff", None, 0,
        remaining_242=0, remaining_153=2_000_000, compensation_amount=0,
    )
    assert len(rows) == 1
    assert rows[0]["account_debit"] == "632"


def test_invalid_event_raises():
    with pytest.raises(Exception):
        build_default_entries("Bogus Event", None, 1_000_000)
