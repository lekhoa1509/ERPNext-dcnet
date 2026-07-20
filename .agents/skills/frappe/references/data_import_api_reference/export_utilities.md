# API Reference: Export Utilities

**Language**: Python

**Source**: `frappe/core/doctype/data_import/exporter.py`, `data_import.py`

---

## Overview

Export utilities provide functions for exporting data from Frappe DocTypes to CSV, Excel, and JSON formats. Used for backups, data transfer, and generating import templates.

## Main Export Functions

### export_json

Export DocType records to JSON file.

```python
def export_json(
    doctype: str,
    path: str,
    filters: dict = None,
    or_filters: dict = None,
    name: str = None,
    order_by: str = "creation asc"
) -> None:
    """
    Export records to JSON file.

    Args:
        doctype: DocType to export
        path: Output file path
        filters: Query filters
        or_filters: OR query filters
        name: Specific document name
        order_by: Sort order
    """
```

**Example:**

```python
from frappe.core.doctype.data_import.data_import import export_json

# Export all customers
export_json("Customer", "/tmp/customers.json")

# Export filtered customers
export_json(
    "Customer",
    "/tmp/vietnam_customers.json",
    filters={"territory": "Vietnam"}
)

# Export specific customer
export_json(
    "Customer",
    "/tmp/customer_001.json",
    name="CUST-001"
)
```

### export_csv

Export DocType records to CSV file.

```python
def export_csv(doctype: str, path: str) -> None:
    """
    Export all records to CSV file.

    Args:
        doctype: DocType to export
        path: Output file path
    """
```

**Example:**

```python
from frappe.core.doctype.data_import.data_import import export_csv

export_csv("Item", "/tmp/items.csv")
```

## Exporter Class

### Basic Usage

```python
from frappe.core.doctype.data_import.exporter import Exporter

# Export with specific fields
exporter = Exporter(
    doctype="Customer",
    export_fields={
        "Customer": ["name", "customer_name", "customer_type", "territory"]
    },
    export_data=True,
    export_filters={"territory": "Vietnam"},
    file_type="CSV"  # or "Excel"
)

# Get as 2D array
csv_array = exporter.get_csv_array()

# Build HTTP response (triggers download)
exporter.build_response()
```

### Export All Fields

```python
exporter = Exporter(
    doctype="Item",
    export_fields="All",  # All exportable fields
    export_data=True
)
```

### Export Mandatory Fields Only

```python
exporter = Exporter(
    doctype="Sales Order",
    export_fields="Mandatory",  # Only required fields
    export_data=False  # Blank template
)
```

### Export with Child Tables

```python
exporter = Exporter(
    doctype="Sales Order",
    export_fields={
        "Sales Order": ["name", "customer", "transaction_date", "grand_total"],
        "Sales Order Item": ["item_code", "qty", "rate", "amount"]
    },
    export_data=True,
    export_filters={"docstatus": 1}  # Only submitted
)
```

## Export Field Selection

### get_all_exportable_fields

```python
def get_all_exportable_fields(self) -> dict:
    """
    Get all exportable fields for DocType and child tables.

    Returns:
        dict: {doctype: [field1, field2, ...], child_doctype: [...]}
    """
```

### get_exportable_fields

```python
def get_exportable_fields(
    self,
    doctype: str,
    fieldnames: list
) -> list:
    """
    Get DocField objects for specified fields.

    Args:
        doctype: DocType name
        fieldnames: List of field names

    Returns:
        list: DocField objects
    """
```

### is_exportable

```python
def is_exportable(df: DocField) -> bool:
    """
    Check if field can be exported.

    Exportable fields:
    - Not hidden
    - Not read_only (except name)
    - Not Table type
    - Not Attach/Attach Image
    - Not HTML/Button

    Args:
        df: DocField to check

    Returns:
        bool: True if exportable
    """
```

## Data Export Methods

### get_data_to_export

```python
def get_data_to_export(self) -> list:
    """
    Query and format data for export.

    Returns:
        list: 2D array of values
    """
```

### get_data_as_docs

```python
def get_data_as_docs(self) -> list:
    """
    Get data as list of document dicts.

    Returns:
        list: Document dictionaries
    """
```

### get_csv_array

```python
def get_csv_array(self) -> list:
    """
    Get complete CSV array with headers and data.

    Returns:
        list: [[header1, header2, ...], [val1, val2, ...], ...]
    """
```

### get_csv_array_for_export

```python
def get_csv_array_for_export(self) -> list:
    """
    Get CSV array formatted for file export.

    Handles special formatting:
    - Dates formatted for locale
    - Numbers formatted consistently
    - Empty child rows have empty parent columns
    """
```

## HTTP Response

### build_response

```python
def build_response(self) -> None:
    """
    Build HTTP response for file download.

    Sets frappe.response:
    - type: "csv" or "xlsx"
    - doctype: "Data Export"
    - result: CSV content or Excel workbook
    """
```

**Example:**

```python
@frappe.whitelist()
def download_customers():
    exporter = Exporter(
        doctype="Customer",
        export_fields="All",
        export_data=True,
        file_type="Excel"
    )
    exporter.build_response()
```

## Custom Export Functions

### Export with Transformation

```python
import frappe
from frappe.core.doctype.data_import.exporter import Exporter

def export_customers_for_external_system(filters=None):
    """
    Export customers with field transformations.
    """
    exporter = Exporter(
        doctype="Customer",
        export_fields={
            "Customer": ["name", "customer_name", "customer_type", "territory"]
        },
        export_data=True,
        export_filters=filters
    )

    csv_array = exporter.get_csv_array()

    # Transform data
    header = csv_array[0]
    transformed = [header]

    for row in csv_array[1:]:
        # Transform customer_type
        type_idx = header.index("Customer Type")
        if row[type_idx] == "Company":
            row[type_idx] = "B2B"
        else:
            row[type_idx] = "B2C"

        transformed.append(row)

    return transformed
```

### Export to Multiple Formats

```python
def export_data_multiformat(doctype, filters=None):
    """
    Export data to CSV, Excel, and JSON.
    """
    import csv
    import json
    from io import StringIO, BytesIO
    from openpyxl import Workbook

    exporter = Exporter(
        doctype=doctype,
        export_fields="All",
        export_data=True,
        export_filters=filters
    )

    csv_array = exporter.get_csv_array()

    # CSV
    csv_output = StringIO()
    writer = csv.writer(csv_output)
    writer.writerows(csv_array)
    csv_content = csv_output.getvalue()

    # Excel
    wb = Workbook()
    ws = wb.active
    for row in csv_array:
        ws.append(row)
    excel_output = BytesIO()
    wb.save(excel_output)
    excel_content = excel_output.getvalue()

    # JSON
    docs = exporter.get_data_as_docs()
    json_content = json.dumps(docs, indent=2, default=str)

    return {
        "csv": csv_content,
        "xlsx": excel_content,
        "json": json_content
    }
```

### Scheduled Export

```python
import frappe
from frappe.utils import get_site_path
import os

def scheduled_export():
    """
    Export data daily for backup.
    """
    export_dir = os.path.join(get_site_path(), "private", "backups", "exports")
    os.makedirs(export_dir, exist_ok=True)

    doctypes_to_export = ["Customer", "Supplier", "Item", "Sales Order"]

    from frappe.core.doctype.data_import.data_import import export_json

    for doctype in doctypes_to_export:
        filename = f"{doctype.lower().replace(' ', '_')}_{frappe.utils.today()}.json"
        filepath = os.path.join(export_dir, filename)

        export_json(doctype, filepath)
        frappe.logger().info(f"Exported {doctype} to {filepath}")
```

## Filtered Exports

### Export by Date Range

```python
def export_orders_by_date(start_date, end_date):
    """
    Export Sales Orders within date range.
    """
    exporter = Exporter(
        doctype="Sales Order",
        export_fields={
            "Sales Order": ["name", "customer", "transaction_date", "grand_total"],
            "Sales Order Item": ["item_code", "qty", "rate", "amount"]
        },
        export_data=True,
        export_filters={
            "transaction_date": ["between", [start_date, end_date]],
            "docstatus": 1
        }
    )

    return exporter.get_csv_array()
```

### Export with Pagination

```python
def export_large_dataset(doctype, page_size=1000):
    """
    Export large dataset in pages.
    """
    total = frappe.db.count(doctype)
    pages = (total + page_size - 1) // page_size

    all_data = []
    header = None

    for page in range(pages):
        exporter = Exporter(
            doctype=doctype,
            export_fields="All",
            export_data=True,
            export_page_length=page_size,
            export_filters={}  # Add offset via SQL
        )

        csv_array = exporter.get_csv_array()

        if page == 0:
            header = csv_array[0]
            all_data.append(header)

        all_data.extend(csv_array[1:])

    return all_data
```

## Column Formatting

### format_column_name

```python
def format_column_name(df: DocField) -> str:
    """
    Format column name for export.

    Args:
        df: DocField

    Returns:
        str: Formatted column header
    """
```

### Custom Column Headers

```python
def export_with_custom_headers(doctype, field_labels):
    """
    Export with custom column headers.

    Args:
        doctype: DocType name
        field_labels: Dict of {fieldname: custom_label}
    """
    exporter = Exporter(
        doctype=doctype,
        export_fields="All",
        export_data=True
    )

    csv_array = exporter.get_csv_array()

    # Replace headers
    header = csv_array[0]
    new_header = []
    for col in header:
        new_header.append(field_labels.get(col, col))

    csv_array[0] = new_header

    return csv_array
```

## Related Functions

- [Exporter Class](exporter.md) - Main exporter class
- [Template Generator](template_generator.md) - Generate templates
- [Data Import](data_import.md) - Import functions

---

*Source: frappe/core/doctype/data_import/exporter.py | Last updated: 2026-02-04*
