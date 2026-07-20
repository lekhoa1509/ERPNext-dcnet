# API Reference: test_oauth20.py

**Language**: Python

**Source**: `tests/test_oauth20.py`

---

## Classes

### FrappeRequestTestCase

**Inherits from**: IntegrationTestCase

#### Methods

##### sid(self) → str

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`


##### get(self, path: str, params: dict | None = None) → TestResponse

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| path | str | - | - |
| params | dict | None | None | - |

**Returns**: `TestResponse`


##### post(self, path, data) → TestResponse

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| path | None | - | - |
| data | None | - | - |

**Returns**: `TestResponse`


##### put(self, path, data) → TestResponse

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| path | None | - | - |
| data | None | - | - |

**Returns**: `TestResponse`


##### delete(self, path) → TestResponse

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| path | None | - | - |

**Returns**: `TestResponse`




### TestOAuth20

**Inherits from**: FrappeRequestTestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_invalid_login(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_login_using_authorization_code(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_login_using_authorization_code_with_pkce(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_revoke_token(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_resource_owner_password_credentials_grant(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_login_using_implicit_token(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_openid_code_id_token(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_build_oauth_url(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### decode_id_token(self, id_token)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| id_token | None | - | - |




## Functions

### check_valid_openid_response(access_token = None, client: 'FrappeRequestTestCase' = None)

Return True for valid response.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| access_token | None | None | - |
| client | 'FrappeRequestTestCase' | None | - |

**Returns**: (none)



### login(session)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| session | None | - | - |

**Returns**: (none)



### get_full_url(endpoint)

Turn '/endpoint' into 'http://127.0.0.1:8000/endpoint'.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| endpoint | None | - | - |

**Returns**: (none)



### update_client_for_auth_code_grant(client_id)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| client_id | None | - | - |

**Returns**: (none)


