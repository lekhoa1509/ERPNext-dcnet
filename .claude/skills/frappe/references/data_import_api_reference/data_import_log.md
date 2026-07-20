# API Reference: Data Import Log

**Language**: Python

**Source**: `frappe/core/doctype/data_import_log/data_import_log.py`

---

## Overview

`Data Import Log` is a child DocType that stores individual import results for each row processed. It tracks success/failure status, error messages, and links to created documents.

## DocType Definition

### Fields

| Fieldname | Type | Description |
|-----------|------|-------------|
| `log_index` | Int | Row index in import file |
| `success` | Check | Whether import succeeded |
| `docname` | Data | Name of created/updated document |
| `messages` | Text | Error or warning messages (JSON) |
| `exception` | Text | Full exception traceback |
| `row_indexes` | Data | Source row indexes (comma-separated) |

### Parent DocType

- **Parent**: `Data Import`
- **Parent Field**: `import_log`

## Python API

### Creating Import Logs

```python
from frappe.core.doctype.data_import.importer import create_import_log

# Create a success log
create_import_log(
    data_import="DATA-IMPORT-001",
    log_index=1,
    log_details={
        "success": True,
        "docname": "CUST-001",
        "messages": [],
        "row_indexes": [1]
    }
)

# Create a failure log
create_import_log(
    data_import="DATA-IMPORT-001",
    log_index=2,
    log_details={
        "success": False,
        "docname": None,
        "messages": ["Customer name is required"],
        "exception": "frappe.ValidationError: Customer name is required",
        "row_indexes": [2]
    }
)
```

### Reading Import Logs

```python
import frappe

# Get all logs for an import
data_import = frappe.get_doc("Data Import", "DATA-IMPORT-001")

for log in data_import.import_log:
    print(f"Row {log.log_index}: {'Success' if log.success else 'Failed'}")
    if log.docname:
        print(f"  Created: {log.docname}")
    if log.messages:
        messages = frappe.parse_json(log.messages)
        for msg in messages:
            print(f"  Message: {msg}")
```

### Filtering Logs

```python
import frappe

# Get failed imports only
failed_logs = frappe.get_all(
    "Data Import Log",
    filters={
        "parent": "DATA-IMPORT-001",
        "success": 0
    },
    fields=["log_index", "messages", "exception"]
)

for log in failed_logs:
    print(f"Row {log.log_index} failed")
    print(f"Error: {log.messages}")
```

### Log Statistics

```python
import frappe

data_import_name = "DATA-IMPORT-001"

# Count success/failure
total = frappe.db.count("Data Import Log", {"parent": data_import_name})
success = frappe.db.count("Data Import Log", {
    "parent": data_import_name,
    "success": 1
})
failed = total - success

print(f"Total: {total}, Success: {success}, Failed: {failed}")
```

## Log Message Structure

### Success Log

```python
{
    "success": True,
    "docname": "CUST-001",
    "messages": [],
    "row_indexes": [1]
}
```

### Failure Log

```python
{
    "success": False,
    "docname": None,
    "messages": [
        "Mandatory fields required in row 1",
        "Customer Name is required"
    ],
    "exception": "frappe.exceptions.MandatoryError: ...",
    "row_indexes": [1, 2]  # For multi-row documents
}
```

### Warning Log

```python
{
    "success": True,
    "docname": "CUST-001",
    "messages": [
        "Territory 'Unknown' does not exist, using default"
    ],
    "row_indexes": [1]
}
```

## Usage Examples

### Export Failed Rows

```python
import frappe
from frappe.core.doctype.data_import.importer import Importer

# Get the importer
data_import = frappe.get_doc("Data Import", "DATA-IMPORT-001")
importer = Importer(
    data_import.reference_doctype,
    data_import=data_import
)

# Export only errored rows
errored_csv = importer.export_errored_rows()
# Returns CSV with only rows that failed
```

### Download Full Import Log

```python
import frappe

def download_import_log(data_import_name):
    """Download complete import log as CSV."""
    import csv
    from io import StringIO

    logs = frappe.get_all(
        "Data Import Log",
        filters={"parent": data_import_name},
        fields=["log_index", "success", "docname", "messages"],
        order_by="log_index"
    )

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Row", "Status", "Document", "Messages"])

    for log in logs:
        writer.writerow([
            log.log_index,
            "Success" if log.success else "Failed",
            log.docname or "",
            log.messages or ""
        ])

    return output.getvalue()
```

### Analyze Import Errors

```python
import frappe
from collections import Counter

def analyze_import_errors(data_import_name):
    """Analyze and categorize import errors."""

    failed_logs = frappe.get_all(
        "Data Import Log",
        filters={
            "parent": data_import_name,
            "success": 0
        },
        fields=["messages"]
    )

    error_types = Counter()

    for log in failed_logs:
        if log.messages:
            messages = frappe.parse_json(log.messages)
            for msg in messages:
                # Categorize error
                if "required" in msg.lower():
                    error_types["Missing Required Field"] += 1
                elif "does not exist" in msg.lower():
                    error_types["Invalid Link"] += 1
                elif "duplicate" in msg.lower():
                    error_types["Duplicate Entry"] += 1
                else:
                    error_types["Other"] += 1

    return dict(error_types)
```

### Retry Failed Rows

```python
import frappe

def retry_failed_imports(data_import_name):
    """Get data for retrying failed imports."""

    data_import = frappe.get_doc("Data Import", data_import_name)
    importer = data_import.get_importer()

    # Get failed row indexes
    failed_rows = []
    for log in data_import.import_log:
        if not log.success:
            row_indexes = log.row_indexes.split(",") if log.row_indexes else []
            failed_rows.extend([int(i) for i in row_indexes])

    # Export template with failed rows only
    csv_content = importer.export_errored_rows()

    # Create new import with failed rows
    new_import = frappe.new_doc("Data Import")
    new_import.reference_doctype = data_import.reference_doctype
    new_import.import_type = data_import.import_type
    # ... save file and start import
```

## Hooks for Custom Processing

### after_import Hook

```python
# In your custom app's hooks.py
doc_events = {
    "Data Import Log": {
        "after_insert": "your_app.utils.after_import_log"
    }
}

# In your_app/utils.py
def after_import_log(doc, method):
    """Custom processing after each row is logged."""
    if doc.success and doc.docname:
        # Send notification for new Customer
        if frappe.get_meta(doc.parenttype).get_field("reference_doctype"):
            data_import = frappe.get_doc(doc.parenttype, doc.parent)
            if data_import.reference_doctype == "Customer":
                frappe.publish_realtime(
                    "new_customer_imported",
                    {"customer": doc.docname}
                )
```

## Related DocTypes

- [Data Import](data_import.md) - Parent DocType
- [Importer](importer.md) - Creates import logs

---

*Source: frappe/core/doctype/data_import_log/ | Last updated: 2026-02-04*
