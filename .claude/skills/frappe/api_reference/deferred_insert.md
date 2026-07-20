# API Reference: deferred_insert.py

**Language**: Python

**Source**: `deferred_insert.py`

---

## Functions

### deferred_insert(doctype: str, records: list[dict | 'Document'] | str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| records | list[dict | 'Document'] | str | - | - |

**Returns**: (none)



### save_to_db()

**Returns**: (none)



### insert_record(record: dict | 'Document', doctype: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| record | dict | 'Document' | - | - |
| doctype | str | - | - |

**Returns**: (none)



### get_key_name(key: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | str | - | - |

**Returns**: `str`



### get_doctype_name(key: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | str | - | - |

**Returns**: `str`


