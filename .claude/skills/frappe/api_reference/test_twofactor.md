# API Reference: test_twofactor.py

**Language**: Python

**Source**: `tests/test_twofactor.py`

---

## Classes

### TestTwoFactor

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_should_run_2fa(self)

Should return true if enabled.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_cached_user_pass(self)

Cached data should not contain user and pass before 2fa.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_authenticate_for_2factor(self)

Verification obj and tmp_id should be set in frappe.local.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_two_factor_is_enabled(self)

1. Should return true, if enabled and not bypass_2fa_for_retricted_ip_users
2. Should return false, if not enabled
3. Should return true, if enabled and not bypass_2fa_for_retricted_ip_users and ip in restrict_ip
4. Should return true, if enabled and bypass_2fa_for_retricted_ip_users and not restrict_ip
5. Should return false, if enabled and bypass_2fa_for_retricted_ip_users and ip in restrict_ip

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_two_factor_is_enabled_for_user(self)

Should return true if enabled for user.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_otpsecret_for_user(self)

OTP secret should be set for user.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_confirm_otp_token(self)

Ensure otp is confirmed

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_verification_obj(self)

Confirm verification object is returned.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_render_string_template(self)

String template renders as expected with variables.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bypass_restict_ip(self)

1. Raise error if user not login from one of the restrict_ip, Bypass restrict ip check disabled by default
2. Bypass restrict ip check enabled in System Settings
3. Bypass restrict ip check enabled for User

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_otp_attempt_tracker(self)

Check that OTP login attempts are tracked.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_http_request()

Get http request object.

**Returns**: (none)



### enable_2fa(bypass_two_factor_auth = 0, bypass_restrict_ip_check = 0)

Enable Two factor in system settings.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bypass_two_factor_auth | None | 0 | - |
| bypass_restrict_ip_check | None | 0 | - |

**Returns**: (none)



### disable_2fa()

**Returns**: (none)



### toggle_2fa_all_role(state = None)

Enable or disable 2fa for 'all' role on the system.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| state | None | None | - |

**Returns**: (none)



### get_otp(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)


