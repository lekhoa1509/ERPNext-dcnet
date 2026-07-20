# API Reference: oauth.py

**Language**: Python

**Source**: `utils/oauth.py`

---

## Classes

### SignupDisabledError

**Inherits from**: frappe.PermissionError



## Functions

### build_oauth_url(base_url: str, url: str | None = None) → str

Build a complete OAuth authorization URL.

This helper constructs a full OAuth URL starting from a given base URL.

If `url` is omitted, the function simply returns the normalized base URL.  If the
`url` contains the relative or absolute path, the function will return this
appended to the base URL.  If the `url` contains a `scheme` (e.g. "https://" and a
`netloc` (e.g. "www.example.com")), the function will return the passed `url` alone.

Args:
        base_url (str): The base OAuth endpoint (e.g. "https://example.com").
        url (str | None): An optional path or override URL to combine with the base.

Returns:
        str: The fully qualified OAuth URL ready for use in redirects or API calls.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| base_url | str | - | - |
| url | str | None | None | - |

**Returns**: `str`



### get_oauth2_providers() → dict[str, dict]

**Returns**: `dict[str, dict]`



### get_oauth_keys(provider: str) → dict[str, str]

get client_id and client_secret from database or conf

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| provider | str | - | - |

**Returns**: `dict[str, str]`



### get_oauth2_authorize_url(provider: str, redirect_to: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| provider | str | - | - |
| redirect_to | str | - | - |

**Returns**: `str`



### get_oauth2_flow(provider: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| provider | str | - | - |

**Returns**: (none)



### get_redirect_uri(provider: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| provider | str | - | - |

**Returns**: `str`



### login_via_oauth2(provider: str, code: str, state: str, decoder: Callable | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| provider | str | - | - |
| code | str | - | - |
| state | str | - | - |
| decoder | Callable | None | None | - |

**Returns**: (none)



### login_via_oauth2_id_token(provider: str, code: str, state: str, decoder: Callable | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| provider | str | - | - |
| code | str | - | - |
| state | str | - | - |
| decoder | Callable | None | None | - |

**Returns**: (none)



### get_info_via_oauth(provider: str, code: str, decoder: Callable | None = None, id_token: bool = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| provider | str | - | - |
| code | str | - | - |
| decoder | Callable | None | None | - |
| id_token | bool | False | - |

**Returns**: (none)



### login_oauth_user(data: dict | str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | dict | str | - | - |

**Returns**: (none)



### get_user_record(user: str, data: dict, provider: str) → 'User'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | str | - | - |
| data | dict | - | - |
| provider | str | - | - |

**Returns**: `'User'`



### update_oauth_user(user: str, data: dict, provider: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | str | - | - |
| data | dict | - | - |
| provider | str | - | - |

**Returns**: (none)



### get_first_name(data: dict) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | dict | - | - |

**Returns**: `str`



### get_last_name(data: dict) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | dict | - | - |

**Returns**: `str`



### get_email(data: dict) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | dict | - | - |

**Returns**: `str`



### redirect_post_login(desk_user: bool, redirect_to: str | None = None, provider: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| desk_user | bool | - | - |
| redirect_to | str | None | None | - |
| provider | str | None | None | - |

**Returns**: (none)


