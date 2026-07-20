# API Reference: ldap_settings.py

**Language**: Python

**Source**: `doctype/ldap_settings/ldap_settings.py`

---

## Classes

### LDAPSettings

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### connect_to_ldap(self, base_dn, password, read_only = True) → ldap3.Connection

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| base_dn | None | - | - |
| password | None | - | - |
| read_only | None | True | - |

**Returns**: `ldap3.Connection`


##### get_ldap_client_settings() → dict

**Decorators**: `@staticmethod`

**Returns**: `dict`


##### update_user_fields(cls, user: 'User', user_data: dict)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| user | 'User' | - | - |
| user_data | dict | - | - |


##### sync_roles(self, user: 'User', additional_groups: list | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | 'User' | - | - |
| additional_groups | list | None | None | - |


##### create_or_update_user(self, user_data: dict, groups: list | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user_data | dict | - | - |
| groups | list | None | None | - |


##### get_ldap_attributes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### fetch_ldap_groups(self, user: Entry, conn: ldap3.Connection) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | Entry | - | - |
| conn | ldap3.Connection | - | - |

**Returns**: `list`


##### authenticate(self, username: str, password: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| username | str | - | - |
| password | str | - | - |


##### reset_password(self, user: str, password: str, logout_sessions: int = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | str | - | - |
| password | str | - | - |
| logout_sessions | int | 0 | - |


##### convert_ldap_entry_to_dict(self, user_entry: Entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user_entry | Entry | - | - |




## Functions

### login()

**Returns**: (none)



### reset_password(user: str, password: str, logout: int)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | str | - | - |
| password | str | - | - |
| logout | int | - | - |

**Returns**: (none)


