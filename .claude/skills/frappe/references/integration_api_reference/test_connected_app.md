# API Reference: test_connected_app.py

**Language**: Python

**Source**: `doctype/connected_app/test_connected_app.py`

---

## Classes

### TestConnectedApp

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

Set up a Connected App that connects to our own oAuth provider.

Frappe comes with it's own oAuth2 provider that we can test against. The
client credentials can be obtained from an "OAuth Client". All depends
on "Social Login Key" so we create one as well.

The redirect URIs from "Connected App" and "OAuth Client" have to match.
Frappe's "Authorization URL" and "Access Token URL" (actually they're
just endpoints) are stored in "Social Login Key" so we get them from
there.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_web_application_flow(self)

Simulate a logged in user who opens the authorization URL.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_user(usr, pwd)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| usr | None | - | - |
| pwd | None | - | - |

**Returns**: (none)



### get_connected_app()

**Returns**: (none)



### get_oauth_client()

**Returns**: (none)



### login()

**Returns**: (none)



### delete_if_exists(attribute)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| attribute | None | - | - |

**Returns**: (none)


