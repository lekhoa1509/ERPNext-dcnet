# API Reference: like.py

**Language**: Python

**Source**: `like.py`

---

## Functions

### toggle_like(doctype, name, add = False)

Adds / removes the current user in the `__liked_by` property of the given document.
If column does not exist, will add it in the database.

The `_liked_by` property is always set from this function and is ignored if set via
Document API

:param doctype: DocType of the document to like
:param name: Name of the document to like
:param add: `Yes` if like is to be added. If not `Yes` the like will be removed.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| add | None | False | - |

**Returns**: (none)



### _toggle_like(doctype, name, add, user = None)

Same as toggle_like but hides param `user` from API

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| add | None | - | - |
| user | None | None | - |

**Returns**: (none)



### remove_like(doctype, name)

Remove previous Like

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |

**Returns**: (none)



### add_comment(doctype, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |

**Returns**: (none)


