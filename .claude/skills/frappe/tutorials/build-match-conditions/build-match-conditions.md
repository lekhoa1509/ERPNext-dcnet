# How To: Build Match Conditions

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test build match conditions

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `datetime`
- `contextlib`
- `unittest.mock`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.custom.doctype.property_setter.property_setter`
- `frappe.database.utils`
- `frappe.desk.reportview`
- `frappe.handler`
- `frappe.model.db_query`
- `frappe.permissions`
- `frappe.query_builder`
- `frappe.tests`
- `frappe.tests.test_helpers`
- `frappe.tests.test_query_builder`
- `frappe.utils.testutils`
- `frappe.utils`
- `frappe.desk.search`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.desk.doctype.dashboard_settings.dashboard_settings`
- `frappe.desk.reportview`
- `frappe.desk`
- `frappe.types.filter`

**Setup Required:**
```python
setup_for_tests()
frappe.set_user('Administrator')
```

## Step-by-Step Guide

### Step 1: Call clear_user_permissions_for_doctype()

```python
clear_user_permissions_for_doctype('Test Blog Post', 'test2@example.com')
```

**Verification:**
```python
assertion_string = "(((ifnull(`tabTest Blog Post`.`name`, '')='' or `tabTest Blog Post`.`name` in ('_Test Blog Post 1', '_Test Blog Post'))))"
```

### Step 2: Assign test2user = frappe.get_doc(...)

```python
test2user = frappe.get_doc('User', 'test2@example.com')
```

**Verification:**
```python
assertion_string = "(((ifnull(cast(`tabTest Blog Post`.`name` as varchar), '')='' or cast(`tabTest Blog Post`.`name` as varchar) in ('_Test Blog Post 1', '_Test Blog Post'))))"
```

### Step 3: Call test2user.add_roles()

```python
test2user.add_roles('Blogger')
```

### Step 4: Call frappe.set_user()

```python
frappe.set_user('test2@example.com')
```

### Step 5: Assign build_match_conditions = value

```python
build_match_conditions = DatabaseQuery('Test Blog Post').build_match_conditions
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(build_match_conditions(as_condition=False), [])
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(build_match_conditions(as_condition=True), '')
```

### Step 8: Call add_user_permission()

```python
add_user_permission('Test Blog Post', '_Test Blog Post', 'test2@example.com', True)
```

### Step 9: Call add_user_permission()

```python
add_user_permission('Test Blog Post', '_Test Blog Post 1', 'test2@example.com', True)
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue({'Test Blog Post': ['_Test Blog Post 1', '_Test Blog Post']} in build_match_conditions(as_condition=False))
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(build_match_conditions(as_condition=True), assertion_string)
```

### Step 12: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 13: Assign assertion_string = "(((ifnull(`tabTest Blog Post`.`name`, '')='' or `tabTest Blog Post`.`name` in ('_Test Blog Post 1', '_Test Blog Post'))))"

```python
assertion_string = "(((ifnull(`tabTest Blog Post`.`name`, '')='' or `tabTest Blog Post`.`name` in ('_Test Blog Post 1', '_Test Blog Post'))))"
```

### Step 14: Assign assertion_string = "(((ifnull(cast(`tabTest Blog Post`.`name` as varchar), '')='' or cast(`tabTest Blog Post`.`name` as varchar) in ('_Test Blog Post 1', '_Test Blog Post'))))"

```python
assertion_string = "(((ifnull(cast(`tabTest Blog Post`.`name` as varchar), '')='' or cast(`tabTest Blog Post`.`name` as varchar) in ('_Test Blog Post 1', '_Test Blog Post'))))"
```


## Complete Example

```python
# Setup
setup_for_tests()
frappe.set_user('Administrator')

# Workflow
clear_user_permissions_for_doctype('Test Blog Post', 'test2@example.com')
test2user = frappe.get_doc('User', 'test2@example.com')
test2user.add_roles('Blogger')
frappe.set_user('test2@example.com')
build_match_conditions = DatabaseQuery('Test Blog Post').build_match_conditions
self.assertEqual(build_match_conditions(as_condition=False), [])
self.assertEqual(build_match_conditions(as_condition=True), '')
add_user_permission('Test Blog Post', '_Test Blog Post', 'test2@example.com', True)
add_user_permission('Test Blog Post', '_Test Blog Post 1', 'test2@example.com', True)
self.assertTrue({'Test Blog Post': ['_Test Blog Post 1', '_Test Blog Post']} in build_match_conditions(as_condition=False))
if frappe.db.db_type == 'mariadb':
    assertion_string = "(((ifnull(`tabTest Blog Post`.`name`, '')='' or `tabTest Blog Post`.`name` in ('_Test Blog Post 1', '_Test Blog Post'))))"
elif frappe.db.db_type == 'postgres':
    assertion_string = "(((ifnull(cast(`tabTest Blog Post`.`name` as varchar), '')='' or cast(`tabTest Blog Post`.`name` as varchar) in ('_Test Blog Post 1', '_Test Blog Post'))))"
self.assertEqual(build_match_conditions(as_condition=True), assertion_string)
frappe.set_user('Administrator')
```

## Next Steps


---

*Source: test_db_query.py:196 | Complexity: Advanced | Last updated: 2026-02-04*