# API Reference: assign_to.py

**Language**: Python

**Source**: `form/assign_to.py`

---

## Classes

### DuplicateToDoError

**Inherits from**: frappe.ValidationError



## Functions

### get(args = None)

get assigned to

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | None | - |

**Returns**: (none)



### add(args = None)

add in someone's to do list
args = {
        "assign_to": [],
        "doctype": ,
        "name": ,
        "description": ,
        "assignment_rule":
}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | None | - |

**Returns**: (none)



### add_multiple(args = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | None | - |

**Returns**: (none)



### close_all_assignments(doctype, name, ignore_permissions = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| ignore_permissions | None | False | - |

**Returns**: (none)



### remove(doctype, name, assign_to, ignore_permissions = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| assign_to | None | - | - |
| ignore_permissions | None | False | - |

**Returns**: (none)



### remove_multiple(doctype, names, ignore_permissions = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| names | None | - | - |
| ignore_permissions | None | False | - |

**Returns**: (none)



### close(doctype: str, name: str, assign_to: str, ignore_permissions = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |
| assign_to | str | - | - |
| ignore_permissions | None | False | - |

**Returns**: (none)



### set_status(doctype, name, todo = None, assign_to = None, status = 'Cancelled', ignore_permissions = False)

remove from todo

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| todo | None | None | - |
| assign_to | None | None | - |
| status | None | 'Cancelled' | - |
| ignore_permissions | None | False | - |

**Returns**: (none)



### clear(doctype, name, ignore_permissions = False)

Clears assignments, return False if not assigned.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| ignore_permissions | None | False | - |

**Returns**: (none)



### notify_assignment(assigned_by, allocated_to, doc_type, doc_name, action = 'CLOSE', description = None)

Notify assignee that there is a change in assignment

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| assigned_by | None | - | - |
| allocated_to | None | - | - |
| doc_type | None | - | - |
| doc_name | None | - | - |
| action | None | 'CLOSE' | - |
| description | None | None | - |

**Returns**: (none)



### format_message_for_assign_to(users)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| users | None | - | - |

**Returns**: (none)


