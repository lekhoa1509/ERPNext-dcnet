# How To: Set Allow On Submit

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test set allow on submit

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

### Step 2: Assign unknown.allow_on_submit = 1

```python
d.get('fields', {'fieldname': 'subject'})[0].allow_on_submit = 1
```

### Step 3: Assign unknown.allow_on_submit = 1

```python
d.get('fields', {'fieldname': 'custom_test_field'})[0].allow_on_submit = 1
```

### Step 4: Call d.run_method()

```python
d.run_method('save_customization')
```

### Step 5: Assign d = self.get_customize_form(...)

```python
d = self.get_customize_form('Event')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(d.get('fields', {'fieldname': 'subject'})[0].allow_on_submit or 0, 0)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(d.get('fields', {'fieldname': 'custom_test_field'})[0].allow_on_submit, 1)
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
d.get('fields', {'fieldname': 'subject'})[0].allow_on_submit = 1
d.get('fields', {'fieldname': 'custom_test_field'})[0].allow_on_submit = 1
d.run_method('save_customization')
d = self.get_customize_form('Event')
self.assertEqual(d.get('fields', {'fieldname': 'subject'})[0].allow_on_submit or 0, 0)
self.assertEqual(d.get('fields', {'fieldname': 'custom_test_field'})[0].allow_on_submit, 1)
```

## Next Steps


---

*Source: test_customize_form.py:189 | Complexity: Intermediate | Last updated: 2026-02-04*