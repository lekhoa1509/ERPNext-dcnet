# How To: Save On Discard Throws

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test save on discard throws

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

### Step 1: Assign d3 = self.test_insert(...)

```python
d3 = self.test_insert()
```

### Step 2: Assign d3.on_discard = test_on_discard(...)

```python
d3.on_discard = test_on_discard(d3)
```

### Step 3: Assign d3.on_discard = test_on_discard.__get__(...)

```python
d3.on_discard = test_on_discard.__get__(d3, Event)
```

### Step 4: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, d3.discard)
```

### Step 5: Assign d3.subject = value

```python
d3.subject = d3.subject + 'update'
```

### Step 6: Call d3.save()

```python
d3.save()
```


## Complete Example

```python
# Workflow
from frappe.desk.doctype.event.event import Event
d3 = self.test_insert()

def test_on_discard(d3):
    d3.subject = d3.subject + 'update'
    d3.save()
d3.on_discard = test_on_discard(d3)
d3.on_discard = test_on_discard.__get__(d3, Event)
self.assertRaises(frappe.ValidationError, d3.discard)
```

## Next Steps


---

*Source: test_document.py:120 | Complexity: Intermediate | Last updated: 2026-02-04*