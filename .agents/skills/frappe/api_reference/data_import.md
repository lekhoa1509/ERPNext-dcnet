# API Reference: data_import.py

**Language**: Python

**Source**: `core/doctype/data_import/data_import.py`

---

## Classes

### DataImport

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_delimiters_flag(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_doctype(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_import_file(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_google_sheets_url(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_payload_count(self, importer: Importer | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| importer | Importer | None | None | - |


##### get_preview_from_template(self, import_file = None, google_sheets_url = None)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| import_file | None | None | - |
| google_sheets_url | None | None | - |


##### start_import(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### export_errored_rows(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### download_import_log(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_importer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_preview_from_template(data_import: str, import_file: str | None = None, google_sheets_url: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data_import | str | - | - |
| import_file | str | None | None | - |
| google_sheets_url | str | None | None | - |

**Returns**: (none)



### form_start_import(data_import: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data_import | str | - | - |

**Returns**: (none)



### stop_data_import(doc_name: str)

Stop a running Data Import job.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc_name | str | - | - |

**Returns**: (none)



### start_import(data_import)

This method runs in background job

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data_import | None | - | - |

**Returns**: (none)



### download_template(doctype, export_fields = None, export_records = None, export_filters = None, file_type = 'CSV')

Download template from Exporter
        :param doctype: Document Type
        :param export_fields=None: Fields to export as dict {'Sales Invoice': ['name', 'customer'], 'Sales Invoice Item': ['item_code']}
        :param export_records=None: One of 'all', 'by_filter', 'blank_template'
        :param export_filters: Filter dict
        :param file_type: File type to export into

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| export_fields | None | None | - |
| export_records | None | None | - |
| export_filters | None | None | - |
| file_type | None | 'CSV' | - |

**Returns**: (none)



### download_errored_template(data_import_name: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data_import_name | str | - | - |

**Returns**: (none)



### download_import_log(data_import_name: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data_import_name | str | - | - |

**Returns**: (none)



### get_import_status(data_import_name: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data_import_name | str | - | - |

**Returns**: (none)



### get_import_logs(data_import: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data_import | str | - | - |

**Returns**: (none)



### import_file(doctype, file_path, import_type, submit_after_import = False, console = False)

Import documents in from CSV or XLSX using data import.

:param doctype: DocType to import
:param file_path: Path to .csv, .xls, or .xlsx file to import
:param import_type: One of "Insert" or "Update"
:param submit_after_import: Whether to submit documents after import
:param console: Set to true if this is to be used from command line. Will print errors or progress to stdout.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| file_path | None | - | - |
| import_type | None | - | - |
| submit_after_import | None | False | - |
| console | None | False | - |

**Returns**: (none)



### import_doc(path, pre_process = None, sort = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |
| pre_process | None | None | - |
| sort | None | False | - |

**Returns**: (none)



### export_json(doctype, path, filters = None, or_filters = None, name = None, order_by = 'creation asc')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| path | None | - | - |
| filters | None | None | - |
| or_filters | None | None | - |
| name | None | None | - |
| order_by | None | 'creation asc' | - |

**Returns**: (none)



### export_csv(doctype, path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| path | None | - | - |

**Returns**: (none)



### post_process(out)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| out | None | - | - |

**Returns**: (none)


