# API Reference: oauth2.py

**Language**: Python

**Source**: `oauth2.py`

---

## Functions

### get_oauth_server()

**Returns**: (none)



### sanitize_kwargs(param_kwargs)

Remove 'data' and 'cmd' keys, if present.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| param_kwargs | None | - | - |

**Returns**: (none)



### encode_params(params)

Encode a dict of params into a query string.

Use `quote_via=urllib.parse.quote` so that whitespaces will be encoded as
`%20` instead of as `+`. This is needed because oauthlib cannot handle `+`
as a whitespace.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| params | None | - | - |

**Returns**: (none)



### approve()

**Returns**: (none)



### authorize()

**Returns**: (none)



### get_token()

**Returns**: (none)



### revoke_token()

**Returns**: (none)



### openid_profile()

**Returns**: (none)



### get_openid_configuration()

**Returns**: (none)



### introspect_token(token: str, token_type_hint = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| token | str | - | - |
| token_type_hint | None | None | - |

**Returns**: (none)



### handle_wellknown(path: str)

Path handler for GET requests to /.well-known/ endpoints. Invoked in app.py

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | str | - | - |

**Returns**: (none)



### get_authorization_server_metadata()

Creates response for the /.well-known/oauth-authorization-server endpoint.

Reference: https://datatracker.ietf.org/doc/html/rfc8414

**Returns**: (none)



### _get_authorization_server_metadata()

Responds with the authorization server metadata.

Reference: https://datatracker.ietf.org/doc/html/rfc8414#section-2

Note:
        Value for response_types_supported does not include token because, PKCE
        token flow is not supported. Responding with token in the redirect URL
        is an unsafe practice, so code is the only supported response type.

**Returns**: (none)



### register_client()

Registers an OAuth client.

Reference: https://datatracker.ietf.org/doc/html/rfc7591

**Returns**: (none)



### get_protected_resource_metadata()

Creates response for the /.well-known/oauth-protected-resource endpoint.

Reference: https://datatracker.ietf.org/doc/html/rfc9728

**Returns**: (none)



### _get_protected_resource_metadata()

**Returns**: (none)



### is_oauth_metadata_enabled(label: Literal['resource', 'auth_server'])

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| label | Literal['resource', 'auth_server'] | - | - |

**Returns**: (none)



### get_resource_url()

Uses request URL to reflect the resource URL

**Returns**: (none)



### _del_none_values(d: dict)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | dict | - | - |

**Returns**: (none)



### set_cors_for_privileged_requests()

Called in before_request hook, prevents failure of privileged requests,
for OPTIONS and:
1. GET requests on /.well-known/
2. POST requests on /api/method/frappe.integrations.oauth2.register_client

Point 2. also depends on OAuth Settings for dynamic client registration.
Without these, registration requests from public clients will fail due to
preflight requests failing.

**Returns**: (none)



### _set_allowed_cors()

**Returns**: (none)


