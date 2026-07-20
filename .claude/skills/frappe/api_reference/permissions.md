# API Reference: permissions.py

**Language**: Python

**Source**: `permissions.py`

---

## Functions

### print_has_permission_check_logs(func)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | None | - | - |

**Returns**: (none)



### _debug_log(log: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| log | str | - | - |

**Returns**: (none)



### _pop_debug_log() → list[str]

**Returns**: `list[str]`



### has_permission(doctype, ptype = 'read', doc = None, user = None) → bool

Return True if user has permission `ptype` for given `doctype`.
If `doc` is passed, also check user, share and owner permissions.

:param doctype: DocType to check permission for
:param ptype: Permission Type to check
:param doc: Check User Permissions for specified document.
:param user: User to check permission for. Defaults to current user.
:param print_logs: If True, will display a message using frappe.msgprint
                which explains why the permission check failed.
:param parent_doctype:
        Required when checking permission for a child DocType (unless doc is specified)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| ptype | None | 'read' | - |
| doc | None | None | - |
| user | None | None | - |

**Returns**: `bool`



### get_doc_permissions(doc, user = None, ptype = None, debug = False)

Return a dict of evaluated permissions for given `doc` like `{"read":1, "write":1}`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| user | None | None | - |
| ptype | None | None | - |
| debug | None | False | - |

**Returns**: (none)



### get_role_permissions(doctype_meta, user = None, is_owner = None, debug = False)

Return dict of evaluated role permissions like:
        {
                "read": 1,
                "write": 0,
                // if "if_owner" is enabled
                "if_owner":
                        {
                                "read": 1,
                                "write": 0
                        }
        }

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype_meta | None | - | - |
| user | None | None | - |
| is_owner | None | None | - |
| debug | None | False | - |

**Returns**: (none)



### get_user_permissions(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### has_user_permission(doc, user = None, debug = False)

Return True if User is allowed to view considering User Permissions.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| user | None | None | - |
| debug | None | False | - |

**Returns**: (none)



### has_controller_permissions(doc, ptype, user = None, debug = False) → bool

Return controller permissions if denied, True if not defined.

Controllers can only deny permission, they can not explicitly grant any permission that wasn't
already present.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| ptype | None | - | - |
| user | None | None | - |
| debug | None | False | - |

**Returns**: `bool`



### get_doctypes_with_read()

**Returns**: (none)



### get_valid_perms(doctype = None, user = None)

Get valid permissions for the current user from DocPerm and Custom DocPerm

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | None | - |
| user | None | None | - |

**Returns**: (none)



### get_all_perms(role)

Return valid permissions for a given role.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| role | None | - | - |

**Returns**: (none)



### get_roles(user = None, with_standard = True)

get roles of current user

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | None | - |
| with_standard | None | True | - |

**Returns**: (none)



### get_doctype_roles(doctype, access_type = 'read')

Return a list of roles that are allowed to access the given `doctype`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| access_type | None | 'read' | - |

**Returns**: (none)



### get_perms_for(roles, perm_doctype = 'DocPerm')

Get perms for given roles

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| roles | None | - | - |
| perm_doctype | None | 'DocPerm' | - |

**Returns**: (none)



### get_doctypes_with_custom_docperms()

Return all the doctypes with Custom Docperms.

**Returns**: (none)



### add_user_permission(doctype, name, user, ignore_permissions = False, applicable_for = None, is_default = 0, hide_descendants = 0)

Add user permission

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| user | None | - | - |
| ignore_permissions | None | False | - |
| applicable_for | None | None | - |
| is_default | None | 0 | - |
| hide_descendants | None | 0 | - |

**Returns**: (none)



### remove_user_permission(doctype, name, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| user | None | - | - |

**Returns**: (none)



### clear_user_permissions_for_doctype(doctype, user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| user | None | None | - |

**Returns**: (none)



### can_import(doctype, raise_exception = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| raise_exception | None | False | - |

**Returns**: (none)



### can_export(doctype, raise_exception = False, is_owner = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| raise_exception | None | False | - |
| is_owner | None | False | - |

**Returns**: (none)



### update_permission_property(doctype, role, permlevel, ptype, value = None, validate = True, if_owner = 0)

Update a property in Custom Perm

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| role | None | - | - |
| permlevel | None | - | - |
| ptype | None | - | - |
| value | None | None | - |
| validate | None | True | - |
| if_owner | None | 0 | - |

**Returns**: (none)



### setup_custom_perms(parent)

if custom permssions are not setup for the current doctype, set them up

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parent | None | - | - |

**Returns**: (none)



### add_permission(doctype, role, permlevel = 0, ptype = None)

Add a new permission rule to the given doctype
for the given Role and Permission Level

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| role | None | - | - |
| permlevel | None | 0 | - |
| ptype | None | None | - |

**Returns**: (none)



### copy_perms(parent)

Copy all DocPerm in to Custom DocPerm for the given document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parent | None | - | - |

**Returns**: (none)



### reset_perms(doctype)

Reset permissions for given doctype.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### get_linked_doctypes(dt: str) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | str | - | - |

**Returns**: `list`



### get_doc_name(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_rights(doctype = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | None | - |

**Returns**: (none)



### allow_everything(doctype = None)

Return a dict with access to everything, eg. {"read": 1, "write": 1, ...}.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | None | - |

**Returns**: (none)



### get_allowed_docs_for_doctype(user_permissions, doctype)

Return all the docs from the passed `user_permissions` that are allowed under provided doctype.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user_permissions | None | - | - |
| doctype | None | - | - |

**Returns**: (none)



### filter_allowed_docs_for_doctype(user_permissions, doctype, with_default_doc = True)

Return all the docs from the passed `user_permissions` that are
allowed under provided doctype along with default doc value if `with_default_doc` is set.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user_permissions | None | - | - |
| doctype | None | - | - |
| with_default_doc | None | True | - |

**Returns**: (none)



### push_perm_check_log(log, debug = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| log | None | - | - |
| debug | None | False | - |

**Returns**: (none)



### has_child_permission(child_doctype, ptype = 'read', child_doc = None, user = None, parent_doctype = None) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| child_doctype | None | - | - |
| ptype | None | 'read' | - |
| child_doc | None | None | - |
| user | None | None | - |
| parent_doctype | None | None | - |

**Returns**: `bool`



### is_system_user(user: str | None = None) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | str | None | None | - |

**Returns**: `bool`



### check_doctype_permission(doctype: str, ptype: str = 'read') → None

Designed specfically to override DoesNotExistError in some scenarios.
Ignores share permissions.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| ptype | str | 'read' | - |

**Returns**: `None`



### handle_does_not_exist_error(fn)

Decorator to override DoesNotExistError when handling exceptions.
Requires the first argument to be an Exception.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fn | None | - | - |

**Returns**: (none)



### _get_parent_and_ancestors(doctype, parent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| parent | None | - | - |

**Returns**: (none)



### inner()

**Returns**: (none)



### false_if_not_shared()

**Returns**: (none)



### is_user_owner()

**Returns**: (none)



### check_user_permission_on_link_fields(d)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |

**Returns**: (none)



### get()

**Returns**: (none)



### wrapper(e)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | None | - | - |

**Returns**: (none)



### is_perm_applicable(perm)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| perm | None | - | - |

**Returns**: (none)



### has_permission_without_if_owner_enabled(ptype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ptype | None | - | - |

**Returns**: (none)


