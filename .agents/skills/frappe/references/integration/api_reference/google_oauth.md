# API Reference: google_oauth.py

**Language**: Python

**Source**: `google_oauth.py`

---

## Classes

### GoogleAuthenticationError

**Inherits from**: Exception



### GoogleOAuth

**Inherits from**: (none)

#### Methods

##### __init__(self, domain: str, validate: bool = True, config = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| domain | str | - | - |
| validate | bool | True | - |
| config | None | None | - |


##### validate_google_settings(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### authorize(self, oauth_code: str) → dict[str, str | int]

Return a dict with access and refresh token.

:param oauth_code: code got back from google upon successful auhtorization

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| oauth_code | str | - | - |

**Returns**: `dict[str, str | int]`


##### refresh_access_token(self, refresh_token: str) → dict[str, str | int]

Refreshes google access token using refresh token

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| refresh_token | str | - | - |

**Returns**: `dict[str, str | int]`


##### get_authentication_url(self, state: dict[str, str]) → dict[str, str]

Return Google authentication url.

:param state: dict of values which you need on callback (for calling methods, redirection back to the form, doc name, etc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| state | dict[str, str] | - | - |

**Returns**: `dict[str, str]`


##### get_google_service_object(self, access_token: str, refresh_token: str)

Return Google service object.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| access_token | str | - | - |
| refresh_token | str | - | - |




## Functions

### handle_response(response: dict[str, str | int], error_title: str, error_message: str, raise_err: bool = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| response | dict[str, str | int] | - | - |
| error_title | str | - | - |
| error_message | str | - | - |
| raise_err | bool | False | - |

**Returns**: (none)



### is_valid_access_token(access_token: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| access_token | str | - | - |

**Returns**: `bool`



### callback(state: str, code: str | None = None, error: str | None = None) → None

Common callback for google integrations.
Invokes functions using `frappe.get_attr` and also adds required (keyworded) arguments
along with committing and redirecting us back to frappe site.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| state | str | - | - |
| code | str | None | None | - |
| error | str | None | None | - |

**Returns**: `None`


