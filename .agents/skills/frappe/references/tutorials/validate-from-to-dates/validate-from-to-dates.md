# How To: Validate From To Dates

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test validate from to dates

## Prerequisites

**Required Modules:**
- `inspect`
- `contextlib`
- `copy`
- `datetime`
- `unittest.mock`
- `frappe`
- `frappe.app`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.doctype.user.user`
- `frappe.desk.doctype.note.note`
- `frappe.model.document`
- `frappe.model.naming`
- `frappe.tests`
- `frappe.utils`
- `frappe.website.serve`
- `frappe.desk.doctype.event.event`
- `pathlib`
- `frappe.modules.utils`
- `frappe.model.document`


## Step-by-Step Guide

### Step 1: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc('Web Page')
```

### Step 2: Assign doc.start_date = None

```python
doc.start_date = None
```

### Step 3: Assign doc.end_date = None

```python
doc.end_date = None
```

### Step 4: Call doc.validate_from_to_dates()

```python
doc.validate_from_to_dates('start_date', 'end_date')
```

### Step 5: Assign doc.start_date = '2020-01-01'

```python
doc.start_date = '2020-01-01'
```

### Step 6: Assign doc.end_date = None

```python
doc.end_date = None
```

### Step 7: Call doc.validate_from_to_dates()

```python
doc.validate_from_to_dates('start_date', 'end_date')
```

### Step 8: Assign doc.start_date = None

```python
doc.start_date = None
```

### Step 9: Assign doc.end_date = '2020-12-31'

```python
doc.end_date = '2020-12-31'
```

### Step 10: Call doc.validate_from_to_dates()

```python
doc.validate_from_to_dates('start_date', 'end_date')
```

### Step 11: Assign doc.start_date = '2020-01-01'

```python
doc.start_date = '2020-01-01'
```

### Step 12: Assign doc.end_date = '2020-12-31'

```python
doc.end_date = '2020-12-31'
```

### Step 13: Call doc.validate_from_to_dates()

```python
doc.validate_from_to_dates('start_date', 'end_date')
```

### Step 14: Assign doc.end_date = '2020-01-01'

```python
doc.end_date = '2020-01-01'
```

### Step 15: Assign doc.start_date = '2020-12-31'

```python
doc.start_date = '2020-12-31'
```

### Step 16: Call self.assertRaises()

```python
self.assertRaises(frappe.exceptions.InvalidDates, doc.validate_from_to_dates, 'start_date', 'end_date')
```


## Complete Example

```python
# Workflow
doc = frappe.new_doc('Web Page')
doc.start_date = None
doc.end_date = None
doc.validate_from_to_dates('start_date', 'end_date')
doc.start_date = '2020-01-01'
doc.end_date = None
doc.validate_from_to_dates('start_date', 'end_date')
doc.start_date = None
doc.end_date = '2020-12-31'
doc.validate_from_to_dates('start_date', 'end_date')
doc.start_date = '2020-01-01'
doc.end_date = '2020-12-31'
doc.validate_from_to_dates('start_date', 'end_date')
doc.end_date = '2020-01-01'
doc.start_date = '2020-12-31'
self.assertRaises(frappe.exceptions.InvalidDates, doc.validate_from_to_dates, 'start_date', 'end_date')
```

## Next Steps


---

*Source: test_document.py:510 | Complexity: Advanced | Last updated: 2026-02-04*