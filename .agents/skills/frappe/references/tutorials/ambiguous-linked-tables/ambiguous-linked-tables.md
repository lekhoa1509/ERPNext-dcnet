# How To: Ambiguous Linked Tables

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test ambiguous linked tables

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

### Step 1: Assign todo_one = frappe.get_doc.insert(...)

```python
todo_one = frappe.get_doc({'doctype': 'ToDo', 'description': 'Todo One'}).insert()
```

### Step 2: Assign todo_two = frappe.get_doc.insert(...)

```python
todo_two = frappe.get_doc({'doctype': 'ToDo', 'description': 'Todo Two'}).insert()
```

### Step 3: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'Related Todos', 'todo_one': todo_one.name, 'todo_two': todo_two.name}).insert()
```

### Step 4: Assign frappe.form_dict.doctype = 'Related Todos'

```python
frappe.form_dict.doctype = 'Related Todos'
```

### Step 5: Assign frappe.form_dict.fields = value

```python
frappe.form_dict.fields = ['`tabRelated Todos`.`name`', '`tabRelated Todos`.`todo_one`', '`tabRelated Todos`.`todo_two`', 'todo_one.description as todo_one_description', 'todo_two.description as todo_two_description']
```

### Step 6: Assign data = get(...)

```python
data = get()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(data['values']), 1)
```

### Step 8: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'DocType', 'custom': 1, 'module': 'Custom', 'name': 'Related Todos', 'naming_rule': 'Random', 'autoname': 'hash', 'fields': [{'label': 'Todo One', 'fieldname': 'todo_one', 'fieldtype': 'Link', 'options': 'ToDo', 'reqd': 1}, {'label': 'Todo Two', 'fieldname': 'todo_two', 'fieldtype': 'Link', 'options': 'ToDo', 'reqd': 1}]}).insert()
```

### Step 9: Call frappe.db.delete()

```python
frappe.db.delete('Related Todos')
```


## Complete Example

```python
# Setup
setup_for_tests()
frappe.set_user('Administrator')

# Workflow
from frappe.desk.reportview import get
if not frappe.db.exists('DocType', 'Related Todos'):
    frappe.get_doc({'doctype': 'DocType', 'custom': 1, 'module': 'Custom', 'name': 'Related Todos', 'naming_rule': 'Random', 'autoname': 'hash', 'fields': [{'label': 'Todo One', 'fieldname': 'todo_one', 'fieldtype': 'Link', 'options': 'ToDo', 'reqd': 1}, {'label': 'Todo Two', 'fieldname': 'todo_two', 'fieldtype': 'Link', 'options': 'ToDo', 'reqd': 1}]}).insert()
else:
    frappe.db.delete('Related Todos')
todo_one = frappe.get_doc({'doctype': 'ToDo', 'description': 'Todo One'}).insert()
todo_two = frappe.get_doc({'doctype': 'ToDo', 'description': 'Todo Two'}).insert()
frappe.get_doc({'doctype': 'Related Todos', 'todo_one': todo_one.name, 'todo_two': todo_two.name}).insert()
frappe.form_dict.doctype = 'Related Todos'
frappe.form_dict.fields = ['`tabRelated Todos`.`name`', '`tabRelated Todos`.`todo_one`', '`tabRelated Todos`.`todo_two`', 'todo_one.description as todo_one_description', 'todo_two.description as todo_two_description']
data = get()
self.assertEqual(len(data['values']), 1)
```

## Next Steps


---

*Source: test_db_query.py:1077 | Complexity: Advanced | Last updated: 2026-02-04*