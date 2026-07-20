# API Reference: nestedset.py

**Language**: Python

**Source**: `utils/nestedset.py`

---

## Classes

### NestedSetRecursionError

**Inherits from**: frappe.ValidationError



### NestedSetMultipleRootsError

**Inherits from**: frappe.ValidationError



### NestedSetChildExistsError

**Inherits from**: frappe.ValidationError



### NestedSetInvalidMergeError

**Inherits from**: frappe.ValidationError



### NestedSet

**Inherits from**: Document

#### Methods

##### __setup__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self, allow_root_deletion = False)

Runs on deletion of a document/node

:param allow_root_deletion: used for allowing root document deletion (DEPRECATED)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| allow_root_deletion | None | False | - |


##### validate_if_child_exists(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_rename(self, olddn, newdn, merge = False, group_fname = 'is_group')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| olddn | None | - | - |
| newdn | None | - | - |
| merge | None | False | - |
| group_fname | None | 'is_group' | - |


##### after_rename(self, olddn, newdn, merge = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| olddn | None | - | - |
| newdn | None | - | - |
| merge | None | False | - |


##### validate_one_root(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_root_node_count(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_ledger(self, group_identifier = 'is_group')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| group_identifier | None | 'is_group' | - |


##### get_ancestors(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_parent(self) → 'NestedSet'

Return the parent Document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `'NestedSet'`


##### get_children(self) → Iterator['NestedSet']

Return a generator that yields child Documents.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `Iterator['NestedSet']`




## Functions

### update_nsm(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### update_add_node(doc, parent, parent_field)

insert a new node

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| parent | None | - | - |
| parent_field | None | - | - |

**Returns**: (none)



### update_move_node(doc: Document, parent_field: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | Document | - | - |
| parent_field | str | - | - |

**Returns**: (none)



### rebuild_tree(doctype: str) → None

Call rebuild_node for all root nodes.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |

**Returns**: `None`



### rebuild_node(doctype, parent, left, parent_field)

reset lft, rgt and recursive call for all children

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| parent | None | - | - |
| left | None | - | - |
| parent_field | None | - | - |

**Returns**: (none)



### validate_loop(doctype, name, lft, rgt)

check if item not an ancestor (loop)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| lft | None | - | - |
| rgt | None | - | - |

**Returns**: (none)



### remove_subtree(doctype: str, name: str, throw = True)

Remove doc and all its children.

WARN: This does not run any controller hooks for deletion and deletes them with raw SQL query.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |
| throw | None | True | - |

**Returns**: (none)



### get_root_of(doctype)

Get root element of a DocType with a tree structure

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### get_ancestors_of(doctype, name, order_by = 'lft desc', limit = None)

Get ancestor elements of a DocType with a tree structure

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| order_by | None | 'lft desc' | - |
| limit | None | None | - |

**Returns**: (none)



### get_descendants_of(doctype, name, order_by = 'lft desc', limit = None, ignore_permissions = False)

Return descendants of the current record

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| order_by | None | 'lft desc' | - |
| limit | None | None | - |
| ignore_permissions | None | False | - |

**Returns**: (none)


