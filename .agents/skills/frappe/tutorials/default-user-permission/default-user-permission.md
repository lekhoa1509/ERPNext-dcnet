# How To: Default User Permission

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test default user permission

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

### Step 1: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 2: Assign user = create_user(...)

```python
user = create_user('test_user_perm1@example.com', 'Website Manager')
```

### Step 3: Assign param = get_params(...)

```python
param = get_params(user, 'Test Blog Category', 'general', is_default=1)
```

### Step 4: Call add_user_permissions()

```python
add_user_permissions(param)
```

### Step 5: Assign param = get_params(...)

```python
param = get_params(user, 'Test Blog Category', 'public')
```

### Step 6: Call add_user_permissions()

```python
add_user_permissions(param)
```

### Step 7: Call frappe.set_user()

```python
frappe.set_user('test_user_perm1@example.com')
```

### Step 8: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc('Test Blog Post')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(doc.blog_category, 'general')
```

### Step 10: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 11: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'Test Blog Category', 'title': category}).insert()
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
frappe.set_user('Administrator')
user = create_user('test_user_perm1@example.com', 'Website Manager')
for category in ['general', 'public']:
    if not frappe.db.exists('Test Blog Category', category):
        frappe.get_doc({'doctype': 'Test Blog Category', 'title': category}).insert()
param = get_params(user, 'Test Blog Category', 'general', is_default=1)
add_user_permissions(param)
param = get_params(user, 'Test Blog Category', 'public')
add_user_permissions(param)
frappe.set_user('test_user_perm1@example.com')
doc = frappe.new_doc('Test Blog Post')
self.assertEqual(doc.blog_category, 'general')
frappe.set_user('Administrator')
```

## Next Steps


---

*Source: test_user_permission.py:49 | Complexity: Advanced | Last updated: 2026-02-04*