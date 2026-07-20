# API Reference: share.py

**Language**: Python

**Source**: `share.py`

---

## Functions

### add(doctype, name, user = None, read = 1, write = 0, submit = 0, share = 0, everyone = 0, notify = 0)

Expose function without flags to the client-side

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| user | None | None | - |
| read | None | 1 | - |
| write | None | 0 | - |
| submit | None | 0 | - |
| share | None | 0 | - |
| everyone | None | 0 | - |
| notify | None | 0 | - |

**Returns**: (none)



### add_docshare(doctype, name, user = None, read = 1, write = 0, submit = 0, share = 0, everyone = 0, flags = None, notify = 0)

Share the given document with a user.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| user | None | None | - |
| read | None | 1 | - |
| write | None | 0 | - |
| submit | None | 0 | - |
| share | None | 0 | - |
| everyone | None | 0 | - |
| flags | None | None | - |
| notify | None | 0 | - |

**Returns**: (none)



### remove(doctype, name, user, flags = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| user | None | - | - |
| flags | None | None | - |

**Returns**: (none)



### set_permission(doctype, name, user, permission_to, value = 1, everyone = 0)

Expose function without flags to the client-side

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| user | None | - | - |
| permission_to | None | - | - |
| value | None | 1 | - |
| everyone | None | 0 | - |

**Returns**: (none)



### set_docshare_permission(doctype, name, user, permission_to, value = 1, everyone = 0, flags = None)

Set share permission.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| user | None | - | - |
| permission_to | None | - | - |
| value | None | 1 | - |
| everyone | None | 0 | - |
| flags | None | None | - |

**Returns**: (none)



### get_users(doctype: str, name: str) → list

Get list of users with which this document is shared

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |

**Returns**: `list`



### _get_users(doc: 'Document') → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | 'Document' | - | - |

**Returns**: `list`



### get_shared(doctype, user = None, rights = None)

Get list of shared document names for given user and DocType.

:param doctype: DocType of which shared names are queried.
:param user: User for which shared names are queried.
:param rights: List of rights for which the document is shared. List of `read`, `write`, `share`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| user | None | None | - |
| rights | None | None | - |

**Returns**: (none)



### get_shared_doctypes(user = None)

Return list of doctypes in which documents are shared for the given user.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | None | - |

**Returns**: (none)



### get_share_name(doctype, name, user, everyone)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| user | None | - | - |
| everyone | None | - | - |

**Returns**: (none)



### check_share_permission(doctype, name, permissions = None, custom_perms = None)

Check if the user can share with other users and has the permissions they are trying to grant.

:param doctype: DocType being shared
:param name: Document name being shared
:param permissions: Permissions that the user wants to share
:param custom_perms: List of custom permission types for the doctype

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| permissions | None | None | - |
| custom_perms | None | None | - |

**Returns**: (none)



### notify_assignment(shared_by, doctype, doc_name, everyone, notify = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| shared_by | None | - | - |
| doctype | None | - | - |
| doc_name | None | - | - |
| everyone | None | - | - |
| notify | None | 0 | - |

**Returns**: (none)


