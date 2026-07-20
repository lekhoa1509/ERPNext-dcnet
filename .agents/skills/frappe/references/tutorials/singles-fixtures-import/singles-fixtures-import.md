# How To: Singles Fixtures Import

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test singles fixtures import

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
self.assertFalse(frappe.db.exists('DocType', 'temp_singles'))
```

### Step 2: Call self.create_new_doctype()

```python
self.create_new_doctype('temp_singles')
```

### Step 3: Assign dummy_name_list = value

```python
dummy_name_list = ['Phoebe']
```

### Step 4: Assign path_to_exported_fixtures = self.insert_dummy_data_and_export(...)

```python
path_to_exported_fixtures = self.insert_dummy_data_and_export('temp_singles', dummy_name_list)
```

### Step 5: Assign singles_doctype = frappe.qb.DocType(...)

```python
singles_doctype = frappe.qb.DocType('Singles')
```

### Step 6: Assign truncate_query = frappe.qb.from_.delete.where(...)

```python
truncate_query = frappe.qb.from_(singles_doctype).delete().where(singles_doctype.doctype == 'temp_singles')
```

### Step 7: Call truncate_query.run()

```python
truncate_query.run()
```

### Step 8: Call import_doc()

```python
import_doc(path_to_exported_fixtures)
```

### Step 9: Assign data = frappe.db.get_single_value(...)

```python
data = frappe.db.get_single_value('temp_singles', 'member_name')
```

### Step 10: Call truncate_query.run()

```python
truncate_query.run()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(data, dummy_name_list[0])
```

### Step 12: Call delete_doc()

```python
delete_doc('DocType', 'temp_singles', delete_permanently=True)
```

### Step 13: Call os.remove()

```python
os.remove(path_to_exported_fixtures)
```

### Step 14: Call frappe.db.commit()

```python
frappe.db.commit()
```


## Complete Example

```python
# Workflow
self.assertFalse(frappe.db.exists('DocType', 'temp_singles'))
self.create_new_doctype('temp_singles')
dummy_name_list = ['Phoebe']
path_to_exported_fixtures = self.insert_dummy_data_and_export('temp_singles', dummy_name_list)
singles_doctype = frappe.qb.DocType('Singles')
truncate_query = frappe.qb.from_(singles_doctype).delete().where(singles_doctype.doctype == 'temp_singles')
truncate_query.run()
import_doc(path_to_exported_fixtures)
data = frappe.db.get_single_value('temp_singles', 'member_name')
truncate_query.run()
self.assertEqual(data, dummy_name_list[0])
delete_doc('DocType', 'temp_singles', delete_permanently=True)
os.remove(path_to_exported_fixtures)
frappe.db.commit()
```

## Next Steps


---

*Source: test_fixture_import.py:58 | Complexity: Advanced | Last updated: 2026-02-04*