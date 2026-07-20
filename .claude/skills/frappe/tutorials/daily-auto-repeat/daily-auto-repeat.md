# How To: Daily Auto Repeat

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test daily auto repeat

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
todo = frappe.get_doc(doctype='ToDo', description='test recurring todo', assigned_by='Administrator').insert()
```

### Step 2: Assign doc = make_auto_repeat(...)

```python
doc = make_auto_repeat(reference_document=todo.name)
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(doc.next_schedule_date, today())
```

### Step 4: Assign data = get_auto_repeat_entries(...)

```python
data = get_auto_repeat_entries(getdate(today()))
```

### Step 5: Call create_repeated_entries()

```python
create_repeated_entries(data)
```

### Step 6: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 7: Assign todo = frappe.get_doc(...)

```python
todo = frappe.get_doc(doc.reference_doctype, doc.reference_document)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(todo.auto_repeat, doc.name)
```

### Step 9: Assign new_todo = frappe.db.get_value(...)

```python
new_todo = frappe.db.get_value('ToDo', {'auto_repeat': doc.name, 'name': ('!=', todo.name)}, 'name')
```

### Step 10: Assign new_todo = frappe.get_doc(...)

```python
new_todo = frappe.get_doc('ToDo', new_todo)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(todo.get('description'), new_todo.get('description'))
```


## Complete Example

```python
# Workflow
todo = frappe.get_doc(doctype='ToDo', description='test recurring todo', assigned_by='Administrator').insert()
doc = make_auto_repeat(reference_document=todo.name)
self.assertEqual(doc.next_schedule_date, today())
data = get_auto_repeat_entries(getdate(today()))
create_repeated_entries(data)
frappe.db.commit()
todo = frappe.get_doc(doc.reference_doctype, doc.reference_document)
self.assertEqual(todo.auto_repeat, doc.name)
new_todo = frappe.db.get_value('ToDo', {'auto_repeat': doc.name, 'name': ('!=', todo.name)}, 'name')
new_todo = frappe.get_doc('ToDo', new_todo)
self.assertEqual(todo.get('description'), new_todo.get('description'))
```

## Next Steps


---

*Source: test_auto_repeat.py:42 | Complexity: Advanced | Last updated: 2026-02-04*