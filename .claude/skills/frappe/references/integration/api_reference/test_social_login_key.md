# API Reference: test_social_login_key.py

**Language**: Python

**Source**: `doctype/social_login_key/test_social_login_key.py`

---

## Classes

### TestSocialLoginKey

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### test_adding_frappe_social_login_provider(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_github_login_with_private_email(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_github_login_with_public_email(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_normal_signup_and_github_login(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_force_disabled_signups(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_force_enabled_signups(self)

Social login key can override website settings for disabled signups.

**Decorators**: `@IntegrationTestCase.change_settings('Website Settings', disable_signup=1)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### make_social_login_key()

**Returns**: (none)



### create_or_update_social_login_key()

**Returns**: (none)



### create_github_social_login_key()

**Returns**: (none)



### github_response_for_private_email(url)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| url | None | - | - |

**Returns**: (none)



### github_response_for_public_email(url)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| url | None | - | - |

**Returns**: (none)



### github_response_for_login(url)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| url | None | - | - |

**Returns**: (none)



### github_social_login_setup()

**Returns**: (none)


