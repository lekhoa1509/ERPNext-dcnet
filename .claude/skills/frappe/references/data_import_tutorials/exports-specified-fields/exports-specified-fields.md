# How To: Exports Specified Fields

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test exports specified fields

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.core.doctype.data_import.exporter`
- `frappe.core.doctype.data_import.test_importer`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign e = Exporter(...)

```python
e = Exporter(doctype_name, export_fields={doctype_name: ['title', 'description', 'number', 'another_number'], 'table_field_1': ['name', 'child_title', 'child_description'], 'table_field_2': ['child_2_date', 'child_2_number'], 'table_field_1_again': ['child_title', 'child_date', 'child_number', 'child_another_number']}, export_data=True)
```

### Step 2: Assign csv_array = e.get_csv_array(...)

```python
csv_array = e.get_csv_array()
```

### Step 3: Assign header_row = value

```python
header_row = csv_array[0]
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(header_row, ['Title', 'Description', 'Number', 'another_number', 'ID (Table Field 1)', 'Child Title (Table Field 1)', 'Child Description (Table Field 1)', 'Child 2 Date (Table Field 2)', 'Child 2 Number (Table Field 2)', 'Child Title (Table Field 1 Again)', 'Child Date (Table Field 1 Again)', 'Child Number (Table Field 1 Again)', 'table_field_1_again.child_another_number'])
```

### Step 5: Assign table_field_1_row_1_name = value

```python
table_field_1_row_1_name = doc.table_field_1[0].name
```

### Step 6: Assign table_field_1_row_2_name = value

```python
table_field_1_row_2_name = doc.table_field_1[1].name
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(csv_array[1], ['Test', 'Test Description', 0, 0, table_field_1_row_1_name, 'Child Title 1', 'Child Description 1', None, 0, 'Child Title 1 Again', None, 0, 0])
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(csv_array[2], ['', '', '', '', table_field_1_row_2_name, 'Child Title 2', 'Child Description 2', '', '', '', '', '', ''])
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(csv_array), 3)
```

### Step 10: Assign doc = frappe.get_doc.insert(...)

```python
doc = frappe.get_doc(doctype=doctype_name, title='Test', description='Test Description', table_field_1=[{'child_title': 'Child Title 1', 'child_description': 'Child Description 1'}, {'child_title': 'Child Title 2', 'child_description': 'Child Description 2'}], table_field_2=[{'child_2_title': 'Child Title 1', 'child_2_description': 'Child Description 1'}], table_field_1_again=[{'child_title': 'Child Title 1 Again', 'child_description': 'Child Description 1 Again'}]).insert()
```

### Step 11: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc(doctype_name, 'Test')
```


## Complete Example

```python
# Workflow
if not frappe.db.exists(doctype_name, 'Test'):
    doc = frappe.get_doc(doctype=doctype_name, title='Test', description='Test Description', table_field_1=[{'child_title': 'Child Title 1', 'child_description': 'Child Description 1'}, {'child_title': 'Child Title 2', 'child_description': 'Child Description 2'}], table_field_2=[{'child_2_title': 'Child Title 1', 'child_2_description': 'Child Description 1'}], table_field_1_again=[{'child_title': 'Child Title 1 Again', 'child_description': 'Child Description 1 Again'}]).insert()
else:
    doc = frappe.get_doc(doctype_name, 'Test')
e = Exporter(doctype_name, export_fields={doctype_name: ['title', 'description', 'number', 'another_number'], 'table_field_1': ['name', 'child_title', 'child_description'], 'table_field_2': ['child_2_date', 'child_2_number'], 'table_field_1_again': ['child_title', 'child_date', 'child_number', 'child_another_number']}, export_data=True)
csv_array = e.get_csv_array()
header_row = csv_array[0]
self.assertEqual(header_row, ['Title', 'Description', 'Number', 'another_number', 'ID (Table Field 1)', 'Child Title (Table Field 1)', 'Child Description (Table Field 1)', 'Child 2 Date (Table Field 2)', 'Child 2 Number (Table Field 2)', 'Child Title (Table Field 1 Again)', 'Child Date (Table Field 1 Again)', 'Child Number (Table Field 1 Again)', 'table_field_1_again.child_another_number'])
table_field_1_row_1_name = doc.table_field_1[0].name
table_field_1_row_2_name = doc.table_field_1[1].name
self.assertEqual(csv_array[1], ['Test', 'Test Description', 0, 0, table_field_1_row_1_name, 'Child Title 1', 'Child Description 1', None, 0, 'Child Title 1 Again', None, 0, 0])
self.assertEqual(csv_array[2], ['', '', '', '', table_field_1_row_2_name, 'Child Title 2', 'Child Description 2', '', '', '', '', '', ''])
self.assertEqual(len(csv_array), 3)
```

## Next Steps


---

*Source: test_exporter.py:15 | Complexity: Advanced | Last updated: 2026-02-04*