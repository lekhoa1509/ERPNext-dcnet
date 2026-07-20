# How To: Save Customization Field Property

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test save customization field property

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.core.doctype.doctype.doctype`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.tests`
- `frappe.tests.utils`


## Step-by-Step Guide

### Step 1: Assign d = self.get_customize_form(...)

```python
d = self.get_customize_form('Event')
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Property Setter', {'doc_type': 'Event', 'property': 'reqd', 'field_name': 'repeat_this_event'}, 'value'), None)
```

### Step 3: Assign repeat_this_event_field = value

```python
repeat_this_event_field = d.get('fields', {'fieldname': 'repeat_this_event'})[0]
```

### Step 4: Assign repeat_this_event_field.reqd = 1

```python
repeat_this_event_field.reqd = 1
```

### Step 5: Call d.run_method()

```python
d.run_method('save_customization')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Property Setter', {'doc_type': 'Event', 'property': 'reqd', 'field_name': 'repeat_this_event'}, 'value'), '1')
```

### Step 7: Assign repeat_this_event_field = value

```python
repeat_this_event_field = d.get('fields', {'fieldname': 'repeat_this_event'})[0]
```

### Step 8: Assign repeat_this_event_field.reqd = 0

```python
repeat_this_event_field.reqd = 0
```

### Step 9: Call d.run_method()

```python
d.run_method('save_customization')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Property Setter', {'doc_type': 'Event', 'property': 'reqd', 'field_name': 'repeat_this_event'}, 'value'), None)
```


## Complete Example

```python
# Workflow
d = self.get_customize_form('Event')
self.assertEqual(frappe.db.get_value('Property Setter', {'doc_type': 'Event', 'property': 'reqd', 'field_name': 'repeat_this_event'}, 'value'), None)
repeat_this_event_field = d.get('fields', {'fieldname': 'repeat_this_event'})[0]
repeat_this_event_field.reqd = 1
d.run_method('save_customization')
self.assertEqual(frappe.db.get_value('Property Setter', {'doc_type': 'Event', 'property': 'reqd', 'field_name': 'repeat_this_event'}, 'value'), '1')
repeat_this_event_field = d.get('fields', {'fieldname': 'repeat_this_event'})[0]
repeat_this_event_field.reqd = 0
d.run_method('save_customization')
self.assertEqual(frappe.db.get_value('Property Setter', {'doc_type': 'Event', 'property': 'reqd', 'field_name': 'repeat_this_event'}, 'value'), None)
```

## Next Steps


---

*Source: test_customize_form.py:90 | Complexity: Advanced | Last updated: 2026-02-04*