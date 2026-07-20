# How To: If Owner Constraint With Shared Docs

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that shared docs trump if_owner constraint.

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

### Step 1: 'Test that shared docs trump if_owner constraint.'

```python
'Test that shared docs trump if_owner constraint.'
```

### Step 2: Assign test_user = 'test2@example.com'

```python
test_user = 'test2@example.com'
```

### Step 3: Assign test_user_doc = frappe.get_doc(...)

```python
test_user_doc = frappe.get_doc('User', test_user)
```

### Step 4: Call test_user_doc.add_roles()

```python
test_user_doc.add_roles('Blogger')
```

### Step 5: Assign blog_post = frappe.get_doc.insert(...)

```python
blog_post = frappe.get_doc(doctype='Test Blog Post', title='If Owner Test Post', content='Test Content', blog_category='_Test Blog Category').insert(ignore_permissions=True, ignore_mandatory=True)
```

### Step 6: Call update()

```python
update('Test Blog Post', 'Blogger', 0, 'if_owner', 1)
```

### Step 7: Call self.addCleanup()

```python
self.addCleanup(lambda: test_user_doc.remove_roles('Blogger'))
```

### Step 8: Call self.addCleanup()

```python
self.addCleanup(blog_post.delete)
```

### Step 9: Call self.addCleanup()

```python
self.addCleanup(lambda: update('Test Blog Post', 'Blogger', 0, 'if_owner', 0))
```

### Step 10: Call self.addCleanup()

```python
self.addCleanup(lambda: frappe.set_user('Administrator'))
```

### Step 11: Call frappe.set_user()

```python
frappe.set_user(test_user)
```

### Step 12: Assign result = frappe.qb.get_query.run(...)

```python
result = frappe.qb.get_query('Test Blog Post', filters={'name': blog_post.name}, ignore_permissions=False).run()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(len(result), 0, 'User should not see post owned by others with if_owner')
```

### Step 14: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 15: Call frappe.share.add()

```python
frappe.share.add('Test Blog Post', blog_post.name, test_user)
```

### Step 16: Call frappe.set_user()

```python
frappe.set_user(test_user)
```

### Step 17: Assign result = frappe.qb.get_query.run(...)

```python
result = frappe.qb.get_query('Test Blog Post', filters={'name': blog_post.name}, ignore_permissions=False).run()
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(len(result), 1, 'User should see post via share despite if_owner')
```


## Complete Example

```python
# Setup
setup_for_tests()

# Workflow
'Test that shared docs trump if_owner constraint.'
import frappe.share
from frappe.core.page.permission_manager.permission_manager import update
test_user = 'test2@example.com'
test_user_doc = frappe.get_doc('User', test_user)
test_user_doc.add_roles('Blogger')
blog_post = frappe.get_doc(doctype='Test Blog Post', title='If Owner Test Post', content='Test Content', blog_category='_Test Blog Category').insert(ignore_permissions=True, ignore_mandatory=True)
update('Test Blog Post', 'Blogger', 0, 'if_owner', 1)
self.addCleanup(lambda: test_user_doc.remove_roles('Blogger'))
self.addCleanup(blog_post.delete)
self.addCleanup(lambda: update('Test Blog Post', 'Blogger', 0, 'if_owner', 0))
self.addCleanup(lambda: frappe.set_user('Administrator'))
frappe.set_user(test_user)
result = frappe.qb.get_query('Test Blog Post', filters={'name': blog_post.name}, ignore_permissions=False).run()
self.assertEqual(len(result), 0, 'User should not see post owned by others with if_owner')
frappe.set_user('Administrator')
frappe.share.add('Test Blog Post', blog_post.name, test_user)
frappe.set_user(test_user)
result = frappe.qb.get_query('Test Blog Post', filters={'name': blog_post.name}, ignore_permissions=False).run()
self.assertEqual(len(result), 1, 'User should see post via share despite if_owner')
```

## Next Steps


---

*Source: test_query.py:1982 | Complexity: Advanced | Last updated: 2026-02-04*