# API Reference: Row Class

**Language**: Python

**Source**: `frappe/core/doctype/data_import/importer.py`

---

## Overview

The `Row` class represents a single data row in an import file. It handles parsing values, type conversion, validation, and building document dictionaries.

## Class Definition

```python
class Row:
    def __init__(
        self,
        index: int,
        row: list,
        doctype: str,
        header: Header,
        import_type: str
    )
```

## Constructor Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `index` | int | Row number in the file (0-indexed) |
| `row` | list | Raw row data as list of values |
| `doctype` | str | Target DocType |
| `header` | Header | Header object for column mapping |
| `import_type` | str | "Insert New Records" or "Update Existing Records" |

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `index` | int | Row index in file |
| `row` | list | Raw row values |
| `doctype` | str | Target DocType |
| `header` | Header | Header row reference |
| `import_type` | str | Import type |
| `warnings` | list | Validation warnings |
| `errors` | list | Validation errors |

## Methods

### parse_doc

Parses row data into a document dictionary.

```python
def parse_doc(
    self,
    doctype: str,
    parent_doc: dict = None,
    table_df: DocField = None
) -> dict:
    """
    Args:
        doctype: Target DocType
        parent_doc: Parent document for child tables
        table_df: Table field definition for child tables

    Returns:
        dict: Document dictionary with field values
    """
```

**Example:**

```python
# Parse main document
doc = row.parse_doc("Customer")
print(doc)
# {'customer_name': 'ACME Corp', 'customer_type': 'Company', ...}

# Parse child table row
child_doc = row.parse_doc(
    "Sales Order Item",
    parent_doc=parent,
    table_df=items_field
)
```

### validate_value

Validates a cell value against field constraints.

```python
def validate_value(self, value: Any, col: Column) -> None:
    """
    Args:
        value: Cell value to validate
        col: Column definition

    Raises:
        Adds to self.warnings or self.errors
    """
```

**Validations performed:**
- Required field check
- Link field existence
- Select field options
- Data type compatibility
- Length constraints

### link_exists

Checks if a Link field value exists.

```python
def link_exists(self, value: str, df: DocField) -> bool:
    """
    Args:
        value: Link field value
        df: Field definition

    Returns:
        bool: True if linked document exists
    """
```

### parse_value

Converts raw string value to appropriate Python type.

```python
def parse_value(self, value: str, col: Column) -> Any:
    """
    Args:
        value: Raw string value
        col: Column definition

    Returns:
        Converted value (int, float, date, etc.)
    """
```

**Type Conversions:**

| Field Type | Conversion |
|------------|------------|
| Int | `int(value)` |
| Float, Currency, Percent | `float(value)` |
| Check | `1` or `0` |
| Date | `datetime.date` |
| Datetime | `datetime.datetime` |
| Time | `datetime.time` |
| Duration | seconds as int |
| JSON | parsed JSON |

### get_date

Parses date value with format detection.

```python
def get_date(self, value: str, column: Column) -> date:
    """
    Args:
        value: Date string
        column: Column with date_format

    Returns:
        datetime.date object
    """
```

**Supported Formats:**
- `YYYY-MM-DD` (ISO, recommended)
- `DD-MM-YYYY`
- `MM/DD/YYYY`
- `DD/MM/YYYY`
- `DD.MM.YYYY`

### get_datetime

Parses datetime value.

```python
def get_datetime(self, value: str, column: Column) -> datetime:
    """
    Args:
        value: Datetime string
        column: Column with date_format

    Returns:
        datetime.datetime object
    """
```

### get_values

Gets values at specified column indexes.

```python
def get_values(self, indexes: list) -> list:
    """
    Args:
        indexes: List of column indexes

    Returns:
        list: Values at those indexes
    """
```

### get

Gets value at a specific index.

```python
def get(self, index: int) -> Any:
    """
    Args:
        index: Column index

    Returns:
        Value at index or None
    """
```

### as_list

Returns row as list.

```python
def as_list(self) -> list:
    """
    Returns:
        list: Raw row values
    """
```

## Usage Examples

### Basic Row Parsing

```python
from frappe.core.doctype.data_import.importer import Row, Header

# Create header
header = Header(0, ["Name", "Email", "Phone"], "Contact", raw_data)

# Create row
row = Row(
    index=1,
    row=["John Doe", "john@example.com", "123-456-7890"],
    doctype="Contact",
    header=header,
    import_type="Insert New Records"
)

# Parse to document
doc = row.parse_doc("Contact")
print(doc)
# {'first_name': 'John Doe', 'email_id': 'john@example.com', 'phone': '123-456-7890'}
```

### Handling Date Parsing

```python
# Row with date values
row = Row(
    index=1,
    row=["SO-001", "2024-01-15", "2024-01-30"],
    doctype="Sales Order",
    header=header,
    import_type="Insert New Records"
)

doc = row.parse_doc("Sales Order")
print(doc['transaction_date'])  # datetime.date(2024, 1, 15)
print(doc['delivery_date'])     # datetime.date(2024, 1, 30)
```

### Value Type Conversion

```python
# Row with mixed types
row_data = ["ITEM-001", "100", "99.50", "1", "2024-01-15"]
row = Row(1, row_data, "Sales Order Item", header, "Insert New Records")

doc = row.parse_doc("Sales Order Item")
print(doc['qty'])   # 100 (int)
print(doc['rate'])  # 99.50 (float)
print(doc['is_free_item'])  # 1 (check)
```

### Validation and Warnings

```python
row = Row(1, row_data, "Customer", header, "Insert New Records")
doc = row.parse_doc("Customer")

# Check for validation issues
if row.warnings:
    for warning in row.warnings:
        print(f"Warning at row {warning['row']}, col {warning['col']}: {warning['message']}")

if row.errors:
    for error in row.errors:
        print(f"Error: {error['message']}")
```

### Link Field Validation

```python
# Check if linked document exists
exists = row.link_exists("CUST-001", customer_field)
if not exists:
    print("Customer CUST-001 does not exist")
```

## Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Value missing for required field" | Empty required field | Fill in the value |
| "Invalid value for field" | Type mismatch | Check data type |
| "Link does not exist" | Invalid link reference | Create linked document first |
| "Invalid option" | Select field value not in options | Use valid option |
| "Date format not recognized" | Unparseable date | Use YYYY-MM-DD format |

## Related Classes

- [Header](header.md) - Header row processing
- [Column](column.md) - Column definition
- [ImportFile](import_file.md) - File parsing

---

*Source: frappe/core/doctype/data_import/importer.py | Last updated: 2026-02-04*
