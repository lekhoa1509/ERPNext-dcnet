<!-- Source: frappe-data-import skill -->

# Frappe Data Import/Export Skill

> Comprehensive guide for importing and exporting data in Frappe/ERPNext.

## Quick Topic Reference

| Topic | Documentation | API Reference |
|-------|---------------|---------------|
| **Data Import** | [SKILL.md#data-import](#data-import---complete-guide) | [api_reference/data_import.md](api_reference/data_import.md) |
| **Importer Class** | [references/docs/importer-api.md](references/docs/importer-api.md) | [api_reference/importer.md](api_reference/importer.md) |
| **Exporter Class** | [SKILL.md#data-export](#data-export) | [api_reference/exporter.md](api_reference/exporter.md) |
| **ImportFile Class** | - | [api_reference/import_file.md](api_reference/import_file.md) |
| **Field Mapping** | [tutorials/complex-field-mappings](tutorials/complex-field-mappings/complex-field-mappings.md) | [api_reference/field_mapping.md](api_reference/field_mapping.md) |
| **Background Jobs** | [tutorials/bulk-import-background-jobs](tutorials/bulk-import-background-jobs/bulk-import-background-jobs.md) | [api_reference/background_jobs.md](api_reference/background_jobs.md) |
| **Bank Statement Import** | [tutorials/bank-statement-import](tutorials/bank-statement-import/bank-statement-import.md) | [api_reference/bank_statement_import.md](api_reference/bank_statement_import.md) |
| **COA Import** | - | [api_reference/chart_of_accounts_importer.md](api_reference/chart_of_accounts_importer.md) |
| **Migration Patterns** | [tutorials/data-migration-bravo-erpnext](tutorials/data-migration-bravo-erpnext/data-migration-bravo-erpnext.md) | - |

## When to Use This Skill

Use this skill when you need to:
- Import CSV/Excel data into Frappe DocTypes
- Export data for backup or transfer
- Download import templates
- Handle bulk imports with background jobs
- Import bank statements (ERPNext)
- Import Chart of Accounts (ERPNext)
- Migrate data from BRAVO or other systems to ERPNext

## Codebase Statistics

**Languages:**
- **Python**: 7 core files

**Analysis Performed:**
- API Reference - 19 files (covering all classes and utilities)
- Tutorials - 17 how-to guides
- Test Examples - 20 examples from tests
- Design Patterns - 19 patterns in 5 files
- Configuration Patterns - 22 settings

---

## Data Import - Complete Guide

### 1. Via UI (Desk)

```
Setup > Data > Data Import
```

**Steps:**
1. Select **Document Type** to import
2. Choose **Import Type**: Insert or Update
3. **Download Template** (blank or with sample data)
4. Fill template with data
5. **Upload File** or paste Google Sheets URL
6. Review **Preview** and fix warnings
7. Click **Start Import**

### 2. Via Python API

#### Basic Import

```python
from frappe.core.doctype.data_import.data_import import import_file

# Import from file
import_file(
    doctype="Customer",
    file_path="/path/to/customers.csv",
    import_type="Insert",  # or "Update"
    submit_after_import=False,
    console=True  # Show progress in console
)
```

#### Create Data Import Document

```python
import frappe

# Create import document
data_import = frappe.new_doc("Data Import")
data_import.reference_doctype = "Customer"
data_import.import_type = "Insert New Records"
data_import.import_file = "/files/customers.csv"
data_import.mute_emails = True  # Don't send notifications
data_import.submit_after_import = False
data_import.insert()

# Start import (runs in background)
data_import.start_import()
```

#### Using Importer Class Directly

```python
from frappe.core.doctype.data_import.importer import Importer

# Create importer
importer = Importer(
    doctype="Customer",
    file_path="/path/to/customers.csv",
    import_type="Insert New Records",
    console=True
)

# Get preview
preview = importer.get_data_for_import_preview()
print(f"Columns: {len(preview.columns)}")
print(f"Rows: {len(preview.data)}")
print(f"Warnings: {preview.warnings}")

# Run import
import_log = importer.import_data()
```

### 3. Via Bench Command

```bash
# Import from CSV
bench --site mysite.local data-import --doctype "Customer" \
    --file /path/to/customers.csv --type "Insert"

# Import with submit
bench --site mysite.local data-import --doctype "Sales Invoice" \
    --file /path/to/invoices.csv --type "Insert" --submit-after-import
```

---

## Template Format

### Header Row

Headers must match field **labels** or **fieldnames**:

```csv
ID,Customer Name,Customer Type,Territory
CUST-001,ACME Corp,Company,Vietnam
```

### Child Tables

For child tables, use format: `Field Label (Child Table Label)`

```csv
ID,Customer Name,Item Code (Items),Qty (Items),Rate (Items)
SO-001,ACME Corp,ITEM-001,10,1000
,,ITEM-002,5,2000
```

### Date Formats

Supported formats (auto-detected):
- `YYYY-MM-DD` (recommended)
- `DD-MM-YYYY`
- `MM/DD/YYYY`
- `DD/MM/YYYY`

---

## Data Export

### Via Python API

```python
from frappe.core.doctype.data_import.exporter import Exporter

# Export with specific fields
exporter = Exporter(
    doctype="Customer",
    export_fields={
        "Customer": ["name", "customer_name", "customer_type", "territory"],
    },
    export_data=True,
    export_filters={"customer_type": "Company"},
    file_type="CSV"  # or "Excel"
)

# Get data array
csv_array = exporter.get_csv_array()

# Build response (triggers download)
exporter.build_response()
```

---

## Migration Patterns (BRAVO to ERPNext)

### Step 1: Export from Source System

```python
from frappe.core.doctype.data_import.data_import import export_json

export_json("Customer", "/tmp/customers.json", filters={})
export_json("Item", "/tmp/items.json", filters={})
```

### Step 2: Transform Data

```python
import json

with open("/tmp/bravo_customers.json") as f:
    bravo_data = json.load(f)

erpnext_data = []
for row in bravo_data:
    erpnext_data.append({
        "customer_name": row["ten_khach_hang"],
        "customer_type": "Company" if row["loai"] == "DN" else "Individual",
        "territory": "Vietnam",
    })

with open("/tmp/erpnext_customers.json", "w") as f:
    json.dump(erpnext_data, f, ensure_ascii=False)
```

### Step 3: Import to ERPNext

```python
from frappe.core.doctype.data_import.data_import import import_doc

import_doc("/tmp/erpnext_customers.json")
frappe.db.commit()
```

---

## Available References

This skill includes detailed reference documentation:

### API Reference (`api_reference/`) - 19 files

**Core Classes:**
- [data_import.md](api_reference/data_import.md) - Data Import DocType
- [importer.md](api_reference/importer.md) - Importer class
- [exporter.md](api_reference/exporter.md) - Exporter class
- [import_file.md](api_reference/import_file.md) - ImportFile class
- [row.md](api_reference/row.md) - Row parsing class
- [header.md](api_reference/header.md) - Header parsing class
- [column.md](api_reference/column.md) - Column mapping class

**Utilities:**
- [field_mapping.md](api_reference/field_mapping.md) - Field mapping utilities
- [validation_utils.md](api_reference/validation_utils.md) - Validation functions
- [error_handling.md](api_reference/error_handling.md) - Error handling classes
- [background_jobs.md](api_reference/background_jobs.md) - Background job handlers
- [csv_parser.md](api_reference/csv_parser.md) - CSV/Excel parsers
- [bulk_operations.md](api_reference/bulk_operations.md) - Bulk operations
- [export_utilities.md](api_reference/export_utilities.md) - Export utilities
- [template_generator.md](api_reference/template_generator.md) - Template generation
- [data_import_log.md](api_reference/data_import_log.md) - Import log management

**ERPNext Specific:**
- [bank_statement_import.md](api_reference/bank_statement_import.md) - Bank statement import
- [chart_of_accounts_importer.md](api_reference/chart_of_accounts_importer.md) - COA import

### Tutorials (`tutorials/`) - 17 how-to guides

**Basic Import/Export:**
- [Data Import From File](tutorials/data-import-from-file/data-import-from-file.md)
- [Data Import Update](tutorials/data-import-update/data-import-update.md)
- [Exports Specified Fields](tutorials/exports-specified-fields/exports-specified-fields.md)

**Template & Field Mapping:**
- [Creating Custom Import Templates](tutorials/custom-import-templates/custom-import-templates.md)
- [Handling Complex Field Mappings](tutorials/complex-field-mappings/complex-field-mappings.md)
- [Importing Linked Documents](tutorials/importing-linked-documents/importing-linked-documents.md)

**Advanced Techniques:**
- [Bulk Import with Background Jobs](tutorials/bulk-import-background-jobs/bulk-import-background-jobs.md)
- [Import Validation and Error Handling](tutorials/import-validation-error-handling/import-validation-error-handling.md)
- [Performance Optimization](tutorials/performance-optimization/performance-optimization.md)
- [Rollback and Recovery Strategies](tutorials/rollback-recovery/rollback-recovery.md)

**ERPNext Specific:**
- [Bank Statement Import (MT940, CSV)](tutorials/bank-statement-import/bank-statement-import.md)

**Data Migration:**
- [Data Migration from BRAVO to ERPNext](tutorials/data-migration-bravo-erpnext/data-migration-bravo-erpnext.md)

### Other References

- **Manual Docs**: `references/docs/` - Comprehensive guides
- **Examples**: `test_examples/` - 20 usage examples from tests
- **Dependencies**: `dependencies/` - Dependency graph
- **Patterns**: `patterns/` - Design patterns detected

---

## Quick Scenario Guide

| Scenario | Recommended Resource |
|----------|---------------------|
| First time import | [tutorials/data-import-from-file](tutorials/data-import-from-file/data-import-from-file.md) |
| Custom CSV headers | [tutorials/complex-field-mappings](tutorials/complex-field-mappings/complex-field-mappings.md) |
| 10,000+ records | [tutorials/bulk-import-background-jobs](tutorials/bulk-import-background-jobs/bulk-import-background-jobs.md) + [tutorials/performance-optimization](tutorials/performance-optimization/performance-optimization.md) |
| Import failed | [tutorials/rollback-recovery](tutorials/rollback-recovery/rollback-recovery.md) |
| Bank transactions | [tutorials/bank-statement-import](tutorials/bank-statement-import/bank-statement-import.md) |
| Migrate from BRAVO | [tutorials/data-migration-bravo-erpnext](tutorials/data-migration-bravo-erpnext/data-migration-bravo-erpnext.md) |
| Validate before import | [tutorials/import-validation-error-handling](tutorials/import-validation-error-handling/import-validation-error-handling.md) |

---

## Related Skills

- **frappe** - Frappe Framework core (DocType, Database API)
- **erpnext_accounting** - ERPNext Accounts module
- **frappe-integration** - Webhooks, REST API for external systems

---

**Generated by Skill Seeker** | Codebase Analyzer with C3.x Analysis | Version 4.0.0
