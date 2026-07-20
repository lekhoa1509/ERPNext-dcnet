# How To: External Doctype Link With Dashboard Override

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test external doctype link with dashboard override

## Prerequisites

**Required Modules:**
- `os`
- `unittest.mock`
- `frappe`
- `frappe.utils`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.custom.doctype.customize_form.test_customize_form`
- `frappe.desk.notifications`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign todo = TestCustomizeForm.get_customize_form(...)

```python
todo = TestCustomizeForm().get_customize_form('ToDo')
```

### Step 2: Call todo.append()

```python
todo.append('links', dict(link_doctype='Test Doctype D', link_fieldname='doclink', group='Test'))
```

### Step 3: Call todo.append()

```python
todo.append('links', dict(link_doctype='Test Doctype E', link_fieldname='todo', group='Test'))
```

### Step 4: Call todo.run_method()

```python
todo.run_method('save_customization')
```

### Step 5: Assign todo_doc = frappe.get_doc.insert(...)

```python
todo_doc = frappe.get_doc(doctype='ToDo', description='test').insert()
```

### Step 6: Call frappe.get_doc.insert()

```python
frappe.get_doc(doctype='Test Doctype D', title='d-001', doclink=todo_doc.name).insert()
```

### Step 7: Call frappe.get_doc.insert()

```python
frappe.get_doc(doctype='Test Doctype E', title='e-001', todo=todo_doc.name).insert()
```

### Step 8: Assign connections = value

```python
connections = get_open_count('ToDo', todo_doc.name)['count']
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(connections['external_links_found']), 2)
```

### Step 10: Assign todo = TestCustomizeForm.get_customize_form(...)

```python
todo = TestCustomizeForm().get_customize_form('ToDo')
```

### Step 11: Assign todo.links = value

```python
todo.links = todo.links[:-2]
```

### Step 12: Call todo.run_method()

```python
todo.run_method('save_customization')
```

### Step 13: Assign connections = value

```python
connections = get_open_count('ToDo', todo_doc.name)['count']
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(len(connections['external_links_found']), 2)
```


## Complete Example

```python
# Workflow
todo = TestCustomizeForm().get_customize_form('ToDo')
todo.append('links', dict(link_doctype='Test Doctype D', link_fieldname='doclink', group='Test'))
todo.append('links', dict(link_doctype='Test Doctype E', link_fieldname='todo', group='Test'))
todo.run_method('save_customization')
todo_doc = frappe.get_doc(doctype='ToDo', description='test').insert()
frappe.get_doc(doctype='Test Doctype D', title='d-001', doclink=todo_doc.name).insert()
frappe.get_doc(doctype='Test Doctype E', title='e-001', todo=todo_doc.name).insert()
connections = get_open_count('ToDo', todo_doc.name)['count']
self.assertEqual(len(connections['external_links_found']), 2)
with self.patch_hooks({'override_doctype_dashboards': {'ToDo': ['frappe.tests.test_dashboard_connections.get_dashboard_for_todo']}}):
    connections = get_open_count('ToDo', todo_doc.name)['count']
    self.assertEqual(len(connections['external_links_found']), 2)
todo = TestCustomizeForm().get_customize_form('ToDo')
todo.links = todo.links[:-2]
todo.run_method('save_customization')
```

## Next Steps


---

*Source: test_dashboard_connections.py:125 | Complexity: Advanced | Last updated: 2026-02-04*