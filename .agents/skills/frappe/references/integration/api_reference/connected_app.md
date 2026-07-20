# API Reference: connected_app.py

**Language**: Python

**Source**: `doctype/connected_app/connected_app.py`

---

## Classes

### ConnectedApp

**Inherits from**: Document

#### Methods

##### get_openid_configuration(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_oauth2_session(self, user = None, init = False)

Return an auto-refreshing OAuth2 session which is an extension of a requests.Session()

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | None | None | - |
| init | None | False | - |


##### initiate_web_application_flow(self, user = None, success_uri = None)

Return an authorization URL for the user. Save state in Token Cache.

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | None | None | - |
| success_uri | None | None | - |


##### get_user_token(self, user = None, success_uri = None)

Return an existing user token or initiate a Web Application Flow.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | None | None | - |
| success_uri | None | None | - |


##### get_token_cache(self, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | None | - | - |


##### get_scopes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_query_params(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_active_token(self, user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | None | None | - |


##### get_backend_app_token(self, include_client_id = None)

Get an Access Token for the Cloud-Registered Service Principal

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| include_client_id | None | None | - |




## Functions

### callback(code = None, state = None)

Handle client's code.

Called during the oauthorization flow by the remote oAuth2 server to
transmit a code that can be used by the local server to obtain an access
token.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | None | None | - |
| state | None | None | - |

**Returns**: (none)



### has_token(connected_app, connected_user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| connected_app | None | - | - |
| connected_user | None | None | - |

**Returns**: (none)


