# API Reference: user_permission.py

**Language**: Python

**Source**: `core/doctype/user_permission/user_permission.py`

---

## Classes

### UserPermission

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_user_permission(self)

checks for duplicate user permission records

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_default_permission(self)

validate user permission overlap for default value of a particular doctype

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_permission_log_options(self, event = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| event | None | None | - |




## Functions

### send_user_permissions(bootinfo)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bootinfo | None | - | - |

**Returns**: (none)



### get_user_permissions(user = None)

Get all users permissions for the user as a dict of doctype

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | None | - |

**Returns**: (none)



### user_permission_exists(user, allow, for_value, applicable_for = None)

Checks if similar user permission already exists

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |
| allow | None | - | - |
| for_value | None | - | - |
| applicable_for | None | None | - |

**Returns**: (none)



### get_applicable_for_doctype_list(doctype, txt, searchfield, start, page_len, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |
| searchfield | None | - | - |
| start | None | - | - |
| page_len | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_permitted_documents(doctype)

Return permitted documents from the given doctype for the session user.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### check_applicable_doc_perm(user, doctype, docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |
| doctype | None | - | - |
| docname | None | - | - |

**Returns**: (none)



### clear_user_permissions(user, for_doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |
| for_doctype | None | - | - |

**Returns**: (none)



### add_user_permissions(data)

Add and update the user permissions

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### insert_user_perm(user, doctype, docname, is_default = 0, hide_descendants = 0, apply_to_all = None, applicable = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |
| doctype | None | - | - |
| docname | None | - | - |
| is_default | None | 0 | - |
| hide_descendants | None | 0 | - |
| apply_to_all | None | None | - |
| applicable | None | None | - |

**Returns**: (none)



### remove_applicable(perm_applied_docs, user, doctype, docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| perm_applied_docs | None | - | - |
| user | None | - | - |
| doctype | None | - | - |
| docname | None | - | - |

**Returns**: (none)



### remove_apply_to_all(user, doctype, docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |
| doctype | None | - | - |
| docname | None | - | - |

**Returns**: (none)



### update_applicable(already_applied, to_apply, user, doctype, docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| already_applied | None | - | - |
| to_apply | None | - | - |
| user | None | - | - |
| doctype | None | - | - |
| docname | None | - | - |

**Returns**: (none)



### add_doc_to_perm(perm, doc_name, is_default, hide_descendants)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| perm | None | - | - |
| doc_name | None | - | - |
| is_default | None | - | - |
| hide_descendants | None | - | - |

**Returns**: (none)


