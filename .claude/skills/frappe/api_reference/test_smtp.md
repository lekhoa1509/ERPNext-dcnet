# API Reference: test_smtp.py

**Language**: Python

**Source**: `email/test_smtp.py`

---

## Classes

### TestSMTP

**Inherits from**: IntegrationTestCase

#### Methods

##### test_smtp_ssl_session(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_smtp_tls_session(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_email_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_email_account(email_id, password, enable_outgoing, default_outgoing = 0, append_to = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email_id | None | - | - |
| password | None | - | - |
| enable_outgoing | None | - | - |
| default_outgoing | None | 0 | - |
| append_to | None | None | - |

**Returns**: (none)



### make_server(port, ssl, tls)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| port | None | - | - |
| ssl | None | - | - |
| tls | None | - | - |

**Returns**: (none)


