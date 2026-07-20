# How To: Data Import From File

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test data import from file

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
import_file = get_import_file('sample_import_file')
```

### Step 2: Assign data_import = self.get_importer(...)

```python
data_import = self.get_importer(doctype_name, import_file)
```

### Step 3: Call data_import.start_import()

```python
data_import.start_import()
```

### Step 4: Assign doc1 = frappe.get_doc(...)

```python
doc1 = frappe.get_doc(doctype_name, 'Test')
```

### Step 5: Assign doc2 = frappe.get_doc(...)

```python
doc2 = frappe.get_doc(doctype_name, 'Test 2')
```

### Step 6: Assign doc3 = frappe.get_doc(...)

```python
doc3 = frappe.get_doc(doctype_name, 'Test 3')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(doc1.description, 'test description')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(doc1.number, 1)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(format_duration(doc1.duration), '3h')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(doc1.table_field_1[0].child_title, 'child title')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(doc1.table_field_1[0].child_description, 'child description')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(doc1.table_field_1[1].child_title, 'child title 2')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(doc1.table_field_1[1].child_description, 'child description 2')
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(doc1.table_field_2[1].child_2_title, 'title child')
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(doc1.table_field_2[1].child_2_date, getdate('2019-10-30'))
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(doc1.table_field_2[1].child_2_another_number, 5)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(doc1.table_field_1_again[0].child_title, 'child title again')
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(doc1.table_field_1_again[1].child_title, 'child title again 2')
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(doc1.table_field_1_again[1].child_date, getdate('2021-09-22'))
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(doc2.description, 'test description 2')
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(format_duration(doc2.duration), '4d 3h')
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(doc3.another_number, 5)
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(format_duration(doc3.duration), '5d 5h 45m')
```


## Complete Example

```python
# Workflow
import_file = get_import_file('sample_import_file')
data_import = self.get_importer(doctype_name, import_file)
data_import.start_import()
doc1 = frappe.get_doc(doctype_name, 'Test')
doc2 = frappe.get_doc(doctype_name, 'Test 2')
doc3 = frappe.get_doc(doctype_name, 'Test 3')
self.assertEqual(doc1.description, 'test description')
self.assertEqual(doc1.number, 1)
self.assertEqual(format_duration(doc1.duration), '3h')
self.assertEqual(doc1.table_field_1[0].child_title, 'child title')
self.assertEqual(doc1.table_field_1[0].child_description, 'child description')
self.assertEqual(doc1.table_field_1[1].child_title, 'child title 2')
self.assertEqual(doc1.table_field_1[1].child_description, 'child description 2')
self.assertEqual(doc1.table_field_2[1].child_2_title, 'title child')
self.assertEqual(doc1.table_field_2[1].child_2_date, getdate('2019-10-30'))
self.assertEqual(doc1.table_field_2[1].child_2_another_number, 5)
self.assertEqual(doc1.table_field_1_again[0].child_title, 'child title again')
self.assertEqual(doc1.table_field_1_again[1].child_title, 'child title again 2')
self.assertEqual(doc1.table_field_1_again[1].child_date, getdate('2021-09-22'))
self.assertEqual(doc2.description, 'test description 2')
self.assertEqual(format_duration(doc2.duration), '4d 3h')
self.assertEqual(doc3.another_number, 5)
self.assertEqual(format_duration(doc3.duration), '5d 5h 45m')
```

## Next Steps


---

*Source: test_importer.py:20 | Complexity: Advanced | Last updated: 2026-02-04*