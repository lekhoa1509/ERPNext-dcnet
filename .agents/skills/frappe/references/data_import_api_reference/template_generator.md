# API Reference: Import Template Generator

**Language**: Python

**Source**: `frappe/core/doctype/data_import/exporter.py`

---

## Overview

The template generator creates import templates for any DocType. Templates include header rows with field labels and optionally sample data. Used by `download_template` API.

## Main Function

### download_template

```python
@frappe.whitelist()
def download_template(
    doctype: str,
    export_fields: dict = None,
    export_records: str = None,
    export_filters: dict = None,
    file_type: str = "CSV"
) -> None
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `doctype` | str | Required | Target DocType |
| `export_fields` | dict | None | Fields to include (see format below) |
| `export_records` | str | None | "all", "by_filter", or "blank_template" |
| `export_filters` | dict | None | Filters for "by_filter" mode |
| `file_type` | str | "CSV" | "CSV" or "Excel" |

**Export Fields Format:**

```python
export_fields = {
    "Customer": ["name", "customer_name", "customer_type", "territory"],
    "Address": ["address_line1", "city", "country"]  # Child table
}
```

## Python API

### Generate Blank Template

```python
from frappe.core.doctype.data_import.data_import import download_template

# Blank template with all fields
download_template(
    doctype="Customer",
    export_records="blank_template"
)

# Blank template with specific fields only
download_template(
    doctype="Customer",
    export_fields={
        "Customer": ["customer_name", "customer_type", "territory"]
    },
    export_records="blank_template"
)
```

### Generate Template with Sample Data

```python
from frappe.core.doctype.data_import.data_import import download_template

# All records as sample
download_template(
    doctype="Customer",
    export_records="all",
    file_type="Excel"
)

# Filtered records as sample
download_template(
    doctype="Customer",
    export_records="by_filter",
    export_filters={"customer_type": "Company"},
    file_type="CSV"
)
```

## Using Exporter Class Directly

### Basic Template Generation

```python
from frappe.core.doctype.data_import.exporter import Exporter

# Create exporter for blank template
exporter = Exporter(
    doctype="Sales Order",
    export_fields="All",  # or "Mandatory"
    export_data=False
)

# Get as CSV array (list of lists)
csv_array = exporter.get_csv_array()
print(csv_array[0])  # Header row

# Build HTTP response (triggers download)
exporter.build_response()
```

### Template with Child Tables

```python
from frappe.core.doctype.data_import.exporter import Exporter

exporter = Exporter(
    doctype="Sales Order",
    export_fields={
        "Sales Order": [
            "name", "customer", "transaction_date", "delivery_date"
        ],
        "Sales Order Item": [
            "item_code", "qty", "rate", "amount"
        ]
    },
    export_data=False
)

csv_array = exporter.get_csv_array()
# Header includes: Customer, Transaction Date, ..., Item Code (Items), Qty (Items), ...
```

### Template with Sample Data

```python
from frappe.core.doctype.data_import.exporter import Exporter

exporter = Exporter(
    doctype="Item",
    export_fields={
        "Item": ["item_code", "item_name", "item_group", "stock_uom"]
    },
    export_data=True,  # Include existing records
    export_filters={"item_group": "Products"},
    export_page_length=100  # Limit records
)

csv_array = exporter.get_csv_array()
print(f"Header: {csv_array[0]}")
print(f"First record: {csv_array[1]}")
```

## Field Selection

### All Fields

```python
exporter = Exporter(
    doctype="Customer",
    export_fields="All"  # All exportable fields
)
```

### Mandatory Fields Only

```python
exporter = Exporter(
    doctype="Customer",
    export_fields="Mandatory"  # Only required fields
)
```

### Custom Field Selection

```python
exporter = Exporter(
    doctype="Customer",
    export_fields={
        "Customer": ["customer_name", "customer_type", "territory"],
        "Contact": ["first_name", "email_id", "phone"]
    }
)
```

## Exportable Field Rules

The `is_exportable` function determines which fields can be exported:

```python
def is_exportable(df):
    """
    Fields are exportable if:
    - Not hidden
    - Not read-only (except for name/autoname)
    - Not virtual field
    - Not internal fields (docstatus, idx, etc.)
    """
```

**Non-exportable field types:**
- Table fields (child tables are handled separately)
- Attach/Attach Image (binary data)
- HTML fields
- Button fields

## Column Header Format

### Parent DocType Fields

```
Field Label
```

Examples:
- `Customer Name`
- `Transaction Date`
- `Grand Total`

### Child Table Fields

```
Field Label (Child Table Label)
```

Examples:
- `Item Code (Items)`
- `Qty (Items)`
- `Account Head (Taxes)`

### ID Fields

```
ID
ID (Child Table Label)
```

## Usage Examples

### Generate Template for Update

```python
from frappe.core.doctype.data_import.exporter import Exporter

# Template with existing data for updates
exporter = Exporter(
    doctype="Customer",
    export_fields={
        "Customer": ["name", "customer_name", "territory"]  # name is required for updates
    },
    export_data=True,
    export_filters={"territory": "Vietnam"}
)

# Get CSV content
csv_array = exporter.get_csv_array_for_export()
```

### Save Template to File

```python
import csv
from frappe.core.doctype.data_import.exporter import Exporter

exporter = Exporter(
    doctype="Item",
    export_fields="Mandatory",
    export_data=False
)

csv_array = exporter.get_csv_array()

# Save to file
with open("/tmp/item_template.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(csv_array)
```

### Generate Excel Template

```python
from frappe.core.doctype.data_import.exporter import Exporter

exporter = Exporter(
    doctype="Sales Invoice",
    export_fields="All",
    export_data=False,
    file_type="Excel"
)

# build_response() handles Excel generation
exporter.build_response()
```

### Custom Template Builder

```python
import frappe
from frappe.core.doctype.data_import.exporter import Exporter, format_column_name

def build_custom_template(doctype, field_mapping):
    """
    Build template with custom column headers.

    Args:
        doctype: Target DocType
        field_mapping: Dict of {custom_header: fieldname}
    """
    meta = frappe.get_meta(doctype)

    headers = []
    for custom_header, fieldname in field_mapping.items():
        df = meta.get_field(fieldname)
        if df:
            headers.append(custom_header)

    return [headers]  # Return as CSV array with header only
```

## API Endpoints

### REST API

```bash
# Download blank template
GET /api/method/frappe.core.doctype.data_import.data_import.download_template?doctype=Customer&export_records=blank_template

# Download template with data
GET /api/method/frappe.core.doctype.data_import.data_import.download_template?doctype=Customer&export_records=all&file_type=Excel
```

### JavaScript API

```javascript
// Download template from client
frappe.call({
    method: "frappe.core.doctype.data_import.data_import.download_template",
    args: {
        doctype: "Customer",
        export_fields: JSON.stringify({
            "Customer": ["customer_name", "customer_type", "territory"]
        }),
        export_records: "blank_template",
        file_type: "CSV"
    }
});
```

## Related Classes

- [Exporter](exporter.md) - Full exporter class
- [Data Import](data_import.md) - Import DocType

---

*Source: frappe/core/doctype/data_import/data_import.py, exporter.py | Last updated: 2026-02-04*
