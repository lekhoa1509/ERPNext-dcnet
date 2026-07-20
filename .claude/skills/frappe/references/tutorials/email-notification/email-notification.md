# How To: Email Notification

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test email notification

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
todo = frappe.get_doc(doctype='ToDo', description='Test recurring notification attachment', assigned_by='Administrator').insert()
```

### Step 2: Assign doc = make_auto_repeat(...)

```python
doc = make_auto_repeat(reference_document=todo.name, notify=1, recipients='test@domain.com', subject='New ToDo', message='A new ToDo has just been created for you')
```

### Step 3: Assign data = get_auto_repeat_entries(...)

```python
data = get_auto_repeat_entries(getdate(today()))
```

### Step 4: Call create_repeated_entries()

```python
create_repeated_entries(data)
```

### Step 5: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 6: Assign new_todo = frappe.db.get_value(...)

```python
new_todo = frappe.db.get_value('ToDo', {'auto_repeat': doc.name, 'name': ('!=', todo.name)}, 'name')
```

### Step 7: Assign email_queue = frappe.db.exists(...)

```python
email_queue = frappe.db.exists('Email Queue', dict(reference_doctype='ToDo', reference_name=new_todo))
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(email_queue)
```


## Complete Example

```python
# Workflow
todo = frappe.get_doc(doctype='ToDo', description='Test recurring notification attachment', assigned_by='Administrator').insert()
doc = make_auto_repeat(reference_document=todo.name, notify=1, recipients='test@domain.com', subject='New ToDo', message='A new ToDo has just been created for you')
data = get_auto_repeat_entries(getdate(today()))
create_repeated_entries(data)
frappe.db.commit()
new_todo = frappe.db.get_value('ToDo', {'auto_repeat': doc.name, 'name': ('!=', todo.name)}, 'name')
email_queue = frappe.db.exists('Email Queue', dict(reference_doctype='ToDo', reference_name=new_todo))
self.assertTrue(email_queue)
```

## Next Steps


---

*Source: test_auto_repeat.py:186 | Complexity: Advanced | Last updated: 2026-02-04*