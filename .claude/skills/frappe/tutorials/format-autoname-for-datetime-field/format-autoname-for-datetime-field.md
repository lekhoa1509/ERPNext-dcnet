# How To: Format Autoname For Datetime Field

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test if datetime, date and time objects get converted to strings for naming.

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

### Step 1: 'Test if datetime, date and time objects get converted to strings for naming.'

```python
'Test if datetime, date and time objects get converted to strings for naming.'
```

### Step 2: Assign doctype = new_doctype.insert(...)

```python
doctype = new_doctype(autoname='format:TODO-{field}-{##}').insert()
```

### Step 3: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc(doctype.name)
```

### Step 4: Assign doc.field = field

```python
doc.field = field
```

### Step 5: Call doc.insert()

```python
doc.insert()
```

### Step 6: Assign series = getseries(...)

```python
series = getseries('', 2)
```

### Step 7: Assign series = value

```python
series = int(series) - 1
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(doc.name, f'TODO-{field}-{series:02}')
```


## Complete Example

```python
# Setup
frappe.db.delete('Note')

# Workflow
'Test if datetime, date and time objects get converted to strings for naming.'
doctype = new_doctype(autoname='format:TODO-{field}-{##}').insert()
for field in [now_datetime(), nowdate(), nowtime()]:
    doc = frappe.new_doc(doctype.name)
    doc.field = field
    doc.insert()
    series = getseries('', 2)
    series = int(series) - 1
    self.assertEqual(doc.name, f'TODO-{field}-{series:02}')
```

## Next Steps


---

*Source: test_naming.py:110 | Complexity: Advanced | Last updated: 2026-02-04*