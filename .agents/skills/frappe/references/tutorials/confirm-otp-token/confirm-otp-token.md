# How To: Confirm Otp Token

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Ensure otp is confirmed

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

### Step 1: 'Ensure otp is confirmed'

```python
'Ensure otp is confirmed'
```

### Step 2: Assign frappe.flags.otp_expiry = 2

```python
frappe.flags.otp_expiry = 2
```

### Step 3: Call authenticate_for_2factor()

```python
authenticate_for_2factor(self.user)
```

### Step 4: Assign tmp_id = value

```python
tmp_id = frappe.local.response['tmp_id']
```

### Step 5: Assign otp = 'wrongotp'

```python
otp = 'wrongotp'
```

### Step 6: Assign frappe.flags.otp_expiry = None

```python
frappe.flags.otp_expiry = None
```

### Step 7: Call print()

```python
print('Sleeping for 2 secs to confirm token expires..')
```

### Step 8: Call time.sleep()

```python
time.sleep(2)
```

### Step 9: Call confirm_otp_token()

```python
confirm_otp_token(self.login_manager, otp=otp, tmp_id=tmp_id)
```

### Step 10: Assign otp = get_otp(...)

```python
otp = get_otp(self.user)
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(confirm_otp_token(self.login_manager, otp=otp, tmp_id=tmp_id))
```

### Step 12: Call confirm_otp_token()

```python
confirm_otp_token(self.login_manager, otp=otp, tmp_id=tmp_id)
```


## Complete Example

```python
# Workflow
'Ensure otp is confirmed'
frappe.flags.otp_expiry = 2
authenticate_for_2factor(self.user)
tmp_id = frappe.local.response['tmp_id']
otp = 'wrongotp'
with self.assertRaises(frappe.AuthenticationError):
    confirm_otp_token(self.login_manager, otp=otp, tmp_id=tmp_id)
with self.freeze_time(datetime.datetime.now()):
    otp = get_otp(self.user)
    self.assertTrue(confirm_otp_token(self.login_manager, otp=otp, tmp_id=tmp_id))
frappe.flags.otp_expiry = None
print('Sleeping for 2 secs to confirm token expires..')
time.sleep(2)
with self.assertRaises(ExpiredLoginException):
    confirm_otp_token(self.login_manager, otp=otp, tmp_id=tmp_id)
```

## Next Steps


---

*Source: test_twofactor.py:111 | Complexity: Advanced | Last updated: 2026-02-04*