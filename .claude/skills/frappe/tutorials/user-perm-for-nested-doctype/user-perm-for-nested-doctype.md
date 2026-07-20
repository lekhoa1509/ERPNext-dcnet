# How To: User Perm For Nested Doctype

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test if descendants' visibility is controlled for a nested DocType.

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

### Step 1: "Test if descendants' visibility is controlled for a nested DocType."

```python
"Test if descendants' visibility is controlled for a nested DocType."
```

### Step 2: Assign user = create_user(...)

```python
user = create_user('nested_doc_user@example.com', 'Blogger')
```

### Step 3: Assign parent_record = frappe.get_doc.insert(...)

```python
parent_record = frappe.get_doc({'doctype': 'Person', 'person_name': 'Parent', 'is_group': 1}).insert()
```

### Step 4: Assign child_record = frappe.get_doc.insert(...)

```python
child_record = frappe.get_doc({'doctype': 'Person', 'person_name': 'Child', 'is_group': 0, 'parent_person': parent_record.name}).insert()
```

### Step 5: Call add_user_permissions()

```python
add_user_permissions(get_params(user, 'Person', parent_record.name))
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(has_user_permission(frappe.get_doc('Person', parent_record.name), user.name))
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(has_user_permission(frappe.get_doc('Person', child_record.name), user.name))
```

### Step 8: Call add_permission()

```python
add_permission('Person', 'Blogger')
```

### Step 9: Call frappe.set_user()

```python
frappe.set_user(user.name)
```

### Step 10: Assign visible_names = frappe.get_list(...)

```python
visible_names = frappe.get_list(doctype='Person', pluck='person_name')
```

### Step 11: Assign user_permission = frappe.get_doc(...)

```python
user_permission = frappe.get_doc('User Permission', {'allow': 'Person', 'for_value': parent_record.name})
```

### Step 12: Assign user_permission.hide_descendants = 1

```python
user_permission.hide_descendants = 1
```

### Step 13: Call user_permission.save()

```python
user_permission.save(ignore_permissions=True)
```

### Step 14: Call self.assertTrue()

```python
self.assertTrue(has_user_permission(frappe.get_doc('Person', parent_record.name), user.name))
```

### Step 15: Call self.assertFalse()

```python
self.assertFalse(has_user_permission(frappe.get_doc('Person', child_record.name), user.name))
```

### Step 16: Assign visible_names_after_hide_descendants = frappe.get_list(...)

```python
visible_names_after_hide_descendants = frappe.get_list('Person', pluck='person_name')
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(visible_names, ['Child', 'Parent'])
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(visible_names_after_hide_descendants, ['Parent'])
```

### Step 19: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 20: Assign doc = new_doctype(...)

```python
doc = new_doctype('Person', fields=[{'label': 'Person Name', 'fieldname': 'person_name', 'fieldtype': 'Data'}], unique=0)
```

### Step 21: Assign doc.is_tree = 1

```python
doc.is_tree = 1
```

### Step 22: Call doc.insert()

```python
doc.insert()
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
"Test if descendants' visibility is controlled for a nested DocType."
from frappe.core.doctype.doctype.test_doctype import new_doctype
user = create_user('nested_doc_user@example.com', 'Blogger')
if not frappe.db.exists('DocType', 'Person'):
    doc = new_doctype('Person', fields=[{'label': 'Person Name', 'fieldname': 'person_name', 'fieldtype': 'Data'}], unique=0)
    doc.is_tree = 1
    doc.insert()
parent_record = frappe.get_doc({'doctype': 'Person', 'person_name': 'Parent', 'is_group': 1}).insert()
child_record = frappe.get_doc({'doctype': 'Person', 'person_name': 'Child', 'is_group': 0, 'parent_person': parent_record.name}).insert()
add_user_permissions(get_params(user, 'Person', parent_record.name))
self.assertTrue(has_user_permission(frappe.get_doc('Person', parent_record.name), user.name))
self.assertTrue(has_user_permission(frappe.get_doc('Person', child_record.name), user.name))
add_permission('Person', 'Blogger')
frappe.set_user(user.name)
visible_names = frappe.get_list(doctype='Person', pluck='person_name')
user_permission = frappe.get_doc('User Permission', {'allow': 'Person', 'for_value': parent_record.name})
user_permission.hide_descendants = 1
user_permission.save(ignore_permissions=True)
self.assertTrue(has_user_permission(frappe.get_doc('Person', parent_record.name), user.name))
self.assertFalse(has_user_permission(frappe.get_doc('Person', child_record.name), user.name))
visible_names_after_hide_descendants = frappe.get_list('Person', pluck='person_name')
self.assertEqual(visible_names, ['Child', 'Parent'])
self.assertEqual(visible_names_after_hide_descendants, ['Parent'])
frappe.set_user('Administrator')
```

## Next Steps


---

*Source: test_user_permission.py:146 | Complexity: Advanced | Last updated: 2026-02-04*