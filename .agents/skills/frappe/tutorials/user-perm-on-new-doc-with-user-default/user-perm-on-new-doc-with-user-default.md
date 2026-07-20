# How To: User Perm On New Doc With User Default

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test User Perm impact on frappe.new_doc. with *user* default value

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

### Step 1: 'Test User Perm impact on frappe.new_doc. with *user* default value'

```python
'Test User Perm impact on frappe.new_doc. with *user* default value'
```

### Step 2: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 3: Assign user = create_user(...)

```python
user = create_user('user_default_test@example.com', 'Blogger')
```

### Step 4: Call add_user_permissions()

```python
add_user_permissions(get_params(user, 'DocType', 'ToDo', applicable=['Assignment Rule']))
```

### Step 5: Call frappe.set_user()

```python
frappe.set_user('user_default_test@example.com')
```

### Step 6: Call set_session_default_values()

```python
set_session_default_values({'doc': 'ToDo'})
```

### Step 7: Assign new_doc = frappe.new_doc(...)

```python
new_doc = frappe.new_doc('Doc A')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(new_doc.doc, 'ToDo')
```

### Step 9: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 10: Call clear_session_defaults()

```python
clear_session_defaults()
```

### Step 11: Call remove_applicable()

```python
remove_applicable(['Assignment Rule'], 'user_default_test@example.com', 'DocType', 'ToDo')
```

### Step 12: Assign doc = new_doctype(...)

```python
doc = new_doctype('Doc A', fields=[{'label': 'DocType', 'fieldname': 'doc', 'fieldtype': 'Link', 'options': 'DocType'}], unique=0)
```

### Step 13: Call doc.insert()

```python
doc.insert()
```

### Step 14: Assign settings = frappe.get_single(...)

```python
settings = frappe.get_single('Session Default Settings')
```

### Step 15: Call settings.append()

```python
settings.append('session_defaults', {'ref_doctype': 'DocType'})
```

### Step 16: Call settings.save()

```python
settings.save()
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
'Test User Perm impact on frappe.new_doc. with *user* default value'
from frappe.core.doctype.session_default_settings.session_default_settings import clear_session_defaults, set_session_default_values
frappe.set_user('Administrator')
user = create_user('user_default_test@example.com', 'Blogger')
if not frappe.db.exists('DocType', 'Doc A'):
    doc = new_doctype('Doc A', fields=[{'label': 'DocType', 'fieldname': 'doc', 'fieldtype': 'Link', 'options': 'DocType'}], unique=0)
    doc.insert()
if not frappe.db.exists('Session Default', {'ref_doctype': 'DocType'}):
    settings = frappe.get_single('Session Default Settings')
    settings.append('session_defaults', {'ref_doctype': 'DocType'})
    settings.save()
add_user_permissions(get_params(user, 'DocType', 'ToDo', applicable=['Assignment Rule']))
frappe.set_user('user_default_test@example.com')
set_session_default_values({'doc': 'ToDo'})
new_doc = frappe.new_doc('Doc A')
self.assertEqual(new_doc.doc, 'ToDo')
frappe.set_user('Administrator')
clear_session_defaults()
remove_applicable(['Assignment Rule'], 'user_default_test@example.com', 'DocType', 'ToDo')
```

## Next Steps


---

*Source: test_user_permission.py:239 | Complexity: Advanced | Last updated: 2026-02-04*