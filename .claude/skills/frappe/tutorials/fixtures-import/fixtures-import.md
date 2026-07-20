# How To: Fixtures Import

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test fixtures import

## Prerequisites

**Required Modules:**
- `os`
- `frappe`
- `frappe.core.doctype.data_import.data_import`
- `frappe.desk.form.save`
- `frappe.model.delete_doc`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Call self.assertFalse()

```python
self.assertFalse(frappe.db.exists('DocType', 'temp_doctype'))
```

### Step 2: Call self.create_new_doctype()

```python
self.create_new_doctype('temp_doctype')
```

### Step 3: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 4: Assign dummy_name_list = value

```python
dummy_name_list = ['jhon', 'jane']
```

### Step 5: Assign path_to_exported_fixtures = self.insert_dummy_data_and_export(...)

```python
path_to_exported_fixtures = self.insert_dummy_data_and_export('temp_doctype', dummy_name_list)
```

### Step 6: Call frappe.db.truncate()

```python
frappe.db.truncate('temp_doctype')
```

### Step 7: Call import_doc()

```python
import_doc(path_to_exported_fixtures)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(frappe.db.count('temp_doctype'), len(dummy_name_list))
```

### Step 9: Assign data = frappe.get_all(...)

```python
data = frappe.get_all('temp_doctype', 'member_name')
```

### Step 10: Call frappe.db.truncate()

```python
frappe.db.truncate('temp_doctype')
```

### Step 11: Assign imported_data = set(...)

```python
imported_data = set()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(set(dummy_name_list), imported_data)
```

### Step 13: Call delete_doc()

```python
delete_doc('DocType', 'temp_doctype', delete_permanently=True)
```

### Step 14: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 15: Call os.remove()

```python
os.remove(path_to_exported_fixtures)
```

### Step 16: Call imported_data.add()

```python
imported_data.add(item['member_name'])
```


## Complete Example

```python
# Workflow
self.assertFalse(frappe.db.exists('DocType', 'temp_doctype'))
self.create_new_doctype('temp_doctype')
frappe.db.commit()
dummy_name_list = ['jhon', 'jane']
path_to_exported_fixtures = self.insert_dummy_data_and_export('temp_doctype', dummy_name_list)
frappe.db.truncate('temp_doctype')
import_doc(path_to_exported_fixtures)
self.assertEqual(frappe.db.count('temp_doctype'), len(dummy_name_list))
data = frappe.get_all('temp_doctype', 'member_name')
frappe.db.truncate('temp_doctype')
imported_data = set()
for item in data:
    imported_data.add(item['member_name'])
self.assertEqual(set(dummy_name_list), imported_data)
delete_doc('DocType', 'temp_doctype', delete_permanently=True)
frappe.db.commit()
os.remove(path_to_exported_fixtures)
```

## Next Steps


---

*Source: test_fixture_import.py:31 | Complexity: Advanced | Last updated: 2026-02-04*