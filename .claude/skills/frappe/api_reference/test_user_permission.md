# API Reference: test_user_permission.py

**Language**: Python

**Source**: `core/doctype/user_permission/test_user_permission.py`

---

## Classes

### TestUserPermission

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_default_user_permission_validation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_default_user_permission_corectness(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_default_user_permission(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_apply_to_all(self)

Create User permission for User having access to all applicable Doctypes

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_for_apply_to_all_on_update_from_apply_all(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_for_applicable_on_update_from_apply_to_all(self)

Update User Permission from all to some applicable Doctypes

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_for_apply_to_all_on_update_from_applicable(self)

Update User Permission from some to all applicable Doctypes

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_user_perm_for_nested_doctype(self)

Test if descendants' visibility is controlled for a nested DocType.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_user_perm_on_new_doc_with_field_default(self)

Test User Perm impact on frappe.new_doc. with *field* default value

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_user_perm_on_new_doc_with_user_default(self)

Test User Perm impact on frappe.new_doc. with *user* default value

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_user(email)

create user with role system manager

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email | None | - | - |

**Returns**: (none)



### get_params(user, doctype, docname, is_default = 0, hide_descendants = 0, applicable = None)

Return param to insert

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |
| doctype | None | - | - |
| docname | None | - | - |
| is_default | None | 0 | - |
| hide_descendants | None | 0 | - |
| applicable | None | None | - |

**Returns**: (none)



### get_exists_param(user, applicable = None)

param to check existing Document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |
| applicable | None | None | - |

**Returns**: (none)


