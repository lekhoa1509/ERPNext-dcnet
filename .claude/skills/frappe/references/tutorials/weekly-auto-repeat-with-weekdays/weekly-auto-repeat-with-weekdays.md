# How To: Weekly Auto Repeat With Weekdays

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test weekly auto repeat with weekdays

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
todo = frappe.get_doc(doctype='ToDo', description='test auto repeat with weekdays', assigned_by='Administrator').insert()
```

### Step 2: Assign weekdays = list(...)

```python
weekdays = list(week_map.keys())
```

### Step 3: Assign current_weekday = getdate.weekday(...)

```python
current_weekday = getdate().weekday()
```

### Step 4: Assign days = value

```python
days = [{'day': weekdays[current_weekday]}, {'day': weekdays[(current_weekday + 2) % 7]}]
```

### Step 5: Assign doc = make_auto_repeat(...)

```python
doc = make_auto_repeat(reference_doctype='ToDo', frequency='Weekly', reference_document=todo.name, start_date=add_days(today(), -7), days=days)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(doc.next_schedule_date, today())
```

### Step 7: Assign data = get_auto_repeat_entries(...)

```python
data = get_auto_repeat_entries(getdate(today()))
```

### Step 8: Call create_repeated_entries()

```python
create_repeated_entries(data)
```

### Step 9: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 10: Assign todo = frappe.get_doc(...)

```python
todo = frappe.get_doc(doc.reference_doctype, doc.reference_document)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(todo.auto_repeat, doc.name)
```

### Step 12: Call doc.reload()

```python
doc.reload()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(doc.next_schedule_date, add_days(getdate(), 2))
```


## Complete Example

```python
# Workflow
todo = frappe.get_doc(doctype='ToDo', description='test auto repeat with weekdays', assigned_by='Administrator').insert()
weekdays = list(week_map.keys())
current_weekday = getdate().weekday()
days = [{'day': weekdays[current_weekday]}, {'day': weekdays[(current_weekday + 2) % 7]}]
doc = make_auto_repeat(reference_doctype='ToDo', frequency='Weekly', reference_document=todo.name, start_date=add_days(today(), -7), days=days)
self.assertEqual(doc.next_schedule_date, today())
data = get_auto_repeat_entries(getdate(today()))
create_repeated_entries(data)
frappe.db.commit()
todo = frappe.get_doc(doc.reference_doctype, doc.reference_document)
self.assertEqual(todo.auto_repeat, doc.name)
doc.reload()
self.assertEqual(doc.next_schedule_date, add_days(getdate(), 2))
```

## Next Steps


---

*Source: test_auto_repeat.py:114 | Complexity: Advanced | Last updated: 2026-02-04*