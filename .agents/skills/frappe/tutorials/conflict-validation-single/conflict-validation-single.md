# How To: Conflict Validation Single

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test conflict validation single

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

### Step 1: Assign d1 = frappe.get_doc(...)

```python
d1 = frappe.get_doc('Website Settings', 'Website Settings')
```

### Step 2: Assign d1.home_page = 'test-web-page-1'

```python
d1.home_page = 'test-web-page-1'
```

### Step 3: Assign d2 = frappe.get_doc(...)

```python
d2 = frappe.get_doc('Website Settings', 'Website Settings')
```

### Step 4: Assign d2.home_page = 'test-web-page-1'

```python
d2.home_page = 'test-web-page-1'
```

### Step 5: Call d1.save()

```python
d1.save()
```

### Step 6: Call self.assertRaises()

```python
self.assertRaises(frappe.TimestampMismatchError, d2.save)
```


## Complete Example

```python
# Workflow
d1 = frappe.get_doc('Website Settings', 'Website Settings')
d1.home_page = 'test-web-page-1'
d2 = frappe.get_doc('Website Settings', 'Website Settings')
d2.home_page = 'test-web-page-1'
d1.save()
self.assertRaises(frappe.TimestampMismatchError, d2.save)
```

## Next Steps


---

*Source: test_document.py:184 | Complexity: Intermediate | Last updated: 2026-02-04*