# API Reference: save.py

**Language**: Python

**Source**: `form/save.py`

---

## Functions

### savedocs(doc, action)

save / submit / update doclist

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| action | None | - | - |

**Returns**: (none)



### cancel(doctype = None, name = None, workflow_state_fieldname = None, workflow_state = None)

cancel a doclist

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | None | - |
| name | None | None | - |
| workflow_state_fieldname | None | None | - |
| workflow_state | None | None | - |

**Returns**: (none)



### discard(doctype: str, name: str | int)

discard a draft document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | int | - | - |

**Returns**: (none)



### send_updated_docs(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### set_local_name(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### _set_local_name(d)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |

**Returns**: (none)


