# How To: Save Customization Custom Field Property

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test save customization custom field property

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `json`
- `frappe`
- `frappe.core.doctype.doctype.doctype`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.tests`
- `frappe.tests.utils`

**Setup Required:**
```python
self.insert_custom_field()
frappe.db.delete('Property Setter', dict(doc_type='Event'))
frappe.db.commit()
frappe.clear_cache(doctype='Event')
```

## Step-by-Step Guide

### Step 1: Assign d = self.get_customize_form(...)

```python
d = self.get_customize_form('Event')
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Custom Field', self.field.name, 'reqd'), 0)
```

### Step 3: Assign custom_field = value

```python
custom_field = d.get('fields', {'fieldname': self.field.fieldname})[0]
```

### Step 4: Assign custom_field.reqd = 1

```python
custom_field.reqd = 1
```

### Step 5: Assign custom_field.no_copy = 1

```python
custom_field.no_copy = 1
```

### Step 6: Call d.run_method()

```python
d.run_method('save_customization')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Custom Field', self.field.name, 'reqd'), 1)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Custom Field', self.field.name, 'no_copy'), 1)
```

### Step 9: Assign custom_field = value

```python
custom_field = d.get('fields', {'is_custom_field': True})[0]
```

### Step 10: Assign custom_field.reqd = 0

```python
custom_field.reqd = 0
```

### Step 11: Assign custom_field.no_copy = 0

```python
custom_field.no_copy = 0
```

### Step 12: Call d.run_method()

```python
d.run_method('save_customization')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Custom Field', self.field.name, 'reqd'), 0)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Custom Field', self.field.name, 'no_copy'), 0)
```


## Complete Example

```python
# Setup
self.insert_custom_field()
frappe.db.delete('Property Setter', dict(doc_type='Event'))
frappe.db.commit()
frappe.clear_cache(doctype='Event')

# Workflow
d = self.get_customize_form('Event')
self.assertEqual(frappe.db.get_value('Custom Field', self.field.name, 'reqd'), 0)
custom_field = d.get('fields', {'fieldname': self.field.fieldname})[0]
custom_field.reqd = 1
custom_field.no_copy = 1
d.run_method('save_customization')
self.assertEqual(frappe.db.get_value('Custom Field', self.field.name, 'reqd'), 1)
self.assertEqual(frappe.db.get_value('Custom Field', self.field.name, 'no_copy'), 1)
custom_field = d.get('fields', {'is_custom_field': True})[0]
custom_field.reqd = 0
custom_field.no_copy = 0
d.run_method('save_customization')
self.assertEqual(frappe.db.get_value('Custom Field', self.field.name, 'reqd'), 0)
self.assertEqual(frappe.db.get_value('Custom Field', self.field.name, 'no_copy'), 0)
```

## Next Steps


---

*Source: test_customize_form.py:125 | Complexity: Advanced | Last updated: 2026-02-04*