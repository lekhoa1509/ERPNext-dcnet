# API Reference: user_invitation.py

**Language**: Python

**Source**: `core/doctype/user_invitation/user_invitation.py`

---

## Classes

### UserInvitation

**Inherits from**: Document

#### Methods

##### before_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### accept(self, ignore_permissions: bool = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| ignore_permissions | bool | False | - |


##### cancel_invite(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### expire(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _validate_invite(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _after_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _accept(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _upsert_user(self, ignore_permissions: bool = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| ignore_permissions | bool | False | - |


##### _run_after_accept_hooks(self, user: Document, user_inserted: bool)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | Document | - | - |
| user_inserted | bool | - | - |


##### _get_email_title(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _validate_app_name(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _get_allowed_roles(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _validate_roles(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _validate_email(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_redirect_to_path(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_app_name(app_name: str)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app_name | str | - | - |


##### validate_role(app_name: str) → None

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app_name | str | - | - |

**Returns**: `None`




## Functions

### mark_expired_invitations() → None

**Returns**: `None`



### get_allowed_apps(user: Document | None) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | Document | None | - | - |

**Returns**: `list[str]`



### get_permission_query_conditions(user: Document | None) → str | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | Document | None | - | - |

**Returns**: `str | None`



### has_permission(doc: UserInvitation, user: Document | None = None, permission_type: str | None = None) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | UserInvitation | - | - |
| user | Document | None | None | - |
| permission_type | str | None | None | - |

**Returns**: `bool`



### get_user_roles(user: Document | None) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | Document | None | - | - |

**Returns**: `list[str]`



### get_user(user: Document | None) → Document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | Document | None | - | - |

**Returns**: `Document`


