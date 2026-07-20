# API Reference: file.py

**Language**: Python

**Source**: `core/doctype/file/file.py`

---

## Classes

### File

**Inherits from**: Document

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_remote_file(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### autoname(self)

Set name for folder

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_attachment_references(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### enforce_public_file_restrictions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_rename(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_rollback(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_name_based_on_parent_folder(self) → str | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str | None`


##### get_successors(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_file_path(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_file_url(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### handle_is_private_changed(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### fetch_attached_to_field(self, old_file_url)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old_file_url | None | - | - |


##### validate_attachment_limit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_remote_file(self)

Validates if file uploaded using URL already exist

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_folder_name(self)

Make parent folders if not exists based on reference doctype and name

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_file_type(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_file_on_disk(self)

Validates existence file

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_file_extension(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_content(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_duplicate_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_file_name(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### generate_content_hash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_thumbnail(self, set_as_thumbnail: bool = True, width: int = 300, height: int = 300, suffix: str = 'small', crop: bool = False) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| set_as_thumbnail | bool | True | - |
| width | int | 300 | - |
| height | int | 300 | - |
| suffix | str | 'small' | - |
| crop | bool | False | - |

**Returns**: `str`


##### validate_empty_folder(self)

Throw exception if folder is not empty

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_protected_file(self)

Throw an exception if this file is attached to a doctype that protects files.

Allows deleting the attached file if the linked document is in draft. If submitted,
deletion is not allowed. If canceled, requires delete permissions on the linked document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _delete_file_on_disk(self)

If file not attached to any other record, delete it

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### unzip(self) → list['File']

Unzip current file and replace it by its children

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list['File']`


##### exists_on_disk(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_content(self, encodings = None) → bytes | str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| encodings | None | None | - |

**Returns**: `bytes | str`


##### get_full_path(self)

Return file path using the set file name.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### write_file(self)

write file to disk with a random name (to compare)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### save_file(self, content: bytes | str | None = None, decode = False, ignore_existing_file_check = False, overwrite = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| content | bytes | str | None | None | - |
| decode | None | False | - |
| ignore_existing_file_check | None | False | - |
| overwrite | None | False | - |


##### save_file_on_filesystem(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_max_file_size(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete_file_data_content(self, only_thumbnail = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| only_thumbnail | None | False | - |


##### delete_file_from_filesystem(self, only_thumbnail = False)

Delete file, thumbnail from File document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| only_thumbnail | None | False | - |


##### is_downloadable(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_extension(self)

Split and return filename and extension for the set `file_name`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_attachment_record(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_comment_in_reference_doc(self, comment_type, text)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| comment_type | None | - | - |
| text | None | - | - |


##### set_is_private(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### optimize_file(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### unique_url(self) → str

Unique URL contains file ID in URL to speed up permisison checks.

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`


##### zip_files(files)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| files | None | - | - |




## Functions

### on_doctype_update()

**Returns**: (none)



### has_permission(doc, ptype = None, user = None, debug = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| ptype | None | None | - |
| user | None | None | - |
| debug | None | False | - |

**Returns**: (none)



### get_permission_query_conditions(user: str | None = None) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | str | None | None | - |

**Returns**: `str`



### pop_rollback_flags()

**Returns**: (none)


