# API Reference: role.py

**Language**: Python

**Source**: `core/doctype/role/role.py`

---

## Classes

### Role

**Inherits from**: Document

#### Methods

##### before_rename(self, old, new, merge = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old | None | - | - |
| new | None | - | - |
| merge | None | False | - |


##### after_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### disable_role(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_homepage(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_desk_properties(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### remove_roles(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

update system user desk access if this has changed in this update

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_user_type_on_change(self)

When desk access changes, all the users that have this role need to be re-evaluated

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_info_based_on_role(role, field = 'email', ignore_permissions = False)

Get information of all users that have been assigned this role

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| role | None | - | - |
| field | None | 'email' | - |
| ignore_permissions | None | False | - |

**Returns**: (none)



### get_user_info(users, field = 'email')

Fetch details about users for the specified field

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| users | None | - | - |
| field | None | 'email' | - |

**Returns**: (none)



### get_users(role)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| role | None | - | - |

**Returns**: (none)



### role_query(doctype, txt, searchfield, start, page_len, filters)

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


