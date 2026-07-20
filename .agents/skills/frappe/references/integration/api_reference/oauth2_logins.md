# API Reference: oauth2_logins.py

**Language**: Python

**Source**: `oauth2_logins.py`

---

## Functions

### login_via_google(code: str, state: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | str | - | - |
| state | str | - | - |

**Returns**: (none)



### login_via_github(code: str, state: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | str | - | - |
| state | str | - | - |

**Returns**: (none)



### login_via_facebook(code: str, state: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | str | - | - |
| state | str | - | - |

**Returns**: (none)



### login_via_frappe(code: str, state: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | str | - | - |
| state | str | - | - |

**Returns**: (none)



### login_via_office365(code: str, state: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | str | - | - |
| state | str | - | - |

**Returns**: (none)



### login_via_salesforce(code: str, state: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | str | - | - |
| state | str | - | - |

**Returns**: (none)



### login_via_fairlogin(code: str, state: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | str | - | - |
| state | str | - | - |

**Returns**: (none)



### login_via_keycloak(code: str, state: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | str | - | - |
| state | str | - | - |

**Returns**: (none)



### custom(code: str, state: str)

Callback for processing code and state for user added providers

process social login from /api/method/frappe.integrations.oauth2_logins.custom/<provider>

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | str | - | - |
| state | str | - | - |

**Returns**: (none)



### decoder_compat(b)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| b | None | - | - |

**Returns**: (none)


