# API Reference: test_auth.py

**Language**: Python

**Source**: `tests/test_auth.py`

---

## Classes

### TestAuth

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### tearDownClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### set_system_settings(self, k, v)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| k | None | - | - |
| v | None | - | - |


##### test_allow_login_using_mobile(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_allow_login_using_only_email(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_allow_login_using_username(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_allow_login_using_username_and_mobile(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_deny_multiple_login(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_disable_user_pass_login(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_login_with_email_link(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_correct_cookie_expiry_set(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestAllowedReferrer

**Inherits from**: UnitTestCase

#### Methods

##### test_is_allowed_referrer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestLoginAttemptTracker

**Inherits from**: IntegrationTestCase

#### Methods

##### test_account_lock(self)

Make sure that account locks after `n consecutive failures

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_account_unlock(self)

Make sure that locked account gets unlocked after lock_interval of time.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestSessionExpiry

**Inherits from**: FrappeAPITestCase

#### Methods

##### test_session_expires(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### add_user(email, password, username = None, mobile_no = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email | None | - | - |
| password | None | - | - |
| username | None | None | - |
| mobile_no | None | None | - |

**Returns**: (none)



### create_request(headers)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| headers | None | - | - |

**Returns**: (none)


