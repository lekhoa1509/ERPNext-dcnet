# API Reference: Header Class

**Language**: Python

**Source**: `frappe/core/doctype/data_import/importer.py`

---

## Overview

The `Header` class extends `Row` and handles parsing of the header row in import files. It maps column headers to DocType fields, handles child table columns, and provides column metadata.

## Class Definition

```python
class Header(Row):
    def __init__(
        self,
        index: int,
        row: list,
        doctype: str,
        raw_data: list,
        column_to_field_map: dict = None
    )
```

## Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `index` | int | Required | Row index (usually 0) |
| `row` | list | Required | Header row values (column names) |
| `doctype` | str | Required | Target DocType |
| `raw_data` | list | Required | All data including header for column analysis |
| `column_to_field_map` | dict | None | Custom column-to-field mapping |

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `columns` | list[Column] | List of Column objects |
| `column_indexes` | dict | Maps doctype to column indexes |
| `fields_dict` | dict | Maps header strings to DocFields |

## Methods

### get_column_indexes

Gets column indexes for a specific doctype or child table.

```python
def get_column_indexes(
    self,
    doctype: str,
    tablefield: DocField = None
) -> list:
    """
    Args:
        doctype: DocType name
        tablefield: Table field definition (for child tables)

    Returns:
        list: Column indexes belonging to that doctype
    """
```

**Example:**

```python
header = Header(0, header_row, "Sales Order", raw_data)

# Get main doctype columns
so_indexes = header.get_column_indexes("Sales Order")
print(f"Sales Order columns: {so_indexes}")

# Get child table columns
item_indexes = header.get_column_indexes("Sales Order Item", items_field)
print(f"Item columns: {item_indexes}")
```

### get_columns

Gets Column objects at specified indexes.

```python
def get_columns(self, indexes: list) -> list:
    """
    Args:
        indexes: List of column indexes

    Returns:
        list: Column objects at those indexes
    """
```

**Example:**

```python
# Get all Customer columns
customer_indexes = header.get_column_indexes("Customer")
columns = header.get_columns(customer_indexes)

for col in columns:
    print(f"{col.header} -> {col.df.fieldname}")
```

## Column Mapping Logic

### Header Format Rules

The Header class maps column headers to fields using these patterns:

1. **Field Label**: `Customer Name` -> `customer_name`
2. **Field Name**: `customer_name` -> `customer_name`
3. **Child Table Label**: `Item Code (Items)` -> `items.item_code`
4. **Child Table Fieldname**: `Sales Order Item:item_code` -> `items.item_code`

### Mapping Priority

```
1. Exact label match
2. Exact fieldname match
3. Case-insensitive label match
4. Child table pattern match
```

### Custom Column Mapping

```python
# Override default mapping
custom_map = {
    "Customer ID": "customer",
    "Product": "item_code",
    "Qty": "qty"
}

header = Header(
    index=0,
    row=["Customer ID", "Product", "Qty"],
    doctype="Sales Order Item",
    raw_data=data,
    column_to_field_map=custom_map
)
```

## Usage Examples

### Basic Header Parsing

```python
from frappe.core.doctype.data_import.importer import Header

# Simple header row
header_row = ["Customer Name", "Customer Type", "Territory", "Email"]
data = [header_row, ["ACME Corp", "Company", "Vietnam", "acme@example.com"]]

header = Header(
    index=0,
    row=header_row,
    doctype="Customer",
    raw_data=data
)

# Check mapped columns
for col in header.columns:
    if col.df:
        print(f"'{col.header}' -> {col.df.fieldname} ({col.df.fieldtype})")
    else:
        print(f"'{col.header}' -> UNMAPPED")
```

### Child Table Headers

```python
# Sales Order with Items child table
header_row = [
    "Customer",           # Parent field
    "Delivery Date",      # Parent field
    "Item Code (Items)",  # Child table field
    "Qty (Items)",        # Child table field
    "Rate (Items)"        # Child table field
]

header = Header(0, header_row, "Sales Order", raw_data)

# Get parent columns
parent_cols = header.get_column_indexes("Sales Order")
print(f"Parent columns: {parent_cols}")  # [0, 1]

# Get child columns
items_field = frappe.get_meta("Sales Order").get_field("items")
child_cols = header.get_column_indexes("Sales Order Item", items_field)
print(f"Child columns: {child_cols}")  # [2, 3, 4]
```

### Multiple Child Tables

```python
# Sales Invoice with Items and Taxes
header_row = [
    "Customer",
    "Posting Date",
    "Item Code (Items)",
    "Qty (Items)",
    "Account Head (Taxes)",
    "Rate (Taxes)"
]

header = Header(0, header_row, "Sales Invoice", raw_data)

# Map each child table separately
items_indexes = header.get_column_indexes(
    "Sales Invoice Item",
    frappe.get_meta("Sales Invoice").get_field("items")
)

taxes_indexes = header.get_column_indexes(
    "Sales Taxes and Charges",
    frappe.get_meta("Sales Invoice").get_field("taxes")
)
```

### Accessing Column Metadata

```python
header = Header(0, header_row, "Customer", raw_data)

for col in header.columns:
    print(f"Index: {col.index}")
    print(f"Header: {col.header}")
    print(f"Field: {col.df.fieldname if col.df else None}")
    print(f"Type: {col.df.fieldtype if col.df else None}")
    print(f"Required: {col.df.reqd if col.df else False}")
    print(f"Date Format: {col.date_format}")
    print("---")
```

## Field Matching Details

### build_fields_dict_for_column_matching

The Header class uses this helper function internally:

```python
def build_fields_dict_for_column_matching(parent_doctype):
    """
    Builds dict mapping various header formats to DocFields.

    Returns dict like:
    {
        'Customer': df1,           # Label
        'customer': df1,           # Fieldname
        'Due Date': df2,
        'due_date': df2,
        'Item Code (Items)': df3,  # Child table label
        'Sales Order Item:item_code': df3,  # Child table fieldname
    }
    """
```

### Handling Duplicate Headers

```python
# If same header appears multiple times
header_row = ["Name", "Description", "Name"]  # Duplicate "Name"

header = Header(0, header_row, "DocType", raw_data)

# Second "Name" is marked as duplicate with warning
for col in header.columns:
    if col.skip_import:
        print(f"Skipping duplicate column: {col.header}")
```

## Warnings

| Warning | Cause | Solution |
|---------|-------|----------|
| "Column not mapped" | Header doesn't match any field | Check spelling or use fieldname |
| "Duplicate column" | Same header appears twice | Remove duplicate |
| "Invalid child table reference" | Child table doesn't exist | Check DocType structure |

## Related Classes

- [Row](row.md) - Base class for row handling
- [Column](column.md) - Individual column processing
- [ImportFile](import_file.md) - File-level parsing

---

*Source: frappe/core/doctype/data_import/importer.py | Last updated: 2026-02-04*
