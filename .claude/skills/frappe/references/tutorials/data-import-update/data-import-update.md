# How To: Data Import Update

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test data import update

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.core.doctype.data_import.importer`
- `frappe.tests`
- `frappe.tests.test_query_builder`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Assign existing_doc = frappe.get_doc(...)

```python
existing_doc = frappe.get_doc(doctype=doctype_name, title=frappe.generate_hash(length=8), table_field_1=[{'child_title': 'child title to update'}])
```

### Step 2: Call existing_doc.save()

```python
existing_doc.save()
```

### Step 3: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 4: Assign import_file = get_import_file(...)

```python
import_file = get_import_file('sample_import_file_for_update')
```

### Step 5: Assign data_import = self.get_importer(...)

```python
data_import = self.get_importer(doctype_name, import_file, update=True)
```

### Step 6: Assign i = Importer(...)

```python
i = Importer(data_import.reference_doctype, data_import=data_import)
```

### Step 7: Assign unknown = value

```python
i.import_file.raw_data[1][4] = existing_doc.table_field_1[0].name
```

### Step 8: Call i.import_file.parse_data_from_template()

```python
i.import_file.parse_data_from_template()
```

### Step 9: Call i.import_data()

```python
i.import_data()
```

### Step 10: Assign updated_doc = frappe.get_doc(...)

```python
updated_doc = frappe.get_doc(doctype_name, existing_doc.name)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(existing_doc.title, updated_doc.title)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(updated_doc.description, 'test description')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(updated_doc.table_field_1[0].child_title, 'child title')
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(updated_doc.table_field_1[0].name, existing_doc.table_field_1[0].name)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(updated_doc.table_field_1[0].child_description, 'child description')
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(updated_doc.table_field_1_again[0].child_title, 'child title again')
```

### Step 17: Assign unknown = existing_doc.name.upper(...)

```python
i.import_file.raw_data[1][0] = existing_doc.name.upper()
```

### Step 18: Assign unknown = value

```python
i.import_file.raw_data[1][0] = existing_doc.name
```


## Complete Example

```python
# Workflow
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

## Next Steps


---

*Source: test_importer.py:116 | Complexity: Advanced | Last updated: 2026-02-04*