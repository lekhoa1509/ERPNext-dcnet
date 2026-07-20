# API Reference: test_permission_type.py

**Language**: Python

**Source**: `core/doctype/permission_type/test_permission_type.py`

---

## Classes

### IntegrationTestPermissionType

Integration tests for PermissionType.
Use this class for testing interactions between multiple components.

**Inherits from**: IntegrationTestCase

#### Methods

##### test_approve_ptype_on_blog_post(self)

Test that custom permission types are applied correctly.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_permission_type_creation_reserved_name(self)

Test that permission types with reserved names are rejected.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _create_test_user(self, email, role)

Create a test user with the specified role.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| email | None | - | - |
| role | None | - | - |


##### _create_permission_type(self, name, doc_type)

Create a permission type for the specified doctype.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | None | - | - |
| doc_type | None | - | - |


##### _verify_custom_fields_created(self, ptype_doc, doc_type)

Verify that custom fields are created for the permission type.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| ptype_doc | None | - | - |
| doc_type | None | - | - |


##### _verify_user_lacks_permission(self, doc_type, ptype_name, user_name)

Verify that user does not have the specified permission type.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc_type | None | - | - |
| ptype_name | None | - | - |
| user_name | None | - | - |


##### _verify_user_has_permission(self, doc_type, ptype_name, user_name)

Verify that user has the specified permission type.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc_type | None | - | - |
| ptype_name | None | - | - |
| user_name | None | - | - |



