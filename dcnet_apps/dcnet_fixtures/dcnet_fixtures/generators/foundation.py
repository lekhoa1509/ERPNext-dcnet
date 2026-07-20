"""
Foundation Setup Generator for DCNET 3-Year Data

Creates:
- Fiscal Years (2023, 2024, 2025 - 2026 already exists)
- Cost Centers (department structure)
- Warehouses (HCM main, HN showroom, Fitting, Transit, Returns)
- Tax Templates (Vietnam VAT 10%, 8%, 0%, Purchase VAT 10%)
- Departments
- Mode of Payment extensions (QR Pay/MoMo)

Growth Config used across all generators:
    GROWTH_CONFIG = {
        2023: multiplier=1.0,  avg_order_value=15M, margin=0.25
        2024: multiplier=1.5,  avg_order_value=18M, margin=0.28
        2025: multiplier=2.25, avg_order_value=22M, margin=0.30
        2026: multiplier=3.375, avg_order_value=25M, margin=0.32
    }
"""

import frappe
from frappe.utils import getdate


# =============================================================================
# GROWTH CONFIG - shared by all generators
# =============================================================================

GROWTH_CONFIG = {
    2023: {"multiplier": 1.0,   "avg_order_value": 15_000_000, "margin": 0.25, "so_per_quarter": 30, "po_per_quarter": 20},
    2024: {"multiplier": 1.5,   "avg_order_value": 18_000_000, "margin": 0.28, "so_per_quarter": 45, "po_per_quarter": 30},
    2025: {"multiplier": 2.25,  "avg_order_value": 22_000_000, "margin": 0.30, "so_per_quarter": 68, "po_per_quarter": 45},
    2026: {"multiplier": 3.375, "avg_order_value": 25_000_000, "margin": 0.32, "so_per_quarter": 85, "po_per_quarter": 55},
}

# Seasonal multipliers per quarter
SEASONAL_MULTIPLIERS = {
    1: 1.2,   # Q1: After Tet, golf season starts
    2: 0.8,   # Q2: Low season
    3: 0.85,  # Q3: Low-medium
    4: 1.3,   # Q4: Tet gifts, year-end orders
}


# =============================================================================
# FISCAL YEARS
# =============================================================================

def setup_fiscal_years():
    """Create Fiscal Years 2023, 2024, 2025 (2026 already exists)"""
    print("\n[Foundation] Setting up Fiscal Years...")
    created = []

    years_to_create = [
        {"name": "2023", "year_start_date": "2023-01-01", "year_end_date": "2023-12-31"},
        {"name": "2024", "year_start_date": "2024-01-01", "year_end_date": "2024-12-31"},
        {"name": "2025", "year_start_date": "2025-01-01", "year_end_date": "2025-12-31"},
    ]

    for year_data in years_to_create:
        if frappe.db.exists("Fiscal Year", year_data["name"]):
            print(f"  Fiscal Year {year_data['name']} already exists, skipping...")
            continue

        try:
            fy = frappe.get_doc({
                "doctype": "Fiscal Year",
                "year": year_data["name"],
                "year_start_date": year_data["year_start_date"],
                "year_end_date": year_data["year_end_date"],
            })
            fy.flags.ignore_permissions = True
            fy.insert()
            created.append(year_data["name"])
            print(f"  ✅ Created Fiscal Year {year_data['name']}")
        except Exception as e:
            print(f"  ⚠️  Error creating Fiscal Year {year_data['name']}: {e}")

    frappe.db.commit()
    print(f"  Created {len(created)} fiscal years")
    return created


# =============================================================================
# COST CENTERS
# =============================================================================

def setup_cost_centers():
    """Create department-based Cost Centers"""
    print("\n[Foundation] Setting up Cost Centers...")

    company = frappe.db.get_single_value("Global Defaults", "default_company") or \
              frappe.db.get_value("Company", {}, "name")
    abbr = frappe.db.get_value("Company", company, "abbr")
    root_cc = f"{company} - {abbr}"

    cost_centers = [
        # (name, parent, is_group)
        ("Ban Giám đốc",     root_cc,                  0),
        ("Kinh doanh",       root_cc,                  1),
        ("Bán lẻ",           f"Kinh doanh - {abbr}",   0),
        ("Bán sỉ",           f"Kinh doanh - {abbr}",   0),
        ("Kho vận",          root_cc,                  0),
        ("Kế toán",          root_cc,                  0),
        ("Fitting & Dịch vụ", root_cc,                 0),
        ("Marketing",        root_cc,                  0),
    ]

    created = []
    for (cc_name, parent, is_group) in cost_centers:
        full_name = f"{cc_name} - {abbr}"
        if frappe.db.exists("Cost Center", full_name):
            print(f"  Cost Center '{full_name}' already exists, skipping...")
            continue

        # Ensure parent exists
        if not frappe.db.exists("Cost Center", parent):
            print(f"  ⚠️  Parent '{parent}' not found, skipping '{full_name}'")
            continue

        try:
            cc = frappe.get_doc({
                "doctype": "Cost Center",
                "cost_center_name": cc_name,
                "parent_cost_center": parent,
                "company": company,
                "is_group": is_group,
            })
            cc.flags.ignore_permissions = True
            cc.insert()
            created.append(full_name)
            print(f"  ✅ Created Cost Center: {full_name}")
        except Exception as e:
            print(f"  ⚠️  Error creating Cost Center '{full_name}': {e}")

    frappe.db.commit()
    print(f"  Created {len(created)} cost centers")
    return created


# =============================================================================
# WAREHOUSES
# =============================================================================

def setup_warehouses():
    """Create business warehouses"""
    print("\n[Foundation] Setting up Warehouses...")

    company = frappe.db.get_single_value("Global Defaults", "default_company") or \
              frappe.db.get_value("Company", {}, "name")
    abbr = frappe.db.get_value("Company", company, "abbr")
    root_wh = f"All Warehouses - {abbr}"

    warehouses = [
        ("Kho Chính HCM",           root_wh, 0),
        ("Kho Showroom Hà Nội",     root_wh, 0),
        ("Kho Fitting",             root_wh, 0),
        ("Kho Hàng Đang Chuyển",    root_wh, 0),
        ("Kho Lỗi Trả Hàng",       root_wh, 0),
    ]

    created = []
    for (wh_name, parent, is_group) in warehouses:
        full_name = f"{wh_name} - {abbr}"
        if frappe.db.exists("Warehouse", full_name):
            print(f"  Warehouse '{full_name}' already exists, skipping...")
            continue

        try:
            wh = frappe.get_doc({
                "doctype": "Warehouse",
                "warehouse_name": wh_name,
                "parent_warehouse": parent,
                "company": company,
                "is_group": is_group,
            })
            wh.flags.ignore_permissions = True
            wh.insert()
            created.append(full_name)
            print(f"  ✅ Created Warehouse: {full_name}")
        except Exception as e:
            print(f"  ⚠️  Error creating Warehouse '{full_name}': {e}")

    frappe.db.commit()
    print(f"  Created {len(created)} warehouses")
    return created


# =============================================================================
# TAX TEMPLATES
# =============================================================================

def _get_tax_account(company, account_type="Tax"):
    """Get or find a suitable tax account for the company"""
    abbr = frappe.db.get_value("Company", company, "abbr")

    # Try common tax account names
    candidates = [
        f"VAT - {abbr}",
        f"Tax Assets - {abbr}",
        f"Output Tax - {abbr}",
        f"Sales Tax - {abbr}",
    ]
    for acc in candidates:
        if frappe.db.exists("Account", acc):
            return acc

    # Fallback: find any tax account
    tax_acc = frappe.db.get_value("Account", {
        "company": company,
        "account_type": "Tax",
        "is_group": 0,
    }, "name")
    return tax_acc


def setup_tax_templates():
    """Create Vietnam VAT tax templates"""
    print("\n[Foundation] Setting up Tax Templates...")

    company = frappe.db.get_single_value("Global Defaults", "default_company") or \
              frappe.db.get_value("Company", {}, "name")
    abbr = frappe.db.get_value("Company", company, "abbr")

    tax_account = _get_tax_account(company)
    if not tax_account:
        print("  ⚠️  No tax account found, skipping tax templates")
        return []

    print(f"  Using tax account: {tax_account}")

    sales_templates = [
        {
            "name": f"VAT 10% Bán Hàng - {abbr}",
            "title": "VAT 10% - Bán hàng",
            "rate": 10.0,
        },
        {
            "name": f"VAT 8% Dịch Vụ - {abbr}",
            "title": "VAT 8% - Dịch vụ Fitting",
            "rate": 8.0,
        },
        {
            "name": f"Không VAT - {abbr}",
            "title": "Không chịu thuế VAT",
            "rate": 0.0,
        },
    ]

    purchase_templates = [
        {
            "name": f"VAT 10% Mua Hàng - {abbr}",
            "title": "VAT 10% - Mua hàng",
            "rate": 10.0,
        },
    ]

    created = []

    # Sales tax templates
    for tpl in sales_templates:
        if frappe.db.exists("Sales Taxes and Charges Template", tpl["name"]):
            print(f"  Sales Tax Template '{tpl['name']}' already exists, skipping...")
            continue
        try:
            doc = frappe.get_doc({
                "doctype": "Sales Taxes and Charges Template",
                "title": tpl["title"],
                "company": company,
                "taxes": [{
                    "charge_type": "On Net Total",
                    "account_head": tax_account,
                    "description": tpl["title"],
                    "rate": tpl["rate"],
                }] if tpl["rate"] > 0 else [],
            })
            doc.flags.ignore_permissions = True
            doc.insert()
            created.append(tpl["name"])
            print(f"  ✅ Created Sales Tax Template: {tpl['title']}")
        except Exception as e:
            print(f"  ⚠️  Error: {e}")

    # Purchase tax templates
    for tpl in purchase_templates:
        if frappe.db.exists("Purchase Taxes and Charges Template", tpl["name"]):
            print(f"  Purchase Tax Template '{tpl['name']}' already exists, skipping...")
            continue
        try:
            doc = frappe.get_doc({
                "doctype": "Purchase Taxes and Charges Template",
                "title": tpl["title"],
                "company": company,
                "taxes": [{
                    "charge_type": "On Net Total",
                    "account_head": tax_account,
                    "description": tpl["title"],
                    "rate": tpl["rate"],
                }],
            })
            doc.flags.ignore_permissions = True
            doc.insert()
            created.append(tpl["name"])
            print(f"  ✅ Created Purchase Tax Template: {tpl['title']}")
        except Exception as e:
            print(f"  ⚠️  Error: {e}")

    frappe.db.commit()
    print(f"  Created {len(created)} tax templates")
    return created


# =============================================================================
# DEPARTMENTS
# =============================================================================

def setup_departments():
    """Create company departments"""
    print("\n[Foundation] Setting up Departments...")

    company = frappe.db.get_single_value("Global Defaults", "default_company") or \
              frappe.db.get_value("Company", {}, "name")

    departments = [
        "Ban Giám đốc",
        "Kinh doanh",
        "Kho vận",
        "Kế toán",
        "Dịch vụ Fitting",
        "Marketing",
        "IT",
    ]

    created = []
    for dept_name in departments:
        full = f"{dept_name} - {company}"
        if frappe.db.exists("Department", full):
            print(f"  Department '{full}' already exists, skipping...")
            continue
        try:
            dept = frappe.get_doc({
                "doctype": "Department",
                "department_name": dept_name,
                "company": company,
                "is_group": 0,
            })
            dept.flags.ignore_permissions = True
            dept.insert()
            created.append(full)
            print(f"  ✅ Created Department: {full}")
        except Exception as e:
            dept_name_only = dept_name
            # try without company suffix
            if frappe.db.exists("Department", dept_name_only):
                print(f"  Department '{dept_name_only}' already exists, skipping...")
            else:
                print(f"  ⚠️  Error creating Department '{dept_name}': {e}")

    frappe.db.commit()
    print(f"  Created {len(created)} departments")
    return created


# =============================================================================
# MAIN SETUP FUNCTION
# =============================================================================

def setup_all_foundation():
    """Run all foundation setup steps"""
    print("\n" + "=" * 60)
    print("DCNET Foundation Setup - 3 Year Data")
    print("=" * 60)

    results = {}

    print("\n[1/5] Setting up Fiscal Years...")
    results["fiscal_years"] = setup_fiscal_years()

    print("\n[2/5] Setting up Cost Centers...")
    results["cost_centers"] = setup_cost_centers()

    print("\n[3/5] Setting up Warehouses...")
    results["warehouses"] = setup_warehouses()

    print("\n[4/5] Setting up Tax Templates...")
    results["tax_templates"] = setup_tax_templates()

    print("\n[5/5] Setting up Departments...")
    results["departments"] = setup_departments()

    frappe.db.commit()

    print("\n" + "=" * 60)
    print("Foundation Setup Complete!")
    for key, val in results.items():
        print(f"  {key}: {len(val)} created")
    print("=" * 60)
    return results
