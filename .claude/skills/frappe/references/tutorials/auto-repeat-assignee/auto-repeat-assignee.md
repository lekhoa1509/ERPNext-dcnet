# How To: Auto Repeat Assignee

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test auto repeat assignee

## Prerequisites

**Required Modules:**
- `typing`
- `frappe`
- `frappe.automation.doctype.auto_repeat.auto_repeat`
- `frappe.custom.doctype.custom_field.custom_field`
- `frappe.tests`
- `frappe.utils`
- `frappe.custom.doctype.custom_field.custom_field`


## Step-by-Step Guide

### Step 1: Assign todo = frappe.get_doc.insert(...)

```python
todo = frappe.get_doc(doctype='ToDo', description='test assignee todo', assigned_by='Administrator').insert()
```

### Step 2: Assign doc = make_auto_repeat(...)

```python
doc = make_auto_repeat(reference_document=todo.name)
```

### Step 3: Call doc.update()

```python
doc.update({'assignee': [{'user': 'Administrator'}, {'user': 'Guest'}]})
```

### Step 4: Call doc.save()

```python
doc.save()
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(doc.next_schedule_date, today())
```

### Step 6: Assign data = get_auto_repeat_entries(...)

```python
data = get_auto_repeat_entries(getdate(today()))
```

### Step 7: Call create_repeated_entries()

```python
create_repeated_entries(data)
```

### Step 8: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 9: Assign todo = frappe.get_doc(...)

```python
todo = frappe.get_doc(doc.reference_doctype, doc.reference_document)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(todo.auto_repeat, doc.name)
```

### Step 11: Assign new_todo = frappe.db.get_value(...)

```python
new_todo = frappe.db.get_value('ToDo', {'auto_repeat': doc.name, 'name': ('!=', todo.name)}, 'name')
```

### Step 12: Assign new_todo = frappe.get_doc(...)

```python
new_todo = frappe.get_doc('ToDo', new_todo)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(todo.get('description'), new_todo.get('description'))
```

### Step 14: Call self.assertListEqual()

```python
self.assertListEqual(sorted(list(new_todo.get_assigned_users())), sorted(['Administrator', 'Guest']))
```


## Complete Example

```python
# Workflow
todo = frappe.get_doc(doctype='ToDo', description='test assignee todo', assigned_by='Administrator').insert()
doc = make_auto_repeat(reference_document=todo.name)
doc.update({'assignee': [{'user': 'Administrator'}, {'user': 'Guest'}]})
doc.save()
self.assertEqual(doc.next_schedule_date, today())
data = get_auto_repeat_entries(getdate(today()))
create_repeated_entries(data)
frappe.db.commit()
todo = frappe.get_doc(doc.reference_doctype, doc.reference_document)
self.assertEqual(todo.auto_repeat, doc.name)
new_todo = frappe.db.get_value('ToDo', {'auto_repeat': doc.name, 'name': ('!=', todo.name)}, 'name')
new_todo = frappe.get_doc('ToDo', new_todo)
self.assertEqual(todo.get('description'), new_todo.get('description'))
self.assertListEqual(sorted(list(new_todo.get_assigned_users())), sorted(['Administrator', 'Guest']))
```

## Next Steps


---

*Source: test_auto_repeat.py:250 | Complexity: Advanced | Last updated: 2026-02-04*