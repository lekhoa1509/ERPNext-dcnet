# API Reference: note.py

**Language**: Python

**Source**: `desk/doctype/note/note.py`

---

## Classes

### Note

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_print(self, settings = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| settings | None | None | - |


##### clear_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### mark_seen_by(self, user: str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | str | - | - |

**Returns**: `None`




## Functions

### mark_as_seen(note: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| note | str | - | - |

**Returns**: (none)



### get_permission_query_conditions(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### has_permission(doc, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| user | None | - | - |

**Returns**: (none)



### get_unseen_notes()

**Returns**: (none)



### reset_notes()

**Returns**: (none)



### _get_unseen_notes()

**Returns**: (none)


