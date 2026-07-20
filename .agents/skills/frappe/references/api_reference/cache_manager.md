# API Reference: cache_manager.py

**Language**: Python

**Source**: `cache_manager.py`

---

## Functions

### get_doctype_map_key(doctype, name = '*') → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | '*' | - |

**Returns**: `str`



### clear_user_cache(user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | None | - |

**Returns**: (none)



### clear_domain_cache(user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | None | - |

**Returns**: (none)



### clear_global_cache()

**Returns**: (none)



### clear_defaults_cache(user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | None | - |

**Returns**: (none)



### clear_doctype_cache(doctype = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | None | - |

**Returns**: (none)



### _clear_doctype_cache_from_redis(doctype: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | None | None | - |

**Returns**: (none)



### clear_controller_cache(doctype = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | None | - |

**Returns**: (none)



### get_doctype_map(doctype, name, filters = None, order_by = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| filters | None | None | - |
| order_by | None | None | - |

**Returns**: (none)



### clear_doctype_map(doctype, name = '*')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | '*' | - |

**Returns**: (none)



### build_table_count_cache()

**Returns**: (none)



### build_domain_restricted_doctype_cache()

**Returns**: (none)



### build_domain_restricted_page_cache()

**Returns**: (none)



### clear_cache(user: str | None = None, doctype: str | None = None)

Clear **User**, **DocType** or global cache.

:param user: If user is given, only user cache is cleared.
:param doctype: If doctype is given, only DocType cache is cleared.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | str | None | None | - |
| doctype | str | None | None | - |

**Returns**: (none)



### reset_metadata_version()

Reset `metadata_version` (Client (Javascript) build ID) hash.

**Returns**: (none)



### clear_single(dt)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |

**Returns**: (none)


