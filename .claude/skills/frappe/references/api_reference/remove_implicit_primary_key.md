# API Reference: remove_implicit_primary_key.py

**Language**: Python

**Source**: `patches/v15_0/remove_implicit_primary_key.py`

---

## Functions

### execute()

Few doctypes had int PKs even though schema didn't mention them, this requires detecting it
at runtime which is prone to bugs and adds unnecessary overhead.

This patch converts them back to varchar.

**Returns**: (none)



### _is_implicit_int_pk(doctype: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |

**Returns**: `bool`


