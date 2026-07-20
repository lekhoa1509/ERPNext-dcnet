# API Reference: email_domain.py

**Language**: Python

**Source**: `email/doctype/email_domain/email_domain.py`

---

## Classes

### EmailDomain

**Inherits from**: Document

#### Methods

##### validate(self)

Validate POP3/IMAP and SMTP connections.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

update all email accounts using this domain

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_incoming_server_conn(self)

**Decorators**: `@handle_error('incoming')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_outgoing_server_conn(self)

**Decorators**: `@handle_error('outgoing')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_error_message(event)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| event | None | - | - |

**Returns**: (none)



### handle_error(event)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| event | None | - | - |

**Returns**: (none)



### decorator(fn)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fn | None | - | - |

**Returns**: (none)



### wrapper()

**Returns**: (none)


