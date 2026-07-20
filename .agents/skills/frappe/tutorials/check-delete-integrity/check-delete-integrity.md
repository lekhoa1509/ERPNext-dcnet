# How To: Check Delete Integrity

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Don't allow deleting cancelled document if amendment exists

## Prerequisites

**Required Modules:**
- `random`
- `string`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.database`
- `frappe.desk.form`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: "Don't allow deleting cancelled document if amendment exists"

```python
"Don't allow deleting cancelled document if amendment exists"
```

### Step 2: Assign doc = frappe.get_doc.insert(...)

```python
doc = frappe.get_doc({'doctype': 'Parent DocType'}).insert()
```

### Step 3: Call doc.submit()

```python
doc.submit()
```

### Step 4: Call doc.cancel()

```python
doc.cancel()
```

### Step 5: Assign amendment = frappe.copy_doc(...)

```python
amendment = frappe.copy_doc(doc)
```

### Step 6: Assign amendment.amended_from = value

```python
amendment.amended_from = doc.name
```

### Step 7: Assign amendment.docstatus = 0

```python
amendment.docstatus = 0
```

### Step 8: Call amendment.insert()

```python
amendment.insert()
```

### Step 9: Call amendment.submit()

```python
amendment.submit()
```

### Step 10: Call self.assertRaises()

```python
self.assertRaises(frappe.LinkExistsError, doc.delete)
```


## Complete Example

```python
# Workflow
"Don't allow deleting cancelled document if amendment exists"
doc = frappe.get_doc({'doctype': 'Parent DocType'}).insert()
doc.submit()
doc.cancel()
amendment = frappe.copy_doc(doc)
amendment.amended_from = doc.name
amendment.docstatus = 0
amendment.insert()
amendment.submit()
self.assertRaises(frappe.LinkExistsError, doc.delete)
```

## Next Steps


---

*Source: test_linked_with.py:142 | Complexity: Advanced | Last updated: 2026-02-04*