# How To: Doc Read Access

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test doc read access

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.core.doctype.doctype.doctype`
- `frappe.model.db_query`
- `frappe.permissions`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign todo1 = create_new_todo(...)

```python
todo1 = create_new_todo('Test1', 'testperm@example.com')
```

### Step 2: Assign test_user = frappe.get_doc(...)

```python
test_user = frappe.get_doc('User', 'test4@example.com')
```

### Step 3: Assign todo2 = create_new_todo(...)

```python
todo2 = create_new_todo('Test2', 'test4@example.com')
```

### Step 4: Call frappe.set_user()

```python
frappe.set_user('test4@example.com')
```

### Step 5: Assign todo3 = create_new_todo(...)

```python
todo3 = create_new_todo('Test3', 'test4@example.com')
```

### Step 6: Call self.assertFalse()

```python
self.assertFalse(todo1.has_permission('read'))
```

### Step 7: Call self.assertFalse()

```python
self.assertFalse(todo1.has_permission('write'))
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(todo2.has_permission('read'))
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(todo2.has_permission('write'))
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(todo3.has_permission('read'))
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(todo3.has_permission('write'))
```

### Step 12: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 13: Call test_user.add_roles()

```python
test_user.add_roles('Website Manager')
```

### Step 14: Call add_permission()

```python
add_permission('ToDo', 'Website Manager')
```

### Step 15: Call frappe.set_user()

```python
frappe.set_user('test4@example.com')
```

### Step 16: Call self.assertTrue()

```python
self.assertTrue(todo1.has_permission('read'))
```

### Step 17: Call self.assertFalse()

```python
self.assertFalse(todo1.has_permission('write'))
```

### Step 18: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 19: Call test_user.remove_roles()

```python
test_user.remove_roles('Website Manager')
```

### Step 20: Call reset_perms()

```python
reset_perms('ToDo')
```

### Step 21: Call clear_permissions_cache()

```python
clear_permissions_cache('ToDo')
```

### Step 22: Call frappe.db.rollback()

```python
frappe.db.rollback()
```


## Complete Example

```python
# Workflow
todo1 = create_new_todo('Test1', 'testperm@example.com')
test_user = frappe.get_doc('User', 'test4@example.com')
todo2 = create_new_todo('Test2', 'test4@example.com')
frappe.set_user('test4@example.com')
todo3 = create_new_todo('Test3', 'test4@example.com')
self.assertFalse(todo1.has_permission('read'))
self.assertFalse(todo1.has_permission('write'))
self.assertTrue(todo2.has_permission('read'))
self.assertTrue(todo2.has_permission('write'))
self.assertTrue(todo3.has_permission('read'))
self.assertTrue(todo3.has_permission('write'))
frappe.set_user('Administrator')
test_user.add_roles('Website Manager')
add_permission('ToDo', 'Website Manager')
frappe.set_user('test4@example.com')
self.assertTrue(todo1.has_permission('read'))
self.assertFalse(todo1.has_permission('write'))
frappe.set_user('Administrator')
test_user.remove_roles('Website Manager')
reset_perms('ToDo')
clear_permissions_cache('ToDo')
frappe.db.rollback()
```

## Next Steps


---

*Source: test_todo.py:70 | Complexity: Advanced | Last updated: 2026-02-04*