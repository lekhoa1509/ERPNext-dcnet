# API Reference: bank_statement_import.py

**Language**: Python

**Source**: `doctype/bank_statement_import/bank_statement_import.py`

---

## Classes

### BankStatementImport

**Inherits from**: DataImport

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### start_import(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### preprocess_mt940_content(content: str) → str

Preprocess MT940 content to fix statement number format issues.

The MT940 standard expects statement numbers to be maximum 5 digits,
but some banks provide longer statement numbers that cause parsing errors.
This function truncates statement numbers longer than 5 digits to the last 5 digits.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| content | str | - | - |

**Returns**: `str`



### convert_mt940_to_csv(data_import, mt940_file_path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data_import | None | - | - |
| mt940_file_path | None | - | - |

**Returns**: (none)



### get_preview_from_template(data_import, import_file = None, google_sheets_url = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data_import | None | - | - |
| import_file | None | None | - |
| google_sheets_url | None | None | - |

**Returns**: (none)



### form_start_import(data_import)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data_import | None | - | - |

**Returns**: (none)



### download_errored_template(data_import_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data_import_name | None | - | - |

**Returns**: (none)



### download_import_log(data_import_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data_import_name | None | - | - |

**Returns**: (none)



### is_mt940_format(content: str) → bool

Check if the content has key MT940 tags

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| content | str | - | - |

**Returns**: `bool`



### parse_data_from_template(raw_data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| raw_data | None | - | - |

**Returns**: (none)



### start_import(data_import, bank_account, import_file_path, google_sheets_url, bank, template_options)

This method runs in background job

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data_import | None | - | - |
| bank_account | None | - | - |
| import_file_path | None | - | - |
| google_sheets_url | None | - | - |
| bank | None | - | - |
| template_options | None | - | - |

**Returns**: (none)



### update_mapping_db(bank, template_options)

Update bank transaction mapping database with template options.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bank | None | - | - |
| template_options | None | - | - |

**Returns**: (none)



### add_bank_account(data, bank_account)

Add bank account information to data rows.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| bank_account | None | - | - |

**Returns**: (none)



### write_files(import_file, data)

Write processed data to CSV or Excel files.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| import_file | None | - | - |
| data | None | - | - |

**Returns**: (none)



### write_xlsx(data, sheet_name, wb = None, column_widths = None, file_path = None)

Write data to Excel file with formatting.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| sheet_name | None | - | - |
| wb | None | None | - |
| column_widths | None | None | - |
| file_path | None | None | - |

**Returns**: (none)



### get_import_status(docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | None | - | - |

**Returns**: (none)



### get_import_logs(docname: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | str | - | - |

**Returns**: (none)



### upload_bank_statement()

**Returns**: (none)



### replace_statement_number(match)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| match | None | - | - |

**Returns**: (none)


