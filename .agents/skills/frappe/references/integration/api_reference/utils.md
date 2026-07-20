# API Reference: utils.py

**Language**: Python

**Source**: `utils.py`

---

## Classes

### OAuth2DynamicClientMetadata

OAuth 2.0 Dynamic Client Registration Metadata.

As defined in RFC7591 - OAuth 2.0 Dynamic Client Registration Protocol
https://datatracker.ietf.org/doc/html/rfc7591#section-2

**Inherits from**: BaseModel



## Functions

### make_request(method: str, url: str, auth = None, headers = None, data = None, json = None, params = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| method | str | - | - |
| url | str | - | - |
| auth | None | None | - |
| headers | None | None | - |
| data | None | None | - |
| json | None | None | - |
| params | None | None | - |

**Returns**: (none)



### make_get_request(url: str)

Make a 'GET' HTTP request to the given `url` and return processed response.

You can optionally pass the below parameters:

* `headers`: Headers to be set in the request.
* `params`: Query parameters to be passed in the request.
* `auth`: Auth credentials.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| url | str | - | - |

**Returns**: (none)



### make_post_request(url: str)

Make a 'POST' HTTP request to the given `url` and return processed response.

You can optionally pass the below parameters:

* `headers`: Headers to be set in the request.
* `data`: Data to be passed in body of the request.
* `json`: JSON to be passed in the request.
* `params`: Query parameters to be passed in the request.
* `auth`: Auth credentials.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| url | str | - | - |

**Returns**: (none)



### make_put_request(url: str)

Make a 'PUT' HTTP request to the given `url` and return processed response.

You can optionally pass the below parameters:

* `headers`: Headers to be set in the request.
* `data`: Data to be passed in body of the request.
* `json`: JSON to be passed in the request.
* `params`: Query parameters to be passed in the request.
* `auth`: Auth credentials.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| url | str | - | - |

**Returns**: (none)



### make_patch_request(url: str)

Make a 'PATCH' HTTP request to the given `url` and return processed response.

You can optionally pass the below parameters:

* `headers`: Headers to be set in the request.
* `data`: Data to be passed in body of the request.
* `json`: JSON to be passed in the request.
* `params`: Query parameters to be passed in the request.
* `auth`: Auth credentials.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| url | str | - | - |

**Returns**: (none)



### make_delete_request(url: str)

Make a 'DELETE' HTTP request to the given `url` and return processed response.

You can optionally pass the below parameters:

* `headers`: Headers to be set in the request.
* `data`: Data to be passed in body of the request.
* `json`: JSON to be passed in the request.
* `params`: Query parameters to be passed in the request.
* `auth`: Auth credentials.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| url | str | - | - |

**Returns**: (none)



### create_request_log(data, integration_type = None, service_name = None, name = None, error = None, request_headers = None, output = None)

DEPRECATED: The parameter integration_type will be removed in the next major release.
Use is_remote_request instead.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| integration_type | None | None | - |
| service_name | None | None | - |
| name | None | None | - |
| error | None | None | - |
| request_headers | None | None | - |
| output | None | None | - |

**Returns**: (none)



### get_json(obj)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| obj | None | - | - |

**Returns**: (none)



### json_handler(obj)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| obj | None | - | - |

**Returns**: (none)



### validate_dynamic_client_metadata(client: OAuth2DynamicClientMetadata)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| client | OAuth2DynamicClientMetadata | - | - |

**Returns**: (none)



### create_new_oauth_client(client: OAuth2DynamicClientMetadata)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| client | OAuth2DynamicClientMetadata | - | - |

**Returns**: (none)



### get_oauth_settings()

Return OAuth settings.

**Returns**: (none)


