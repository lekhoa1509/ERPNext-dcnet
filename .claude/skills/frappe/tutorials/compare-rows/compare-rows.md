# How To: Compare Rows

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test compare rows

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc('Test Custom Doctype for Doc Comparator')
```

### Step 2: Call doc.append()

```python
doc.append('child_table_field', {'test_table_field': 'old row 1 value'})
```

### Step 3: Call doc.submit()

```python
doc.submit()
```

### Step 4: Call doc.cancel()

```python
doc.cancel()
```

### Step 5: Assign child_table_new = value

```python
child_table_new = [{'test_table_field': 'new row 1 value'}, {'test_table_field': 'row 2 value'}]
```

### Step 6: Assign rows_updated = frappe._dict(...)

```python
rows_updated = frappe._dict(child_table_field=child_table_new)
```

### Step 7: Assign amended_doc = amend_document(...)

```python
amended_doc = amend_document(doc, {}, rows_updated, 1)
```

### Step 8: Assign comparator = create_comparator_doc(...)

```python
comparator = create_comparator_doc('Test Custom Doctype for Doc Comparator', amended_doc.name)
```

### Step 9: Assign unknown = comparator.compare_document(...)

```python
_documents, results = comparator.compare_document()
```

### Step 10: Assign results = frappe._dict(...)

```python
results = frappe._dict(results)
```

### Step 11: Call self.check_rows_updated()

```python
self.check_rows_updated(results.row_changed)
```

### Step 12: Call self.check_rows_added()

```python
self.check_rows_added(results.added[amended_doc.name])
```


## Complete Example

```python
# Workflow
doc = frappe.new_doc('Test Custom Doctype for Doc Comparator')
doc.append('child_table_field', {'test_table_field': 'old row 1 value'})
doc.submit()
doc.cancel()
child_table_new = [{'test_table_field': 'new row 1 value'}, {'test_table_field': 'row 2 value'}]
rows_updated = frappe._dict(child_table_field=child_table_new)
amended_doc = amend_document(doc, {}, rows_updated, 1)
comparator = create_comparator_doc('Test Custom Doctype for Doc Comparator', amended_doc.name)
_documents, results = comparator.compare_document()
results = frappe._dict(results)
self.check_rows_updated(results.row_changed)
self.check_rows_added(results.added[amended_doc.name])
```

## Next Steps


---

*Source: test_audit_trail.py:33 | Complexity: Advanced | Last updated: 2026-02-04*