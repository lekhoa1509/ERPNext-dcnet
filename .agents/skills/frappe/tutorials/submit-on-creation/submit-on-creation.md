# How To: Submit On Creation

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test submit on creation

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

### Step 1: Assign doctype = 'Test Submittable DocType'

```python
doctype = 'Test Submittable DocType'
```

### Step 2: Call create_submittable_doctype()

```python
create_submittable_doctype(doctype)
```

### Step 3: Assign current_date = getdate(...)

```python
current_date = getdate()
```

### Step 4: Assign submittable_doc = frappe.get_doc.insert(...)

```python
submittable_doc = frappe.get_doc(doctype=doctype, test='test submit on creation').insert()
```

### Step 5: Call submittable_doc.submit()

```python
submittable_doc.submit()
```

### Step 6: Assign doc = make_auto_repeat(...)

```python
doc = make_auto_repeat(frequency='Daily', reference_doctype=doctype, reference_document=submittable_doc.name, start_date=add_days(current_date, -1), submit_on_creation=1)
```

### Step 7: Assign data = get_auto_repeat_entries(...)

```python
data = get_auto_repeat_entries(current_date)
```

### Step 8: Call create_repeated_entries()

```python
create_repeated_entries(data)
```

### Step 9: Assign docnames = frappe.get_all(...)

```python
docnames = frappe.get_all(doc.reference_doctype, filters={'auto_repeat': doc.name}, fields=['docstatus'], limit=1)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(docnames[0].docstatus, 1)
```


## Complete Example

```python
# Workflow
doctype = 'Test Submittable DocType'
create_submittable_doctype(doctype)
current_date = getdate()
submittable_doc = frappe.get_doc(doctype=doctype, test='test submit on creation').insert()
submittable_doc.submit()
doc = make_auto_repeat(frequency='Daily', reference_doctype=doctype, reference_document=submittable_doc.name, start_date=add_days(current_date, -1), submit_on_creation=1)
data = get_auto_repeat_entries(current_date)
create_repeated_entries(data)
docnames = frappe.get_all(doc.reference_doctype, filters={'auto_repeat': doc.name}, fields=['docstatus'], limit=1)
self.assertEqual(docnames[0].docstatus, 1)
```

## Next Steps


---

*Source: test_auto_repeat.py:228 | Complexity: Advanced | Last updated: 2026-02-04*