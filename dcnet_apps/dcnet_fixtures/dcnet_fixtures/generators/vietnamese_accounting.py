"""
Vietnamese Accounting (TT200) Generator for DCNET 3-Year Data

This module handles:
1. Chart of Accounts (COA) normalization to TT200 standard.
2. Initial Capital injection.
3. Fixed Asset (TSCĐ) lifecycle: Purchase -> Depreciation -> Disposal.
4. Tool (CCDC) lifecycle: Purchase -> Amortization.
"""

import frappe
from frappe.utils import getdate, add_months
from random import uniform

# =============================================================================
# TT200 COA CONFIGURATION
# =============================================================================

TT200_MAPPING = [
    # Asset
    {"number": "1111", "name": "Tiền mặt", "type": "Cash", "root": "Asset", "parent_hint": "Cash"},
    {"number": "1121", "name": "Tiền gửi Ngân hàng (Techcombank)", "type": "Bank", "root": "Asset", "parent_hint": "Bank"},
    {"number": "1122", "name": "Tiền gửi Ngân hàng (Vietcombank)", "type": "Bank", "root": "Asset", "parent_hint": "Bank"},
    {"number": "131",  "name": "Phải thu của khách hàng", "type": "Receivable", "root": "Asset", "parent_hint": "Receivable"},
    {"number": "1331", "name": "Thuế GTGT được khấu trừ của HHDV", "type": "Tax", "root": "Asset", "parent_hint": "Tax"},
    {"number": "153",  "name": "Công cụ, dụng cụ", "type": "Stock", "root": "Asset", "parent_hint": "Stock"},
    {"number": "156",  "name": "Hàng hóa", "type": "Stock", "root": "Asset", "parent_hint": "Stock"},
    {"number": "2111", "name": "TSCĐ hữu hình", "type": "Fixed Asset", "root": "Asset", "parent_hint": "Fixed Asset"},
    {"number": "2141", "name": "Hao mòn TSCĐ hữu hình", "type": "Accumulated Depreciation", "root": "Asset", "parent_hint": "Accumulated Depreciation"},
    {"number": "242",  "name": "Chi phí trả trước", "type": "", "root": "Asset", "parent_hint": "Asset"},
    
    # Liability
    {"number": "331",  "name": "Phải trả cho người bán", "type": "Payable", "root": "Liability", "parent_hint": "Payable"},
    {"number": "3331", "name": "Thuế GTGT phải nộp", "type": "Tax", "root": "Liability", "parent_hint": "Tax"},
    {"number": "334",  "name": "Phải trả người lao động", "type": "", "root": "Liability", "parent_hint": "Liability"},
    {"number": "3383", "name": "Bảo hiểm xã hội", "type": "", "root": "Liability", "parent_hint": "Liability"},
    {"number": "3384", "name": "Bảo hiểm y tế", "type": "", "root": "Liability", "parent_hint": "Liability"},
    
    # Equity
    {"number": "4111", "name": "Vốn góp của chủ sở hữu", "type": "Equity", "root": "Equity", "parent_hint": "Equity"},
    {"number": "4212", "name": "Lợi nhuận chưa phân phối năm nay", "type": "Equity", "root": "Equity", "parent_hint": "Equity"},
    
    # Income
    {"number": "5111", "name": "Doanh thu bán hàng hóa", "type": "Income Account", "root": "Income", "parent_hint": "Income"},
    {"number": "515",  "name": "Doanh thu hoạt động tài chính", "type": "Income Account", "root": "Income", "parent_hint": "Income"},
    {"number": "711",  "name": "Thu nhập khác", "type": "Income Account", "root": "Income", "parent_hint": "Income"},
    
    # Expense
    {"number": "632",  "name": "Giá vốn hàng bán", "type": "Cost of Goods Sold", "root": "Expense", "parent_hint": "Expense"},
    {"number": "6411", "name": "Chi phí nhân viên bán hàng", "type": "Expense Account", "root": "Expense", "parent_hint": "Expense"},
    {"number": "6421", "name": "Chi phí nhân viên quản lý", "type": "Expense Account", "root": "Expense", "parent_hint": "Expense"},
    {"number": "6422", "name": "Chi phí vật liệu quản lý", "type": "Expense Account", "root": "Expense", "parent_hint": "Expense"},
    {"number": "6423", "name": "Chi phí đồ dùng văn phòng", "type": "Expense Account", "root": "Expense", "parent_hint": "Expense"},
    {"number": "6424", "name": "Chi phí khấu hao TSCĐ", "type": "Expense Account", "root": "Expense", "parent_hint": "Expense"},
    {"number": "6427", "name": "Chi phí dịch vụ mua ngoài", "type": "Expense Account", "root": "Expense", "parent_hint": "Expense"},
    {"number": "811",  "name": "Chi phí khác", "type": "Expense Account", "root": "Expense", "parent_hint": "Expense"},
]

def _get_company_info():
    company = frappe.db.get_single_value("Global Defaults", "default_company") or \
              frappe.db.get_value("Company", {}, "name")
    abbr = frappe.db.get_value("Company", company, "abbr")
    return company, abbr

def setup_tt200_coa():
    """Inject TT200 accounts into Chart of Accounts"""
    print("\n[Accounting] Normalizing COA to TT200 standard...")
    company, abbr = _get_company_info()
    
    created = 0
    updated = 0
    
    for item in TT200_MAPPING:
        # Construct full account name: "Number - Name - Abbr"
        # ERPNext usually stores Account Name as "Name - Abbr" or "Number - Name - Abbr"
        # We search by account_number first
        existing = frappe.db.get_value("Account", {"account_number": item["number"], "company": company}, "name")
        
        if not existing:
            # Search by name hint
            existing = frappe.db.get_value("Account", {"account_name": ["like", f"%{item['name']}%"], "company": company}, "name")
            
        if existing:
            # Update existing to match TT200
            acc = frappe.get_doc("Account", existing)
            acc.account_number = item["number"]
            # To avoid "X - X - Name" we strip existing numbers if present
            acc.account_name = item["name"]
            if item["type"]:
                acc.account_type = item["type"]
            acc.flags.ignore_permissions = True
            acc.save()
            updated += 1
        else:
            # Create new
            # Find parent
            parent = _find_parent_account(company, item["root"], item["parent_hint"])
            if not parent:
                print(f"  ⚠️ Could not find parent for {item['number']} {item['name']}, skipping...")
                continue
                
            acc = frappe.get_doc({
                "doctype": "Account",
                "account_name": item["name"],
                "account_number": item["number"],
                "parent_account": parent,
                "company": company,
                "account_type": item["type"],
                "root_type": item["root"]
            })
            acc.flags.ignore_permissions = True
            acc.insert()
            created += 1
            
    frappe.db.commit()
    print(f"  ✅ TT200 COA Ready: {created} created, {updated} updated.")

def _find_parent_account(company, root_type, hint):
    """Fallback search for parent account"""
    # 1. Search by exact type and root
    if hint:
        match = frappe.db.get_value("Account", {
            "company": company,
            "root_type": root_type,
            "account_type": hint,
            "is_group": 1
        }, "name")
        if match: return match
        
    # 2. Search by root name (ERPNext defaults)
    roots = {
        "Asset": ["Application of Funds (Assets)", "Assets", "Tài sản"],
        "Liability": ["Source of Funds (Liabilities)", "Liabilities", "Nợ phải trả"],
        "Equity": ["Equity", "Vốn chủ sở hữu"],
        "Income": ["Income", "Doanh thu"],
        "Expense": ["Expenses", "Chi phí"]
    }
    company_abbr = frappe.db.get_value("Company", company, "abbr")
    
    for r_name in roots.get(root_type, []):
        full = f"{r_name} - {company_abbr}"
        if frappe.db.exists("Account", full):
            return full
            
    # 3. Final fallback: any group in that root
    return frappe.db.get_value("Account", {"company": company, "root_type": root_type, "is_group": 1}, "name")

# =============================================================================
# INITIAL CAPITAL
# =============================================================================

def create_initial_capital():
    """Inject 10B VND capital at 2023-01-01"""
    print("\n[Accounting] Injecting Initial Capital (10B VND)...")
    company, abbr = _get_company_info()
    
    posting_date = "2023-01-01"
    
    # Check if already exists
    if frappe.db.exists("Journal Entry", {"remark": ["like", "%Initial Capital%"], "company": company}):
        print("  Initial Capital already exists, skipping...")
        return
        
    cash = frappe.db.get_value("Account", {"account_number": "1111", "company": company}, "name")
    bank = frappe.db.get_value("Account", {"account_number": "1121", "company": company}, "name")
    equity = frappe.db.get_value("Account", {"account_number": "4111", "company": company}, "name")
    
    if not all([cash, bank, equity]):
        print("  ⚠️ Missing core accounts (1111, 1121, or 4111) for capital injection.")
        return

    je = frappe.get_doc({
        "doctype": "Journal Entry",
        "company": company,
        "posting_date": posting_date,
        "remark": "Initial Capital Contribution from Owners",
        "accounts": [
            {"account": cash, "debit_in_account_currency": 2_000_000_000},
            {"account": bank, "debit_in_account_currency": 8_000_000_000},
            {"account": equity, "credit_in_account_currency": 10_000_000_000}
        ]
    })
    je.flags.ignore_permissions = True
    je.insert()
    je.submit()
    frappe.db.commit()
    print("  ✅ 10B VND Capital Injected via Journal Entry.")

# =============================================================================
# ASSET LIFECYCLE
# =============================================================================

def setup_assets_and_tools():
    """Create Asset purchases and monthly depreciation"""
    print("\n[Accounting] Generating Asset/Tool lifecycle data...")
    company, abbr = _get_company_info()
    
    # 1. Purchase Truck (TSCĐ) - 2023-02-15
    _create_asset_purchase(
        company, "Xe tải giao hàng Hyundai", "2023-02-15", 
        amount=650_000_000, acc_number="2111", dep_acc="2141"
    )
    
    # 2. Purchase Laptops (CCDC) - 2023-01-10
    _create_asset_purchase(
        company, "Lô 5 máy tính Dell", "2023-01-10", 
        amount=120_000_000, acc_number="242", is_tool=True
    )
    
    # 3. Monthly Depreciation/Amortization entries
    _generate_all_depreciation(company)
    
    # 4. Disposal of a small equipment in 2025
    _liquidate_asset_2025(company)
    
    frappe.db.commit()

def _create_asset_purchase(company, name, date, amount, acc_number, dep_acc=None, is_tool=False):
    """Simple purchase entry for asset (using Journal Entry to avoid Asset module complexity)"""
    if frappe.db.exists("Journal Entry", {"remark": ["like", f"%Mua {name}%"], "company": company}):
        return

    bank = frappe.db.get_value("Account", {"account_number": "1121", "company": company}, "name")
    asset_acc = frappe.db.get_value("Account", {"account_number": acc_number, "company": company}, "name")
    vat_acc = frappe.db.get_value("Account", {"account_number": "1331", "company": company}, "name")
    
    if not all([bank, asset_acc, vat_acc]): return

    vat_amount = amount * 0.1
    
    je = frappe.get_doc({
        "doctype": "Journal Entry",
        "company": company,
        "posting_date": date,
        "remark": f"Mua {name}",
        "accounts": [
            {"account": asset_acc, "debit_in_account_currency": amount},
            {"account": vat_acc, "debit_in_account_currency": vat_amount},
            {"account": bank, "credit_in_account_currency": amount + vat_amount}
        ]
    })
    je.flags.ignore_permissions = True
    je.insert()
    je.submit()

def _generate_all_depreciation(company):
    """Simulate monthly depreciation entries via JV"""
    # 1111 -> 33 months approx
    start_date = getdate("2023-03-01")
    end_date = getdate("2026-03-01")
    
    # Truck: 650M / 60 months = 10.8M/month
    # Laptops: 120M / 24 months = 5M/month
    
    dep_acc = frappe.db.get_value("Account", {"account_number": "2141", "company": company}, "name")
    amort_acc = frappe.db.get_value("Account", {"account_number": "242", "company": company}, "name")
    expense_acc = frappe.db.get_value("Account", {"account_number": "6424", "company": company}, "name")
    
    if not all([dep_acc, amort_acc, expense_acc]): return

    current = start_date
    while current <= end_date:
        posting_date = add_months(current, 0)
        remark = f"Khấu hao & Phân bổ tháng {posting_date.month}/{posting_date.year}"
        
        if not frappe.db.exists("Journal Entry", {"remark": remark, "company": company}):
            je = frappe.get_doc({
                "doctype": "Journal Entry",
                "company": company,
                "posting_date": posting_date,
                "remark": remark,
                "accounts": [
                    {"account": expense_acc, "debit_in_account_currency": 15_800_000},
                    {"account": dep_acc, "credit_in_account_currency": 10_800_000},
                    {"account": amort_acc, "credit_in_account_currency": 5_000_000}
                ]
            })
            je.flags.ignore_permissions = True
            je.insert()
            je.submit()
            
        current = add_months(current, 1)

def _liquidate_asset_2025(company):
    """Liquidate a small portion of assets in 2025-06-15"""
    date = "2025-06-15"
    if frappe.db.exists("Journal Entry", {"remark": "Thanh lý tài sản cố định cũ", "company": company}):
        return

    bank = frappe.db.get_value("Account", {"account_number": "1121", "company": company}, "name")
    asset_acc = frappe.db.get_value("Account", {"account_number": "2111", "company": company}, "name")
    dep_acc = frappe.db.get_value("Account", {"account_number": "2141", "company": company}, "name")
    income_acc = frappe.db.get_value("Account", {"account_number": "711", "company": company}, "name")
    expense_acc = frappe.db.get_value("Account", {"account_number": "811", "company": company}, "name")
    
    if not all([bank, asset_acc, dep_acc, income_acc, expense_acc]): return

    # Sell for 50M (Income), Net Book Value 40M (Exp)
    # Original Cost 100M, Acc Dep 60M
    
    je = frappe.get_doc({
        "doctype": "Journal Entry",
        "company": company,
        "posting_date": date,
        "remark": "Thanh lý tài sản cố định cũ",
        "accounts": [
            {"account": bank, "debit_in_account_currency": 50_000_000},
            {"account": income_acc, "credit_in_account_currency": 50_000_000},
            
            {"account": dep_acc, "debit_in_account_currency": 60_000_000},
            {"account": expense_acc, "debit_in_account_currency": 40_000_000},
            {"account": asset_acc, "credit_in_account_currency": 100_000_000}
        ]
    })
    je.flags.ignore_permissions = True
    je.insert()
    je.submit()

# =============================================================================
# ORCHESTRATOR
# =============================================================================

def setup_all_vietnamese_accounting():
    """Run all accounting setup steps"""
    setup_tt200_coa()
    create_initial_capital()
    setup_assets_and_tools()
    return True
