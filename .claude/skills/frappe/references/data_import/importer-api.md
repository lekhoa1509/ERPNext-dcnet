# Importer API Reference

> Source: `frappe/core/doctype/data_import/importer.py`

## Importer Class

Main class for importing data from CSV/Excel files.

### Constructor

```python
Importer(
    doctype,           # DocType to import
    data_import=None,  # Data Import document (optional)
    file_path=None,    # Path to import file
    import_type=None,  # "Insert New Records" or "Update Existing Records"
    console=False,     # Print progress to console
    use_sniffer=False  # Use CSV sniffer for delimiter detection
)
```

### Methods

#### `get_data_for_import_preview()`

Returns preview data for the import file.

```python
preview = importer.get_data_for_import_preview()
# Returns:
# {
#     "data": [[row_num, val1, val2, ...], ...],
#     "columns": [{"header_title": "...", "df": {...}, ...}, ...],
#     "warnings": [{"row": 1, "message": "...", "type": "warning"}, ...],
#     "import_log": [...],
#     "max_rows_exceeded": False,
#     "max_rows_in_preview": 10,
#     "total_number_of_rows": 100
# }
```

#### `import_data()`

Executes the import process.

```python
import_log = importer.import_data()
# Returns list of import log entries
```

#### `export_errored_rows()`

Exports failed rows as CSV for re-import.

```python
importer.export_errored_rows()  # Triggers CSV download
```

#### `export_import_log()`

Exports full import log as CSV.

```python
importer.export_import_log()  # Triggers CSV download
```

---

## ImportFile Class

Handles parsing of import files (CSV, Excel, Google Sheets).

### Constructor

```python
ImportFile(
    doctype,              # DocType being imported
    file,                 # File path, URL, or Google Sheets URL
    template_options=None, # Column mapping options
    import_type=None,     # Import type
    console=False,        # Console mode
    use_sniffer=False     # CSV sniffer
)
```

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `raw_data` | list | Raw rows from file |
| `header` | Header | Parsed header row |
| `columns` | list[Column] | Column definitions |
| `data` | list[Row] | Parsed data rows |
| `warnings` | list | Parsing warnings |

### Methods

#### `get_data_for_import_preview()`

Returns preview with columns and data.

#### `get_payloads_for_import()`

Returns list of document payloads ready for import.

```python
payloads = import_file.get_payloads_for_import()
# Each payload: {"doc": {...}, "rows": [Row, ...]}
```

#### `get_warnings()`

Returns all warnings from file, columns, and rows.

---

## Row Class

Represents a single data row.

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `index` | int | 0-based row index |
| `row_number` | int | 1-based row number |
| `data` | list | Raw row values |
| `warnings` | list | Row-level warnings |

### Methods

#### `parse_doc(doctype, parent_doc=None, table_df=None)`

Parses row into document dict.

```python
doc = row.parse_doc("Customer")
# Returns: {"customer_name": "...", "territory": "...", ...}
```

#### `get_values(indexes)`

Gets values at specific column indexes.

#### `as_list()`

Returns raw row data as list.

---

## Column Class

Represents a column in the import file.

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `index` | int | 0-based column index |
| `column_number` | int | 1-based column number |
| `header_title` | str | Column header text |
| `df` | DocField | Matched DocField |
| `skip_import` | bool | Whether to skip this column |
| `date_format` | str | Detected date format |
| `warnings` | list | Column-level warnings |

### Methods

#### `as_dict()`

Returns column metadata as dict.

---

## Header Class

Represents the header row with column definitions.

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `columns` | list[Column] | All columns |
| `doctypes` | list | Involved doctypes (parent + child tables) |

### Methods

#### `get_column_indexes(doctype, tablefield=None)`

Gets column indexes for a specific doctype.

#### `get_columns(indexes)`

Gets Column objects at specific indexes.

---

## Utility Functions

### `get_id_field(doctype)`

Returns the ID field for a doctype.

```python
id_field = get_id_field("Customer")
# Returns: {"label": "ID", "fieldname": "name", "fieldtype": "Data"}
```

### `get_autoname_field(doctype)`

Returns the autoname field if doctype uses `field:` autoname.

```python
autoname_field = get_autoname_field("Customer")
# Returns DocField or None
```

### `build_fields_dict_for_column_matching(parent_doctype)`

Builds mapping of possible headers to DocFields.

```python
mapping = build_fields_dict_for_column_matching("Sales Order")
# Returns: {
#     "Customer": df,
#     "customer": df,
#     "Item Code (Items)": df,
#     "items.item_code": df,
#     ...
# }
```

### `create_import_log(data_import, log_index, log_details)`

Creates a Data Import Log entry.

```python
create_import_log(
    data_import="Customer Import on 2026-02-04",
    log_index=0,
    log_details={
        "success": True,
        "docname": "CUST-001",
        "row_indexes": [2]
    }
)
```

---

## Constants

```python
INVALID_VALUES = ("", None)
MAX_ROWS_IN_PREVIEW = 10
INSERT = "Insert New Records"
UPDATE = "Update Existing Records"
```

---

## Import Process Flow

```
1. ImportFile.__init__()
   ├── get_data_from_template_file()  # Read CSV/Excel/Google Sheets
   └── parse_data_from_template()     # Parse header + rows

2. Importer.import_data()
   ├── before_import()                # Set flags, clear warnings
   ├── get_payloads_for_import()      # Build document payloads
   ├── For each payload:
   │   ├── process_doc()              # Insert or Update
   │   │   ├── insert_record()        # Create new doc
   │   │   └── update_record()        # Update existing doc
   │   └── create_import_log()        # Log result
   └── after_import()                 # Reset flags
```

---

## Error Handling

### ValidationError

Thrown when:
- DocType doesn't allow import
- User lacks import permission
- File format not supported

### ImportWarning

Added to warnings list when:
- Column can't be matched
- Link value doesn't exist
- Select value invalid
- Date format mismatch

### ImportError

Logged when:
- Required field missing
- Validation fails
- Database error
