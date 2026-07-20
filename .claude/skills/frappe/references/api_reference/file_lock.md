# API Reference: file_lock.py

**Language**: Python

**Source**: `utils/file_lock.py`

---

## Classes

### LockTimeoutError

**Inherits from**: Exception



## Functions

### create_lock(name)

Creates a file in the /locks folder by the given name.

Note: This is a "weak lock" and is prone to race conditions. Do not use this lock for small
sections of code that execute immediately.

This is primarily use for locking documents for background submission.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### lock_exists(name)

Return True if lock of the given name exists.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### lock_age(name) → float

Return time in seconds since lock was created.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: `float`



### check_lock(path, timeout = 600)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |
| timeout | None | 600 | - |

**Returns**: (none)



### delete_lock(name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### get_lock_path(name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### release_document_locks()

Unlocks all documents that were locked by the current context.

**Returns**: (none)


