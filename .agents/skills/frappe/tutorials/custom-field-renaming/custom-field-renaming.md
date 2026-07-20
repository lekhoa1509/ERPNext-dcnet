# How To: Custom Field Renaming

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test custom field renaming

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.custom.doctype.custom_field.custom_field`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign field = create_custom_field(...)

```python
field = create_custom_field('ToDo', {'label': gen_fieldname()}, is_system_generated=False)
```

### Step 2: Assign old = value

```python
old = field.fieldname
```

### Step 3: Assign new = gen_fieldname(...)

```python
new = gen_fieldname()
```

### Step 4: Assign data = frappe.generate_hash(...)

```python
data = frappe.generate_hash()
```

### Step 5: Assign doc = frappe.get_doc.insert(...)

```python
doc = frappe.get_doc({'doctype': 'ToDo', old: data, 'description': 'Something'}).insert()
```

### Step 6: Call rename_fieldname()

```python
rename_fieldname(field.name, new)
```

### Step 7: Call field.reload()

```python
field.reload()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(field.fieldname, new)
```

### Step 9: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc('ToDo', doc.name)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(doc.get(new), data)
```

### Step 11: Call self.assertFalse()

```python
self.assertFalse(doc.get(old))
```

### Step 12: Call field.delete()

```python
field.delete()
```


## Complete Example

```python
# Workflow
def gen_fieldname():
    return 'test_' + frappe.generate_hash()
field = create_custom_field('ToDo', {'label': gen_fieldname()}, is_system_generated=False)
old = field.fieldname
new = gen_fieldname()
data = frappe.generate_hash()
doc = frappe.get_doc({'doctype': 'ToDo', old: data, 'description': 'Something'}).insert()
rename_fieldname(field.name, new)
field.reload()
self.assertEqual(field.fieldname, new)
doc = frappe.get_doc('ToDo', doc.name)
self.assertEqual(doc.get(new), data)
self.assertFalse(doc.get(old))
field.delete()
```

## Next Steps


---

*Source: test_custom_field.py:167 | Complexity: Advanced | Last updated: 2026-02-04*