# API Reference: Column Class

**Language**: Python

**Source**: `frappe/core/doctype/data_import/importer.py`

---

## Overview

The `Column` class represents a single column in an import file. It handles field mapping, date format detection, value validation, and provides metadata for import processing.

## Class Definition

```python
class Column:
    def __init__(
        self,
        index: int,
        header: str,
        doctype: str,
        column_values: list,
        map_to_field: str = None,
        seen: set = None
    )
```

## Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `index` | int | Required | Column index (0-based) |
| `header` | str | Required | Column header text |
| `doctype` | str | Required | Target DocType |
| `column_values` | list | Required | All values in this column (for analysis) |
| `map_to_field` | str | None | Override automatic field mapping |
| `seen` | set | None | Set of already mapped fields (for duplicate detection) |

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `index` | int | Column index |
| `header` | str | Original header text |
| `df` | DocField | Mapped DocType field |
| `skip_import` | bool | Whether to skip this column |
| `date_format` | str | Detected date format |
| `warnings` | list | Column-level warnings |

## Methods

### parse

Parses the column and maps to a DocType field.

```python
def parse(self) -> None:
    """
    Parses column header and maps to DocField.
    Sets:
    - self.df: Matched DocField or None
    - self.skip_import: True if column should be skipped
    - self.date_format: Detected format for date columns
    """
```

**Example:**

```python
column = Column(
    index=0,
    header="Customer Name",
    doctype="Customer",
    column_values=["ACME Corp", "Beta Inc", "Gamma LLC"]
)
column.parse()

print(f"Mapped to: {column.df.fieldname}")  # customer_name
print(f"Field type: {column.df.fieldtype}")  # Data
```

### guess_date_format_for_column

Detects the most common date format in the column.

```python
def guess_date_format_for_column(self) -> str:
    """
    Analyzes all values to detect date format.

    Returns:
        str: Date format string (e.g., '%Y-%m-%d')
    """
```

**Supported Formats:**

| Format | Example | Pattern |
|--------|---------|---------|
| ISO | 2024-01-15 | `%Y-%m-%d` |
| European | 15-01-2024 | `%d-%m-%Y` |
| US | 01/15/2024 | `%m/%d/%Y` |
| UK | 15/01/2024 | `%d/%m/%Y` |
| German | 15.01.2024 | `%d.%m.%Y` |

**Example:**

```python
column = Column(
    index=3,
    header="Posting Date",
    doctype="Sales Invoice",
    column_values=["2024-01-15", "2024-01-16", "2024-01-17"]
)
column.parse()

print(f"Date format: {column.date_format}")  # %Y-%m-%d
```

### validate_values

Validates all values in the column.

```python
def validate_values(self) -> list:
    """
    Validates each value against field constraints.

    Returns:
        list: Warning dictionaries
    """
```

**Example:**

```python
column = Column(0, "Status", "Lead", ["Open", "Invalid", "Converted"])
column.parse()
warnings = column.validate_values()

for w in warnings:
    print(f"Row {w['row']}: {w['message']}")
```

### as_dict

Returns column metadata as dictionary.

```python
def as_dict(self) -> dict:
    """
    Returns:
        dict: Column information for preview
    """
```

**Example:**

```python
column_info = column.as_dict()
print(column_info)
# {
#     'index': 0,
#     'header': 'Customer Name',
#     'fieldname': 'customer_name',
#     'fieldtype': 'Data',
#     'label': 'Customer Name',
#     'options': None,
#     'reqd': 1,
#     'skip_import': False
# }
```

## Field Type Handling

### Text Fields

```python
# Data, Small Text, Text, Long Text, Text Editor
column = Column(0, "Description", "Item", ["Desc 1", "Desc 2"])
# No special parsing needed
```

### Numeric Fields

```python
# Int, Float, Currency, Percent
column = Column(0, "Qty", "Sales Order Item", ["100", "50", "25"])
# Validates numeric format
```

### Link Fields

```python
# Link to another DocType
column = Column(0, "Customer", "Sales Order", ["CUST-001", "CUST-002"])
# Validates linked documents exist
```

### Select Fields

```python
# Select with predefined options
column = Column(0, "Status", "Lead", ["Open", "Converted"])
# Validates against allowed options
```

### Date/Datetime Fields

```python
# Date, Datetime
column = Column(0, "Posting Date", "Journal Entry", ["2024-01-15"])
# Auto-detects format and parses
```

### Check Fields

```python
# Checkbox (boolean)
column = Column(0, "Is Active", "Customer", ["1", "0", "Yes", "No"])
# Accepts: 1, 0, Yes, No, True, False
```

## Usage Examples

### Basic Column Analysis

```python
from frappe.core.doctype.data_import.importer import Column

# Analyze a column
values = ["ACME Corp", "Beta Inc", "Gamma LLC", "Delta Ltd"]
column = Column(
    index=0,
    header="Customer Name",
    doctype="Customer",
    column_values=values
)
column.parse()

print(f"Header: {column.header}")
print(f"Mapped to: {column.df.fieldname if column.df else 'None'}")
print(f"Field type: {column.df.fieldtype if column.df else 'None'}")
print(f"Required: {column.df.reqd if column.df else False}")
```

### Custom Field Mapping

```python
# Override automatic mapping
column = Column(
    index=0,
    header="Cust ID",  # Non-standard header
    doctype="Customer",
    column_values=["C001", "C002"],
    map_to_field="customer_name"  # Force mapping
)
column.parse()
print(f"Mapped to: {column.df.fieldname}")  # customer_name
```

### Duplicate Detection

```python
seen_fields = {"customer_name"}  # Already used

column = Column(
    index=1,
    header="Customer Name",  # Duplicate
    doctype="Customer",
    column_values=["Test"],
    seen=seen_fields
)
column.parse()

if column.skip_import:
    print("Column skipped - duplicate field")
```

### Date Format Detection

```python
# Mixed date formats in column
values = ["15/01/2024", "20/01/2024", "25/01/2024"]

column = Column(0, "Due Date", "Sales Order", values)
column.parse()

print(f"Detected format: {column.date_format}")  # %d/%m/%Y
```

### Validation Example

```python
# Validate Select field options
values = ["Open", "Invalid Option", "Converted", "Bad Value"]

column = Column(0, "Status", "Lead", values)
column.parse()
warnings = column.validate_values()

for w in warnings:
    print(f"Row {w['row']}: {w['message']}")
# Row 2: 'Invalid Option' is not a valid option
# Row 4: 'Bad Value' is not a valid option
```

## Child Table Columns

```python
# Child table column parsing
# Header format: "Field Label (Child Table Label)"

column = Column(
    index=2,
    header="Item Code (Items)",  # Child table field
    doctype="Sales Order",
    column_values=["ITEM-001", "ITEM-002"]
)
column.parse()

print(f"Field: {column.df.fieldname}")  # item_code
print(f"Parent: {column.df.parent}")    # Sales Order Item
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Column not mapped | Header doesn't match any field | Use exact label or fieldname |
| Duplicate column | Field already mapped | Remove duplicate column |
| Invalid date format | Can't detect date format | Use ISO format (YYYY-MM-DD) |
| Invalid option | Select value not in options | Check valid options |

## Related Classes

- [Header](header.md) - Header row with all columns
- [Row](row.md) - Data row parsing
- [ImportFile](import_file.md) - File-level parsing

---

*Source: frappe/core/doctype/data_import/importer.py | Last updated: 2026-02-04*
