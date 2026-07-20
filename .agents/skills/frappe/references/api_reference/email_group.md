# API Reference: email_group.py

**Language**: Python

**Source**: `email/doctype/email_group/email_group.py`

---

## Classes

### EmailGroup

**Inherits from**: Document

#### Methods

##### onload(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### import_from(self, doctype)

Extract Email Addresses from given doctype and add them to the current list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |


##### update_total_subscribers(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_total_subscribers(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### preview_welcome_url(self, email: str | None = None) → str | None

Get Welcome URL for the email group.

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| email | str | None | None | - |

**Returns**: `str | None`


##### get_welcome_url(self, email: str | None = None) → str | None

Get Welcome URL for the email group.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| email | str | None | None | - |

**Returns**: `str | None`


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### import_from(name, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| doctype | None | - | - |

**Returns**: (none)



### add_subscribers(name, email_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| email_list | None | - | - |

**Returns**: (none)



### send_welcome_email(welcome_email, email, email_group)

Send welcome email for the subscribers of a given email group.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| welcome_email | None | - | - |
| email | None | - | - |
| email_group | None | - | - |

**Returns**: (none)



### add_query_params(url: str, params: dict) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| url | str | - | - |
| params | dict | - | - |

**Returns**: `str`


