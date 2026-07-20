# API Reference: frappemail.py

**Language**: Python

**Source**: `email/frappemail.py`

---

## Classes

### FrappeMail

Class to interact with the Frappe Mail API.

**Inherits from**: (none)

#### Methods

##### __init__(self, site: str, email: str, api_key: str | None = None, api_secret: str | None = None, access_token: str | None = None) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| site | str | - | - |
| email | str | - | - |
| api_key | str | None | None | - |
| api_secret | str | None | None | - |
| access_token | str | None | None | - |

**Returns**: `None`


##### get_client(site: str, email: str, api_key: str | None = None, api_secret: str | None = None, access_token: str | None = None) → FrappeClient | FrappeOAuth2Client

Returns a FrappeClient or FrappeOAuth2Client instance.

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | str | - | - |
| email | str | - | - |
| api_key | str | None | None | - |
| api_secret | str | None | None | - |
| access_token | str | None | None | - |

**Returns**: `FrappeClient | FrappeOAuth2Client`


##### request(self, method: str, endpoint: str, params: dict | None = None, data: dict | None = None, json: dict | None = None, files: dict | None = None, headers: dict[str, str] | None = None, timeout: int | tuple[int, int] = (60, 120)) → Any | None

Makes a request to the Frappe Mail API.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| method | str | - | - |
| endpoint | str | - | - |
| params | dict | None | None | - |
| data | dict | None | None | - |
| json | dict | None | None | - |
| files | dict | None | None | - |
| headers | dict[str, str] | None | None | - |
| timeout | int | tuple[int, int] | (60, 120) | - |

**Returns**: `Any | None`


##### validate(self) → None

Validates if the user is allowed to send or receive emails.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### send_raw(self, sender: str, recipients: str | list, message: str | bytes, is_newsletter: bool = False) → None

Sends an email using the Frappe Mail API.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sender | str | - | - |
| recipients | str | list | - | - |
| message | str | bytes | - | - |
| is_newsletter | bool | False | - |

**Returns**: `None`


##### pull_raw(self, mailbox: str = 'inbox', limit: int = 50, last_received_at: str | None = None) → dict[str, str | list[str]]

Pull emails for the account using the Frappe Mail API.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| mailbox | str | 'inbox' | - |
| limit | int | 50 | - |
| last_received_at | str | None | None | - |

**Returns**: `dict[str, str | list[str]]`




## Functions

### add_or_update_tzinfo(date_time: datetime | str, timezone: str | None = None) → str

Adds or updates timezone to the datetime.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date_time | datetime | str | - | - |
| timezone | str | None | None | - |

**Returns**: `str`



### raise_for_status(response: requests.Response) → None

Raises an HTTPError if the response status code indicates an error.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| response | requests.Response | - | - |

**Returns**: `None`


