# API Reference: test_ldap_settings.py

**Language**: Python

**Source**: `integrations/doctype/ldap_settings/test_ldap_settings.py`

---

## Classes

### LDAP_TestCase

**Inherits from**: (none)

#### Methods

##### mock_ldap_connection(f)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| f | None | - | - |


##### clean_test_users()


##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### tearDownClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### test_mandatory_fields(self)

**Decorators**: `@mock_ldap_connection`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validation_ldap_search_string(self)

**Decorators**: `@mock_ldap_connection`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_connect_to_ldap(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_ldap_client_settings(self)

**Decorators**: `@mock_ldap_connection`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_user_fields(self)

**Decorators**: `@mock_ldap_connection`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_create_website_user(self)

**Decorators**: `@mock_ldap_connection`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sync_roles(self)

**Decorators**: `@mock_ldap_connection`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_create_or_update_user(self)

**Decorators**: `@mock_ldap_connection`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_ldap_attributes(self)

**Decorators**: `@mock_ldap_connection`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_fetch_ldap_groups(self)

**Decorators**: `@mock_ldap_connection`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_authenticate(self)

**Decorators**: `@mock_ldap_connection`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_complex_ldap_search_filter(self)

**Decorators**: `@mock_ldap_connection`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reset_password(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_convert_ldap_entry_to_dict(self)

**Decorators**: `@mock_ldap_connection`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### Test_OpenLDAP

**Inherits from**: LDAP_TestCase, TestCase



### Test_ActiveDirectory

**Inherits from**: LDAP_TestCase, TestCase



## Functions

### wrapped(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: (none)


