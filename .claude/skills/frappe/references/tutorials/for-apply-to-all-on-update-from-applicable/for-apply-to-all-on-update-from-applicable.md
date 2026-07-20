# How To: For Apply To All On Update From Applicable

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Update User Permission from some to all applicable Doctypes

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.doctype.user_permission.user_permission`
- `frappe.permissions`
- `frappe.tests`
- `frappe.tests.test_helpers`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.doctype.session_default_settings.session_default_settings`

**Setup Required:**
```python
test_users = ('test_bulk_creation_update@example.com', 'test_user_perm1@example.com', 'nested_doc_user@example.com')
frappe.db.delete('User Permission', {'user': ('in', test_users)})
frappe.delete_doc_if_exists('DocType', 'Person')
frappe.db.sql_ddl('DROP TABLE IF EXISTS `tabPerson`')
frappe.delete_doc_if_exists('DocType', 'Doc A')
frappe.db.sql_ddl('DROP TABLE IF EXISTS `tabDoc A`')
setup_for_tests()
```

## Step-by-Step Guide

### Step 1: 'Update User Permission from some to all applicable Doctypes'

```python
'Update User Permission from some to all applicable Doctypes'
```

### Step 2: Assign user = create_user(...)

```python
user = create_user('test_bulk_creation_update@example.com')
```

### Step 3: Assign param = get_params(...)

```python
param = get_params(user, 'User', user.name)
```

### Step 4: Assign is_created = add_user_permissions(...)

```python
is_created = add_user_permissions(get_params(user, 'User', user.name, applicable=['Comment', 'Contact']))
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(is_created, 1)
```

### Step 6: Assign is_created = add_user_permissions(...)

```python
is_created = add_user_permissions(param)
```

### Step 7: Assign is_created_apply_to_all = frappe.db.exists(...)

```python
is_created_apply_to_all = frappe.db.exists('User Permission', get_exists_param(user))
```

### Step 8: Assign removed_applicable_first = frappe.db.exists(...)

```python
removed_applicable_first = frappe.db.exists('User Permission', get_exists_param(user, applicable='Comment'))
```

### Step 9: Assign removed_applicable_second = frappe.db.exists(...)

```python
removed_applicable_second = frappe.db.exists('User Permission', get_exists_param(user, applicable='Contact'))
```

### Step 10: Call self.assertIsNotNone()

```python
self.assertIsNotNone(is_created_apply_to_all)
```

### Step 11: Call self.assertIsNone()

```python
self.assertIsNone(removed_applicable_first)
```

### Step 12: Call self.assertIsNone()

```python
self.assertIsNone(removed_applicable_second)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(is_created, 1)
```


## Complete Example

```python
# Setup
test_users = ('test_bulk_creation_update@example.com', 'test_user_perm1@example.com', 'nested_doc_user@example.com')
frappe.db.delete('User Permission', {'user': ('in', test_users)})
frappe.delete_doc_if_exists('DocType', 'Person')
frappe.db.sql_ddl('DROP TABLE IF EXISTS `tabPerson`')
frappe.delete_doc_if_exists('DocType', 'Doc A')
frappe.db.sql_ddl('DROP TABLE IF EXISTS `tabDoc A`')
setup_for_tests()

# Workflow
'Update User Permission from some to all applicable Doctypes'
user = create_user('test_bulk_creation_update@example.com')
param = get_params(user, 'User', user.name)
is_created = add_user_permissions(get_params(user, 'User', user.name, applicable=['Comment', 'Contact']))
self.assertEqual(is_created, 1)
is_created = add_user_permissions(param)
is_created_apply_to_all = frappe.db.exists('User Permission', get_exists_param(user))
removed_applicable_first = frappe.db.exists('User Permission', get_exists_param(user, applicable='Comment'))
removed_applicable_second = frappe.db.exists('User Permission', get_exists_param(user, applicable='Contact'))
self.assertIsNotNone(is_created_apply_to_all)
self.assertIsNone(removed_applicable_first)
self.assertIsNone(removed_applicable_second)
self.assertEqual(is_created, 1)
```

## Next Steps


---

*Source: test_user_permission.py:117 | Complexity: Advanced | Last updated: 2026-02-04*