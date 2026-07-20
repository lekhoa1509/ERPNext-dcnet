# API Reference: sync.py

**Language**: Python

**Source**: `model/sync.py`

---

## Functions

### sync_all(force = 0, reset_permissions = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| force | None | 0 | - |
| reset_permissions | None | False | - |

**Returns**: (none)



### sync_for(app_name, force = 0, reset_permissions = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app_name | None | - | - |
| force | None | 0 | - |
| reset_permissions | None | False | - |

**Returns**: (none)



### get_doc_files(files, start_path)

walk and sync all doctypes and pages

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| files | None | - | - |
| start_path | None | - | - |

**Returns**: (none)



### remove_orphan_doctypes()

Find and remove any orphaned doctypes.

These are doctypes for which code and schema file is
deleted but entry is present in DocType table.

Note: Deleting the entry doesn't delete any data.
So this is supposed to be non-destrictive operation.

**Returns**: (none)



### remove_orphan_entities()

**Returns**: (none)



### create_entity_file_map(entities)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| entities | None | - | - |

**Returns**: (none)



### check_if_record_exists(type = None, path = None, entity_type = None, name = None, module_name = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| type | None | None | - |
| path | None | None | - |
| entity_type | None | None | - |
| name | None | None | - |
| module_name | None | None | - |

**Returns**: (none)



### delete_duplicate_icons()

**Returns**: (none)



### build_path(entity_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| entity_name | None | - | - |

**Returns**: (none)


