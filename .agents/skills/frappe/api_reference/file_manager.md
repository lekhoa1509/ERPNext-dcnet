# API Reference: file_manager.py

**Language**: Python

**Source**: `utils/file_manager.py`

---

## Classes

### MaxFileSizeReachedError

**Inherits from**: frappe.ValidationError



## Functions

### safe_b64decode(binary: bytes) → bytes

Adds padding if doesn't already exist before decoding.

This attempts to avoid the `binascii.Error: Incorrect padding` error raised
when the number of trailing = is simply not enough :crie:. Although, it may
be an indication of corrupted data.

Refs:
        * https://en.wikipedia.org/wiki/Base64
        * https://stackoverflow.com/questions/2941995/python-ignore-incorrect-padding-error-when-base64-decoding

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| binary | bytes | - | - |

**Returns**: `bytes`



### get_file_url(file_data_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_data_name | None | - | - |

**Returns**: (none)



### upload()

**Returns**: (none)



### get_file_doc(dt = None, dn = None, folder = None, is_private = None, df = None)

Return File object (Document) from given parameters or `form_dict`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | None | - |
| dn | None | None | - |
| folder | None | None | - |
| is_private | None | None | - |
| df | None | None | - |

**Returns**: (none)



### save_uploaded(dt, dn, folder, is_private, df = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |
| dn | None | - | - |
| folder | None | - | - |
| is_private | None | - | - |
| df | None | None | - |

**Returns**: (none)



### save_url(file_url, filename, dt, dn, folder, is_private, df = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_url | None | - | - |
| filename | None | - | - |
| dt | None | - | - |
| dn | None | - | - |
| folder | None | - | - |
| is_private | None | - | - |
| df | None | None | - |

**Returns**: (none)



### get_uploaded_content()

**Returns**: (none)



### save_file(fname, content, dt, dn, folder = None, decode = False, is_private = 0, df = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fname | None | - | - |
| content | None | - | - |
| dt | None | - | - |
| dn | None | - | - |
| folder | None | None | - |
| decode | None | False | - |
| is_private | None | 0 | - |
| df | None | None | - |

**Returns**: (none)



### get_file_data_from_hash(content_hash, is_private = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| content_hash | None | - | - |
| is_private | None | 0 | - |

**Returns**: (none)



### save_file_on_filesystem(fname, content, content_type = None, is_private = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fname | None | - | - |
| content | None | - | - |
| content_type | None | None | - |
| is_private | None | 0 | - |

**Returns**: (none)



### get_max_file_size()

**Returns**: (none)



### check_max_file_size(content)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| content | None | - | - |

**Returns**: (none)



### write_file(content, fname, is_private = 0)

write file to disk with a random name (to compare)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| content | None | - | - |
| fname | None | - | - |
| is_private | None | 0 | - |

**Returns**: (none)



### remove_all(dt, dn, from_delete = False, delete_permanently = False)

remove all files in a transaction

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |
| dn | None | - | - |
| from_delete | None | False | - |
| delete_permanently | None | False | - |

**Returns**: (none)



### remove_file(fid = None, attached_to_doctype = None, attached_to_name = None, from_delete = False, delete_permanently = False)

Remove file and File entry

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fid | None | None | - |
| attached_to_doctype | None | None | - |
| attached_to_name | None | None | - |
| from_delete | None | False | - |
| delete_permanently | None | False | - |

**Returns**: (none)



### delete_file_data_content(doc, only_thumbnail = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| only_thumbnail | None | False | - |

**Returns**: (none)



### delete_file_from_filesystem(doc, only_thumbnail = False)

Delete file, thumbnail from File document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| only_thumbnail | None | False | - |

**Returns**: (none)



### delete_file(path)

Delete file from `public folder`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)



### get_file(fname)

Return [`file_name`, `content`] for given file name `fname`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fname | None | - | - |

**Returns**: (none)



### get_file_path(file_name)

Return file path from given file name.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_name | None | - | - |

**Returns**: (none)



### get_content_hash(content)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| content | None | - | - |

**Returns**: (none)



### get_file_name(fname, optional_suffix)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fname | None | - | - |
| optional_suffix | None | - | - |

**Returns**: (none)



### add_attachments(doctype, name, attachments)

Add attachments to the given DocType

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| attachments | None | - | - |

**Returns**: (none)



### is_safe_path(path: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | str | - | - |

**Returns**: `bool`


