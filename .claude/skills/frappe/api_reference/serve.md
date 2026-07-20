# API Reference: serve.py

**Language**: Python

**Source**: `website/serve.py`

---

## Functions

### get_response(path = None, http_status_code = 200) → Response

Resolves path and renders page

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | None | - |
| http_status_code | None | 200 | - |

**Returns**: `Response`



### handle_exception(e, endpoint, path, http_status_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | None | - | - |
| endpoint | None | - | - |
| path | None | - | - |
| http_status_code | None | - | - |

**Returns**: (none)



### get_response_content(path = None, http_status_code = 200) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | None | - |
| http_status_code | None | 200 | - |

**Returns**: `str`



### get_response_without_exception_handling(path = None, http_status_code = 200) → Response

Resolves path and renders page.

Note: This doesn't do any exception handling and assumes you'll implement the exception
handling that's required.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | None | - |
| http_status_code | None | 200 | - |

**Returns**: `Response`


