# How To: Edit Field Nullable Status

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test edit field nullable status

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.database.schema`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc(doctype=self.nullable_doctype_name)
```

### Step 2: Call doc.insert()

```python
doc.insert()
```

### Step 3: Assign inserted_doc = frappe.db.get(...)

```python
inserted_doc = frappe.db.get(self.nullable_doctype_name, {'name': doc.name})
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(inserted_doc.test_field, None)
```

### Step 5: Assign table = DBTable(...)

```python
table = DBTable(self.nullable_doctype_name)
```

### Step 6: Assign query = "SELECT column_name AS name, column_default is NULL AS default_null,is_nullable = 'NO' AS not_nullable FROM information_schema.columns WHERE table_name=%s"

```python
query = "SELECT column_name AS name, column_default is NULL AS default_null,is_nullable = 'NO' AS not_nullable FROM information_schema.columns WHERE table_name=%s"
```

### Step 7: Assign doctype_doc = frappe.get_doc(...)

```python
doctype_doc = frappe.get_doc('DocType', self.nullable_doctype_name)
```

### Step 8: Call doctype_doc.save()

```python
doctype_doc.save()
```

### Step 9: Assign inserted_doc = frappe.db.get(...)

```python
inserted_doc = frappe.db.get(self.nullable_doctype_name, {'name': doc.name})
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(inserted_doc.test_field, '')
```

### Step 11: Call self.assertFalse()

```python
self.assertFalse(column.not_nullable)
```

### Step 12: Assign field.not_nullable = 1

```python
field.not_nullable = 1
```

### Step 13: Call self.assertFalse()

```python
self.assertFalse(column.default_null)
```

### Step 14: Call self.assertTrue()

```python
self.assertTrue(column.not_nullable)
```


## Complete Example

```python
# Workflow
doc = frappe.new_doc(doctype=self.nullable_doctype_name)
doc.insert()
inserted_doc = frappe.db.get(self.nullable_doctype_name, {'name': doc.name})
self.assertEqual(inserted_doc.test_field, None)
table = DBTable(self.nullable_doctype_name)
query = "SELECT column_name AS name, column_default is NULL AS default_null,is_nullable = 'NO' AS not_nullable FROM information_schema.columns WHERE table_name=%s"
for column in frappe.db.sql(query, table.table_name, as_dict=True):
    if column.name == 'test_field':
        self.assertFalse(column.not_nullable)
doctype_doc = frappe.get_doc('DocType', self.nullable_doctype_name)
for field in doctype_doc.fields:
    if field.fieldname == 'test_field':
        field.not_nullable = 1
        break
doctype_doc.save()
for column in frappe.db.sql(query, table.table_name, as_dict=True):
    if column.name == 'test_field':
        self.assertFalse(column.default_null)
        self.assertTrue(column.not_nullable)
inserted_doc = frappe.db.get(self.nullable_doctype_name, {'name': doc.name})
self.assertEqual(inserted_doc.test_field, '')
```

## Next Steps


---

*Source: test_non_nullable_docfield.py:40 | Complexity: Advanced | Last updated: 2026-02-04*