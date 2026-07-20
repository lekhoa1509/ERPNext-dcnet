# API Reference: sequence.py

**Language**: Python

**Source**: `database/sequence.py`

---

## Functions

### create_sequence(doctype_name: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype_name | str | - | - |

**Returns**: `str`



### get_next_val(doctype_name: str, slug: str = '_id_seq') → int

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype_name | str | - | - |
| slug | str | '_id_seq' | - |

**Returns**: `int`



### set_next_val(doctype_name: str, next_val: int) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype_name | str | - | - |
| next_val | int | - | - |

**Returns**: `None`


