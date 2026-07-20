# How To: Child Table Doctype Creation And Transitioning

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: This method tests the creation of child table doctype
as well as it's transitioning from child table to normal and normal to child table doctype

## Prerequisites

**Required Modules:**
- `collections.abc`
- `frappe`
- `frappe.model`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: "\n\t\tThis method tests the creation of child table doctype\n\t\tas well as it's transitioning from child table to normal and normal to child table doctype\n\t\t"

```python
"\n\t\tThis method tests the creation of child table doctype\n\t\tas well as it's transitioning from child table to normal and normal to child table doctype\n\t\t"
```

### Step 2: Assign self.doctype_name = 'Test Newy Child Table'

```python
self.doctype_name = 'Test Newy Child Table'
```

### Step 3: Assign doc.istable = 0

```python
doc.istable = 0
```

### Step 4: Call self.check_valid_columns()

```python
self.check_valid_columns(self.assertFalse)
```

### Step 5: Assign doc.istable = 1

```python
doc.istable = 1
```

### Step 6: Call self.check_valid_columns()

```python
self.check_valid_columns(self.assertTrue)
```

### Step 7: Assign doc = frappe.get_doc.insert(...)

```python
doc = frappe.get_doc({'doctype': 'DocType', 'name': self.doctype_name, 'istable': 1, 'custom': 1, 'module': 'Integrations', 'fields': [{'label': 'Some Field', 'fieldname': 'some_fieldname', 'fieldtype': 'Data', 'reqd': 1}]}).insert(ignore_permissions=True)
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(frappe.db.has_column(self.doctype_name, column))
```

### Step 9: Call doc.save()

```python
doc.save(ignore_permissions=True)
```

### Step 10: Call doc.save()

```python
doc.save(ignore_permissions=True)
```

### Step 11: Call self.fail()

```python
self.fail('Not able to create Child Table Doctype')
```

### Step 12: Call self.fail()

```python
self.fail('Not able to transition from Child Table Doctype to Normal Doctype')
```

### Step 13: Call self.fail()

```python
self.fail('Not able to transition from Normal Doctype to Child Table Doctype')
```


## Complete Example

```python
# Workflow
"\n\t\tThis method tests the creation of child table doctype\n\t\tas well as it's transitioning from child table to normal and normal to child table doctype\n\t\t"
self.doctype_name = 'Test Newy Child Table'
try:
    doc = frappe.get_doc({'doctype': 'DocType', 'name': self.doctype_name, 'istable': 1, 'custom': 1, 'module': 'Integrations', 'fields': [{'label': 'Some Field', 'fieldname': 'some_fieldname', 'fieldtype': 'Data', 'reqd': 1}]}).insert(ignore_permissions=True)
except Exception:
    self.fail('Not able to create Child Table Doctype')
for column in child_table_fields:
    self.assertTrue(frappe.db.has_column(self.doctype_name, column))
doc.istable = 0
try:
    doc.save(ignore_permissions=True)
except Exception:
    self.fail('Not able to transition from Child Table Doctype to Normal Doctype')
self.check_valid_columns(self.assertFalse)
doc.istable = 1
try:
    doc.save(ignore_permissions=True)
except Exception:
    self.fail('Not able to transition from Normal Doctype to Child Table Doctype')
self.check_valid_columns(self.assertTrue)
```

## Next Steps


---

*Source: test_child_table.py:15 | Complexity: Advanced | Last updated: 2026-02-04*