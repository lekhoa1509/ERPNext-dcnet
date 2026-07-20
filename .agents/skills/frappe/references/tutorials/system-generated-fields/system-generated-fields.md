# How To: System Generated Fields

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test system generated fields

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

### Step 1: Assign doctype = 'Event'

```python
doctype = 'Event'
```

### Step 2: Assign custom_field_name = 'custom_test_field'

```python
custom_field_name = 'custom_test_field'
```

### Step 3: Assign custom_field = frappe.get_doc(...)

```python
custom_field = frappe.get_doc('Custom Field', {'dt': doctype, 'fieldname': custom_field_name})
```

### Step 4: Assign custom_field.is_system_generated = 1

```python
custom_field.is_system_generated = 1
```

### Step 5: Call custom_field.save()

```python
custom_field.save()
```

### Step 6: Assign d = self.get_customize_form(...)

```python
d = self.get_customize_form(doctype)
```

### Step 7: Assign custom_field = d.getone(...)

```python
custom_field = d.getone('fields', {'fieldname': custom_field_name})
```

### Step 8: Assign custom_field.description = 'Test Description'

```python
custom_field.description = 'Test Description'
```

### Step 9: Call d.run_method()

```python
d.run_method('save_customization')
```

### Step 10: Assign property_setter_filters = value

```python
property_setter_filters = {'doc_type': doctype, 'field_name': custom_field_name, 'property': 'description'}
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Property Setter', property_setter_filters, 'value'), 'Test Description')
```


## Complete Example

```python
# Setup
self.insert_custom_field()
frappe.db.delete('Property Setter', dict(doc_type='Event'))
frappe.db.commit()
frappe.clear_cache(doctype='Event')

# Workflow
doctype = 'Event'
custom_field_name = 'custom_test_field'
custom_field = frappe.get_doc('Custom Field', {'dt': doctype, 'fieldname': custom_field_name})
custom_field.is_system_generated = 1
custom_field.save()
d = self.get_customize_form(doctype)
custom_field = d.getone('fields', {'fieldname': custom_field_name})
custom_field.description = 'Test Description'
d.run_method('save_customization')
property_setter_filters = {'doc_type': doctype, 'field_name': custom_field_name, 'property': 'description'}
self.assertEqual(frappe.db.get_value('Property Setter', property_setter_filters, 'value'), 'Test Description')
```

## Next Steps


---

*Source: test_customize_form.py:393 | Complexity: Advanced | Last updated: 2026-02-04*