# How To: Bulk Submit In Background

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bulk submit in background

## Prerequisites

**Required Modules:**
- `time`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.desk.doctype.bulk_update.bulk_update`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign unsubmitted = frappe.get_all(...)

```python
unsubmitted = frappe.get_all(self.doctype, {'docstatus': 0}, limit=5, pluck='name')
```

### Step 2: Assign failed = submit_cancel_or_update_docs(...)

```python
failed = submit_cancel_or_update_docs(self.doctype, unsubmitted, action='submit')
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(failed, [])
```

### Step 4: Assign unsubmitted = frappe.get_all(...)

```python
unsubmitted = frappe.get_all(self.doctype, {'docstatus': 0}, limit=20, pluck='name')
```

### Step 5: Call submit_cancel_or_update_docs()

```python
submit_cancel_or_update_docs(self.doctype, unsubmitted, action='submit')
```

### Step 6: Call self.wait_for_assertion()

```python
self.wait_for_assertion(lambda: check_docstatus(unsubmitted, 1))
```

### Step 7: Assign submitted = frappe.get_all(...)

```python
submitted = frappe.get_all(self.doctype, {'docstatus': 1}, limit=20, pluck='name')
```

### Step 8: Call submit_cancel_or_update_docs()

```python
submit_cancel_or_update_docs(self.doctype, submitted, action='cancel')
```

### Step 9: Call self.wait_for_assertion()

```python
self.wait_for_assertion(lambda: check_docstatus(submitted, 2))
```

### Step 10: Call frappe.db.rollback()

```python
frappe.db.rollback()
```

### Step 11: Assign matching_docs = frappe.get_all(...)

```python
matching_docs = frappe.get_all(self.doctype, {'docstatus': status, 'name': ('in', docs)}, pluck='name')
```


## Complete Example

```python
# Workflow
unsubmitted = frappe.get_all(self.doctype, {'docstatus': 0}, limit=5, pluck='name')
failed = submit_cancel_or_update_docs(self.doctype, unsubmitted, action='submit')
self.assertEqual(failed, [])

def check_docstatus(docs, status):
    frappe.db.rollback()
    matching_docs = frappe.get_all(self.doctype, {'docstatus': status, 'name': ('in', docs)}, pluck='name')
    return set(matching_docs) == set(docs)
unsubmitted = frappe.get_all(self.doctype, {'docstatus': 0}, limit=20, pluck='name')
submit_cancel_or_update_docs(self.doctype, unsubmitted, action='submit')
self.wait_for_assertion(lambda: check_docstatus(unsubmitted, 1))
submitted = frappe.get_all(self.doctype, {'docstatus': 1}, limit=20, pluck='name')
submit_cancel_or_update_docs(self.doctype, submitted, action='cancel')
self.wait_for_assertion(lambda: check_docstatus(submitted, 2))
```

## Next Steps


---

*Source: test_bulk_update.py:30 | Complexity: Advanced | Last updated: 2026-02-04*