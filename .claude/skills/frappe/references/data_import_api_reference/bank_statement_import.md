# API Reference: Bank Statement Import (ERPNext)

**Language**: Python

**Source**: `erpnext/accounts/doctype/bank_statement_import/`

---

## Overview

Bank Statement Import in ERPNext allows importing bank transactions from CSV, Excel, or MT940 files. It creates Bank Transaction records for reconciliation with Payment Entries.

## DocType: Bank Statement Import

### Fields

| Fieldname | Type | Description |
|-----------|------|-------------|
| `company` | Link (Company) | Target company |
| `bank_account` | Link (Bank Account) | Target bank account |
| `import_file` | Attach | Import file (CSV/XLSX/MT940) |
| `google_sheets_url` | Data | Google Sheets URL |
| `status` | Select | Import status |
| `template_options` | Text | Column mapping configuration |

### Status Flow

```
Not Started -> In Progress -> Success/Partial Success/Error
```

## Python API

### Basic Import

```python
import frappe

# Create Bank Statement Import
bsi = frappe.new_doc("Bank Statement Import")
bsi.company = "DCNET"
bsi.bank_account = "DCNET - Vietcombank"
bsi.import_file = "/files/bank_statement.csv"
bsi.insert()

# Start import
bsi.start_import()
```

### Import from MT940

```python
import frappe

def import_mt940_statement(file_path, bank_account):
    """
    Import MT940 bank statement.

    MT940 is SWIFT standard format used by many banks.
    """
    bsi = frappe.new_doc("Bank Statement Import")
    bsi.company = frappe.db.get_value("Bank Account", bank_account, "company")
    bsi.bank_account = bank_account
    bsi.import_file = file_path
    bsi.insert()

    # Configure MT940 parsing
    bsi.template_options = frappe.as_json({
        "file_format": "MT940",
        "date_format": "%y%m%d"
    })
    bsi.save()

    bsi.start_import()

    return bsi.name
```

### Custom Column Mapping

```python
import frappe

def import_custom_bank_csv(file_path, bank_account, column_mapping):
    """
    Import bank statement with custom column mapping.

    Args:
        file_path: Path to CSV file
        bank_account: Bank Account name
        column_mapping: Dict mapping CSV columns to Bank Transaction fields
    """
    bsi = frappe.new_doc("Bank Statement Import")
    bsi.company = frappe.db.get_value("Bank Account", bank_account, "company")
    bsi.bank_account = bank_account
    bsi.import_file = file_path

    # Set column mapping
    # Example: {"Date": "date", "Description": "description", "Amount": "deposit"}
    bsi.template_options = frappe.as_json({
        "column_to_field_map": column_mapping,
        "date_format": "%d/%m/%Y"
    })

    bsi.insert()
    bsi.start_import()

    return bsi.name
```

## Bank Transaction Fields

Imported data maps to Bank Transaction DocType:

| CSV Column | Bank Transaction Field | Description |
|------------|----------------------|-------------|
| Date | `date` | Transaction date |
| Description | `description` | Transaction description |
| Debit | `withdrawal` | Withdrawal amount |
| Credit | `deposit` | Deposit amount |
| Reference | `reference_number` | Bank reference |
| Balance | `closing_balance` | Running balance |

## Template Options

### CSV Template Options

```python
template_options = {
    "file_format": "CSV",
    "date_format": "%d/%m/%Y",
    "column_to_field_map": {
        "Transaction Date": "date",
        "Narration": "description",
        "Debit": "withdrawal",
        "Credit": "deposit",
        "Ref No": "reference_number"
    },
    "skip_rows": 2,  # Skip header rows
    "decimal_separator": ",",
    "thousands_separator": "."
}
```

### MT940 Template Options

```python
template_options = {
    "file_format": "MT940",
    "date_format": "%y%m%d",
    "account_number_field": "account_no"
}
```

## MT940 Parser

### MT940 Field Structure

```
:20: Transaction Reference
:25: Account Identification
:28C: Statement Number
:60F: Opening Balance
:61: Statement Line (transaction)
:86: Information to Account Owner
:62F: Closing Balance
```

### Parse MT940 File

```python
def parse_mt940(content: str) -> list:
    """
    Parse MT940 file content.

    Returns list of transactions:
    [
        {
            "date": datetime.date,
            "amount": float,
            "description": str,
            "reference_number": str
        },
        ...
    ]
    """
    import re
    from datetime import datetime

    transactions = []

    # Find all :61: statement lines
    pattern = r":61:(\d{6})(\d{4})?(C|D|RC|RD)(\d+),(\d+)(.{4})(.+?)(?=:61:|:62)"

    for match in re.finditer(pattern, content, re.DOTALL):
        date_str = match.group(1)
        credit_debit = match.group(3)
        amount_int = match.group(4)
        amount_dec = match.group(5)
        reference = match.group(7).strip()

        # Parse date (YYMMDD)
        date = datetime.strptime(date_str, "%y%m%d").date()

        # Parse amount
        amount = float(f"{amount_int}.{amount_dec}")
        if credit_debit in ("D", "RD"):  # Debit
            amount = -amount

        transactions.append({
            "date": date,
            "amount": amount,
            "description": reference,
            "reference_number": reference[:20]
        })

    return transactions
```

## Import Workflow

### 1. Upload File

```python
# Upload bank statement file
file_doc = frappe.get_doc({
    "doctype": "File",
    "file_name": "bank_statement_january.csv",
    "is_private": 1,
    "content": open("/path/to/file.csv", "rb").read()
}).insert()
```

### 2. Create Import Document

```python
bsi = frappe.new_doc("Bank Statement Import")
bsi.company = "DCNET"
bsi.bank_account = "DCNET - Vietcombank"
bsi.import_file = file_doc.file_url
bsi.insert()
```

### 3. Preview Import

```python
# Get preview
preview = bsi.get_preview_from_template()
print(f"Columns: {preview.columns}")
print(f"Rows: {len(preview.data)}")
print(f"Warnings: {preview.warnings}")
```

### 4. Start Import

```python
bsi.start_import()

# Check status
bsi.reload()
print(f"Status: {bsi.status}")
```

### 5. Review Results

```python
# Get imported transactions
transactions = frappe.get_all(
    "Bank Transaction",
    filters={
        "bank_account": bsi.bank_account,
        "creation": [">=", bsi.creation]
    },
    fields=["name", "date", "deposit", "withdrawal", "description"]
)

print(f"Imported {len(transactions)} transactions")
```

## Error Handling

### Duplicate Detection

```python
def check_duplicate_transactions(bank_account, transactions):
    """Check for duplicate transactions before import."""
    duplicates = []

    for txn in transactions:
        existing = frappe.db.exists(
            "Bank Transaction",
            {
                "bank_account": bank_account,
                "date": txn["date"],
                "deposit": txn.get("deposit", 0),
                "withdrawal": txn.get("withdrawal", 0),
                "reference_number": txn.get("reference_number")
            }
        )

        if existing:
            duplicates.append(txn)

    return duplicates
```

### Validation Errors

```python
def validate_bank_transaction(txn_data):
    """Validate transaction before creating."""
    errors = []

    if not txn_data.get("date"):
        errors.append("Transaction date is required")

    if not txn_data.get("deposit") and not txn_data.get("withdrawal"):
        errors.append("Either deposit or withdrawal amount is required")

    if txn_data.get("deposit") and txn_data.get("withdrawal"):
        errors.append("Transaction cannot have both deposit and withdrawal")

    return errors
```

## Vietnamese Bank Formats

### Vietcombank CSV Format

```python
vietcombank_mapping = {
    "Ngay GD": "date",
    "Noi dung": "description",
    "So tien ghi no": "withdrawal",
    "So tien ghi co": "deposit",
    "So du": "closing_balance",
    "So chung tu": "reference_number"
}
```

### Techcombank CSV Format

```python
techcombank_mapping = {
    "Transaction Date": "date",
    "Description": "description",
    "Debit": "withdrawal",
    "Credit": "deposit",
    "Reference": "reference_number"
}
```

## Usage Example

### Complete Bank Statement Import

```python
import frappe

def import_bank_statement(company, bank_account, file_path, bank_format="generic"):
    """
    Complete bank statement import with validation.
    """
    # Get format mapping
    mappings = {
        "vietcombank": {
            "Ngay GD": "date",
            "Noi dung": "description",
            "So tien ghi no": "withdrawal",
            "So tien ghi co": "deposit"
        },
        "techcombank": {
            "Transaction Date": "date",
            "Description": "description",
            "Debit": "withdrawal",
            "Credit": "deposit"
        },
        "generic": None  # Auto-detect
    }

    column_mapping = mappings.get(bank_format)

    # Create import
    bsi = frappe.new_doc("Bank Statement Import")
    bsi.company = company
    bsi.bank_account = bank_account
    bsi.import_file = file_path

    if column_mapping:
        bsi.template_options = frappe.as_json({
            "column_to_field_map": column_mapping
        })

    bsi.insert()

    # Preview first
    preview = bsi.get_preview_from_template()
    if preview.warnings:
        for w in preview.warnings:
            print(f"Warning: {w}")

    # Start import
    bsi.start_import()

    # Return results
    bsi.reload()
    return {
        "name": bsi.name,
        "status": bsi.status,
        "transactions_imported": frappe.db.count(
            "Bank Transaction",
            {"bank_account": bank_account}
        )
    }
```

## Related DocTypes

- **Bank Transaction**: Created records
- **Bank Account**: Target account
- **Bank Reconciliation**: Match with Payment Entries
- **Payment Entry**: Reconciliation target

## Related References

- [Data Import](data_import.md) - Base import class
- [Importer](importer.md) - Import logic

---

*Source: erpnext/accounts/doctype/bank_statement_import/ | Last updated: 2026-02-04*
