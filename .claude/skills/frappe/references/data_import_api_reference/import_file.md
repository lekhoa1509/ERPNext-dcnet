# API Reference: ImportFile Class

**Language**: Python

**Source**: `frappe/core/doctype/data_import/importer.py`

---

## Overview

The `ImportFile` class handles parsing and processing of import files (CSV/Excel). It reads the file, parses headers, and prepares data for import.

## Class Definition

```python
class ImportFile:
    def __init__(
        self,
        doctype: str,
        file: str,
        template_options: dict = None,
        import_type: str = None
    )
```

## Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `doctype` | str | Required | Target DocType for import |
| `file` | str | Required | File path or URL to import file |
| `template_options` | dict | None | Options for template parsing |
| `import_type` | str | None | "Insert New Records" or "Update Existing Records" |

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `raw_data` | list | Raw data rows from file |
| `header` | Header | Header row object |
| `data` | list | Parsed data rows |
| `columns` | list | Column definitions |
| `warnings` | list | Parsing warnings |

## Methods

### get_data_from_template_file

Reads and returns raw data from the template file.

```python
def get_data_from_template_file(self) -> list:
    """
    Returns:
        list: Raw data rows including header
    """
```

**Example:**

```python
import_file = ImportFile("Customer", "/path/to/customers.csv")
raw_data = import_file.get_data_from_template_file()
print(f"Total rows: {len(raw_data)}")
```

### parse_data_from_template

Parses raw data and creates structured Row objects.

```python
def parse_data_from_template(self) -> None:
    """
    Parses raw_data and populates:
    - self.header: Header object
    - self.data: List of Row objects
    - self.columns: Column definitions
    """
```

**Example:**

```python
import_file = ImportFile("Customer", "/path/to/customers.csv")
import_file.get_data_from_template_file()
import_file.parse_data_from_template()

for row in import_file.data:
    print(row.as_list())
```

### get_data_for_import_preview

Returns data formatted for UI preview with serial numbers.

```python
def get_data_for_import_preview(self) -> frappe._dict:
    """
    Returns:
        frappe._dict with keys:
        - columns: List of column definitions
        - data: List of row data with serial numbers
        - warnings: List of warning messages
    """
```

**Example:**

```python
import_file = ImportFile("Customer", "/path/to/customers.csv")
preview = import_file.get_data_for_import_preview()

print(f"Columns: {len(preview.columns)}")
print(f"Rows: {len(preview.data)}")
print(f"Warnings: {preview.warnings}")
```

### get_payloads_for_import

Generates document payloads ready for import.

```python
def get_payloads_for_import(self) -> Generator:
    """
    Yields:
        tuple: (doc_dict, rows_list, row_indexes)
    """
```

**Example:**

```python
import_file = ImportFile("Customer", "/path/to/customers.csv")
import_file.parse_data_from_template()

for doc, rows, indexes in import_file.get_payloads_for_import():
    print(f"Document: {doc}")
    print(f"Source rows: {indexes}")
```

### parse_next_row_for_import

Parses rows that make up a single document (handles child tables).

```python
def parse_next_row_for_import(self, data: list) -> tuple:
    """
    Args:
        data: Remaining data rows to parse

    Returns:
        tuple: (doc_dict, rows_used, remaining_data)
    """
```

### read_file

Reads content from a file path.

```python
def read_file(self, file_path: str) -> tuple:
    """
    Args:
        file_path: Path to CSV or Excel file

    Returns:
        tuple: (content_bytes, file_extension)
    """
```

### read_content

Parses file content based on extension.

```python
def read_content(self, content: bytes, extension: str) -> list:
    """
    Args:
        content: File content bytes
        extension: File extension (.csv, .xlsx, .xls)

    Returns:
        list: Parsed rows
    """
```

### get_warnings

Collects all warnings from parsing.

```python
def get_warnings(self) -> list:
    """
    Returns:
        list: Warning dictionaries with 'row', 'col', 'message' keys
    """
```

## Usage Examples

### Basic File Parsing

```python
from frappe.core.doctype.data_import.importer import ImportFile

# Create ImportFile instance
import_file = ImportFile(
    doctype="Customer",
    file="/home/frappe/customers.csv",
    import_type="Insert New Records"
)

# Get raw data
raw_data = import_file.get_data_from_template_file()
print(f"Header: {raw_data[0]}")
print(f"Data rows: {len(raw_data) - 1}")

# Parse into structured format
import_file.parse_data_from_template()

# Access parsed data
for col in import_file.columns:
    print(f"Column: {col.header} -> {col.df.fieldname if col.df else 'unmapped'}")
```

### Processing Child Tables

```python
from frappe.core.doctype.data_import.importer import ImportFile

# Sales Order with child items
import_file = ImportFile(
    doctype="Sales Order",
    file="/home/frappe/sales_orders.csv"
)
import_file.parse_data_from_template()

# Each payload includes parent + children
for doc, rows, indexes in import_file.get_payloads_for_import():
    print(f"Sales Order: {doc.get('customer')}")
    print(f"Items: {len(doc.get('items', []))}")
    print(f"From rows: {indexes}")
```

### Handling Google Sheets URL

```python
from frappe.core.doctype.data_import.importer import ImportFile

# Google Sheets public URL
sheets_url = "https://docs.google.com/spreadsheets/d/xxx/export?format=csv"

import_file = ImportFile(
    doctype="Item",
    file=sheets_url
)

preview = import_file.get_data_for_import_preview()
print(f"Loaded {len(preview.data)} rows from Google Sheets")
```

## Error Handling

```python
from frappe.core.doctype.data_import.importer import ImportFile
import frappe

try:
    import_file = ImportFile("Customer", "/path/to/file.csv")
    import_file.parse_data_from_template()
except frappe.ValidationError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Parse error: {e}")
```

## Related Classes

- [Importer](importer.md) - Main import orchestrator
- [Header](header.md) - Header row processing
- [Row](row.md) - Data row processing
- [Column](column.md) - Column definition and mapping

---

*Source: frappe/core/doctype/data_import/importer.py | Last updated: 2026-02-04*
