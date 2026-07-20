# API Reference: social_login_key.py

**Language**: Python

**Source**: `integrations/doctype/social_login_key/social_login_key.py`

---

## Classes

### BaseUrlNotSetError

**Inherits from**: frappe.ValidationError



### AuthorizeUrlNotSetError

**Inherits from**: frappe.ValidationError



### AccessTokenUrlNotSetError

**Inherits from**: frappe.ValidationError



### RedirectUrlNotSetError

**Inherits from**: frappe.ValidationError



### ClientIDNotSetError

**Inherits from**: frappe.ValidationError



### ClientSecretNotSetError

**Inherits from**: frappe.ValidationError



### SocialLoginKey

**Inherits from**: Document

#### Methods

##### autoname(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_icon(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_social_login_provider(self, provider, initialize = False)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| provider | None | - | - |
| initialize | None | False | - |




## Functions

### provider_allows_signup(provider: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| provider | str | - | - |

**Returns**: `bool`


