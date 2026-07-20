# API Reference: xlsxutils.py

**Language**: Python

**Source**: `utils/xlsxutils.py`

---

## Functions

### get_excel_date_format()

**Returns**: (none)



### make_xlsx(data: list[list[Any]], sheet_name: str, wb: openpyxl.Workbook | None = None, column_widths: list[int] | None = None, header_index: int = 0, has_filters: bool = False) → BytesIO

Create an Excel file with the given data and formatting options.

Args:
        data: List of rows, where each row is a list of cell values
        sheet_name: Name of the Excel sheet
        wb: Existing workbook to add sheet to. If None, creates new workbook
        column_widths: List of column widths in Excel units. If None, auto-sized
        header_index: Row index (0-based) that should be formatted as header making it bold
        has_filters: If True, applies bold formatting to the first column of filter rows

Returns:
        BytesIO: object containing the Excel file data

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | list[list[Any]] | - | - |
| sheet_name | str | - | - |
| wb | openpyxl.Workbook | None | None | - |
| column_widths | list[int] | None | None | - |
| header_index | int | 0 | - |
| has_filters | bool | False | - |

**Returns**: `BytesIO`



### handle_html(data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### read_xlsx_file_from_attached_file(file_url = None, fcontent = None, filepath = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_url | None | None | - |
| fcontent | None | None | - |
| filepath | None | None | - |

**Returns**: (none)



### read_xls_file_from_attached_file(content)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| content | None | - | - |

**Returns**: (none)



### build_xlsx_response(data, filename)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| filename | None | - | - |

**Returns**: (none)


