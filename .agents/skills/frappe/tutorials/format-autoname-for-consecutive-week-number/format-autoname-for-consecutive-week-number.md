# How To: Format Autoname For Consecutive Week Number

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test if braced params are replaced for consecutive week number in format autoname

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `time`
- `uuid`
- `uuid_utils`
- `tenacity`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.model.naming`
- `frappe.query_builder.utils`
- `frappe.tests`
- `frappe.tests.test_query_builder`
- `frappe.utils`
- `datetime`
- `datetime`
- `frappe.core.doctype.doctype.test_doctype`

**Setup Required:**
```python
frappe.db.delete('Note')
```

## Step-by-Step Guide

### Step 1: '\n\t\tTest if braced params are replaced for consecutive week number in format autoname\n\t\t'

```python
'\n\t\tTest if braced params are replaced for consecutive week number in format autoname\n\t\t'
```

### Step 2: Assign doctype = 'ToDo'

```python
doctype = 'ToDo'
```

### Step 3: Assign todo_doctype = frappe.get_doc(...)

```python
todo_doctype = frappe.get_doc('DocType', doctype)
```

### Step 4: Assign todo_doctype.autoname = 'format:TODO-{WW}-{##}'

```python
todo_doctype.autoname = 'format:TODO-{WW}-{##}'
```

### Step 5: Call todo_doctype.save()

```python
todo_doctype.save()
```

### Step 6: Assign description = 'Format'

```python
description = 'Format'
```

### Step 7: Assign todo = frappe.new_doc(...)

```python
todo = frappe.new_doc(doctype)
```

### Step 8: Assign todo.description = description

```python
todo.description = description
```

### Step 9: Call todo.insert()

```python
todo.insert()
```

### Step 10: Assign series = getseries(...)

```python
series = getseries('', 2)
```

### Step 11: Assign series = str(...)

```python
series = str(int(series) - 1)
```

### Step 12: Assign week = determine_consecutive_week_number(...)

```python
week = determine_consecutive_week_number(now_datetime())
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(todo.name, f'TODO-{week}-{series}')
```

### Step 14: Assign series = value

```python
series = '0' + series
```


## Complete Example

```python
# Setup
frappe.db.delete('Note')

# Workflow
'\n\t\tTest if braced params are replaced for consecutive week number in format autoname\n\t\t'
doctype = 'ToDo'
todo_doctype = frappe.get_doc('DocType', doctype)
todo_doctype.autoname = 'format:TODO-{WW}-{##}'
todo_doctype.save()
description = 'Format'
todo = frappe.new_doc(doctype)
todo.description = description
todo.insert()
series = getseries('', 2)
series = str(int(series) - 1)
if len(series) < 2:
    series = '0' + series
week = determine_consecutive_week_number(now_datetime())
self.assertEqual(todo.name, f'TODO-{week}-{series}')
```

## Next Steps


---

*Source: test_naming.py:124 | Complexity: Advanced | Last updated: 2026-02-04*