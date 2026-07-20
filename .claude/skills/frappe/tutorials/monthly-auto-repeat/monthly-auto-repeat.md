# How To: Monthly Auto Repeat

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test monthly auto repeat

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

### Step 1: Assign start_date = today(...)

```python
start_date = today()
```

### Step 2: Assign end_date = add_months(...)

```python
end_date = add_months(start_date, 12)
```

### Step 3: Assign todo = frappe.get_doc.insert(...)

```python
todo = frappe.get_doc(doctype='ToDo', description='test recurring todo', assigned_by='Administrator').insert()
```

### Step 4: Call self.monthly_auto_repeat()

```python
self.monthly_auto_repeat('ToDo', todo.name, start_date, end_date)
```

### Step 5: Assign todo = frappe.get_doc.insert(...)

```python
todo = frappe.get_doc(doctype='ToDo', description='test recurring todo without end_date', assigned_by='Administrator').insert()
```

### Step 6: Call self.monthly_auto_repeat()

```python
self.monthly_auto_repeat('ToDo', todo.name, start_date)
```


## Complete Example

```python
# Workflow
start_date = today()
end_date = add_months(start_date, 12)
todo = frappe.get_doc(doctype='ToDo', description='test recurring todo', assigned_by='Administrator').insert()
self.monthly_auto_repeat('ToDo', todo.name, start_date, end_date)
todo = frappe.get_doc(doctype='ToDo', description='test recurring todo without end_date', assigned_by='Administrator').insert()
self.monthly_auto_repeat('ToDo', todo.name, start_date)
```

## Next Steps


---

*Source: test_auto_repeat.py:141 | Complexity: Intermediate | Last updated: 2026-02-04*