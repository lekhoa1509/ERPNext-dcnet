# API Reference: smtp.py

**Language**: Python

**Source**: `email/smtp.py`

---

## Classes

### InvalidEmailCredentials

**Inherits from**: frappe.ValidationError



### SMTPServer

**Inherits from**: (none)

#### Methods

##### __init__(self, server, login = None, email_account = None, password = None, port = None, use_tls = None, use_ssl = None, use_oauth = 0, access_token = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| server | None | - | - |
| login | None | None | - |
| email_account | None | None | - |
| password | None | None | - |
| port | None | None | - |
| use_tls | None | None | - |
| use_ssl | None | None | - |
| use_oauth | None | 0 | - |
| access_token | None | None | - |


##### port(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### server(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### secure_session(self, conn)

Secure the connection incase of TLS.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| conn | None | - | - |


##### session(self)

Get SMTP session.

We make best effort to revive connection if it's disconnected by checking the connection
health before returning it to user.

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _enqueue_connection_closure(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_session_active(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### quit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### throw_invalid_credentials_exception(cls, email_account = None)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| email_account | None | None | - |



