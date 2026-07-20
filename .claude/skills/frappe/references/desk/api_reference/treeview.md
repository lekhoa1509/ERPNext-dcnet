# API Reference: treeview.py

**Language**: Python

**Source**: `treeview.py`

---

## Functions

### get_all_nodes(doctype, label, parent, tree_method)

Recursively gets all data from tree nodes

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| label | None | - | - |
| parent | None | - | - |
| tree_method | None | - | - |

**Returns**: (none)



### get_children(doctype, parent = '', include_disabled = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| parent | None | '' | - |
| include_disabled | None | False | - |

**Returns**: (none)



### _get_children(doctype, parent = '', ignore_permissions = False, include_disabled = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| parent | None | '' | - |
| ignore_permissions | None | False | - |
| include_disabled | None | False | - |

**Returns**: (none)



### add_node()

**Returns**: (none)



### make_tree_args()

**Returns**: (none)


