# How To: Data Import Without Mandatory Values

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test data import without mandatory values

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.core.doctype.data_import.importer`
- `frappe.tests`
- `frappe.tests.test_query_builder`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Assign import_file = get_import_file(...)

```python
import_file = get_import_file('sample_import_file_without_mandatory')
```

### Step 2: Assign data_import = self.get_importer(...)

```python
data_import = self.get_importer(doctype_name, import_file)
```

### Step 3: Call frappe.clear_messages()

```python
frappe.clear_messages()
```

### Step 4: Call data_import.start_import()

```python
data_import.start_import()
```

### Step 5: Call data_import.reload()

```python
data_import.reload()
```

### Step 6: Assign import_log = frappe.get_all(...)

```python
import_log = frappe.get_all('Data Import Log', fields=['row_indexes', 'success', 'messages', 'exception', 'docname'], filters={'data_import': data_import.name}, order_by='log_index')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(frappe.parse_json(import_log[0]['row_indexes']), [2, 3])
```

### Step 8: Assign expected_error = 'Error: <strong>Child 1 of DocType for Import</strong> Row #1: Value missing for: Child Title'

```python
expected_error = 'Error: <strong>Child 1 of DocType for Import</strong> Row #1: Value missing for: Child Title'
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(frappe.parse_json(frappe.parse_json(import_log[0]['messages'])[0])['message'], expected_error)
```

### Step 10: Assign expected_error = 'Error: <strong>Child 1 of DocType for Import</strong> Row #2: Value missing for: Child Title'

```python
expected_error = 'Error: <strong>Child 1 of DocType for Import</strong> Row #2: Value missing for: Child Title'
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(frappe.parse_json(frappe.parse_json(import_log[0]['messages'])[1])['message'], expected_error)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(frappe.parse_json(import_log[1]['row_indexes']), [4])
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(frappe.parse_json(frappe.parse_json(import_log[1]['messages'])[0])['message'], 'Title is required')
```


## Complete Example

```python
# Workflow
import_file = get_import_file('sample_import_file_without_mandatory')
data_import = self.get_importer(doctype_name, import_file)
frappe.clear_messages()
data_import.start_import()
data_import.reload()
import_log = frappe.get_all('Data Import Log', fields=['row_indexes', 'success', 'messages', 'exception', 'docname'], filters={'data_import': data_import.name}, order_by='log_index')
self.assertEqual(frappe.parse_json(import_log[0]['row_indexes']), [2, 3])
expected_error = 'Error: <strong>Child 1 of DocType for Import</strong> Row #1: Value missing for: Child Title'
self.assertEqual(frappe.parse_json(frappe.parse_json(import_log[0]['messages'])[0])['message'], expected_error)
expected_error = 'Error: <strong>Child 1 of DocType for Import</strong> Row #2: Value missing for: Child Title'
self.assertEqual(frappe.parse_json(frappe.parse_json(import_log[0]['messages'])[1])['message'], expected_error)
self.assertEqual(frappe.parse_json(import_log[1]['row_indexes']), [4])
self.assertEqual(frappe.parse_json(frappe.parse_json(import_log[1]['messages'])[0])['message'], 'Title is required')
```

## Next Steps


---

*Source: test_importer.py:82 | Complexity: Advanced | Last updated: 2026-02-04*