# How To: Child Table Naming

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test child table naming

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `time`
- `uuid`
- `uuid_utils`
- `tenacity`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.model.naming`
- `frappe.query_builder.utils`
- `frappe.tests`
- `frappe.tests.test_query_builder`
- `frappe.utils`
- `datetime`
- `datetime`
- `frappe.core.doctype.doctype.test_doctype`

**Setup Required:**
```python
frappe.db.delete('Note')
```

## Step-by-Step Guide

### Step 1: Assign child_dt_with_naming = new_doctype.insert(...)

```python
child_dt_with_naming = new_doctype(istable=1, autoname='field:some_fieldname').insert()
```

### Step 2: Assign dt_with_child_autoname = new_doctype.insert(...)

```python
dt_with_child_autoname = new_doctype(fields=[{'label': 'table with naming', 'fieldname': 'table_with_naming', 'options': child_dt_with_naming.name, 'fieldtype': 'Table'}]).insert()
```

### Step 3: Assign name = frappe.generate_hash(...)

```python
name = frappe.generate_hash(length=10)
```

### Step 4: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc(dt_with_child_autoname.name)
```

### Step 5: Call doc.append()

```python
doc.append('table_with_naming', {'some_fieldname': name})
```

### Step 6: Call doc.save()

```python
doc.save()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(doc.table_with_naming[0].name, name)
```

### Step 8: Assign unknown.some_fieldname = 'Something else'

```python
doc.table_with_naming[0].some_fieldname = 'Something else'
```

### Step 9: Call doc.save()

```python
doc.save()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(doc.table_with_naming[0].name, name)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(doc.table_with_naming[0].some_fieldname, name)
```

### Step 12: Call doc.delete()

```python
doc.delete()
```

### Step 13: Call dt_with_child_autoname.delete()

```python
dt_with_child_autoname.delete()
```

### Step 14: Call child_dt_with_naming.delete()

```python
child_dt_with_naming.delete()
```


## Complete Example

```python
# Setup
frappe.db.delete('Note')

# Workflow
child_dt_with_naming = new_doctype(istable=1, autoname='field:some_fieldname').insert()
dt_with_child_autoname = new_doctype(fields=[{'label': 'table with naming', 'fieldname': 'table_with_naming', 'options': child_dt_with_naming.name, 'fieldtype': 'Table'}]).insert()
name = frappe.generate_hash(length=10)
doc = frappe.new_doc(dt_with_child_autoname.name)
doc.append('table_with_naming', {'some_fieldname': name})
doc.save()
self.assertEqual(doc.table_with_naming[0].name, name)
doc.table_with_naming[0].some_fieldname = 'Something else'
doc.save()
self.assertEqual(doc.table_with_naming[0].name, name)
self.assertEqual(doc.table_with_naming[0].some_fieldname, name)
doc.delete()
dt_with_child_autoname.delete()
child_dt_with_naming.delete()
```

## Next Steps


---

*Source: test_naming.py:62 | Complexity: Advanced | Last updated: 2026-02-04*