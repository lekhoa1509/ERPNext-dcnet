# How To: Naming For Cancelled And Amended Doc

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test naming for cancelled and amended doc

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

### Step 1: Assign submittable_doctype = frappe.get_doc.insert(...)

```python
submittable_doctype = frappe.get_doc({'doctype': 'DocType', 'module': 'Core', 'custom': 1, 'is_submittable': 1, 'permissions': [{'role': 'System Manager', 'read': 1}], 'name': 'Submittable Doctype'}).insert(ignore_if_duplicate=True)
```

### Step 2: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc('Submittable Doctype')
```

### Step 3: Call doc.save()

```python
doc.save()
```

### Step 4: Assign original_name = value

```python
original_name = doc.name
```

### Step 5: Call doc.submit()

```python
doc.submit()
```

### Step 6: Call doc.cancel()

```python
doc.cancel()
```

### Step 7: Assign cancelled_name = value

```python
cancelled_name = doc.name
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(cancelled_name, original_name)
```

### Step 9: Assign amended_doc = frappe.copy_doc(...)

```python
amended_doc = frappe.copy_doc(doc)
```

### Step 10: Assign amended_doc.docstatus = 0

```python
amended_doc.docstatus = 0
```

### Step 11: Assign amended_doc.amended_from = value

```python
amended_doc.amended_from = doc.name
```

### Step 12: Call amended_doc.save()

```python
amended_doc.save()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(amended_doc.name, f'{original_name}-1')
```

### Step 14: Call amended_doc.submit()

```python
amended_doc.submit()
```

### Step 15: Call amended_doc.cancel()

```python
amended_doc.cancel()
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(amended_doc.name, f'{original_name}-1')
```

### Step 17: Call submittable_doctype.delete()

```python
submittable_doctype.delete()
```


## Complete Example

```python
# Setup
frappe.db.delete('Note')

# Workflow
submittable_doctype = frappe.get_doc({'doctype': 'DocType', 'module': 'Core', 'custom': 1, 'is_submittable': 1, 'permissions': [{'role': 'System Manager', 'read': 1}], 'name': 'Submittable Doctype'}).insert(ignore_if_duplicate=True)
doc = frappe.new_doc('Submittable Doctype')
doc.save()
original_name = doc.name
doc.submit()
doc.cancel()
cancelled_name = doc.name
self.assertEqual(cancelled_name, original_name)
amended_doc = frappe.copy_doc(doc)
amended_doc.docstatus = 0
amended_doc.amended_from = doc.name
amended_doc.save()
self.assertEqual(amended_doc.name, f'{original_name}-1')
amended_doc.submit()
amended_doc.cancel()
self.assertEqual(amended_doc.name, f'{original_name}-1')
submittable_doctype.delete()
```

## Next Steps


---

*Source: test_naming.py:220 | Complexity: Advanced | Last updated: 2026-02-04*