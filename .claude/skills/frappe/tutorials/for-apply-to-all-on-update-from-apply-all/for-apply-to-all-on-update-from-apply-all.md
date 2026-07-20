# How To: For Apply To All On Update From Apply All

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test for apply to all on update from apply all

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

### Step 1: Assign user = create_user(...)

```python
user = create_user('test_bulk_creation_update@example.com')
```

### Step 2: Assign param = get_params(...)

```python
param = get_params(user, 'User', user.name)
```

### Step 3: Assign is_created = add_user_permissions(...)

```python
is_created = add_user_permissions(param)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(is_created, 1)
```

### Step 5: Assign is_created = add_user_permissions(...)

```python
is_created = add_user_permissions(param)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(is_created, 0)
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
user = create_user('test_bulk_creation_update@example.com')
param = get_params(user, 'User', user.name)
is_created = add_user_permissions(param)
self.assertEqual(is_created, 1)
is_created = add_user_permissions(param)
self.assertEqual(is_created, 0)
```

## Next Steps


---

*Source: test_user_permission.py:75 | Complexity: Intermediate | Last updated: 2026-02-04*