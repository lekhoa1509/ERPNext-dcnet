# How To: Login With Email Link

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test login with email link

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

### Step 1: Assign user = value

```python
user = self.test_user_email
```

### Step 2: Assign res = requests.get(...)

```python
res = requests.get(_generate_temporary_login_link(user, 10))
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(res.status_code, 200)
```

### Step 4: Call self.assertTrue()

```python
self.assertTrue(res.cookies.get('sid'))
```

### Step 5: Call self.assertNotEqual()

```python
self.assertNotEqual(res.cookies.get('sid'), 'Guest')
```

### Step 6: Assign res = requests.get(...)

```python
res = requests.get(_generate_temporary_login_link(user, 10) + 'aa')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(res.cookies.get('sid'), 'Guest')
```

### Step 8: Assign res = requests.post(...)

```python
res = requests.post(_generate_temporary_login_link(user, 10))
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(res.status_code, 403)
```

### Step 10: Assign res = requests.get(...)

```python
res = requests.get(_generate_temporary_login_link(user, 10))
```

### Step 11: Call self.fail()

```python
self.fail('Rate limting not working')
```


## Complete Example

```python
# Workflow
user = self.test_user_email
res = requests.get(_generate_temporary_login_link(user, 10))
self.assertEqual(res.status_code, 200)
self.assertTrue(res.cookies.get('sid'))
self.assertNotEqual(res.cookies.get('sid'), 'Guest')
res = requests.get(_generate_temporary_login_link(user, 10) + 'aa')
self.assertEqual(res.cookies.get('sid'), 'Guest')
res = requests.post(_generate_temporary_login_link(user, 10))
self.assertEqual(res.status_code, 403)
for _ in range(6):
    res = requests.get(_generate_temporary_login_link(user, 10))
    if res.status_code == 429:
        break
else:
    self.fail('Rate limting not working')
```

## Next Steps


---

*Source: test_auth.py:139 | Complexity: Advanced | Last updated: 2026-02-04*