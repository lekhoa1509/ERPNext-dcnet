# How To: Child Table Access With Select Permission

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that child table fields are inaccessible if user only has select perm on parent.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `itertools`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.permissions`
- `frappe.query_builder`
- `frappe.query_builder.functions`
- `frappe.tests`
- `frappe.tests.classes.context_managers`
- `frappe.tests.test_db_query`
- `frappe.tests.test_helpers`
- `frappe.tests.test_query_builder`
- `frappe.utils.nestedset`
- `frappe.permissions`
- `frappe.permissions`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.desk.doctype.dashboard_settings.dashboard_settings`
- `frappe.share`
- `frappe.share`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.share`
- `frappe.permissions`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.permissions`
- `frappe.database.query`

**Setup Required:**
```python
setup_for_tests()
```

## Step-by-Step Guide

### Step 1: 'Test that child table fields are inaccessible if user only has select perm on parent.'

```python
'Test that child table fields are inaccessible if user only has select perm on parent.'
```

### Step 2: Assign test_role = 'Select Note Test Role'

```python
test_role = 'Select Note Test Role'
```

### Step 3: Assign test_user_email = 'test2@example.com'

```python
test_user_email = 'test2@example.com'
```

### Step 4: Assign test_note_title = 'Child Select Test Note'

```python
test_note_title = 'Child Select Test Note'
```

### Step 5: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 6: Assign test_user = frappe.get_doc(...)

```python
test_user = frappe.get_doc('User', test_user_email)
```

### Step 7: Call test_user.remove_roles()

```python
test_user.remove_roles(test_role)
```

### Step 8: Call frappe.delete_doc()

```python
frappe.delete_doc('Role', test_role, ignore_missing=True, force=True)
```

### Step 9: Call frappe.delete_doc()

```python
frappe.delete_doc('Note', {'title': test_note_title}, ignore_missing=True, force=True)
```

### Step 10: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'Role', 'role_name': test_role}).insert(ignore_if_duplicate=True)
```

### Step 11: Call add_permission()

```python
add_permission('Note', test_role, 0, ptype='select')
```

### Step 12: Call add_permission()

```python
add_permission('Note Seen By', test_role, 0, ptype='read')
```

### Step 13: Call update_permission_property()

```python
update_permission_property('Note', test_role, 0, 'read', 0, validate=False)
```

### Step 14: Call test_user.add_roles()

```python
test_user.add_roles(test_role)
```

### Step 15: Assign note = frappe.get_doc.insert(...)

```python
note = frappe.get_doc(doctype='Note', title=test_note_title, public=1, seen_by=[{'user': 'Administrator'}]).insert(ignore_permissions=True)
```

### Step 16: Call frappe.set_user()

```python
frappe.set_user(test_user_email)
```

### Step 17: Assign query = frappe.qb.get_query(...)

```python
query = frappe.qb.get_query('Note', filters={'name': note.name}, fields=['name', {'seen_by': ['user']}], ignore_permissions=False)
```

### Step 18: Assign result = query.run(...)

```python
result = query.run(as_dict=True)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(len(result), 1, 'Should find the note record')
```

### Step 20: Call self.assertIn()

```python
self.assertIn('name', result[0], "Parent field 'name' should be accessible")
```

### Step 21: Call self.assertNotIn()

```python
self.assertNotIn('seen_by', result[0], "Child table field 'seen_by' should NOT be accessible with only 'select' on parent")
```

### Step 22: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 23: Call note.delete()

```python
note.delete(ignore_permissions=True)
```

### Step 24: Call test_user.remove_roles()

```python
test_user.remove_roles(test_role)
```

### Step 25: Call frappe.delete_doc()

```python
frappe.delete_doc('Role', test_role, force=True)
```


## Complete Example

```python
# Setup
setup_for_tests()

# Workflow
'Test that child table fields are inaccessible if user only has select perm on parent.'
test_role = 'Select Note Test Role'
test_user_email = 'test2@example.com'
test_note_title = 'Child Select Test Note'
frappe.set_user('Administrator')
test_user = frappe.get_doc('User', test_user_email)
test_user.remove_roles(test_role)
frappe.delete_doc('Role', test_role, ignore_missing=True, force=True)
frappe.delete_doc('Note', {'title': test_note_title}, ignore_missing=True, force=True)
frappe.get_doc({'doctype': 'Role', 'role_name': test_role}).insert(ignore_if_duplicate=True)
add_permission('Note', test_role, 0, ptype='select')
add_permission('Note Seen By', test_role, 0, ptype='read')
update_permission_property('Note', test_role, 0, 'read', 0, validate=False)
test_user.add_roles(test_role)
note = frappe.get_doc(doctype='Note', title=test_note_title, public=1, seen_by=[{'user': 'Administrator'}]).insert(ignore_permissions=True)
frappe.set_user(test_user_email)
query = frappe.qb.get_query('Note', filters={'name': note.name}, fields=['name', {'seen_by': ['user']}], ignore_permissions=False)
result = query.run(as_dict=True)
self.assertEqual(len(result), 1, 'Should find the note record')
self.assertIn('name', result[0], "Parent field 'name' should be accessible")
self.assertNotIn('seen_by', result[0], "Child table field 'seen_by' should NOT be accessible with only 'select' on parent")
frappe.set_user('Administrator')
note.delete(ignore_permissions=True)
test_user.remove_roles(test_role)
frappe.delete_doc('Role', test_role, force=True)
```

## Next Steps


---

*Source: test_query.py:934 | Complexity: Advanced | Last updated: 2026-02-04*