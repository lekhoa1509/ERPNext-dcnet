# How To: Uuid Varchar Migration

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test uuid varchar migration

## Prerequisites

**Required Modules:**
- `random`
- `unittest.case`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.utils`
- `frappe.custom.doctype.property_setter.property_setter`
- `frappe.query_builder.utils`
- `frappe.tests`
- `frappe.tests.test_query_builder`
- `frappe.utils`
- `frappe.database.schema`


## Step-by-Step Guide

### Step 1: Assign doctype = new_doctype.insert(...)

```python
doctype = new_doctype().insert()
```

### Step 2: Assign doctype.autoname = 'UUID'

```python
doctype.autoname = 'UUID'
```

### Step 3: Call doctype.save()

```python
doctype.save()
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_column_type(doctype.name, 'name'), 'uuid')
```

### Step 5: Assign doc = frappe.new_doc.insert(...)

```python
doc = frappe.new_doc(doctype.name).insert()
```

### Step 6: Assign doctype.autoname = 'hash'

```python
doctype.autoname = 'hash'
```

### Step 7: Call doctype.save()

```python
doctype.save()
```

### Step 8: Assign varchar = value

```python
varchar = 'varchar' if frappe.db.db_type == 'mariadb' else 'character varying'
```

### Step 9: Call self.assertIn()

```python
self.assertIn(varchar, frappe.db.get_column_type(doctype.name, 'name'))
```

### Step 10: Call doc.reload()

```python
doc.reload()
```


## Complete Example

```python
# Workflow
doctype = new_doctype().insert()
doctype.autoname = 'UUID'
doctype.save()
self.assertEqual(frappe.db.get_column_type(doctype.name, 'name'), 'uuid')
doc = frappe.new_doc(doctype.name).insert()
doctype.autoname = 'hash'
doctype.save()
varchar = 'varchar' if frappe.db.db_type == 'mariadb' else 'character varying'
self.assertIn(varchar, frappe.db.get_column_type(doctype.name, 'name'))
doc.reload()
```

## Next Steps


---

*Source: test_db_update.py:173 | Complexity: Advanced | Last updated: 2026-02-04*