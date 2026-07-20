# Test Example Extraction Report

**Total Examples**: 20  
**High Value Examples** (confidence > 0.7): 20  
**Average Complexity**: 0.79  

## Examples by Category

- **method_call**: 10
- **workflow**: 10

## Examples by Language

- **Python**: 20

## Extracted Examples

### test_data_import_from_file

**Category**: workflow  
**Description**: Workflow: test data import from file  
**Expected**: self.assertEqual(format_duration(doc3.duration), '5d 5h 45m')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
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

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_importer.py:20*

### test_data_import_without_mandatory_values

**Category**: workflow  
**Description**: Workflow: test data import without mandatory values  
**Expected**: self.assertEqual(frappe.parse_json(frappe.parse_json(import_log[1]['messages'])[0])['message'], 'Title is required')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
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

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_importer.py:82*

### test_data_import_update

**Category**: workflow  
**Description**: Workflow: test data import update  
**Expected**: self.assertEqual(updated_doc.table_field_1_again[0].child_title, 'child title again')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
existing_doc = frappe.get_doc(doctype=doctype_name, title=frappe.generate_hash(length=8), table_field_1=[{'child_title': 'child title to update'}])
existing_doc.save()
frappe.db.commit()
import_file = get_import_file('sample_import_file_for_update')
data_import = self.get_importer(doctype_name, import_file, update=True)
i = Importer(data_import.reference_doctype, data_import=data_import)
i.import_file.raw_data[1][4] = existing_doc.table_field_1[0].name
if frappe.db.db_type == 'mariadb':
    i.import_file.raw_data[1][0] = existing_doc.name.upper()
else:
    i.import_file.raw_data[1][0] = existing_doc.name
i.import_file.parse_data_from_template()
i.import_data()
updated_doc = frappe.get_doc(doctype_name, existing_doc.name)
self.assertEqual(existing_doc.title, updated_doc.title)
self.assertEqual(updated_doc.description, 'test description')
self.assertEqual(updated_doc.table_field_1[0].child_title, 'child title')
self.assertEqual(updated_doc.table_field_1[0].name, existing_doc.table_field_1[0].name)
self.assertEqual(updated_doc.table_field_1[0].child_description, 'child description')
self.assertEqual(updated_doc.table_field_1_again[0].child_title, 'child title again')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_importer.py:116*

### test_data_import_without_label

**Category**: workflow  
**Description**: Workflow: Test fallback to fieldname when label is not set for a table.  
**Expected**: self.assertIn(expected_id_key, fields_dict, 'ID fallback failed')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
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

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_importer.py:149*

### test_data_import_from_file

**Category**: workflow  
**Description**: Workflow: test data import from file  
**Expected**: self.assertEqual(format_duration(doc3.duration), '5d 5h 45m')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
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

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_importer.py:20*

### test_data_import_without_mandatory_values

**Category**: workflow  
**Description**: Workflow: test data import without mandatory values  
**Expected**: self.assertEqual(frappe.parse_json(frappe.parse_json(import_log[1]['messages'])[0])['message'], 'Title is required')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
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

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_importer.py:82*

### test_data_import_update

**Category**: workflow  
**Description**: Workflow: test data import update  
**Expected**: self.assertEqual(updated_doc.table_field_1_again[0].child_title, 'child title again')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
existing_doc = frappe.get_doc(doctype=doctype_name, title=frappe.generate_hash(length=8), table_field_1=[{'child_title': 'child title to update'}])
existing_doc.save()
frappe.db.commit()
import_file = get_import_file('sample_import_file_for_update')
data_import = self.get_importer(doctype_name, import_file, update=True)
i = Importer(data_import.reference_doctype, data_import=data_import)
i.import_file.raw_data[1][4] = existing_doc.table_field_1[0].name
if frappe.db.db_type == 'mariadb':
    i.import_file.raw_data[1][0] = existing_doc.name.upper()
else:
    i.import_file.raw_data[1][0] = existing_doc.name
i.import_file.parse_data_from_template()
i.import_data()
updated_doc = frappe.get_doc(doctype_name, existing_doc.name)
self.assertEqual(existing_doc.title, updated_doc.title)
self.assertEqual(updated_doc.description, 'test description')
self.assertEqual(updated_doc.table_field_1[0].child_title, 'child title')
self.assertEqual(updated_doc.table_field_1[0].name, existing_doc.table_field_1[0].name)
self.assertEqual(updated_doc.table_field_1[0].child_description, 'child description')
self.assertEqual(updated_doc.table_field_1_again[0].child_title, 'child title again')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_importer.py:116*

### test_data_import_without_label

**Category**: workflow  
**Description**: Workflow: Test fallback to fieldname when label is not set for a table.  
**Expected**: self.assertIn(expected_id_key, fields_dict, 'ID fallback failed')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
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

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_importer.py:149*

### test_exports_specified_fields

**Category**: workflow  
**Description**: Workflow: test exports specified fields  
**Expected**: self.assertEqual(len(csv_array), 3)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
create_doctype_if_not_exists(doctype_name)

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

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_exporter.py:15*

### test_exports_specified_fields

**Category**: workflow  
**Description**: Workflow: test exports specified fields  
**Expected**: self.assertEqual(len(csv_array), 3)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
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

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_exporter.py:15*

### test_data_import_from_file

**Category**: method_call  
**Description**: test data import from file  
**Expected**: self.assertEqual(doc1.number, 1)  
**Confidence**: 0.85  

```python
self.assertEqual(doc1.description, 'test description')
self.assertEqual(doc1.number, 1)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_importer.py:29*

### test_data_import_from_file

**Category**: method_call  
**Description**: test data import from file  
**Expected**: self.assertEqual(format_duration(doc1.duration), '3h')  
**Confidence**: 0.85  

```python
self.assertEqual(doc1.number, 1)
self.assertEqual(format_duration(doc1.duration), '3h')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_importer.py:30*

### test_exports_specified_fields

**Category**: method_call  
**Description**: test exports specified fields  
**Expected**: self.assertEqual(csv_array[2], ['', '', '', '', table_field_1_row_2_name, 'Child Title 2', 'Child Description 2', '', '', '', '', '', ''])  
**Confidence**: 0.85  

```python
# Setup
create_doctype_if_not_exists(doctype_name)

self.assertEqual(csv_array[1], ['Test', 'Test Description', 0, 0, table_field_1_row_1_name, 'Child Title 1', 'Child Description 1', None, 0, 'Child Title 1 Again', None, 0, 0])
self.assertEqual(csv_array[2], ['', '', '', '', table_field_1_row_2_name, 'Child Title 2', 'Child Description 2', '', '', '', '', '', ''])
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_exporter.py:78*

### test_exports_specified_fields

**Category**: method_call  
**Description**: test exports specified fields  
**Expected**: self.assertEqual(len(csv_array), 3)  
**Confidence**: 0.85  

```python
# Setup
create_doctype_if_not_exists(doctype_name)

self.assertEqual(csv_array[2], ['', '', '', '', table_field_1_row_2_name, 'Child Title 2', 'Child Description 2', '', '', '', '', '', ''])
self.assertEqual(len(csv_array), 3)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_exporter.py:82*

### test_export_csv_response

**Category**: method_call  
**Description**: test export csv response  
**Expected**: self.assertTrue(frappe.response['result'])  
**Confidence**: 0.85  

```python
# Setup
create_doctype_if_not_exists(doctype_name)

e.build_response()
self.assertTrue(frappe.response['result'])
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_exporter.py:96*

### test_export_csv_response

**Category**: method_call  
**Description**: test export csv response  
**Expected**: self.assertEqual(frappe.response['doctype'], doctype_name)  
**Confidence**: 0.85  

```python
# Setup
create_doctype_if_not_exists(doctype_name)

self.assertTrue(frappe.response['result'])
self.assertEqual(frappe.response['doctype'], doctype_name)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_exporter.py:98*

### test_export_csv_response

**Category**: method_call  
**Description**: test export csv response  
**Expected**: self.assertEqual(frappe.response['type'], 'csv')  
**Confidence**: 0.85  

```python
# Setup
create_doctype_if_not_exists(doctype_name)

self.assertEqual(frappe.response['doctype'], doctype_name)
self.assertEqual(frappe.response['type'], 'csv')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_exporter.py:99*

### test_exports_specified_fields

**Category**: method_call  
**Description**: test exports specified fields  
**Expected**: self.assertEqual(csv_array[2], ['', '', '', '', table_field_1_row_2_name, 'Child Title 2', 'Child Description 2', '', '', '', '', '', ''])  
**Confidence**: 0.85  

```python
self.assertEqual(csv_array[1], ['Test', 'Test Description', 0, 0, table_field_1_row_1_name, 'Child Title 1', 'Child Description 1', None, 0, 'Child Title 1 Again', None, 0, 0])
self.assertEqual(csv_array[2], ['', '', '', '', table_field_1_row_2_name, 'Child Title 2', 'Child Description 2', '', '', '', '', '', ''])
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_exporter.py:78*

### test_exports_specified_fields

**Category**: method_call  
**Description**: test exports specified fields  
**Expected**: self.assertEqual(len(csv_array), 3)  
**Confidence**: 0.85  

```python
self.assertEqual(csv_array[2], ['', '', '', '', table_field_1_row_2_name, 'Child Title 2', 'Child Description 2', '', '', '', '', '', ''])
self.assertEqual(len(csv_array), 3)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_exporter.py:82*

### test_export_csv_response

**Category**: method_call  
**Description**: test export csv response  
**Expected**: self.assertTrue(frappe.response['result'])  
**Confidence**: 0.85  

```python
e.build_response()
self.assertTrue(frappe.response['result'])
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/core/doctype/data_import/test_exporter.py:96*

