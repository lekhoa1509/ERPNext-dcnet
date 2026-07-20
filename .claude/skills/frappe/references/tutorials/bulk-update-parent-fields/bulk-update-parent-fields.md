# How To: Bulk Update Parent Fields

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bulk update parent fields

## Prerequisites

**Required Modules:**
- `time`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.desk.doctype.bulk_update.bulk_update`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign docnames = frappe.get_all(...)

```python
docnames = frappe.get_all(self.doctype, {'docstatus': 0}, limit=5, pluck='name')
```

### Step 2: Assign failed = submit_cancel_or_update_docs(...)

```python
failed = submit_cancel_or_update_docs(self.doctype, docnames, action='update', data={'some_fieldname': '_Test Sync'})
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(failed, [])
```

### Step 4: Assign docnames_bg = frappe.get_all(...)

```python
docnames_bg = frappe.get_all(self.doctype, {'docstatus': 0}, limit=20, pluck='name')
```

### Step 5: Call submit_cancel_or_update_docs()

```python
submit_cancel_or_update_docs(self.doctype, docnames_bg, action='update', data={'some_fieldname': '_Test Background'})
```

### Step 6: Call self.wait_for_assertion()

```python
self.wait_for_assertion(lambda: check_field_values(docnames_bg, '_Test Background'))
```

### Step 7: Call frappe.db.rollback()

```python
frappe.db.rollback()
```

### Step 8: Assign values = frappe.get_all(...)

```python
values = frappe.get_all(self.doctype, {'name': ['in', docs]}, ['name', 'some_fieldname'])
```


## Complete Example

```python
# Workflow
docnames = frappe.get_all(self.doctype, {'docstatus': 0}, limit=5, pluck='name')
failed = submit_cancel_or_update_docs(self.doctype, docnames, action='update', data={'some_fieldname': '_Test Sync'})
self.assertEqual(failed, [])

def check_field_values(docs, expected):
    frappe.db.rollback()
    values = frappe.get_all(self.doctype, {'name': ['in', docs]}, ['name', 'some_fieldname'])
    return all((v.some_fieldname == expected for v in values))
docnames_bg = frappe.get_all(self.doctype, {'docstatus': 0}, limit=20, pluck='name')
submit_cancel_or_update_docs(self.doctype, docnames_bg, action='update', data={'some_fieldname': '_Test Background'})
self.wait_for_assertion(lambda: check_field_values(docnames_bg, '_Test Background'))
```

## Next Steps


---

*Source: test_bulk_update.py:51 | Complexity: Advanced | Last updated: 2026-02-04*