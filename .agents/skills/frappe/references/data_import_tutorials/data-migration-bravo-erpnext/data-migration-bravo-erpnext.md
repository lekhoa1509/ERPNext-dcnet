# How To: Data Migration from BRAVO to ERPNext

**Difficulty**: Advanced
**Estimated Time**: 2-3 hours
**Tags**: migration, bravo, erpnext, accounting

## Overview

Complete guide for migrating data from BRAVO accounting software to ERPNext. Covers master data, transactions, and accounting balance validation.

## Prerequisites

- Access to BRAVO database or exported Excel files
- ERPNext site configured with Company
- Understanding of Vietnamese accounting standards (Circular 200)

## Migration Strategy

### Phase 1: Master Data Migration

```
1. Chart of Accounts (Hệ thống tài khoản)
2. Cost Centers (Trung tâm chi phí)
3. Customers (Khách hàng)
4. Suppliers (Nhà cung cấp)
5. Items (Sản phẩm)
6. Employees (Nhân viên)
```

### Phase 2: Opening Balances

```
1. Account Opening Balances (Số dư đầu kỳ)
2. Customer/Supplier Outstanding (Công nợ)
3. Stock Opening (Tồn kho đầu kỳ)
```

### Phase 3: Transactions (Optional)

```
1. Historical Invoices (Hóa đơn)
2. Payment Entries (Phiếu thu/chi)
3. Journal Entries (Phiếu kế toán)
```

## Step-by-Step Guide

### Step 1: Export Data from BRAVO

```python
# Sample BRAVO export structure
BRAVO_EXPORT_STRUCTURE = {
    "dm_khachhang.xlsx": {
        "columns": ["ma_kh", "ten_kh", "dia_chi", "ma_so_thue", "dien_thoai"],
        "maps_to": "Customer"
    },
    "dm_nhacungcap.xlsx": {
        "columns": ["ma_ncc", "ten_ncc", "dia_chi", "ma_so_thue"],
        "maps_to": "Supplier"
    },
    "dm_hanghoa.xlsx": {
        "columns": ["ma_vt", "ten_vt", "dvt", "nhom_vt", "gia_ban"],
        "maps_to": "Item"
    },
    "dm_taikhoan.xlsx": {
        "columns": ["ma_tk", "ten_tk", "loai_tk", "tk_me"],
        "maps_to": "Account"
    }
}
```

### Step 2: Map BRAVO Fields to ERPNext

```python
# Field mapping configuration
BRAVO_TO_ERPNEXT_MAPPING = {
    "Customer": {
        "ma_kh": "name",
        "ten_kh": "customer_name",
        "dia_chi": None,  # Goes to Address
        "ma_so_thue": "tax_id",
        "dien_thoai": None,  # Goes to Contact
        "defaults": {
            "customer_type": "Company",
            "customer_group": "All Customer Groups",
            "territory": "Vietnam"
        }
    },
    "Supplier": {
        "ma_ncc": "name",
        "ten_ncc": "supplier_name",
        "dia_chi": None,
        "ma_so_thue": "tax_id",
        "defaults": {
            "supplier_group": "All Supplier Groups",
            "country": "Vietnam"
        }
    },
    "Item": {
        "ma_vt": "item_code",
        "ten_vt": "item_name",
        "dvt": "stock_uom",
        "nhom_vt": "item_group",
        "gia_ban": "standard_rate",
        "defaults": {
            "is_stock_item": 1,
            "include_item_in_manufacturing": 0
        }
    },
    "Account": {
        "ma_tk": "account_number",
        "ten_tk": "account_name",
        "loai_tk": "root_type",
        "tk_me": "parent_account",
        "defaults": {
            "company": "DCNET"
        }
    }
}
```

### Step 3: Import Chart of Accounts

```python
import frappe
import pandas as pd

def import_chart_of_accounts(excel_file, company):
    """
    Import Chart of Accounts from BRAVO export.
    """
    df = pd.read_excel(excel_file)

    # Map BRAVO account types to ERPNext root types
    root_type_map = {
        "1": "Asset",      # Tài sản
        "2": "Liability",  # Nợ phải trả
        "3": "Equity",     # Vốn chủ sở hữu
        "4": "Equity",     # Vốn
        "5": "Income",     # Doanh thu
        "6": "Expense",    # Chi phí
        "7": "Income",     # Thu nhập khác
        "8": "Expense"     # Chi phí khác
    }

    # Sort by account number to ensure parents created first
    df = df.sort_values("ma_tk")

    for _, row in df.iterrows():
        account_number = str(row["ma_tk"])
        root_type = root_type_map.get(account_number[0], "Asset")

        # Determine parent account
        parent_account = None
        if row.get("tk_me"):
            parent_name = frappe.db.get_value(
                "Account",
                {"account_number": row["tk_me"], "company": company},
                "name"
            )
            if parent_name:
                parent_account = parent_name

        # Check if account exists
        existing = frappe.db.exists("Account", {
            "account_number": account_number,
            "company": company
        })

        if existing:
            print(f"Skipping existing account: {account_number}")
            continue

        # Create account
        account = frappe.get_doc({
            "doctype": "Account",
            "account_name": row["ten_tk"],
            "account_number": account_number,
            "parent_account": parent_account,
            "root_type": root_type,
            "company": company,
            "is_group": 1 if len(account_number) <= 3 else 0
        })

        try:
            account.insert()
            print(f"Created: {account_number} - {row['ten_tk']}")
        except Exception as e:
            print(f"Error creating {account_number}: {e}")

    frappe.db.commit()
```

### Step 4: Import Customers with Addresses

```python
import frappe
import pandas as pd

def import_customers_from_bravo(excel_file, company):
    """
    Import Customers from BRAVO with addresses and contacts.
    """
    df = pd.read_excel(excel_file)

    for _, row in df.iterrows():
        customer_id = row["ma_kh"]

        # Check if exists
        if frappe.db.exists("Customer", customer_id):
            print(f"Skipping existing: {customer_id}")
            continue

        # Create Customer
        customer = frappe.get_doc({
            "doctype": "Customer",
            "name": customer_id,
            "customer_name": row["ten_kh"],
            "customer_type": "Company" if row.get("ma_so_thue") else "Individual",
            "customer_group": "All Customer Groups",
            "territory": "Vietnam",
            "tax_id": row.get("ma_so_thue"),
            "default_currency": "VND",
            "default_company": company
        })
        customer.insert()

        # Create Address if available
        if row.get("dia_chi"):
            address = frappe.get_doc({
                "doctype": "Address",
                "address_title": row["ten_kh"],
                "address_type": "Billing",
                "address_line1": row["dia_chi"],
                "city": extract_city(row["dia_chi"]),
                "country": "Vietnam",
                "links": [{
                    "link_doctype": "Customer",
                    "link_name": customer.name
                }]
            })
            address.insert()

        # Create Contact if phone available
        if row.get("dien_thoai"):
            contact = frappe.get_doc({
                "doctype": "Contact",
                "first_name": row["ten_kh"],
                "phone": row["dien_thoai"],
                "is_primary_contact": 1,
                "links": [{
                    "link_doctype": "Customer",
                    "link_name": customer.name
                }]
            })
            contact.insert()

        print(f"Created customer: {customer_id}")

    frappe.db.commit()

def extract_city(address):
    """Extract city from Vietnamese address."""
    cities = ["Hà Nội", "TP. Hồ Chí Minh", "Đà Nẵng", "Hải Phòng"]
    for city in cities:
        if city.lower() in address.lower():
            return city
    return ""
```

### Step 5: Import Items with UOM Mapping

```python
import frappe
import pandas as pd

def import_items_from_bravo(excel_file, company):
    """
    Import Items from BRAVO with UOM mapping.
    """
    # UOM mapping (BRAVO -> ERPNext)
    uom_map = {
        "Cái": "Nos",
        "Chiếc": "Nos",
        "Bộ": "Set",
        "Hộp": "Box",
        "Kg": "Kg",
        "Mét": "Meter",
        "Tá": "Dozen"
    }

    df = pd.read_excel(excel_file)

    for _, row in df.iterrows():
        item_code = row["ma_vt"]

        if frappe.db.exists("Item", item_code):
            print(f"Skipping existing: {item_code}")
            continue

        # Map UOM
        bravo_uom = row.get("dvt", "Nos")
        stock_uom = uom_map.get(bravo_uom, "Nos")

        # Ensure UOM exists
        if not frappe.db.exists("UOM", stock_uom):
            frappe.get_doc({
                "doctype": "UOM",
                "uom_name": stock_uom
            }).insert()

        # Map Item Group
        item_group = map_item_group(row.get("nhom_vt"))

        # Create Item
        item = frappe.get_doc({
            "doctype": "Item",
            "item_code": item_code,
            "item_name": row["ten_vt"],
            "item_group": item_group,
            "stock_uom": stock_uom,
            "is_stock_item": 1,
            "is_purchase_item": 1,
            "is_sales_item": 1,
            "standard_rate": row.get("gia_ban", 0),
            "default_warehouse": f"Stores - {company[:2]}"
        })
        item.insert()

        print(f"Created item: {item_code}")

    frappe.db.commit()

def map_item_group(bravo_group):
    """Map BRAVO item group to ERPNext."""
    group_map = {
        "GAY": "Golf Clubs",
        "BONG": "Golf Balls",
        "PHUKIEN": "Golf Accessories",
        "QUANAO": "Golf Apparel"
    }
    return group_map.get(bravo_group, "All Item Groups")
```

### Step 6: Import Opening Balances

```python
import frappe
from frappe.utils import today

def import_opening_balances(excel_file, company, fiscal_year):
    """
    Import opening account balances from BRAVO.
    """
    df = pd.read_excel(excel_file)

    # Create Opening Journal Entry
    je = frappe.new_doc("Journal Entry")
    je.posting_date = frappe.db.get_value(
        "Fiscal Year", fiscal_year, "year_start_date"
    )
    je.company = company
    je.voucher_type = "Opening Entry"
    je.is_opening = "Yes"

    total_debit = 0
    total_credit = 0

    for _, row in df.iterrows():
        account_number = str(row["ma_tk"])

        # Get ERPNext account name
        account_name = frappe.db.get_value(
            "Account",
            {"account_number": account_number, "company": company},
            "name"
        )

        if not account_name:
            print(f"Account not found: {account_number}")
            continue

        debit = float(row.get("so_du_no", 0) or 0)
        credit = float(row.get("so_du_co", 0) or 0)

        if debit or credit:
            je.append("accounts", {
                "account": account_name,
                "debit_in_account_currency": debit,
                "credit_in_account_currency": credit
            })
            total_debit += debit
            total_credit += credit

    # Balance entry to Temporary Opening
    if total_debit != total_credit:
        temp_account = frappe.db.get_value(
            "Account",
            {"account_type": "Temporary", "company": company},
            "name"
        )
        if total_debit > total_credit:
            je.append("accounts", {
                "account": temp_account,
                "credit_in_account_currency": total_debit - total_credit
            })
        else:
            je.append("accounts", {
                "account": temp_account,
                "debit_in_account_currency": total_credit - total_debit
            })

    je.insert()
    je.submit()

    print(f"Created Opening Entry: {je.name}")
    return je.name
```

### Step 7: Import Customer/Supplier Outstanding

```python
def import_outstanding_balances(excel_file, company, posting_date):
    """
    Import customer/supplier outstanding balances.
    """
    df = pd.read_excel(excel_file)

    for _, row in df.iterrows():
        party_type = "Customer" if row["loai"] == "KH" else "Supplier"
        party = row["ma_dt"]

        if not frappe.db.exists(party_type, party):
            print(f"{party_type} not found: {party}")
            continue

        amount = float(row.get("so_du", 0))
        if not amount:
            continue

        # Create Journal Entry for outstanding
        je = frappe.new_doc("Journal Entry")
        je.posting_date = posting_date
        je.company = company
        je.voucher_type = "Opening Entry"
        je.is_opening = "Yes"

        # Determine account
        if party_type == "Customer":
            account = frappe.db.get_value(
                "Company", company, "default_receivable_account"
            )
        else:
            account = frappe.db.get_value(
                "Company", company, "default_payable_account"
            )

        temp_account = frappe.db.get_value(
            "Account",
            {"account_type": "Temporary", "company": company},
            "name"
        )

        if amount > 0:  # Receivable/Payable
            je.append("accounts", {
                "account": account,
                "party_type": party_type,
                "party": party,
                "debit_in_account_currency": abs(amount)
            })
            je.append("accounts", {
                "account": temp_account,
                "credit_in_account_currency": abs(amount)
            })
        else:  # Advance/Overpayment
            je.append("accounts", {
                "account": account,
                "party_type": party_type,
                "party": party,
                "credit_in_account_currency": abs(amount)
            })
            je.append("accounts", {
                "account": temp_account,
                "debit_in_account_currency": abs(amount)
            })

        je.insert()
        je.submit()

        print(f"Created outstanding for {party}: {amount}")

    frappe.db.commit()
```

### Step 8: Validate Migration

```python
def validate_migration(company, bravo_trial_balance_file):
    """
    Validate ERPNext balances match BRAVO trial balance.
    """
    from erpnext.accounts.report.trial_balance.trial_balance import execute

    # Get ERPNext Trial Balance
    filters = {
        "company": company,
        "fiscal_year": frappe.defaults.get_user_default("fiscal_year"),
        "from_date": frappe.db.get_value(
            "Fiscal Year",
            frappe.defaults.get_user_default("fiscal_year"),
            "year_start_date"
        ),
        "to_date": today()
    }

    columns, erpnext_data = execute(filters)

    # Load BRAVO data
    bravo_df = pd.read_excel(bravo_trial_balance_file)

    # Compare
    mismatches = []

    for _, bravo_row in bravo_df.iterrows():
        account_number = str(bravo_row["ma_tk"])

        # Find in ERPNext
        erpnext_row = next(
            (r for r in erpnext_data if r.get("account_number") == account_number),
            None
        )

        if not erpnext_row:
            mismatches.append({
                "account": account_number,
                "issue": "Not found in ERPNext"
            })
            continue

        bravo_balance = float(bravo_row.get("so_du", 0))
        erpnext_balance = float(erpnext_row.get("closing_debit", 0)) - \
                          float(erpnext_row.get("closing_credit", 0))

        if abs(bravo_balance - erpnext_balance) > 0.01:
            mismatches.append({
                "account": account_number,
                "bravo": bravo_balance,
                "erpnext": erpnext_balance,
                "diff": bravo_balance - erpnext_balance
            })

    return mismatches
```

## Complete Migration Script

```python
import frappe

class BravoMigration:
    """Complete BRAVO to ERPNext migration."""

    def __init__(self, company, files_dir):
        self.company = company
        self.files_dir = files_dir
        self.results = {}

    def run_full_migration(self):
        """Run complete migration."""
        steps = [
            ("Chart of Accounts", self.migrate_coa),
            ("Customers", self.migrate_customers),
            ("Suppliers", self.migrate_suppliers),
            ("Items", self.migrate_items),
            ("Opening Balances", self.migrate_opening_balances),
            ("Outstanding", self.migrate_outstanding),
        ]

        for step_name, step_func in steps:
            print(f"\n{'='*50}")
            print(f"Step: {step_name}")
            print('='*50)

            try:
                result = step_func()
                self.results[step_name] = {"status": "Success", "result": result}
            except Exception as e:
                self.results[step_name] = {"status": "Error", "error": str(e)}
                frappe.log_error(f"Migration error: {step_name}")

        return self.results

    def migrate_coa(self):
        file_path = f"{self.files_dir}/dm_taikhoan.xlsx"
        import_chart_of_accounts(file_path, self.company)

    def migrate_customers(self):
        file_path = f"{self.files_dir}/dm_khachhang.xlsx"
        import_customers_from_bravo(file_path, self.company)

    def migrate_suppliers(self):
        file_path = f"{self.files_dir}/dm_nhacungcap.xlsx"
        import_suppliers_from_bravo(file_path, self.company)

    def migrate_items(self):
        file_path = f"{self.files_dir}/dm_hanghoa.xlsx"
        import_items_from_bravo(file_path, self.company)

    def migrate_opening_balances(self):
        file_path = f"{self.files_dir}/so_du_dau_ky.xlsx"
        fiscal_year = frappe.defaults.get_user_default("fiscal_year")
        import_opening_balances(file_path, self.company, fiscal_year)

    def migrate_outstanding(self):
        file_path = f"{self.files_dir}/cong_no.xlsx"
        posting_date = frappe.db.get_value(
            "Fiscal Year",
            frappe.defaults.get_user_default("fiscal_year"),
            "year_start_date"
        )
        import_outstanding_balances(file_path, self.company, posting_date)


# Usage
migration = BravoMigration("DCNET", "/home/frappe/bravo_exports")
results = migration.run_full_migration()

# Validate
mismatches = validate_migration("DCNET", "/home/frappe/bravo_exports/bang_can_doi.xlsx")
if mismatches:
    print("Validation issues found:")
    for m in mismatches:
        print(f"  {m}")
else:
    print("Migration validated successfully!")
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Account mismatch | Different COA structure | Review account mapping |
| Missing customers | Encoding issues | Use UTF-8 encoding |
| Balance difference | Rounding | Check precision settings |
| Duplicate entries | Re-running migration | Clear and restart |

## Next Steps

- [Performance Optimization](../performance-optimization/performance-optimization.md)
- [Rollback and Recovery](../rollback-recovery/rollback-recovery.md)

---

*Last updated: 2026-02-04*
