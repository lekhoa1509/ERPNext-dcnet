# API Reference: permission_manager.py

**Language**: Python

**Source**: `core/page/permission_manager/permission_manager.py`

---

## Functions

### get_roles_and_doctypes()

**Returns**: (none)



### get_permissions(doctype: str | None = None, role: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | None | None | - |
| role | str | None | None | - |

**Returns**: (none)



### add(parent, role, permlevel)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parent | None | - | - |
| role | None | - | - |
| permlevel | None | - | - |

**Returns**: (none)



### update(doctype: str, role: str, permlevel: int, ptype: str, value = None, if_owner = 0) → str | None

Update role permission params.

Args:
        doctype (str): Name of the DocType to update params for
        role (str): Role to be updated for, eg "Website Manager".
        permlevel (int): perm level the provided rule applies to
        ptype (str): permission type, example "read", "delete", etc.
        value (None, optional): value for ptype, None indicates False

Return:
        str: Refresh flag if permission is updated successfully

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| role | str | - | - |
| permlevel | int | - | - |
| ptype | str | - | - |
| value | None | None | - |
| if_owner | None | 0 | - |

**Returns**: `str | None`



### remove(doctype, role, permlevel, if_owner = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| role | None | - | - |
| permlevel | None | - | - |
| if_owner | None | 0 | - |

**Returns**: (none)



### reset(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### get_users_with_role(role)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| role | None | - | - |

**Returns**: (none)



### get_standard_permissions(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### clear_cache()

**Returns**: (none)


