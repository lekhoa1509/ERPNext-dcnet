# How To: High Permlevel Validations

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test high permlevel validations

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

### Step 1: Assign user = frappe.get_meta(...)

```python
user = frappe.get_meta('User')
```

### Step 2: Call self.assertTrue()

```python
self.assertTrue('roles' in [d.fieldname for d in user.get_high_permlevel_fields()])
```

### Step 3: Assign me = frappe.get_doc(...)

```python
me = frappe.get_doc('User', 'testperm@example.com')
```

### Step 4: Call me.remove_roles()

```python
me.remove_roles('System Manager')
```

### Step 5: Call frappe.set_user()

```python
frappe.set_user('testperm@example.com')
```

### Step 6: Assign me = frappe.get_doc(...)

```python
me = frappe.get_doc('User', 'testperm@example.com')
```

### Step 7: Call me.add_roles()

```python
me.add_roles('System Manager')
```

### Step 8: Call self.assertFalse()

```python
self.assertFalse('System Manager' in [d.role for d in me.roles])
```

### Step 9: Assign me.flags.ignore_permlevel_for_fields = value

```python
me.flags.ignore_permlevel_for_fields = ['roles']
```

### Step 10: Call me.add_roles()

```python
me.add_roles('System Manager')
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue('System Manager' in [d.role for d in me.get('roles')])
```

### Step 12: Assign me.flags.ignore_permlevel_for_fields = None

```python
me.flags.ignore_permlevel_for_fields = None
```

### Step 13: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 14: Assign me = frappe.get_doc(...)

```python
me = frappe.get_doc('User', 'testperm@example.com')
```

### Step 15: Call me.add_roles()

```python
me.add_roles('System Manager')
```

### Step 16: Call self.assertTrue()

```python
self.assertTrue('System Manager' in [d.role for d in me.get('roles')])
```


## Complete Example

```python
# Workflow
user = frappe.get_meta('User')
self.assertTrue('roles' in [d.fieldname for d in user.get_high_permlevel_fields()])
me = frappe.get_doc('User', 'testperm@example.com')
me.remove_roles('System Manager')
frappe.set_user('testperm@example.com')
me = frappe.get_doc('User', 'testperm@example.com')
me.add_roles('System Manager')
self.assertFalse('System Manager' in [d.role for d in me.roles])
me.flags.ignore_permlevel_for_fields = ['roles']
me.add_roles('System Manager')
self.assertTrue('System Manager' in [d.role for d in me.get('roles')])
me.flags.ignore_permlevel_for_fields = None
frappe.set_user('Administrator')
me = frappe.get_doc('User', 'testperm@example.com')
me.add_roles('System Manager')
self.assertTrue('System Manager' in [d.role for d in me.get('roles')])
```

## Next Steps


---

*Source: test_user.py:124 | Complexity: Advanced | Last updated: 2026-02-04*