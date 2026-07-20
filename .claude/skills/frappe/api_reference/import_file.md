# API Reference: import_file.py

**Language**: Python

**Source**: `modules/import_file.py`

---

## Functions

### calculate_hash(path: str) → str

Calculate and return md5 hash of the file in binary mode.

Args:
        path (str): Path to the file to be hashed

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | str | - | - |

**Returns**: `str`



### import_files(module, dt = None, dn = None, force = False, pre_process = None, reset_permissions = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| module | None | - | - |
| dt | None | None | - |
| dn | None | None | - |
| force | None | False | - |
| pre_process | None | None | - |
| reset_permissions | None | False | - |

**Returns**: (none)



### import_file(module, dt, dn, force = False, pre_process = None, reset_permissions = False)

Sync a file from txt if modifed, return false if not updated

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| module | None | - | - |
| dt | None | - | - |
| dn | None | - | - |
| force | None | False | - |
| pre_process | None | None | - |
| reset_permissions | None | False | - |

**Returns**: (none)



### get_file_path(module, dt, dn)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| module | None | - | - |
| dt | None | - | - |
| dn | None | - | - |

**Returns**: (none)



### import_file_by_path(path: str, force: bool = False, data_import: bool = False, pre_process = None, ignore_version: bool | None = None, reset_permissions: bool = False) → bool

Import file from the given path.

Some conditions decide if a file should be imported or not.
Evaluation takes place in the order they are mentioned below.

- Check if `force` is true. Import the file. If not, move ahead.
- Get `db_modified_timestamp`(value of the modified field in the database for the file).
        If the return is `none,` this file doesn't exist in the DB, so Import the file. If not, move ahead.
- Check if there is a hash in DB for that file. If there is, Calculate the Hash of the file to import and compare it with the one in DB if they are not equal.
        Import the file. If Hash doesn't exist, move ahead.
- Check if `db_modified_timestamp` is older than the timestamp in the file; if it is, we import the file.

If timestamp comparison happens for doctypes, that means the Hash for it doesn't exist.
So, even if the timestamp is newer on DB (When comparing timestamps), we import the file and add the calculated Hash to the DB.
So in the subsequent imports, we can use hashes to compare. As a precautionary measure, the timestamp is updated to the current time as well.

Args:
        path (str): Path to the file.
        force (bool, optional): Load the file without checking any conditions. Defaults to False.
        data_import (bool, optional): [description]. Defaults to False.
        pre_process ([type], optional): Any preprocesing that may need to take place on the doc. Defaults to None.
        ignore_version (bool, optional): ignore current version. Defaults to None.
        reset_permissions (bool, optional): reset permissions for the file. Defaults to False.

Return True if import takes place, False if it wasn't imported.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | str | - | - |
| force | bool | False | - |
| data_import | bool | False | - |
| pre_process | None | None | - |
| ignore_version | bool | None | None | - |
| reset_permissions | bool | False | - |

**Returns**: `bool`



### read_doc_from_file(path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)



### update_modified(original_modified, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| original_modified | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### import_doc(docdict, data_import = False, pre_process = None, ignore_version = None, reset_permissions = False, path = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docdict | None | - | - |
| data_import | None | False | - |
| pre_process | None | None | - |
| ignore_version | None | None | - |
| reset_permissions | None | False | - |
| path | None | None | - |

**Returns**: (none)



### load_code_properties(doc, path)

Load code files stored in separate files with extensions

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| path | None | - | - |

**Returns**: (none)



### delete_old_doc(doc, reset_permissions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| reset_permissions | None | - | - |

**Returns**: (none)



### reset_tree_properties(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)


