# How To: Next Schedule Date

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test next schedule date

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

### Step 1: Assign current_date = getdate(...)

```python
current_date = getdate(today())
```

### Step 2: Assign todo = frappe.get_doc.insert(...)

```python
todo = frappe.get_doc(doctype='ToDo', description='test next schedule date for monthly', assigned_by='Administrator').insert()
```

### Step 3: Assign doc = make_auto_repeat(...)

```python
doc = make_auto_repeat(frequency='Monthly', reference_document=todo.name, start_date=add_months(today(), -2))
```

### Step 4: Call self.assertTrue()

```python
self.assertTrue(doc.next_schedule_date >= current_date)
```

### Step 5: Assign todo = frappe.get_doc.insert(...)

```python
todo = frappe.get_doc(doctype='ToDo', description='test next schedule date for daily', assigned_by='Administrator').insert()
```

### Step 6: Assign doc = make_auto_repeat(...)

```python
doc = make_auto_repeat(frequency='Daily', reference_document=todo.name, start_date=add_days(today(), -2))
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(getdate(doc.next_schedule_date), current_date)
```


## Complete Example

```python
# Workflow
current_date = getdate(today())
todo = frappe.get_doc(doctype='ToDo', description='test next schedule date for monthly', assigned_by='Administrator').insert()
doc = make_auto_repeat(frequency='Monthly', reference_document=todo.name, start_date=add_months(today(), -2))
self.assertTrue(doc.next_schedule_date >= current_date)
todo = frappe.get_doc(doctype='ToDo', description='test next schedule date for daily', assigned_by='Administrator').insert()
doc = make_auto_repeat(frequency='Daily', reference_document=todo.name, start_date=add_days(today(), -2))
self.assertEqual(getdate(doc.next_schedule_date), current_date)
```

## Next Steps


---

*Source: test_auto_repeat.py:207 | Complexity: Intermediate | Last updated: 2026-02-04*