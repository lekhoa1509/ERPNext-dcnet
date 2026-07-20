# How To: Reportview Get

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test reportview get

## Prerequisites

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


## Step-by-Step Guide

### Step 1: Assign user = frappe.get_doc(...)

```python
user = frappe.get_doc('User', 'test@example.com')
```

### Step 2: Call add_child_table_to_blog_post()

```python
add_child_table_to_blog_post()
```

### Step 3: Assign user_roles = frappe.get_roles(...)

```python
user_roles = frappe.get_roles()
```

### Step 4: Call user.remove_roles()

```python
user.remove_roles(*user_roles)
```

### Step 5: Call user.add_roles()

```python
user.add_roles('Blogger')
```

### Step 6: Call make_property_setter()

```python
make_property_setter('Test Blog Post', 'published', 'permlevel', 1, 'Int')
```

### Step 7: Call reset()

```python
reset('Test Blog Post')
```

### Step 8: Call add()

```python
add('Test Blog Post', 'Website Manager', 1)
```

### Step 9: Call update()

```python
update('Test Blog Post', 'Website Manager', 1, 'write', 1)
```

### Step 10: Call frappe.set_user()

```python
frappe.set_user(user.name)
```

### Step 11: Assign frappe.local.request = frappe._dict(...)

```python
frappe.local.request = frappe._dict()
```

### Step 12: Assign frappe.local.request.method = 'POST'

```python
frappe.local.request.method = 'POST'
```

### Step 13: Assign frappe.local.form_dict = frappe._dict(...)

```python
frappe.local.form_dict = frappe._dict({'doctype': 'Test Blog Post', 'fields': ['published', 'title', '`tabTest Child`.`test_field`']})
```

### Step 14: Assign response = execute_cmd(...)

```python
response = execute_cmd('frappe.desk.reportview.get')
```

### Step 15: Call self.assertListEqual()

```python
self.assertListEqual(response['keys'], ['title'])
```

### Step 16: Assign frappe.local.form_dict = frappe._dict(...)

```python
frappe.local.form_dict = frappe._dict({'doctype': 'Test Blog Post', 'fields': ['*']})
```

### Step 17: Assign response = execute_cmd(...)

```python
response = execute_cmd('frappe.desk.reportview.get')
```

### Step 18: Call self.assertNotIn()

```python
self.assertNotIn('published', response['keys'])
```

### Step 19: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 20: Call user.add_roles()

```python
user.add_roles('Website Manager')
```

### Step 21: Call frappe.set_user()

```python
frappe.set_user(user.name)
```

### Step 22: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 23: Assign frappe.local.form_dict = frappe._dict(...)

```python
frappe.local.form_dict = frappe._dict({'doctype': 'Test Blog Post', 'fields': ['published', 'title', '`tabTest Child`.`test_field`']})
```

### Step 24: Assign response = execute_cmd(...)

```python
response = execute_cmd('frappe.desk.reportview.get')
```

### Step 25: Call self.assertListEqual()

```python
self.assertListEqual(response['keys'], ['published', 'title', 'test_field'])
```

### Step 26: Call user.remove_roles()

```python
user.remove_roles('Blogger', 'Website Manager')
```

### Step 27: Call user.add_roles()

```python
user.add_roles(*user_roles)
```


## Complete Example

```python
# Workflow
user = frappe.get_doc('User', 'test@example.com')
add_child_table_to_blog_post()
user_roles = frappe.get_roles()
user.remove_roles(*user_roles)
user.add_roles('Blogger')
make_property_setter('Test Blog Post', 'published', 'permlevel', 1, 'Int')
reset('Test Blog Post')
add('Test Blog Post', 'Website Manager', 1)
update('Test Blog Post', 'Website Manager', 1, 'write', 1)
frappe.set_user(user.name)
frappe.local.request = frappe._dict()
frappe.local.request.method = 'POST'
frappe.local.form_dict = frappe._dict({'doctype': 'Test Blog Post', 'fields': ['published', 'title', '`tabTest Child`.`test_field`']})
response = execute_cmd('frappe.desk.reportview.get')
self.assertListEqual(response['keys'], ['title'])
frappe.local.form_dict = frappe._dict({'doctype': 'Test Blog Post', 'fields': ['*']})
response = execute_cmd('frappe.desk.reportview.get')
self.assertNotIn('published', response['keys'])
frappe.set_user('Administrator')
user.add_roles('Website Manager')
frappe.set_user(user.name)
frappe.set_user('Administrator')
frappe.local.form_dict = frappe._dict({'doctype': 'Test Blog Post', 'fields': ['published', 'title', '`tabTest Child`.`test_field`']})
response = execute_cmd('frappe.desk.reportview.get')
self.assertListEqual(response['keys'], ['published', 'title', 'test_field'])
user.remove_roles('Blogger', 'Website Manager')
user.add_roles(*user_roles)
```

## Next Steps


---

*Source: test_db_query.py:1242 | Complexity: Advanced | Last updated: 2026-02-04*