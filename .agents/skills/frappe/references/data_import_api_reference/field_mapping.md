# API Reference: Field Mapping Utilities

**Language**: Python

**Source**: `frappe/core/doctype/data_import/importer.py`

---

## Overview

Field mapping utilities handle the mapping of CSV/Excel column headers to DocType fields. This includes automatic detection, custom mapping, and handling of child table fields.

## Core Functions

### build_fields_dict_for_column_matching

Builds a dictionary for matching column headers to DocType fields.

```python
def build_fields_dict_for_column_matching(parent_doctype: str) -> dict:
    """
    Build a dict with various keys to match with column headers.

    Keys include:
    - Field label (e.g., "Customer Name")
    - Fieldname (e.g., "customer_name")
    - Child table field formats (e.g., "Item Code (Items)")

    Args:
        parent_doctype: Main DocType name

    Returns:
        dict: Mapping of header strings to DocField objects
    """
```

**Example:**

```python
from frappe.core.doctype.data_import.importer import build_fields_dict_for_column_matching

fields_dict = build_fields_dict_for_column_matching("Sales Order")

# Result:
{
    "Customer": df_customer,
    "customer": df_customer,
    "Transaction Date": df_transaction_date,
    "transaction_date": df_transaction_date,
    "Item Code (Items)": df_item_code,
    "Sales Order Item:item_code": df_item_code,
    # ... more mappings
}
```

### get_df_for_column_header

Gets the DocField for a specific column header.

```python
def get_df_for_column_header(doctype: str, header: str) -> DocField:
    """
    Get DocField matching a column header.

    Args:
        doctype: Target DocType
        header: Column header text

    Returns:
        DocField or None if not found
    """
```

**Example:**

```python
from frappe.core.doctype.data_import.importer import get_df_for_column_header

df = get_df_for_column_header("Customer", "Customer Name")
print(df.fieldname)  # customer_name
print(df.fieldtype)  # Data
```

### get_id_field

Gets the ID field (usually `name`) for a DocType.

```python
def get_id_field(doctype: str) -> DocField:
    """
    Get the ID/primary key field for a DocType.

    Args:
        doctype: DocType name

    Returns:
        DocField: The ID field definition
    """
```

### get_autoname_field

Gets the field used for autoname if applicable.

```python
def get_autoname_field(doctype: str) -> DocField:
    """
    Get the autoname field if DocType uses field-based naming.

    Example: Customer uses customer_name for naming

    Args:
        doctype: DocType name

    Returns:
        DocField or None
    """
```

## Column Header Formats

### Parent DocType Fields

```
Format: Field Label
Examples:
- "Customer Name" -> customer_name
- "Transaction Date" -> transaction_date
- "Grand Total" -> grand_total
```

### Child Table Fields

```
Format 1: Field Label (Child Table Label)
Examples:
- "Item Code (Items)" -> items.item_code
- "Qty (Items)" -> items.qty
- "Account Head (Taxes)" -> taxes.account_head

Format 2: Child DocType:fieldname
Examples:
- "Sales Order Item:item_code" -> items.item_code
- "Sales Taxes and Charges:rate" -> taxes.rate
```

### ID Fields

```
Format: ID or ID (Child Table Label)
Examples:
- "ID" -> name (parent)
- "ID (Items)" -> items.name (child)
```

## Custom Field Mapping

### Using column_to_field_map

```python
from frappe.core.doctype.data_import.importer import ImportFile

# Custom mapping for non-standard headers
custom_map = {
    "Cust ID": "customer",
    "Order Date": "transaction_date",
    "Product": "item_code",
    "Quantity": "qty",
    "Unit Price": "rate"
}

import_file = ImportFile(
    doctype="Sales Order",
    file="/path/to/orders.csv",
    template_options={"column_to_field_map": custom_map}
)
```

### Via Data Import DocType

```python
import frappe

data_import = frappe.new_doc("Data Import")
data_import.reference_doctype = "Customer"
data_import.import_file = "/files/customers.csv"
data_import.column_to_field_map = frappe.as_json({
    "Company Name": "customer_name",
    "Tax Number": "tax_id",
    "Address Line": "address_line1"
})
data_import.insert()
```

## Field Type Handling

### Link Field Mapping

```python
def map_link_field(header: str, df: DocField, value: str) -> str:
    """
    Map link field value.

    Handles:
    - Direct name match
    - Link by field value (e.g., customer_name instead of name)
    """
    if frappe.db.exists(df.options, value):
        return value

    # Try to find by other unique fields
    meta = frappe.get_meta(df.options)
    for unique_field in meta.get("fields", {"unique": 1}):
        match = frappe.db.get_value(
            df.options,
            {unique_field.fieldname: value},
            "name"
        )
        if match:
            return match

    return value  # Return as-is, will fail validation
```

### Select Field Mapping

```python
def map_select_field(value: str, df: DocField) -> str:
    """
    Map select field value.

    Handles:
    - Exact match
    - Case-insensitive match
    - Partial match
    """
    options = df.options.split("\n") if df.options else []

    # Exact match
    if value in options:
        return value

    # Case-insensitive match
    value_lower = value.lower()
    for opt in options:
        if opt.lower() == value_lower:
            return opt

    return value  # Return as-is, will fail validation
```

## Building Custom Field Maps

### Analyze File Headers

```python
def analyze_headers(doctype: str, headers: list) -> dict:
    """
    Analyze file headers and suggest field mappings.
    """
    fields_dict = build_fields_dict_for_column_matching(doctype)

    result = {
        "mapped": {},
        "unmapped": [],
        "suggestions": {}
    }

    for header in headers:
        if header in fields_dict:
            result["mapped"][header] = fields_dict[header].fieldname
        else:
            result["unmapped"].append(header)

            # Try fuzzy matching
            suggestions = find_similar_fields(header, fields_dict.keys())
            if suggestions:
                result["suggestions"][header] = suggestions

    return result

def find_similar_fields(header: str, field_labels: list) -> list:
    """Find similar field labels using fuzzy matching."""
    from difflib import get_close_matches
    return get_close_matches(header, field_labels, n=3, cutoff=0.6)
```

### Generate Field Mapping UI

```python
def get_field_mapping_options(doctype: str) -> list:
    """
    Get field options for mapping UI.
    """
    meta = frappe.get_meta(doctype)
    options = []

    # Parent fields
    for df in meta.fields:
        if is_importable_field(df):
            options.append({
                "label": df.label or df.fieldname,
                "value": df.fieldname,
                "fieldtype": df.fieldtype,
                "doctype": doctype
            })

    # Child table fields
    for table_df in meta.get_table_fields():
        child_meta = frappe.get_meta(table_df.options)
        for df in child_meta.fields:
            if is_importable_field(df):
                options.append({
                    "label": f"{df.label or df.fieldname} ({table_df.label})",
                    "value": f"{table_df.fieldname}.{df.fieldname}",
                    "fieldtype": df.fieldtype,
                    "doctype": table_df.options
                })

    return options
```

## Usage Examples

### Auto-Map Headers

```python
from frappe.core.doctype.data_import.importer import ImportFile

def auto_map_file(doctype, file_path):
    """
    Auto-map file headers and return mapping report.
    """
    import_file = ImportFile(doctype, file_path)
    raw_data = import_file.get_data_from_template_file()

    if not raw_data:
        return {"error": "Empty file"}

    headers = raw_data[0]
    analysis = analyze_headers(doctype, headers)

    return {
        "total_columns": len(headers),
        "mapped": len(analysis["mapped"]),
        "unmapped": len(analysis["unmapped"]),
        "mapping": analysis["mapped"],
        "suggestions": analysis["suggestions"]
    }
```

### Apply Custom Mapping

```python
def import_with_mapping(doctype, file_path, column_map):
    """
    Import file with custom column mapping.
    """
    import_file = ImportFile(
        doctype=doctype,
        file=file_path,
        template_options={"column_to_field_map": column_map}
    )

    import_file.parse_data_from_template()

    # Verify mapping
    for col in import_file.columns:
        if col.df:
            print(f"'{col.header}' -> {col.df.fieldname}")
        else:
            print(f"'{col.header}' -> UNMAPPED")

    return import_file
```

### Validate Mapping

```python
def validate_field_mapping(doctype: str, mapping: dict) -> dict:
    """
    Validate custom field mapping.
    """
    errors = []
    warnings = []

    meta = frappe.get_meta(doctype)
    all_fields = {df.fieldname for df in meta.fields}

    # Add child table fields
    for table_df in meta.get_table_fields():
        child_meta = frappe.get_meta(table_df.options)
        for df in child_meta.fields:
            all_fields.add(f"{table_df.fieldname}.{df.fieldname}")

    for header, fieldname in mapping.items():
        if fieldname not in all_fields:
            errors.append(f"Unknown field '{fieldname}' for header '{header}'")

    # Check required fields are mapped
    required_fields = [df.fieldname for df in meta.fields if df.reqd]
    mapped_fields = set(mapping.values())

    for field in required_fields:
        if field not in mapped_fields:
            warnings.append(f"Required field '{field}' not in mapping")

    return {"errors": errors, "warnings": warnings, "valid": len(errors) == 0}
```

## Related Functions

- [Header](header.md) - Header parsing class
- [Column](column.md) - Column parsing class
- [ImportFile](import_file.md) - File processing

---

*Source: frappe/core/doctype/data_import/importer.py | Last updated: 2026-02-04*
