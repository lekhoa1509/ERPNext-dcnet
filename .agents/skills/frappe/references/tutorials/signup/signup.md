# How To: Signup

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test signup

## Prerequisites

**Required Modules:**
- `json`
- `time`
- `contextlib`
- `unittest.mock`
- `urllib.parse`
- `werkzeug.http`
- `frappe`
- `frappe.exceptions`
- `frappe.core.doctype.user.user`
- `frappe.desk.notifications`
- `frappe.frappeclient`
- `frappe.model.delete_doc`
- `frappe.tests`
- `frappe.tests.classes.context_managers`
- `frappe.tests.test_api`
- `frappe.tests.utils`
- `frappe.utils`
- `frappe.www.login`
- `frappe.website.utils`
- `frappe.auth`
- `frappe.utils`
- `frappe.desk.form.load`
- `frappe.utils.modules`


## Step-by-Step Guide

### Step 1: Assign random_user = frappe.mock(...)

```python
random_user = frappe.mock('email')
```

### Step 2: Assign random_user_name = frappe.mock(...)

```python
random_user_name = frappe.mock('name')
```

### Step 3: Call self.assertTupleEqual()

```python
self.assertTupleEqual(sign_up(random_user, random_user_name, '/welcome'), (1, 'Please check your email for verification'))
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(frappe.cache.hget('redirect_after_login', random_user), sanitize_redirect('/welcome'))
```

### Step 5: Call self.assertTupleEqual()

```python
self.assertTupleEqual(sign_up(random_user, random_user_name, '/welcome'), (0, 'Already Registered'))
```

### Step 6: Assign user = frappe.get_doc(...)

```python
user = frappe.get_doc('User', random_user)
```

### Step 7: Assign user.enabled = 0

```python
user.enabled = 0
```

### Step 8: Call user.save()

```python
user.save()
```

### Step 9: Call self.assertTupleEqual()

```python
self.assertTupleEqual(sign_up(random_user, random_user_name, '/welcome'), (0, 'Registered but disabled'))
```

### Step 10: Call self.assertRaisesRegex()

```python
self.assertRaisesRegex(frappe.exceptions.ValidationError, 'Sign Up is disabled', sign_up, random_user, random_user_name, '/signup')
```

### Step 11: Call self.assertRaisesRegex()

```python
self.assertRaisesRegex(frappe.exceptions.ValidationError, 'Throttled', sign_up, frappe.mock('email'), random_user_name, '/signup')
```


## Complete Example

```python
# Workflow
import frappe.website.utils
random_user = frappe.mock('email')
random_user_name = frappe.mock('name')
with patch.object(user_module, 'is_signup_disabled', return_value=True):
    self.assertRaisesRegex(frappe.exceptions.ValidationError, 'Sign Up is disabled', sign_up, random_user, random_user_name, '/signup')
self.assertTupleEqual(sign_up(random_user, random_user_name, '/welcome'), (1, 'Please check your email for verification'))
self.assertEqual(frappe.cache.hget('redirect_after_login', random_user), sanitize_redirect('/welcome'))
self.assertTupleEqual(sign_up(random_user, random_user_name, '/welcome'), (0, 'Already Registered'))
user = frappe.get_doc('User', random_user)
user.enabled = 0
user.save()
self.assertTupleEqual(sign_up(random_user, random_user_name, '/welcome'), (0, 'Registered but disabled'))
with patch.object(user_module.frappe.db, 'get_creation_count', return_value=301):
    self.assertRaisesRegex(frappe.exceptions.ValidationError, 'Throttled', sign_up, frappe.mock('email'), random_user_name, '/signup')
```

## Next Steps


---

*Source: test_user.py:317 | Complexity: Advanced | Last updated: 2026-02-04*