# API Reference: login.py

**Language**: Python

**Source**: `www/login.py`

---

## Functions

### get_context(context)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | None | - | - |

**Returns**: (none)



### login_via_token(login_token: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| login_token | str | - | - |

**Returns**: (none)



### get_login_with_email_link_ratelimit() → int

**Returns**: `int`



### send_login_link(email: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email | str | - | - |

**Returns**: (none)



### _generate_temporary_login_link(email: str, expiry: int)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email | str | - | - |
| expiry | int | - | - |

**Returns**: (none)



### login_via_key(key: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | str | - | - |

**Returns**: (none)



### sanitize_redirect(redirect: str | None) → str | None

Only allow redirect on same domain.

Allowed redirects:
- Same host e.g. https://frappe.localhost/path
- Just path e.g. /app gets converted to https://frappe.localhost/app

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| redirect | str | None | - | - |

**Returns**: `str | None`


