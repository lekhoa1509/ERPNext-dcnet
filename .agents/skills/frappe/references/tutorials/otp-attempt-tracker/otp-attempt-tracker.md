# How To: Otp Attempt Tracker

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Check that OTP login attempts are tracked.

## Prerequisites

**Required Modules:**
- `datetime`
- `time`
- `pyotp`
- `frappe`
- `frappe.auth`
- `frappe.tests`
- `frappe.twofactor`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: 'Check that OTP login attempts are tracked.'

```python
'Check that OTP login attempts are tracked.'
```

### Step 2: Call authenticate_for_2factor()

```python
authenticate_for_2factor(self.user)
```

### Step 3: Assign tmp_id = value

```python
tmp_id = frappe.local.response['tmp_id']
```

### Step 4: Assign otp = 'wrongotp'

```python
otp = 'wrongotp'
```

### Step 5: Assign tracker = get_login_attempt_tracker(...)

```python
tracker = get_login_attempt_tracker(self.user, raise_locked_exception=False)
```

### Step 6: Call tracker.add_success_attempt()

```python
tracker.add_success_attempt()
```

### Step 7: Call confirm_otp_token()

```python
confirm_otp_token(self.login_manager, otp=otp, tmp_id=tmp_id)
```

### Step 8: Call confirm_otp_token()

```python
confirm_otp_token(self.login_manager, otp=otp, tmp_id=tmp_id)
```

### Step 9: Call confirm_otp_token()

```python
confirm_otp_token(self.login_manager, otp=otp, tmp_id=tmp_id)
```

### Step 10: Call confirm_otp_token()

```python
confirm_otp_token(self.login_manager, otp=otp, tmp_id=tmp_id)
```

### Step 11: Assign otp = get_otp(...)

```python
otp = get_otp(self.user)
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue(confirm_otp_token(self.login_manager, otp=otp, tmp_id=tmp_id))
```


## Complete Example

```python
# Workflow
'Check that OTP login attempts are tracked.'
authenticate_for_2factor(self.user)
tmp_id = frappe.local.response['tmp_id']
otp = 'wrongotp'
with self.assertRaises(frappe.AuthenticationError):
    confirm_otp_token(self.login_manager, otp=otp, tmp_id=tmp_id)
with self.assertRaises(frappe.AuthenticationError):
    confirm_otp_token(self.login_manager, otp=otp, tmp_id=tmp_id)
with self.assertRaises(frappe.AuthenticationError):
    confirm_otp_token(self.login_manager, otp=otp, tmp_id=tmp_id)
with self.assertRaises(frappe.SecurityException):
    confirm_otp_token(self.login_manager, otp=otp, tmp_id=tmp_id)
tracker = get_login_attempt_tracker(self.user, raise_locked_exception=False)
tracker.add_success_attempt()
with self.freeze_time(datetime.datetime.now()):
    otp = get_otp(self.user)
    self.assertTrue(confirm_otp_token(self.login_manager, otp=otp, tmp_id=tmp_id))
```

## Next Steps


---

*Source: test_twofactor.py:171 | Complexity: Advanced | Last updated: 2026-02-04*