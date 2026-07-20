# How To: Data Import Without Label

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test fallback to fieldname when label is not set for a table.

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.core.doctype.data_import.importer`
- `frappe.tests`
- `frappe.tests.test_query_builder`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: 'Test fallback to fieldname when label is not set for a table.'

```python
'Test fallback to fieldname when label is not set for a table.'
```

### Step 2: Assign meta = frappe.get_meta(...)

```python
meta = frappe.get_meta(doctype_name)
```

### Step 3: Assign table_field = meta.get_field(...)

```python
table_field = meta.get_field('table_field_1')
```

### Step 4: Assign original_label = value

```python
original_label = table_field.label
```

### Step 5: Assign table_field.label = None

```python
table_field.label = None
```

### Step 6: Assign fields_dict = build_fields_dict_for_column_matching(...)

```python
fields_dict = build_fields_dict_for_column_matching(doctype_name)
```

### Step 7: Assign expected_key = 'Child Title (table_field_1)'

```python
expected_key = 'Child Title (table_field_1)'
```

### Step 8: Call self.assertIn()

```python
self.assertIn(expected_key, fields_dict, f"Fallback failed: '{expected_key}' not found in mapping dict")
```

### Step 9: Assign expected_id_key = 'ID (table_field_1)'

```python
expected_id_key = 'ID (table_field_1)'
```

### Step 10: Call self.assertIn()

```python
self.assertIn(expected_id_key, fields_dict, 'ID fallback failed')
```

### Step 11: Assign table_field.label = original_label

```python
table_field.label = original_label
```


## Complete Example

```python
# Workflow
'Test fallback to fieldname when label is not set for a table.'
meta = frappe.get_meta(doctype_name)
table_field = meta.get_field('table_field_1')
original_label = table_field.label
table_field.label = None
fields_dict = build_fields_dict_for_column_matching(doctype_name)
expected_key = 'Child Title (table_field_1)'
self.assertIn(expected_key, fields_dict, f"Fallback failed: '{expected_key}' not found in mapping dict")
expected_id_key = 'ID (table_field_1)'
self.assertIn(expected_id_key, fields_dict, 'ID fallback failed')
table_field.label = original_label
```

## Next Steps


---

*Source: test_importer.py:149 | Complexity: Advanced | Last updated: 2026-02-04*