# API Reference: utils.py

**Language**: Python

**Source**: `utils.py`

---

## Functions

### validate_route_conflict(doctype, name)

Raises exception if name clashes with routes from other documents for /app routing

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |

**Returns**: (none)



### slug(name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### pop_csv_params(form_dict)

Pop csv params from form_dict and return them as a dict.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| form_dict | None | - | - |

**Returns**: (none)



### get_csv_bytes(data: list[list], csv_params: dict) → bytes

Convert data to csv bytes.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | list[list] | - | - |
| csv_params | dict | - | - |

**Returns**: `bytes`



### apply_csv_decimal_sep(data: list[list], decimal_sep: str) → list[list]

Apply decimal separator to csv data.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | list[list] | - | - |
| decimal_sep | str | - | - |

**Returns**: `list[list]`



### provide_binary_file(filename: str, extension: str, content: bytes) → None

Provide a binary file to the client.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filename | str | - | - |
| extension | str | - | - |
| content | bytes | - | - |

**Returns**: `None`



### send_report_email(user_email: str, report_name: str, file_extension: str, content: bytes, attached_to_name: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user_email | str | - | - |
| report_name | str | - | - |
| file_extension | str | - | - |
| content | bytes | - | - |
| attached_to_name | str | - | - |

**Returns**: (none)



### delete_old_exported_report_files()

**Returns**: (none)



### create_exported_report_folder_if_not_exists()

**Returns**: (none)


