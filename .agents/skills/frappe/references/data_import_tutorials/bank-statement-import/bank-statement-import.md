# How To: Bank Statement Import (MT940 and CSV)

**Difficulty**: Intermediate
**Estimated Time**: 30 minutes
**Tags**: banking, import, reconciliation, erpnext

## Overview

Learn how to import bank statements from various formats (MT940, CSV) into ERPNext for bank reconciliation.

## Prerequisites

- ERPNext with Accounts module
- Bank Account configured
- Basic understanding of bank reconciliation

## Supported Formats

| Format | Description | Banks |
|--------|-------------|-------|
| MT940 | SWIFT standard | Most international banks |
| CSV | Generic format | Vietcombank, Techcombank, etc. |
| OFX | Open Financial Exchange | Some US banks |
| QIF | Quicken Interchange | Legacy systems |

## Step-by-Step Guide

### Step 1: Configure Bank Account

```python
import frappe

def setup_bank_account(company, bank_name, account_name, account_number):
    """
    Set up bank account for statement import.
    """
    # Create Bank if not exists
    if not frappe.db.exists("Bank", bank_name):
        bank = frappe.get_doc({
            "doctype": "Bank",
            "bank_name": bank_name
        })
        bank.insert()

    # Create Bank Account
    gl_account = frappe.db.get_value(
        "Account",
        {"account_type": "Bank", "company": company},
        "name"
    )

    bank_account = frappe.get_doc({
        "doctype": "Bank Account",
        "account_name": account_name,
        "bank": bank_name,
        "account": gl_account,
        "company": company,
        "bank_account_no": account_number,
        "is_company_account": 1
    })
    bank_account.insert()

    return bank_account.name
```

### Step 2: Import CSV Bank Statement

```python
import frappe
import csv
from frappe.utils import getdate, flt

def import_csv_bank_statement(file_path, bank_account, column_mapping=None):
    """
    Import bank statement from CSV.

    Args:
        file_path: Path to CSV file
        bank_account: Bank Account name
        column_mapping: Dict mapping CSV columns to fields
    """
    if not column_mapping:
        # Default mapping for Vietnamese banks
        column_mapping = {
            "date": "Ngay GD",
            "description": "Noi dung",
            "withdrawal": "So tien ghi no",
            "deposit": "So tien ghi co",
            "reference": "So chung tu"
        }

    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    created = 0
    skipped = 0
    errors = []

    for row in rows:
        try:
            # Map columns
            date = getdate(row.get(column_mapping["date"]))
            description = row.get(column_mapping["description"], "")
            withdrawal = parse_amount(row.get(column_mapping["withdrawal"]))
            deposit = parse_amount(row.get(column_mapping["deposit"]))
            reference = row.get(column_mapping.get("reference", ""), "")

            # Check for duplicate
            if check_duplicate_transaction(bank_account, date, withdrawal, deposit, reference):
                skipped += 1
                continue

            # Create Bank Transaction
            bt = frappe.get_doc({
                "doctype": "Bank Transaction",
                "bank_account": bank_account,
                "date": date,
                "description": description,
                "withdrawal": withdrawal,
                "deposit": deposit,
                "reference_number": reference[:140] if reference else None,
                "status": "Pending"
            })
            bt.insert()
            created += 1

        except Exception as e:
            errors.append({
                "row": row,
                "error": str(e)
            })

    frappe.db.commit()

    return {
        "created": created,
        "skipped": skipped,
        "errors": errors
    }

def parse_amount(value):
    """Parse amount from string."""
    if not value:
        return 0
    # Handle Vietnamese number format (1.234.567,89)
    value = str(value).replace(".", "").replace(",", ".")
    return flt(value)

def check_duplicate_transaction(bank_account, date, withdrawal, deposit, reference):
    """Check if transaction already exists."""
    filters = {
        "bank_account": bank_account,
        "date": date,
        "withdrawal": withdrawal,
        "deposit": deposit
    }
    if reference:
        filters["reference_number"] = reference

    return frappe.db.exists("Bank Transaction", filters)
```

### Step 3: Import MT940 Bank Statement

```python
import frappe
from frappe.utils import getdate, flt
import re

def import_mt940_statement(file_path, bank_account):
    """
    Import MT940 format bank statement.
    """
    with open(file_path, "r") as f:
        content = f.read()

    transactions = parse_mt940(content)

    created = 0
    errors = []

    for txn in transactions:
        try:
            # Check duplicate
            if check_duplicate_transaction(
                bank_account,
                txn["date"],
                txn.get("withdrawal", 0),
                txn.get("deposit", 0),
                txn.get("reference", "")
            ):
                continue

            # Create Bank Transaction
            bt = frappe.get_doc({
                "doctype": "Bank Transaction",
                "bank_account": bank_account,
                "date": txn["date"],
                "description": txn.get("description", ""),
                "withdrawal": txn.get("withdrawal", 0),
                "deposit": txn.get("deposit", 0),
                "reference_number": txn.get("reference", "")[:140],
                "status": "Pending"
            })
            bt.insert()
            created += 1

        except Exception as e:
            errors.append({
                "transaction": txn,
                "error": str(e)
            })

    frappe.db.commit()

    return {
        "created": created,
        "total_parsed": len(transactions),
        "errors": errors
    }

def parse_mt940(content):
    """
    Parse MT940 file content.

    MT940 Structure:
    :20: Transaction Reference Number
    :25: Account Identification
    :28C: Statement Number
    :60F: Opening Balance
    :61: Statement Line (transactions)
    :86: Information to Account Owner
    :62F: Closing Balance
    """
    transactions = []

    # Split by statement lines (:61:)
    # Format: :61:YYMMDD[MMDD]C/DN,NNN{Reference}
    pattern = r":61:(\d{6})(\d{4})?(C|D|RC|RD)(\d+),(\d{2})N(.{3})(.+?)(?=:61:|:62|:86:|$)"

    for match in re.finditer(pattern, content, re.DOTALL):
        date_str = match.group(1)  # YYMMDD
        credit_debit = match.group(3)  # C=Credit, D=Debit
        amount_int = match.group(4)
        amount_dec = match.group(5)
        ref_type = match.group(6)
        rest = match.group(7).strip()

        # Parse date
        year = int("20" + date_str[:2])
        month = int(date_str[2:4])
        day = int(date_str[4:6])
        date = f"{year}-{month:02d}-{day:02d}"

        # Parse amount
        amount = float(f"{amount_int}.{amount_dec}")

        # Determine direction
        if credit_debit in ("C", "RC"):
            deposit = amount
            withdrawal = 0
        else:
            deposit = 0
            withdrawal = amount

        # Extract reference from :86: tag if present
        description = rest.split("\n")[0] if rest else ""

        # Find associated :86: information
        info_match = re.search(
            rf":86:(.+?)(?=:61:|:62|$)",
            content[match.end():match.end()+500],
            re.DOTALL
        )
        if info_match:
            description = info_match.group(1).replace("\n", " ").strip()

        transactions.append({
            "date": date,
            "deposit": deposit,
            "withdrawal": withdrawal,
            "reference": rest[:20] if rest else "",
            "description": description[:200]
        })

    return transactions
```

### Step 4: Bank-Specific Importers

```python
# Vietcombank CSV format
def import_vietcombank_statement(file_path, bank_account):
    """Import Vietcombank statement."""
    column_mapping = {
        "date": "Ngay GD",
        "description": "Noi dung giao dich",
        "withdrawal": "Phat sinh No",
        "deposit": "Phat sinh Co",
        "reference": "So CT"
    }
    return import_csv_bank_statement(file_path, bank_account, column_mapping)

# Techcombank CSV format
def import_techcombank_statement(file_path, bank_account):
    """Import Techcombank statement."""
    column_mapping = {
        "date": "Transaction Date",
        "description": "Description",
        "withdrawal": "Debit",
        "deposit": "Credit",
        "reference": "Reference No"
    }
    return import_csv_bank_statement(file_path, bank_account, column_mapping)

# BIDV CSV format
def import_bidv_statement(file_path, bank_account):
    """Import BIDV statement."""
    column_mapping = {
        "date": "Ngay",
        "description": "Mo ta",
        "withdrawal": "Ghi no",
        "deposit": "Ghi co",
        "reference": "So tham chieu"
    }
    return import_csv_bank_statement(file_path, bank_account, column_mapping)
```

### Step 5: Using Bank Statement Import DocType

```python
import frappe

def import_via_doctype(file_path, bank_account, file_format="CSV"):
    """
    Import using ERPNext's Bank Statement Import DocType.
    """
    # Upload file
    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": file_path.split("/")[-1],
        "is_private": 1,
        "content": open(file_path, "rb").read()
    }).insert()

    # Get company from bank account
    company = frappe.db.get_value("Bank Account", bank_account, "company")

    # Create Bank Statement Import
    bsi = frappe.get_doc({
        "doctype": "Bank Statement Import",
        "company": company,
        "bank_account": bank_account,
        "import_file": file_doc.file_url
    })
    bsi.insert()

    # Configure template options if needed
    if file_format == "MT940":
        bsi.template_options = frappe.as_json({
            "file_format": "MT940"
        })
        bsi.save()

    # Get preview
    preview = bsi.get_preview_from_template()
    print(f"Preview: {len(preview.data)} transactions")

    # Start import
    bsi.start_import()

    return bsi.name
```

### Step 6: Reconciliation After Import

```python
import frappe

def auto_reconcile_transactions(bank_account, from_date=None, to_date=None):
    """
    Automatically reconcile bank transactions with Payment Entries.
    """
    filters = {
        "bank_account": bank_account,
        "status": "Pending"
    }

    if from_date:
        filters["date"] = [">=", from_date]
    if to_date:
        filters["date"] = ["<=", to_date]

    transactions = frappe.get_all(
        "Bank Transaction",
        filters=filters,
        fields=["name", "date", "deposit", "withdrawal", "reference_number", "description"]
    )

    reconciled = 0

    for txn in transactions:
        # Try to find matching Payment Entry
        amount = txn.deposit or txn.withdrawal
        payment_type = "Receive" if txn.deposit else "Pay"

        # Search by reference number first
        if txn.reference_number:
            pe = frappe.db.get_value(
                "Payment Entry",
                {
                    "reference_no": txn.reference_number,
                    "paid_amount": amount,
                    "docstatus": 1
                },
                "name"
            )

            if pe:
                reconcile_transaction(txn.name, "Payment Entry", pe)
                reconciled += 1
                continue

        # Search by amount and date
        pe = frappe.db.get_value(
            "Payment Entry",
            {
                "posting_date": txn.date,
                "paid_amount": amount,
                "payment_type": payment_type,
                "docstatus": 1,
                "clearance_date": ["is", "not set"]
            },
            "name"
        )

        if pe:
            reconcile_transaction(txn.name, "Payment Entry", pe)
            reconciled += 1

    return {"reconciled": reconciled, "total": len(transactions)}

def reconcile_transaction(bank_transaction, reference_doctype, reference_name):
    """Reconcile a bank transaction with a reference document."""
    bt = frappe.get_doc("Bank Transaction", bank_transaction)

    bt.append("payment_entries", {
        "payment_document": reference_doctype,
        "payment_entry": reference_name,
        "allocated_amount": bt.deposit or bt.withdrawal
    })

    bt.status = "Reconciled"
    bt.save()

    # Set clearance date on Payment Entry
    if reference_doctype == "Payment Entry":
        frappe.db.set_value(
            "Payment Entry",
            reference_name,
            "clearance_date",
            bt.date
        )

    frappe.db.commit()
```

## Complete Example

```python
import frappe

class BankStatementManager:
    """Manage bank statement import and reconciliation."""

    def __init__(self, bank_account):
        self.bank_account = bank_account
        self.company = frappe.db.get_value("Bank Account", bank_account, "company")

    def import_statement(self, file_path, bank_format="auto"):
        """Import bank statement."""
        if bank_format == "auto":
            bank_format = self.detect_format(file_path)

        importers = {
            "vietcombank": import_vietcombank_statement,
            "techcombank": import_techcombank_statement,
            "bidv": import_bidv_statement,
            "mt940": import_mt940_statement,
            "csv": import_csv_bank_statement
        }

        importer = importers.get(bank_format.lower(), import_csv_bank_statement)
        return importer(file_path, self.bank_account)

    def detect_format(self, file_path):
        """Auto-detect bank statement format."""
        with open(file_path, "r") as f:
            content = f.read(1000)

        if ":20:" in content and ":61:" in content:
            return "mt940"
        elif "Ngay GD" in content or "Noi dung giao dich" in content:
            return "vietcombank"
        elif "Transaction Date" in content:
            return "techcombank"
        else:
            return "csv"

    def reconcile(self, auto=True):
        """Reconcile imported transactions."""
        if auto:
            return auto_reconcile_transactions(self.bank_account)
        else:
            # Return pending transactions for manual reconciliation
            return frappe.get_all(
                "Bank Transaction",
                filters={
                    "bank_account": self.bank_account,
                    "status": "Pending"
                },
                fields=["name", "date", "deposit", "withdrawal", "description"]
            )


# Usage
manager = BankStatementManager("DCNET - Vietcombank")

# Import statement
result = manager.import_statement("/path/to/statement.csv")
print(f"Imported: {result['created']} transactions")

# Auto-reconcile
recon_result = manager.reconcile(auto=True)
print(f"Reconciled: {recon_result['reconciled']} / {recon_result['total']}")
```

## Next Steps

- [Chart of Accounts Import](../chart-of-accounts-import/chart-of-accounts-import.md)
- [Data Migration from BRAVO](../data-migration-bravo-erpnext/data-migration-bravo-erpnext.md)

---

*Last updated: 2026-02-04*
