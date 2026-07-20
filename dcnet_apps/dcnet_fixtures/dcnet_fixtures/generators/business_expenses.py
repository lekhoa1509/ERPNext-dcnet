"""
Business Expenses Generator for DCNET 3-Year Data

Generates monthly operating expenses via Journal Entries:
- Rent (increases from 2025 when Hanoi showroom added)
- Utilities (electricity, internet)
- Payroll (increases with headcount/salary growth)
- Marketing spend (scales with revenue growth)
- Shipping/delivery costs (linked to SO volume)
- Insurance (quarterly)
- Bank fees (monthly)

Usage:
    from dcnet_fixtures.dcnet_fixtures.generators.business_expenses import generate_expenses_3y
    generate_expenses_3y()
    frappe.db.commit()
"""

import frappe
from frappe.utils import getdate, add_days, flt
from random import randint, uniform, random, choice
from datetime import date

from dcnet_fixtures.dcnet_fixtures.generators.foundation import GROWTH_CONFIG


# Monthly expense configuration per year
# All amounts in VND
EXPENSE_CONFIG = {
    2023: {
        "rent":       30_000_000,
        "utilities":   6_000_000,
        "internet":    2_000_000,
        "marketing":  15_000_000,
        "payroll":   150_000_000,
        "insurance":   8_000_000,   # quarterly
        "bank_fee":    1_000_000,
    },
    2024: {
        "rent":       35_000_000,
        "utilities":   7_000_000,
        "internet":    2_500_000,
        "marketing":  25_000_000,
        "payroll":   200_000_000,
        "insurance":  10_000_000,
        "bank_fee":    1_500_000,
    },
    2025: {
        "rent":       55_000_000,   # +HN showroom
        "utilities":   9_000_000,
        "internet":    3_000_000,
        "marketing":  40_000_000,
        "payroll":   280_000_000,
        "insurance":  12_000_000,
        "bank_fee":    2_500_000,
    },
    2026: {
        "rent":       60_000_000,
        "utilities":  10_000_000,
        "internet":    3_500_000,
        "marketing":  50_000_000,
        "payroll":   320_000_000,
        "insurance":  14_000_000,
        "bank_fee":    3_000_000,
    },
}


# =============================================================================
# HELPERS
# =============================================================================

def _get_company():
    return frappe.db.get_single_value("Global Defaults", "default_company") or \
           frappe.db.get_value("Company", {}, "name")


def _get_abbr(company):
    return frappe.db.get_value("Company", company, "abbr")


def _get_expense_account(company, abbr, account_type_hint="expense"):
    """Find suitable expense account, prioritizing TT200 numbers"""
    mapping = {
        "rent":      "6427",
        "utilities": "6427",
        "marketing": "6411",
        "payroll":   "6421",
        "expense":   "6427",
        "insurance": "6421",
        "depreciation": "6424",
        "asset_711": "711",
        "asset_811": "811",
    }
    num = mapping.get(account_type_hint, "6427")
    acc = frappe.db.get_value("Account", {"account_number": num, "company": company}, "name")
    if acc: return acc

    # Fallback to names
    candidates = {
        "rent":      [f"Indirect Expenses - {abbr}", f"Administrative Expenses - {abbr}"],
        "marketing": [f"Sales Expenses - {abbr}"],
        "payroll":   [f"Indirect Expenses - {abbr}"],
    }
    for acc_name in candidates.get(account_type_hint, []):
        if frappe.db.exists("Account", acc_name):
            return acc_name

    return frappe.db.get_value("Account", {"company": company, "root_type": "Expense", "is_group": 0}, "name")


def _get_cash_account(company, abbr, type="Bank"):
    """Get TT200 account (1111 for Cash, 1121 for Bank)"""
    num = "1121" if type == "Bank" else "1111"
    acc = frappe.db.get_value("Account", {"account_number": num, "company": company}, "name")
    if acc: return acc

    candidates = [f"{type} - {abbr}"]
    for acc in candidates:
        if frappe.db.exists("Account", acc):
            return acc
    return frappe.db.get_value("Account", {"company": company, "account_type": type, "is_group": 0}, "name")


def _get_cost_center(abbr, department_hint=None):
    """Return appropriate cost center"""
    if department_hint:
        cc = f"{department_hint} - {abbr}"
        if frappe.db.exists("Cost Center", cc):
            return cc
    main = f"Main - {abbr}"
    if frappe.db.exists("Cost Center", main):
        return main
    return frappe.db.get_value("Cost Center", {"is_group": 0}, "name")


def _create_journal_entry(company, posting_date, debit_account, credit_account, amount, remarks, cost_center=None):
    """Create and submit a simple 2-leg Journal Entry"""
    debit_entry = {
        "account": debit_account,
        "debit_in_account_currency": amount,
        "credit_in_account_currency": 0,
    }
    credit_entry = {
        "account": credit_account,
        "debit_in_account_currency": 0,
        "credit_in_account_currency": amount,
    }
    if cost_center:
        debit_entry["cost_center"] = cost_center
        credit_entry["cost_center"] = cost_center

    je = frappe.get_doc({
        "doctype": "Journal Entry",
        "posting_date": posting_date,
        "company": company,
        "user_remark": remarks,
        "accounts": [debit_entry, credit_entry],
    })
    je.flags.ignore_permissions = True
    je.flags.ignore_mandatory = True
    je.insert()
    je.submit()
    return je


# =============================================================================
# EXPENSE GENERATORS
# =============================================================================

def generate_monthly_expenses(company, abbr, year, month):
    """Generate all monthly expenses for a given year/month"""
    cfg = EXPENSE_CONFIG.get(year, EXPENSE_CONFIG[2023])
    posting_date = getdate(f"{year}-{month:02d}-{'28' if month == 2 else '30'}")
    bank_acc = _get_cash_account(company, abbr, "Bank")
    cost_center = _get_cost_center(abbr)

    created = 0
    errors = 0

    # Monthly entries (excluding payroll)
    entries = [
        ("rent",      "Tiền thuê mặt bằng tháng {m}/{y}",      "rent",      "Kế toán"),
        ("utilities", "Điện nước tháng {m}/{y}",               "utilities", "Kho vận"),
        ("marketing", "Chi phí Marketing tháng {m}/{y}",       "marketing", "Marketing"),
        ("bank_fee",  "Phí ngân hàng tháng {m}/{y}",           "expense",   "Kế toán"),
    ]

    for key, remark_tpl, hint, dept in entries:
        amount_base = cfg.get(key, 0)
        if amount_base == 0:
            continue
        amount = int(amount_base * uniform(0.92, 1.08))
        remark = remark_tpl.format(m=month, y=year)
        cc = _get_cost_center(abbr, dept) if dept else cost_center
        exp_acc = _get_expense_account(company, abbr, hint)

        if not exp_acc or not bank_acc:
            continue
        try:
            _create_journal_entry(company, posting_date, exp_acc, bank_acc, amount, remark, cc)
            created += 1
        except Exception:
            errors += 1

    # ----------------------------------------------------------------
    # DETAILED PAYROLL
    # ----------------------------------------------------------------
    payroll_base = cfg["payroll"]
    salary_gross = int(payroll_base * uniform(0.95, 1.05))
    insurance_co = int(salary_gross * 0.215) # Co pays 21.5%
    
    acc_334 = frappe.db.get_value("Account", {"account_number": "334", "company": company}, "name")
    acc_338 = frappe.db.get_value("Account", {"account_number": "3383", "company": company}, "name")
    acc_6421 = _get_expense_account(company, abbr, "payroll")
    
    if acc_334 and acc_6421:
        try:
            # 1. Accrue Salary
            remark_p = f"Trích lương và BHXH tháng {month}/{year}"
            je = frappe.get_doc({
                "doctype": "Journal Entry",
                "company": company,
                "posting_date": posting_date,
                "remark": remark_p,
                "accounts": [
                    {"account": acc_6421, "debit_in_account_currency": salary_gross + insurance_co},
                    {"account": acc_334,  "credit_in_account_currency": salary_gross},
                    {"account": acc_338,  "credit_in_account_currency": insurance_co} if acc_338 else {"account": acc_334, "credit_in_account_currency": 0}
                ]
            })
            je.flags.ignore_permissions = True
            je.insert()
            je.submit()
            
            # 2. Payment (from Bank)
            _create_journal_entry(
                company, add_days(posting_date, 5), acc_334, bank_acc, 
                salary_gross, f"Thanh toán lương tháng {month}/{year} qua ngân hàng"
            )
            created += 2
        except Exception:
            errors += 1

    return created, errors


def generate_quarterly_insurance(company, abbr, year, quarter):
    """Generate quarterly insurance expense"""
    cfg = EXPENSE_CONFIG.get(year, EXPENSE_CONFIG[2023])
    q_month = {1: 3, 2: 6, 3: 9, 4: 12}[quarter]
    posting_date = getdate(f"{year}-{q_month:02d}-25")
    cash_acc = _get_cash_account(company, abbr, "Cash")
    expense_acc = _get_expense_account(company, abbr, "payroll")
    amount = int(cfg["insurance"] * uniform(0.95, 1.05))
    cost_center = _get_cost_center(abbr, "Kế toán")

    try:
        _create_journal_entry(
            company, posting_date, expense_acc, cash_acc, amount,
            f"Phí bảo hiểm Q{quarter}/{year}", cost_center
        )
        return 1
    except Exception:
        return 0


def generate_depreciation_entries(company, abbr, year):
    """Generate monthly depreciation for fixed assets"""
    exp_acc = _get_expense_account(company, abbr, "depreciation")
    dep_acc = frappe.db.get_value("Account", {"account_number": "2141", "company": company}, "name")
    if not exp_acc or not dep_acc:
        return 0

    # Fixed monthly depreciation
    base_depreciation = 5_000_000
    if year >= 2025:
        base_depreciation += 3_000_000
    cost_center = _get_cost_center(abbr, "Kế toán")
    created = 0

    months = 12 if year < 2026 else 3
    for month in range(1, months + 1):
        posting_date = getdate(f"{year}-{month:02d}-28")
        amount = int(base_depreciation * uniform(0.95, 1.05))
        try:
            _create_journal_entry(
                company, posting_date, exp_acc, dep_acc, amount,
                f"Khấu hao TSCĐ tháng {month}/{year}", cost_center
            )
            created += 1
        except Exception:
            pass

    return created


# =============================================================================
# MAIN GENERATOR
# =============================================================================

def generate_expenses_3y(years=None):
    """
    Generate all business expenses for 3 years.

    Args:
        years: list of years, default [2023, 2024, 2025, 2026]
    """
    if years is None:
        years = [2023, 2024, 2025, 2026]

    print("\n" + "=" * 60)
    print("DCNET Business Expenses Generator (3 Years)")
    print("=" * 60)

    company = _get_company()
    abbr = _get_abbr(company)

    print(f"  Company: {company} ({abbr})")

    total_created = 0
    total_errors = 0

    for year in years:
        months = 12 if year < 2026 else 3
        quarters = [1, 2, 3, 4] if year < 2026 else [1]
        print(f"\n  Year {year}: {months} months of expenses + depreciation...")

        for month in range(1, months + 1):
            created, errors = generate_monthly_expenses(company, abbr, year, month)
            total_created += created
            total_errors += errors

        for quarter in quarters:
            created = generate_quarterly_insurance(company, abbr, year, quarter)
            total_created += created

        dep_created = generate_depreciation_entries(company, abbr, year)
        total_created += dep_created
        print(f"    {year}: expenses + {dep_created} depreciation entries")

        frappe.db.commit()
        print(f"    {year}: ✅ committed")

    print("\n" + "=" * 60)
    print(f"Business Expenses Complete: {total_created} entries, {total_errors} errors")
    print("=" * 60)
    return {"created": total_created, "errors": total_errors}
