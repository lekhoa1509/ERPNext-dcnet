# How To: Fieldlevel Permissions In Load For Child Table

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test fieldlevel permissions in load for child table

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.custom.doctype.property_setter.property_setter`
- `frappe.desk.form.load`
- `frappe.tests`
- `frappe.tests.test_helpers`
- `frappe.utils.file_manager`


## Step-by-Step Guide

### Step 1: Assign contact = frappe.new_doc(...)

```python
contact = frappe.new_doc('Contact')
```

### Step 2: Assign contact.first_name = '_Test Contact 1'

```python
contact.first_name = '_Test Contact 1'
```

### Step 3: Call contact.append()

```python
contact.append('phone_nos', {'phone': '123456'})
```

### Step 4: Call contact.insert()

```python
contact.insert()
```

### Step 5: Assign user = frappe.get_doc(...)

```python
user = frappe.get_doc('User', 'test@example.com')
```

### Step 6: Assign user_roles = frappe.get_roles(...)

```python
user_roles = frappe.get_roles()
```

### Step 7: Call user.remove_roles()

```python
user.remove_roles(*user_roles)
```

### Step 8: Call user.add_roles()

```python
user.add_roles('Accounts User')
```

### Step 9: Call make_property_setter()

```python
make_property_setter('Contact Phone', 'phone', 'permlevel', 1, 'Int')
```

### Step 10: Call reset()

```python
reset('Contact Phone')
```

### Step 11: Call add()

```python
add('Contact', 'Sales User', 1)
```

### Step 12: Call update()

```python
update('Contact', 'Sales User', 1, 'write', 1)
```

### Step 13: Call frappe.set_user()

```python
frappe.set_user(user.name)
```

### Step 14: Assign contact = frappe.get_doc(...)

```python
contact = frappe.get_doc('Contact', '_Test Contact 1')
```

### Step 15: Assign unknown.phone = '654321'

```python
contact.phone_nos[0].phone = '654321'
```

### Step 16: Call contact.save()

```python
contact.save()
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(contact.phone_nos[0].phone, '123456')
```

### Step 18: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 19: Call user.add_roles()

```python
user.add_roles('Sales User')
```

### Step 20: Call frappe.set_user()

```python
frappe.set_user(user.name)
```

### Step 21: Assign unknown.phone = '654321'

```python
contact.phone_nos[0].phone = '654321'
```

### Step 22: Call contact.save()

```python
contact.save()
```

### Step 23: Assign contact = frappe.get_doc(...)

```python
contact = frappe.get_doc('Contact', '_Test Contact 1')
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(contact.phone_nos[0].phone, '654321')
```

### Step 25: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 26: Call user.remove_roles()

```python
user.remove_roles('Accounts User', 'Sales User')
```

### Step 27: Call user.add_roles()

```python
user.add_roles(*user_roles)
```

### Step 28: Call contact.delete()

```python
contact.delete()
```


## Complete Example

```python
# Workflow
contact = frappe.new_doc('Contact')
contact.first_name = '_Test Contact 1'
contact.append('phone_nos', {'phone': '123456'})
contact.insert()
user = frappe.get_doc('User', 'test@example.com')
user_roles = frappe.get_roles()
user.remove_roles(*user_roles)
user.add_roles('Accounts User')
make_property_setter('Contact Phone', 'phone', 'permlevel', 1, 'Int')
reset('Contact Phone')
add('Contact', 'Sales User', 1)
update('Contact', 'Sales User', 1, 'write', 1)
frappe.set_user(user.name)
contact = frappe.get_doc('Contact', '_Test Contact 1')
contact.phone_nos[0].phone = '654321'
contact.save()
self.assertEqual(contact.phone_nos[0].phone, '123456')
frappe.set_user('Administrator')
user.add_roles('Sales User')
frappe.set_user(user.name)
contact.phone_nos[0].phone = '654321'
contact.save()
contact = frappe.get_doc('Contact', '_Test Contact 1')
self.assertEqual(contact.phone_nos[0].phone, '654321')
frappe.set_user('Administrator')
user.remove_roles('Accounts User', 'Sales User')
user.add_roles(*user_roles)
contact.delete()
```

## Next Steps


---

*Source: test_form_load.py:107 | Complexity: Advanced | Last updated: 2026-02-04*