# API Reference: user.py

**Language**: Python

**Source**: `utils/user.py`

---

## Classes

### UserPermissions

A user permission object can be accessed as `frappe.get_user()`

**Inherits from**: (none)

#### Methods

##### __init__(self, name = '')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | None | '' | - |


##### setup_user(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_roles(self)

get list of roles

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### build_doctype_map(self)

build map of special doctype properties

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### build_perm_map(self)

build map of permissions at level 0

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### build_permissions(self)

build lists of what the user can read / write / create
quirks:
        read_only => Not in Search
        in_create => Not in create

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_defaults(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _get(self, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |


##### get_can_read(self)

return list of doctypes that the user can read

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### load_user(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_all_reports(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_user_fullname(user: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | str | - | - |

**Returns**: `str`



### get_fullname_and_avatar(user: str) → _dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | str | - | - |

**Returns**: `_dict`



### get_system_managers(only_name: bool = False) → list[str]

Return all system manager's user details.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| only_name | bool | False | - |

**Returns**: `list[str]`



### add_role(user: str, role: str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | str | - | - |
| role | str | - | - |

**Returns**: `None`



### add_system_manager(email: str, first_name: str | None = None, last_name: str | None = None, send_welcome_email: bool = False, password: str | None = None) → 'User'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email | str | - | - |
| first_name | str | None | None | - |
| last_name | str | None | None | - |
| send_welcome_email | bool | False | - |
| password | str | None | None | - |

**Returns**: `'User'`



### get_enabled_system_users() → list[dict]

**Returns**: `list[dict]`



### is_website_user(username: str | None = None) → str | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| username | str | None | None | - |

**Returns**: `str | None`



### is_system_user(username: str | None = None) → str | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| username | str | None | None | - |

**Returns**: `str | None`



### get_users() → list[dict]

**Returns**: `list[dict]`



### get_users_with_role(role: str) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| role | str | - | - |

**Returns**: `list[str]`



### is_portal_user()

**Returns**: (none)



### get_portal_roles()

**Returns**: (none)



### get_user_doc()

**Returns**: (none)


