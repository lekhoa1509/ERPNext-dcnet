# How To: Agg Funcs

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test agg funcs

## Prerequisites

**Required Modules:**
- `unittest`
- `collections.abc`
- `datetime`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.query_builder`
- `frappe.query_builder.builder`
- `frappe.query_builder.custom`
- `frappe.query_builder.functions`
- `frappe.query_builder.utils`
- `frappe.tests`
- `frappe.query_builder.terms`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder.utils`


## Step-by-Step Guide

### Step 1: Assign doc = new_doctype(...)

```python
doc = new_doctype(fields=[{'fieldname': 'number', 'fieldtype': 'Int', 'label': 'Number', 'reqd': 1}])
```

### Step 2: Call doc.insert()

```python
doc.insert()
```

### Step 3: Assign self.doctype_name = value

```python
self.doctype_name = doc.name
```

### Step 4: Call frappe.db.truncate()

```python
frappe.db.truncate(self.doctype_name)
```

### Step 5: Assign sample_data = value

```python
sample_data = {'doctype': self.doctype_name, 'number': 1}
```

### Step 6: Call frappe.get_doc.insert()

```python
frappe.get_doc(sample_data).insert(ignore_mandatory=True)
```

### Step 7: Assign unknown = 3

```python
sample_data['number'] = 3
```

### Step 8: Call frappe.get_doc.insert()

```python
frappe.get_doc(sample_data).insert(ignore_mandatory=True)
```

### Step 9: Assign unknown = 4

```python
sample_data['number'] = 4
```

### Step 10: Call frappe.get_doc.insert()

```python
frappe.get_doc(sample_data).insert(ignore_mandatory=True)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(frappe.qb.max(self.doctype_name, 'number'), 4)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(frappe.qb.min(self.doctype_name, 'number'), 1)
```

### Step 13: Call self.assertAlmostEqual()

```python
self.assertAlmostEqual(frappe.qb.avg(self.doctype_name, 'number'), 2.666, places=2)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(frappe.qb.sum(self.doctype_name, 'number'), 8.0)
```

### Step 15: Call frappe.db.rollback()

```python
frappe.db.rollback()
```


## Complete Example

```python
# Workflow
doc = new_doctype(fields=[{'fieldname': 'number', 'fieldtype': 'Int', 'label': 'Number', 'reqd': 1}])
doc.insert()
self.doctype_name = doc.name
frappe.db.truncate(self.doctype_name)
sample_data = {'doctype': self.doctype_name, 'number': 1}
frappe.get_doc(sample_data).insert(ignore_mandatory=True)
sample_data['number'] = 3
frappe.get_doc(sample_data).insert(ignore_mandatory=True)
sample_data['number'] = 4
frappe.get_doc(sample_data).insert(ignore_mandatory=True)
self.assertEqual(frappe.qb.max(self.doctype_name, 'number'), 4)
self.assertEqual(frappe.qb.min(self.doctype_name, 'number'), 1)
self.assertAlmostEqual(frappe.qb.avg(self.doctype_name, 'number'), 2.666, places=2)
self.assertEqual(frappe.qb.sum(self.doctype_name, 'number'), 8.0)
frappe.db.rollback()
```

## Next Steps


---

*Source: test_query_builder.py:324 | Complexity: Advanced | Last updated: 2026-02-04*