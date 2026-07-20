# How To: Auto Repeat Assignee With Separate Documents

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test auto repeat assignee with separate documents

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
todo = frappe.get_doc(doctype='ToDo', description='test assignee todo with multiple doc', assigned_by='Administrator').insert()
```

### Step 2: Assign doc = make_auto_repeat(...)

```python
doc = make_auto_repeat(reference_document=todo.name)
```

### Step 3: Call doc.update()

```python
doc.update({'assignee': [{'user': 'Administrator'}, {'user': 'Guest'}], 'generate_separate_documents_for_each_assignee': 1})
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

### Step 11: Assign new_todo_count = frappe.db.count(...)

```python
new_todo_count = frappe.db.count('ToDo', {'auto_repeat': doc.name, 'name': ('!=', todo.name)}, 'name')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(new_todo_count, 2)
```


## Complete Example

```python
# Workflow
todo = frappe.get_doc(doctype='ToDo', description='test assignee todo with multiple doc', assigned_by='Administrator').insert()
doc = make_auto_repeat(reference_document=todo.name)
doc.update({'assignee': [{'user': 'Administrator'}, {'user': 'Guest'}], 'generate_separate_documents_for_each_assignee': 1})
doc.save()
self.assertEqual(doc.next_schedule_date, today())
data = get_auto_repeat_entries(getdate(today()))
create_repeated_entries(data)
frappe.db.commit()
todo = frappe.get_doc(doc.reference_doctype, doc.reference_document)
self.assertEqual(todo.auto_repeat, doc.name)
new_todo_count = frappe.db.count('ToDo', {'auto_repeat': doc.name, 'name': ('!=', todo.name)}, 'name')
self.assertEqual(new_todo_count, 2)
```

## Next Steps


---

*Source: test_auto_repeat.py:282 | Complexity: Advanced | Last updated: 2026-02-04*