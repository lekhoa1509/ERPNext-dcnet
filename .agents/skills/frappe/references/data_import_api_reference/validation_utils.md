# API Reference: Validation Utilities

**Language**: Python

**Source**: `frappe/core/doctype/data_import/importer.py`

---

## Overview

Validation utilities provide functions for validating import data before processing. These include field validation, link checking, date parsing, and option verification.

## Field Validation Functions

### validate_value

Validates a single cell value against field constraints.

```python
def validate_value(self, value: Any, col: Column) -> None:
    """
    Validates value and adds warnings/errors to row.

    Checks:
    - Required field has value
    - Link field exists
    - Select options are valid
    - Data type is compatible
    """
```

**Example:**

```python
# In Row class context
row.validate_value("ACME Corp", customer_column)
row.validate_value("Invalid Option", status_column)

# Check warnings after validation
for warning in row.warnings:
    print(f"Warning: {warning['message']}")
```

### link_exists

Checks if a Link field value exists in the database.

```python
def link_exists(self, value: str, df: DocField) -> bool:
    """
    Args:
        value: The link value to check
        df: DocField definition

    Returns:
        bool: True if document exists, False otherwise
    """
```

**Example:**

```python
# Check if customer exists
exists = row.link_exists("CUST-001", customer_field)
if not exists:
    row.warnings.append({
        "row": row.index,
        "col": col.index,
        "message": f"Customer 'CUST-001' does not exist"
    })
```

### get_select_options

Gets valid options for a Select field.

```python
def get_select_options(df: DocField) -> list:
    """
    Args:
        df: DocField with options

    Returns:
        list: Valid option values
    """
```

**Example:**

```python
from frappe.core.doctype.data_import.importer import get_select_options

status_field = frappe.get_meta("Lead").get_field("status")
valid_options = get_select_options(status_field)
print(valid_options)  # ['Lead', 'Open', 'Replied', 'Converted', ...]

# Validate value
if value not in valid_options:
    print(f"Invalid option: {value}")
```

## Date Validation

### guess_date_format

Detects date format from a single value.

```python
def guess_date_format(d: str) -> str:
    """
    Args:
        d: Date string

    Returns:
        str: Format string or None if not detected
    """
```

**Example:**

```python
from frappe.core.doctype.data_import.importer import guess_date_format

format1 = guess_date_format("2024-01-15")  # %Y-%m-%d
format2 = guess_date_format("15/01/2024")  # %d/%m/%Y
format3 = guess_date_format("01-15-2024")  # %m-%d-%Y
```

### get_user_format

Converts internal format to user-friendly description.

```python
def get_user_format(date_format: str) -> str:
    """
    Args:
        date_format: Format string like '%Y-%m-%d'

    Returns:
        str: User-friendly format like 'YYYY-MM-DD'
    """
```

**Example:**

```python
from frappe.core.doctype.data_import.importer import get_user_format

user_format = get_user_format("%d/%m/%Y")
print(user_format)  # "DD/MM/YYYY"
```

## Type Validation

### Numeric Validation

```python
def parse_numeric(value: str, fieldtype: str) -> Union[int, float]:
    """
    Parse and validate numeric values.

    Fieldtypes: Int, Float, Currency, Percent
    """
    if fieldtype == "Int":
        return int(value)
    else:
        return float(value)
```

### Check Field Validation

```python
def parse_check(value: str) -> int:
    """
    Parse checkbox values.

    Accepted values:
    - 1, "1", "Yes", "yes", "True", "true" -> 1
    - 0, "0", "No", "no", "False", "false", "" -> 0
    """
```

### Duration Validation

```python
def parse_duration(value: str) -> int:
    """
    Parse duration strings to seconds.

    Formats:
    - "3h" -> 10800
    - "2d 4h 30m" -> 189000
    - "1d" -> 86400
    """
```

## Custom Validators

### Pre-Import Validation Hook

```python
import frappe

def validate_import_data(doctype, data):
    """
    Custom validation before import.

    Hook in your app:
    doc_events = {
        "*": {
            "validate_import": "your_app.validators.validate_import_data"
        }
    }
    """
    errors = []

    for i, row in enumerate(data):
        # Custom validation logic
        if doctype == "Customer":
            if not row.get("customer_name"):
                errors.append(f"Row {i+1}: Customer Name is required")

            if row.get("tax_id") and len(row.get("tax_id")) != 10:
                errors.append(f"Row {i+1}: Tax ID must be 10 digits")

    return errors
```

### Row-Level Validator

```python
def validate_customer_row(row_data, row_index):
    """
    Validate a single customer row before import.
    """
    errors = []
    warnings = []

    # Check required fields
    if not row_data.get("customer_name"):
        errors.append({
            "row": row_index,
            "field": "customer_name",
            "message": "Customer Name is required"
        })

    # Check email format
    email = row_data.get("email_id")
    if email and "@" not in email:
        errors.append({
            "row": row_index,
            "field": "email_id",
            "message": "Invalid email format"
        })

    # Check for duplicates
    if row_data.get("customer_name"):
        if frappe.db.exists("Customer", {"customer_name": row_data["customer_name"]}):
            warnings.append({
                "row": row_index,
                "field": "customer_name",
                "message": "Customer with this name already exists"
            })

    return {"errors": errors, "warnings": warnings}
```

## Bulk Validation

### Validate Before Import

```python
from frappe.core.doctype.data_import.importer import Importer

def validate_import_file(doctype, file_path):
    """
    Validate entire file before starting import.
    """
    importer = Importer(doctype, file_path=file_path)
    preview = importer.get_data_for_import_preview()

    validation_result = {
        "valid": True,
        "errors": [],
        "warnings": preview.warnings
    }

    # Check for unmapped columns
    for col in preview.columns:
        if not col.get("df"):
            validation_result["warnings"].append({
                "type": "unmapped_column",
                "column": col.get("header"),
                "message": f"Column '{col.get('header')}' not mapped to any field"
            })

    # Check for missing required fields
    meta = frappe.get_meta(doctype)
    required_fields = [df.fieldname for df in meta.fields if df.reqd]
    mapped_fields = [col.get("fieldname") for col in preview.columns if col.get("df")]

    for field in required_fields:
        if field not in mapped_fields and field not in ["name", "doctype"]:
            validation_result["errors"].append({
                "type": "missing_required",
                "field": field,
                "message": f"Required field '{field}' not found in import file"
            })
            validation_result["valid"] = False

    return validation_result
```

### Link Validation

```python
def validate_all_links(doctype, data, link_fields):
    """
    Validate all link field values exist.
    """
    errors = []
    cache = {}  # Cache link existence checks

    for row_idx, row in enumerate(data):
        for field in link_fields:
            value = row.get(field.fieldname)
            if not value:
                continue

            cache_key = f"{field.options}:{value}"
            if cache_key not in cache:
                cache[cache_key] = frappe.db.exists(field.options, value)

            if not cache[cache_key]:
                errors.append({
                    "row": row_idx,
                    "field": field.fieldname,
                    "value": value,
                    "message": f"{field.options} '{value}' does not exist"
                })

    return errors
```

## Error Message Formatting

### Standard Error Format

```python
{
    "row": 5,           # Row number (1-indexed for display)
    "col": 2,           # Column number (0-indexed)
    "field": "status",  # Field name
    "message": "Invalid value 'Bad' for Status. Valid options: Open, Converted, Lost"
}
```

### Grouped Warnings

```python
def group_warnings(warnings):
    """
    Group similar warnings together.
    """
    grouped = {}

    for w in warnings:
        key = w.get("message", "")
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(w.get("row"))

    return [
        {"message": msg, "rows": rows}
        for msg, rows in grouped.items()
    ]

# Usage
warnings = group_warnings(importer.warnings)
for w in warnings:
    print(f"{w['message']} (rows: {w['rows']})")
```

## Usage Example

### Complete Validation Flow

```python
import frappe
from frappe.core.doctype.data_import.importer import Importer

def validate_and_import(doctype, file_path):
    """
    Complete validation flow before import.
    """
    # Step 1: Create importer
    importer = Importer(doctype, file_path=file_path)

    # Step 2: Get preview with validation
    preview = importer.get_data_for_import_preview()

    # Step 3: Check for errors
    if preview.warnings:
        print("Validation Warnings:")
        for w in preview.warnings:
            print(f"  Row {w.get('row')}: {w.get('message')}")

    # Step 4: Ask user to confirm
    has_errors = any(w.get("type") == "error" for w in preview.warnings)
    if has_errors:
        raise frappe.ValidationError("Import file has validation errors")

    # Step 5: Proceed with import
    import_log = importer.import_data()

    return import_log
```

## Related Functions

- [Row.validate_value](row.md#validate_value) - Cell validation
- [Column.validate_values](column.md#validate_values) - Column validation
- [Importer.before_import](importer.md#before_import) - Pre-import hook

---

*Source: frappe/core/doctype/data_import/importer.py | Last updated: 2026-02-04*
