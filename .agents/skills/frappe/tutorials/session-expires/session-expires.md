# How To: Session Expires

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test session expires

## Prerequisites

**Required Modules:**
- `datetime`
- `time`
- `requests`
- `werkzeug.test`
- `werkzeug.wrappers`
- `frappe`
- `frappe.auth`
- `frappe.frappeclient`
- `frappe.sessions`
- `frappe.tests`
- `frappe.tests.test_api`
- `frappe.utils`
- `frappe.utils.data`
- `frappe.www.login`


## Step-by-Step Guide

### Step 1: Assign sid = value

```python
sid = self.sid
```

### Step 2: Assign expiry_in = get_expiry_in_seconds(...)

```python
expiry_in = get_expiry_in_seconds()
```

### Step 3: Assign session_created = now(...)

```python
session_created = now()
```

### Step 4: Assign time_of_expiry = add_to_date(...)

```python
time_of_expiry = add_to_date(session_created, seconds=expiry_in * 1.01, as_string=True)
```

### Step 5: Assign seconds_elapsed = value

```python
seconds_elapsed = expiry_in * step / 100
```

### Step 6: Assign time_now = add_to_date(...)

```python
time_now = add_to_date(session_created, seconds=seconds_elapsed, as_string=True)
```

### Step 7: Call self.assertIn()

```python
self.assertIn(sid, get_expired_sessions())
```

### Step 8: Call self.assertFalse()

```python
self.assertFalse(s.get_session_data_from_db())
```

### Step 9: Assign data = s.get_session_data_from_db(...)

```python
data = s.get_session_data_from_db()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(data.user, 'Administrator')
```


## Complete Example

```python
# Workflow
sid = self.sid
s: Session = frappe.local.session_obj
expiry_in = get_expiry_in_seconds()
session_created = now()
for step in range(0, 100, 1):
    seconds_elapsed = expiry_in * step / 100
    time_now = add_to_date(session_created, seconds=seconds_elapsed, as_string=True)
    with self.freeze_time(time_now):
        data = s.get_session_data_from_db()
        self.assertEqual(data.user, 'Administrator')
time_of_expiry = add_to_date(session_created, seconds=expiry_in * 1.01, as_string=True)
with self.freeze_time(time_of_expiry):
    self.assertIn(sid, get_expired_sessions())
    self.assertFalse(s.get_session_data_from_db())
```

## Next Steps


---

*Source: test_auth.py:257 | Complexity: Advanced | Last updated: 2026-02-04*