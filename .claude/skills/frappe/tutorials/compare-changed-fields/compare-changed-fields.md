# How To: Compare Changed Fields

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test compare changed fields

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

### Step 2: Assign doc.test_field = 'first value'

```python
doc.test_field = 'first value'
```

### Step 3: Call doc.submit()

```python
doc.submit()
```

### Step 4: Call doc.cancel()

```python
doc.cancel()
```

### Step 5: Assign changed_fields = frappe._dict(...)

```python
changed_fields = frappe._dict(test_field='second value')
```

### Step 6: Assign amended_doc = amend_document(...)

```python
amended_doc = amend_document(doc, changed_fields, {}, 1)
```

### Step 7: Call amended_doc.cancel()

```python
amended_doc.cancel()
```

### Step 8: Assign changed_fields = frappe._dict(...)

```python
changed_fields = frappe._dict(test_field='third value')
```

### Step 9: Assign re_amended_doc = amend_document(...)

```python
re_amended_doc = amend_document(amended_doc, changed_fields, {}, 1)
```

### Step 10: Assign comparator = create_comparator_doc(...)

```python
comparator = create_comparator_doc('Test Custom Doctype for Doc Comparator', re_amended_doc.name)
```

### Step 11: Assign unknown = comparator.compare_document(...)

```python
_documents, results = comparator.compare_document()
```

### Step 12: Assign test_field_values = value

```python
test_field_values = results['changed']['Field']
```

### Step 13: Call self.check_expected_values()

```python
self.check_expected_values(test_field_values, ['first value', 'second value', 'third value'])
```


## Complete Example

```python
# Workflow
doc = frappe.new_doc('Test Custom Doctype for Doc Comparator')
doc.test_field = 'first value'
doc.submit()
doc.cancel()
changed_fields = frappe._dict(test_field='second value')
amended_doc = amend_document(doc, changed_fields, {}, 1)
amended_doc.cancel()
changed_fields = frappe._dict(test_field='third value')
re_amended_doc = amend_document(amended_doc, changed_fields, {}, 1)
comparator = create_comparator_doc('Test Custom Doctype for Doc Comparator', re_amended_doc.name)
_documents, results = comparator.compare_document()
test_field_values = results['changed']['Field']
self.check_expected_values(test_field_values, ['first value', 'second value', 'third value'])
```

## Next Steps


---

*Source: test_audit_trail.py:14 | Complexity: Advanced | Last updated: 2026-02-04*