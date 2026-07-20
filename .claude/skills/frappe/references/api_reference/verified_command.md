# API Reference: verified_command.py

**Language**: Python

**Source**: `utils/verified_command.py`

---

## Functions

### get_signed_params(params)

Sign a url by appending `&_signature=xxxxx` to given params (string or dict).

:param params: String or dict of parameters.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| params | None | - | - |

**Returns**: (none)



### get_secret()

**Returns**: (none)



### verify_request()

Verify if the incoming signed request if it is correct.

**Returns**: (none)



### _sign_message(message: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| message | str | - | - |

**Returns**: `str`



### get_url(cmd, params, nonce = None, secret = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cmd | None | - | - |
| params | None | - | - |
| nonce | None | None | - |
| secret | None | None | - |

**Returns**: (none)



### get_signature(params, nonce, secret = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| params | None | - | - |
| nonce | None | - | - |
| secret | None | None | - |

**Returns**: (none)



### verify_using_doc(doc, signature, cmd)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| signature | None | - | - |
| cmd | None | - | - |

**Returns**: (none)



### get_url_using_doc(doc, cmd)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| cmd | None | - | - |

**Returns**: (none)


