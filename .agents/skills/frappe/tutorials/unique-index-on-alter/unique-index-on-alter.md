# How To: Unique Index On Alter

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Only one unique index should be added

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

### Step 1: 'Only one unique index should be added'

```python
'Only one unique index should be added'
```

### Step 2: Assign doctype = new_doctype.insert(...)

```python
doctype = new_doctype(unique=1).insert()
```

### Step 3: Assign field = 'some_fieldname'

```python
field = 'some_fieldname'
```

### Step 4: Call self.check_unique_indexes()

```python
self.check_unique_indexes(doctype.name, field)
```

### Step 5: Assign unknown.length = 142

```python
doctype.fields[0].length = 142
```

### Step 6: Call doctype.save()

```python
doctype.save()
```

### Step 7: Call self.check_unique_indexes()

```python
self.check_unique_indexes(doctype.name, field)
```

### Step 8: Assign unknown.unique = 0

```python
doctype.fields[0].unique = 0
```

### Step 9: Call doctype.save()

```python
doctype.save()
```

### Step 10: Assign unknown.unique = 1

```python
doctype.fields[0].unique = 1
```

### Step 11: Call doctype.save()

```python
doctype.save()
```

### Step 12: Call self.check_unique_indexes()

```python
self.check_unique_indexes(doctype.name, field)
```

### Step 13: Assign new_field = frappe.copy_doc(...)

```python
new_field = frappe.copy_doc(doctype.fields[0])
```

### Step 14: Assign new_field.fieldname = 'duplicate_field'

```python
new_field.fieldname = 'duplicate_field'
```

### Step 15: Call doctype.append()

```python
doctype.append('fields', new_field)
```

### Step 16: Call doctype.save()

```python
doctype.save()
```

### Step 17: Call self.check_unique_indexes()

```python
self.check_unique_indexes(doctype.name, new_field.fieldname)
```

### Step 18: Call doctype.delete()

```python
doctype.delete()
```

### Step 19: Call frappe.db.commit()

```python
frappe.db.commit()
```


## Complete Example

```python
# Workflow
'Only one unique index should be added'
doctype = new_doctype(unique=1).insert()
try:
    field = 'some_fieldname'
    self.check_unique_indexes(doctype.name, field)
    doctype.fields[0].length = 142
    doctype.save()
    self.check_unique_indexes(doctype.name, field)
    doctype.fields[0].unique = 0
    doctype.save()
    doctype.fields[0].unique = 1
    doctype.save()
    self.check_unique_indexes(doctype.name, field)
    new_field = frappe.copy_doc(doctype.fields[0])
    new_field.fieldname = 'duplicate_field'
    doctype.append('fields', new_field)
    doctype.save()
    self.check_unique_indexes(doctype.name, new_field.fieldname)
finally:
    doctype.delete()
    frappe.db.commit()
```

## Next Steps


---

*Source: test_db_update.py:143 | Complexity: Advanced | Last updated: 2026-02-04*