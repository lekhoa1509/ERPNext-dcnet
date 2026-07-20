# API Reference: CSV/Excel Parsers

**Language**: Python

**Source**: `frappe/core/doctype/data_import/importer.py`

---

## Overview

The Data Import module supports parsing CSV and Excel files. The parsers handle encoding detection, delimiter sniffing, and conversion to a common internal format.

## File Reading

### read_file Method

```python
def read_file(self, file_path: str) -> tuple:
    """
    Read file content from path or URL.

    Args:
        file_path: Local path or URL (including Google Sheets)

    Returns:
        tuple: (content_bytes, file_extension)
    """
```

**Supported Sources:**
- Local file path
- Frappe File URL (`/files/...`)
- Google Sheets URL (auto-converted to CSV export URL)
- Direct HTTP URL

### read_content Method

```python
def read_content(self, content: bytes, extension: str) -> list:
    """
    Parse file content based on extension.

    Args:
        content: Raw file bytes
        extension: File extension (.csv, .xlsx, .xls)

    Returns:
        list: 2D list of cell values
    """
```

## CSV Parser

### Basic CSV Parsing

```python
import csv
from io import StringIO

def parse_csv(content: bytes) -> list:
    """
    Parse CSV content to 2D list.

    Handles:
    - UTF-8 and other encodings
    - Different delimiters (comma, semicolon, tab)
    - Quoted fields with newlines
    """
    # Detect encoding
    decoded = content.decode("utf-8-sig")  # Handle BOM

    # Use csv.Sniffer for delimiter detection
    sniffer = csv.Sniffer()
    try:
        dialect = sniffer.sniff(decoded[:8192])
    except csv.Error:
        dialect = csv.excel

    reader = csv.reader(StringIO(decoded), dialect)
    return list(reader)
```

### Delimiter Detection

```python
def detect_delimiter(content: str) -> str:
    """
    Detect CSV delimiter using sniffer.

    Common delimiters:
    - Comma (,) - Standard CSV
    - Semicolon (;) - European CSV
    - Tab (\t) - TSV
    """
    import csv

    try:
        dialect = csv.Sniffer().sniff(content[:8192], delimiters=',;\t|')
        return dialect.delimiter
    except csv.Error:
        return ','  # Default to comma
```

### Encoding Detection

```python
def detect_encoding(content: bytes) -> str:
    """
    Detect file encoding.

    Priority:
    1. UTF-8 with BOM
    2. UTF-8 without BOM
    3. Latin-1 (fallback)
    """
    import codecs

    # Check for BOM
    if content.startswith(codecs.BOM_UTF8):
        return "utf-8-sig"
    if content.startswith(codecs.BOM_UTF16_LE):
        return "utf-16-le"
    if content.startswith(codecs.BOM_UTF16_BE):
        return "utf-16-be"

    # Try UTF-8
    try:
        content.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        pass

    # Fallback to latin-1
    return "latin-1"
```

## Excel Parser

### XLSX Parsing (openpyxl)

```python
def parse_xlsx(content: bytes) -> list:
    """
    Parse Excel .xlsx files using openpyxl.
    """
    from io import BytesIO
    from openpyxl import load_workbook

    wb = load_workbook(BytesIO(content), read_only=True, data_only=True)
    ws = wb.active

    data = []
    for row in ws.iter_rows(values_only=True):
        # Convert None to empty string
        data.append([cell if cell is not None else "" for cell in row])

    return data
```

### XLS Parsing (xlrd)

```python
def parse_xls(content: bytes) -> list:
    """
    Parse Excel .xls files using xlrd.
    """
    from io import BytesIO
    import xlrd

    wb = xlrd.open_workbook(file_contents=content)
    ws = wb.sheet_by_index(0)

    data = []
    for row_idx in range(ws.nrows):
        row = []
        for col_idx in range(ws.ncols):
            cell = ws.cell(row_idx, col_idx)
            value = cell.value

            # Handle dates
            if cell.ctype == xlrd.XL_CELL_DATE:
                value = xlrd.xldate_as_datetime(value, wb.datemode)

            row.append(value if value is not None else "")
        data.append(row)

    return data
```

### Excel Date Handling

```python
def convert_excel_date(value, datemode=0):
    """
    Convert Excel serial date to Python datetime.

    Excel stores dates as days since 1899-12-30 (or 1904-01-01 on Mac).
    """
    import xlrd
    from datetime import datetime

    if isinstance(value, (int, float)):
        return xlrd.xldate_as_datetime(value, datemode)
    return value
```

## Google Sheets Integration

### Parse Google Sheets URL

```python
def get_google_sheets_csv_url(url: str) -> str:
    """
    Convert Google Sheets URL to CSV export URL.

    Input formats:
    - https://docs.google.com/spreadsheets/d/{id}/edit
    - https://docs.google.com/spreadsheets/d/{id}/edit#gid={sheet_id}

    Output:
    - https://docs.google.com/spreadsheets/d/{id}/export?format=csv&gid={sheet_id}
    """
    import re

    # Extract spreadsheet ID
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
    if not match:
        raise ValueError("Invalid Google Sheets URL")

    spreadsheet_id = match.group(1)

    # Extract sheet ID (gid)
    gid_match = re.search(r"gid=(\d+)", url)
    gid = gid_match.group(1) if gid_match else "0"

    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}"
```

### Fetch Google Sheets

```python
import requests

def fetch_google_sheets(url: str) -> bytes:
    """
    Fetch CSV content from Google Sheets.

    Note: Sheet must be publicly accessible or shared with
    the service account.
    """
    csv_url = get_google_sheets_csv_url(url)

    response = requests.get(csv_url, timeout=30)
    response.raise_for_status()

    return response.content
```

## Custom Parsers

### TSV Parser

```python
def parse_tsv(content: bytes) -> list:
    """Parse tab-separated values."""
    import csv
    from io import StringIO

    decoded = content.decode("utf-8-sig")
    reader = csv.reader(StringIO(decoded), delimiter="\t")
    return list(reader)
```

### Fixed-Width Parser

```python
def parse_fixed_width(content: bytes, widths: list) -> list:
    """
    Parse fixed-width format file.

    Args:
        content: File content
        widths: List of column widths [10, 20, 15, ...]
    """
    decoded = content.decode("utf-8")
    lines = decoded.strip().split("\n")

    data = []
    for line in lines:
        row = []
        pos = 0
        for width in widths:
            value = line[pos:pos + width].strip()
            row.append(value)
            pos += width
        data.append(row)

    return data
```

### JSON Lines Parser

```python
import json

def parse_jsonl(content: bytes) -> list:
    """
    Parse JSON Lines format (one JSON object per line).
    """
    decoded = content.decode("utf-8")
    lines = decoded.strip().split("\n")

    # Get all keys for header
    all_keys = set()
    objects = []
    for line in lines:
        obj = json.loads(line)
        objects.append(obj)
        all_keys.update(obj.keys())

    # Build 2D list
    headers = list(sorted(all_keys))
    data = [headers]

    for obj in objects:
        row = [obj.get(key, "") for key in headers]
        data.append(row)

    return data
```

## Usage Examples

### Basic File Parsing

```python
from frappe.core.doctype.data_import.importer import ImportFile

# CSV file
import_file = ImportFile("Customer", "/path/to/customers.csv")
raw_data = import_file.get_data_from_template_file()
print(f"Parsed {len(raw_data)} rows")

# Excel file
import_file = ImportFile("Item", "/path/to/items.xlsx")
raw_data = import_file.get_data_from_template_file()
```

### Handle Different Encodings

```python
def safe_parse_csv(file_path):
    """Parse CSV with encoding detection."""
    with open(file_path, "rb") as f:
        content = f.read()

    # Try different encodings
    for encoding in ["utf-8-sig", "utf-8", "latin-1", "cp1252"]:
        try:
            decoded = content.decode(encoding)
            reader = csv.reader(StringIO(decoded))
            return list(reader)
        except UnicodeDecodeError:
            continue

    raise ValueError("Could not detect file encoding")
```

### Validate CSV Structure

```python
def validate_csv_structure(content: bytes) -> dict:
    """
    Validate CSV file structure before import.
    """
    import csv
    from io import StringIO

    decoded = content.decode("utf-8-sig")
    reader = csv.reader(StringIO(decoded))
    rows = list(reader)

    if not rows:
        return {"valid": False, "error": "File is empty"}

    header = rows[0]
    if not header or all(not cell for cell in header):
        return {"valid": False, "error": "Header row is empty"}

    # Check for consistent column count
    expected_cols = len(header)
    inconsistent_rows = []
    for i, row in enumerate(rows[1:], start=2):
        if len(row) != expected_cols:
            inconsistent_rows.append(i)

    if inconsistent_rows:
        return {
            "valid": False,
            "error": f"Inconsistent column count in rows: {inconsistent_rows[:5]}"
        }

    return {
        "valid": True,
        "rows": len(rows) - 1,
        "columns": expected_cols,
        "headers": header
    }
```

## Configuration

### Parser Settings

```python
# In Data Import DocType
PARSER_SETTINGS = {
    "csv": {
        "encoding": "utf-8-sig",
        "delimiter": ",",
        "quotechar": '"',
        "skip_initial_space": True
    },
    "xlsx": {
        "read_only": True,
        "data_only": True,  # Evaluate formulas
        "sheet_index": 0    # First sheet
    }
}
```

### Custom Delimiter Setting

```python
import frappe

# When creating Data Import
data_import = frappe.new_doc("Data Import")
data_import.reference_doctype = "Customer"
data_import.import_file = "/files/customers.csv"
data_import.do_not_use_sniffer = True  # Skip delimiter detection
# Custom delimiter handled via template_options
```

## Related References

- [ImportFile](import_file.md) - File handling class
- [Importer](importer.md) - Main import class
- [Template Generator](template_generator.md) - Template creation

---

*Source: frappe/core/doctype/data_import/importer.py | Last updated: 2026-02-04*
