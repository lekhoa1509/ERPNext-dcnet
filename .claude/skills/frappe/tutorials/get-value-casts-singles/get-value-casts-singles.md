# How To: Get Value Casts Singles

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get value casts singles

## Prerequisites

**Required Modules:**
- `datetime`
- `math`
- `random`
- `unittest.mock`
- `frappe`
- `frappe.core.utils`
- `frappe.custom.doctype.custom_field.custom_field`
- `frappe.database`
- `frappe.database.database`
- `frappe.database.utils`
- `frappe.query_builder`
- `frappe.query_builder.functions`
- `frappe.tests`
- `frappe.tests.test_query_builder`
- `frappe.utils`
- `frappe.utils.data`
- `frappe.utils.testutils`
- `frappe.database.database`
- `frappe.database.postgres.database`
- `frappe.database.postgres.database`
- `psycopg2.errors`
- `frappe.core.doctype.doctype.test_doctype`
- `contextlib`
- `os`
- `re`
- `frappe.database.postgres.database`


## Step-by-Step Guide

### Step 1: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc('System Settings')
```

### Step 2: Assign results = frappe.db.get_value(...)

```python
results = frappe.db.get_value('System Settings', None, ['language', 'date_format'], as_dict=True)
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(doc.language, results.language)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(doc.date_format, results.date_format)
```

### Step 5: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc('System Settings')
```

### Step 6: Assign unknown = frappe.db.get_value(...)

```python
[lang, date_format] = frappe.db.get_value('System Settings', None, ['language', 'date_format'])
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(doc.language, lang)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(doc.date_format, date_format)
```

### Step 9: Assign results = frappe.db.get_value(...)

```python
results = frappe.db.get_value('System Settings', None, 'enable_telemetry', as_dict=True)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(results, {'enable_telemetry': doc.enable_telemetry})
```


## Complete Example

```python
# Workflow
doc = frappe.get_doc('System Settings')
results = frappe.db.get_value('System Settings', None, ['language', 'date_format'], as_dict=True)
self.assertEqual(doc.language, results.language)
self.assertEqual(doc.date_format, results.date_format)
doc = frappe.get_doc('System Settings')
[lang, date_format] = frappe.db.get_value('System Settings', None, ['language', 'date_format'])
self.assertEqual(doc.language, lang)
self.assertEqual(doc.date_format, date_format)
results = frappe.db.get_value('System Settings', None, 'enable_telemetry', as_dict=True)
self.assertEqual(results, {'enable_telemetry': doc.enable_telemetry})
```

## Next Steps


---

*Source: test_db.py:201 | Complexity: Advanced | Last updated: 2026-02-04*