# API Reference: Chart of Accounts Importer (ERPNext)

**Language**: Python

**Source**: `erpnext/accounts/doctype/chart_of_accounts_importer/`

---

## Overview

The Chart of Accounts Importer allows importing a complete chart of accounts from CSV/Excel into ERPNext. It creates Account records with proper hierarchy and account types.

## DocType: Chart of Accounts Importer

### Fields

| Fieldname | Type | Description |
|-----------|------|-------------|
| `company` | Link (Company) | Target company |
| `import_file` | Attach | CSV/Excel file |
| `google_sheets_url` | Data | Google Sheets URL |

## Python API

### Import Chart of Accounts

```python
import frappe

def import_chart_of_accounts(company, file_path):
    """
    Import chart of accounts from CSV.
    """
    coa_importer = frappe.new_doc("Chart of Accounts Importer")
    coa_importer.company = company
    coa_importer.import_file = file_path
    coa_importer.insert()

    # Start import
    from erpnext.accounts.doctype.chart_of_accounts_importer.chart_of_accounts_importer import (
        import_coa
    )
    import_coa(coa_importer.name)

    return coa_importer.name
```

### Get Template

```python
from erpnext.accounts.doctype.chart_of_accounts_importer.chart_of_accounts_importer import (
    download_template
)

# Download blank template
download_template(company="DCNET")
```

## Template Format

### Required Columns

| Column | Description | Example |
|--------|-------------|---------|
| `Account Name` | Account name | "Cash" |
| `Parent Account` | Parent account name | "Current Assets" |
| `Account Number` | Account code | "1111" |
| `Is Group` | Is group account | 1 or 0 |
| `Account Type` | Account type | "Cash", "Receivable" |
| `Root Type` | Root type | "Asset", "Liability", "Income", "Expense", "Equity" |

### Example CSV

```csv
Account Name,Parent Account,Account Number,Is Group,Account Type,Root Type
Assets,,1000,1,,Asset
Current Assets,Assets,1100,1,,Asset
Cash,Current Assets,1110,0,Cash,Asset
Bank Accounts,Current Assets,1120,1,Bank,Asset
Receivable,Current Assets,1130,0,Receivable,Asset
Fixed Assets,Assets,1200,1,,Asset
Liabilities,,2000,1,,Liability
Current Liabilities,Liabilities,2100,1,,Liability
Payable,Current Liabilities,2110,0,Payable,Liability
Equity,,3000,1,,Equity
Capital Stock,Equity,3100,0,Equity,Equity
Income,,4000,1,,Income
Sales,Income,4100,0,Income Account,Income
Expense,,5000,1,,Expense
Cost of Goods Sold,Expense,5100,0,Cost of Goods Sold,Expense
```

## Account Types

### Valid Account Types

```python
ACCOUNT_TYPES = [
    "Accumulated Depreciation",
    "Asset Received But Not Billed",
    "Bank",
    "Cash",
    "Chargeable",
    "Cost of Goods Sold",
    "Depreciation",
    "Equity",
    "Expense Account",
    "Expenses Included In Asset Valuation",
    "Expenses Included In Valuation",
    "Fixed Asset",
    "Income Account",
    "Payable",
    "Receivable",
    "Round Off",
    "Stock",
    "Stock Adjustment",
    "Stock Received But Not Billed",
    "Tax",
    "Temporary",
]
```

### Root Types

```python
ROOT_TYPES = [
    "Asset",
    "Liability",
    "Income",
    "Expense",
    "Equity"
]
```

## Validation Rules

### Account Hierarchy

```python
def validate_account_hierarchy(accounts):
    """
    Validate parent-child relationships.
    """
    errors = []
    account_names = {a["Account Name"] for a in accounts}

    for account in accounts:
        parent = account.get("Parent Account")
        if parent and parent not in account_names:
            errors.append(f"Parent '{parent}' not found for '{account['Account Name']}'")

    # Check for circular references
    for account in accounts:
        visited = set()
        current = account["Account Name"]
        while current:
            if current in visited:
                errors.append(f"Circular reference detected: {current}")
                break
            visited.add(current)
            parent = next(
                (a["Parent Account"] for a in accounts if a["Account Name"] == current),
                None
            )
            current = parent

    return errors
```

### Root Type Validation

```python
def validate_root_types(accounts):
    """
    Validate root types are consistent with hierarchy.
    """
    errors = []

    for account in accounts:
        if not account.get("Parent Account"):
            # Root account must have Root Type
            if not account.get("Root Type"):
                errors.append(f"Root account '{account['Account Name']}' must have Root Type")
        else:
            # Non-root should inherit Root Type
            parent_root_type = get_parent_root_type(account, accounts)
            if account.get("Root Type") and account["Root Type"] != parent_root_type:
                errors.append(
                    f"Root Type mismatch for '{account['Account Name']}': "
                    f"expected '{parent_root_type}', got '{account['Root Type']}'"
                )

    return errors
```

## Import Process

### 1. Upload Template

```python
# Create import doc
coa_import = frappe.new_doc("Chart of Accounts Importer")
coa_import.company = "DCNET"
coa_import.import_file = "/files/chart_of_accounts.csv"
coa_import.insert()
```

### 2. Preview Import

```python
from erpnext.accounts.doctype.chart_of_accounts_importer.chart_of_accounts_importer import (
    get_coa_preview
)

preview = get_coa_preview(coa_import.name)
print(f"Accounts to create: {len(preview)}")

for account in preview[:10]:
    print(f"  {account.get('account_number', '')} - {account['account_name']}")
```

### 3. Validate Before Import

```python
def validate_coa_before_import(coa_import_name):
    """
    Validate COA data before import.
    """
    from erpnext.accounts.doctype.chart_of_accounts_importer.chart_of_accounts_importer import (
        get_coa_preview
    )

    preview = get_coa_preview(coa_import_name)
    errors = []
    warnings = []

    # Check for duplicates
    names = [a["account_name"] for a in preview]
    duplicates = [n for n in names if names.count(n) > 1]
    if duplicates:
        errors.append(f"Duplicate account names: {set(duplicates)}")

    # Check account numbers
    numbers = [a.get("account_number") for a in preview if a.get("account_number")]
    dup_numbers = [n for n in numbers if numbers.count(n) > 1]
    if dup_numbers:
        errors.append(f"Duplicate account numbers: {set(dup_numbers)}")

    # Check root accounts exist
    root_types_found = {a.get("root_type") for a in preview if not a.get("parent_account")}
    required_roots = {"Asset", "Liability", "Income", "Expense", "Equity"}
    missing_roots = required_roots - root_types_found
    if missing_roots:
        warnings.append(f"Missing root types: {missing_roots}")

    return {"errors": errors, "warnings": warnings}
```

### 4. Execute Import

```python
from erpnext.accounts.doctype.chart_of_accounts_importer.chart_of_accounts_importer import (
    import_coa
)

# Import the chart of accounts
import_coa(coa_import.name)
```

## Vietnamese Chart of Accounts

### Standard Vietnamese COA (Circular 200)

```csv
Account Name,Parent Account,Account Number,Is Group,Account Type,Root Type
Tài sản,,1,1,,Asset
Tài sản ngắn hạn,Tài sản,11,1,,Asset
Tiền,Tài sản ngắn hạn,111,1,,Asset
Tiền mặt,Tiền,1111,0,Cash,Asset
Tiền gửi ngân hàng,Tiền,1121,0,Bank,Asset
Phải thu khách hàng,Tài sản ngắn hạn,131,0,Receivable,Asset
Hàng tồn kho,Tài sản ngắn hạn,152,0,Stock,Asset
Nguồn vốn,,3,1,,Liability
Nợ phải trả,Nguồn vốn,33,1,,Liability
Phải trả người bán,Nợ phải trả,331,0,Payable,Liability
Vốn chủ sở hữu,Nguồn vốn,4,1,,Equity
Vốn đầu tư của chủ sở hữu,Vốn chủ sở hữu,411,0,Equity,Equity
Doanh thu,,5,1,,Income
Doanh thu bán hàng,Doanh thu,511,0,Income Account,Income
Chi phí,,6,1,,Expense
Giá vốn hàng bán,Chi phí,632,0,Cost of Goods Sold,Expense
```

### Import Vietnamese COA

```python
def import_vietnamese_coa(company):
    """
    Import standard Vietnamese Chart of Accounts (Circular 200).
    """
    # Use built-in Vietnamese COA
    from erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts import (
        create_charts
    )

    create_charts(company, chart_template="Vietnam - Chart of Accounts")

    return True
```

## API Endpoints

### REST API

```bash
# Get preview
POST /api/method/erpnext.accounts.doctype.chart_of_accounts_importer.chart_of_accounts_importer.get_coa_preview
Content-Type: application/json
{
    "docname": "COA-IMPORT-001"
}

# Start import
POST /api/method/erpnext.accounts.doctype.chart_of_accounts_importer.chart_of_accounts_importer.import_coa
Content-Type: application/json
{
    "file_name": "COA-IMPORT-001"
}
```

### JavaScript API

```javascript
// Preview COA
frappe.call({
    method: "erpnext.accounts.doctype.chart_of_accounts_importer.chart_of_accounts_importer.get_coa_preview",
    args: {
        docname: frm.doc.name
    },
    callback: function(r) {
        console.log("Preview:", r.message);
    }
});

// Import COA
frappe.call({
    method: "erpnext.accounts.doctype.chart_of_accounts_importer.chart_of_accounts_importer.import_coa",
    args: {
        file_name: frm.doc.name
    },
    callback: function(r) {
        frappe.show_alert(__("Import completed"));
    }
});
```

## Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Root Type required" | Missing root type for root account | Add Root Type column value |
| "Parent not found" | Invalid parent reference | Check parent account exists |
| "Duplicate account" | Account name/number exists | Use unique names |
| "Invalid Account Type" | Unknown account type | Use valid account type |

## Usage Example

### Complete COA Import Flow

```python
import frappe

def setup_company_coa(company, coa_file):
    """
    Set up complete Chart of Accounts for a company.
    """
    # Check company has no existing accounts
    existing = frappe.db.count("Account", {"company": company})
    if existing > 0:
        frappe.throw(f"Company {company} already has {existing} accounts")

    # Create import document
    coa_import = frappe.new_doc("Chart of Accounts Importer")
    coa_import.company = company
    coa_import.import_file = coa_file
    coa_import.insert()

    # Validate
    validation = validate_coa_before_import(coa_import.name)
    if validation["errors"]:
        frappe.throw("\n".join(validation["errors"]))

    if validation["warnings"]:
        for w in validation["warnings"]:
            frappe.msgprint(w, indicator="orange")

    # Import
    from erpnext.accounts.doctype.chart_of_accounts_importer.chart_of_accounts_importer import (
        import_coa
    )
    import_coa(coa_import.name)

    # Verify
    created = frappe.db.count("Account", {"company": company})
    return {
        "import_name": coa_import.name,
        "accounts_created": created
    }
```

## Related DocTypes

- **Account**: Created records
- **Company**: Target company
- **Account Type**: Account classification
- **GL Entry**: Uses accounts

## Related References

- [Data Import](data_import.md) - Base import class
- [Exporter](exporter.md) - Template export

---

*Source: erpnext/accounts/doctype/chart_of_accounts_importer/ | Last updated: 2026-02-04*
