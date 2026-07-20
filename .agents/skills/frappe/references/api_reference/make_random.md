# API Reference: make_random.py

**Language**: Python

**Source**: `utils/make_random.py`

---

## Functions

### add_random_children(doc: 'Document', fieldname: str, rows, randomize: dict, unique = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | 'Document' | - | - |
| fieldname | str | - | - |
| rows | None | - | - |
| randomize | dict | - | - |
| unique | None | None | - |

**Returns**: (none)



### get_random(doctype: str, filters: dict | None = None, doc: bool = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| filters | dict | None | None | - |
| doc | bool | False | - |

**Returns**: (none)



### can_make(doctype: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |

**Returns**: `bool`



### how_many(doctype: str) → int

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |

**Returns**: `int`


