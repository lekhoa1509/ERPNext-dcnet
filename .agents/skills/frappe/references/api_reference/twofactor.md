# API Reference: twofactor.py

**Language**: Python

**Source**: `twofactor.py`

---

## Classes

### ExpiredLoginException

**Inherits from**: Exception



## Functions

### get_default(key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | None | - | - |

**Returns**: (none)



### set_default(key, value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | None | - | - |
| value | None | - | - |

**Returns**: (none)



### clear_default(key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | None | - | - |

**Returns**: (none)



### toggle_two_factor_auth(state, roles = None)

Enable or disable 2FA in site_config and roles

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| state | None | - | - |
| roles | None | None | - |

**Returns**: (none)



### two_factor_is_enabled(user = None)

Return True if 2FA is enabled.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | None | - |

**Returns**: (none)



### should_run_2fa(user)

Check if 2fa should run.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### get_cached_user_pass()

Get user and password if set.

**Returns**: (none)



### authenticate_for_2factor(user)

Authenticate two factor for enabled user before login.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### cache_2fa_data(user, token, otp_secret, tmp_id)

Cache and set expiry for data.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |
| token | None | - | - |
| otp_secret | None | - | - |
| tmp_id | None | - | - |

**Returns**: (none)



### two_factor_is_enabled_for_(user)

Check if 2factor is enabled for user.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### get_otpsecret_for_(user)

Set OTP Secret for user even if not set.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### get_verification_method()

**Returns**: (none)



### confirm_otp_token(login_manager, otp = None, tmp_id = None)

Confirm otp matches.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| login_manager | None | - | - |
| otp | None | None | - |
| tmp_id | None | None | - |

**Returns**: (none)



### get_verification_obj(user, token, otp_secret)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |
| token | None | - | - |
| otp_secret | None | - | - |

**Returns**: (none)



### process_2fa_for_sms(user, token, otp_secret)

Process sms method for 2fa.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |
| token | None | - | - |
| otp_secret | None | - | - |

**Returns**: (none)



### process_2fa_for_otp_app(user, otp_secret, otp_issuer)

Process OTP App method for 2fa.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |
| otp_secret | None | - | - |
| otp_issuer | None | - | - |

**Returns**: (none)



### process_2fa_for_email(user, token, otp_secret, otp_issuer, method = 'Email')

Process Email method for 2fa.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |
| token | None | - | - |
| otp_secret | None | - | - |
| otp_issuer | None | - | - |
| method | None | 'Email' | - |

**Returns**: (none)



### get_email_subject_for_2fa(kwargs_dict)

Get email subject for 2fa.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs_dict | None | - | - |

**Returns**: (none)



### get_email_body_for_2fa(kwargs_dict)

Get email body for 2fa.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs_dict | None | - | - |

**Returns**: (none)



### get_email_subject_for_qr_code(kwargs_dict)

Get QRCode email subject.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs_dict | None | - | - |

**Returns**: (none)



### get_email_body_for_qr_code(kwargs_dict)

Get QRCode email body.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs_dict | None | - | - |

**Returns**: (none)



### get_link_for_qrcode(user, totp_uri)

Get link to temporary page showing QRCode.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |
| totp_uri | None | - | - |

**Returns**: (none)



### send_token_via_sms(otpsecret, token = None, phone_no = None)

Send token as sms to user.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| otpsecret | None | - | - |
| token | None | None | - |
| phone_no | None | None | - |

**Returns**: (none)



### get_rendered_otp_message(otp: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| otp | str | - | - |

**Returns**: `str`



### send_token_via_email(user, token, otp_secret, otp_issuer, subject = None, message = None)

Send token to user as email.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |
| token | None | - | - |
| otp_secret | None | - | - |
| otp_issuer | None | - | - |
| subject | None | None | - |
| message | None | None | - |

**Returns**: (none)



### get_qr_svg_code(totp_uri)

Get SVG code to display Qrcode for OTP.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| totp_uri | None | - | - |

**Returns**: (none)



### create_barcode_folder()

Get Barcodes folder.

**Returns**: (none)



### delete_qrimage(user, check_expiry = False)

Delete Qrimage when user logs in.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |
| check_expiry | None | False | - |

**Returns**: (none)



### delete_all_barcodes_for_users()

Task to delete all barcodes for user.

**Returns**: (none)



### should_remove_barcode_image(barcode)

Check if it's time to delete barcode image from server.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| barcode | None | - | - |

**Returns**: (none)



### disable()

**Returns**: (none)



### reset_otp_secret(user: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | str | - | - |

**Returns**: (none)


