# How To: Custom Label

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test custom label

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

### Step 2: Assign d.label = 'Test Rename'

```python
d.label = 'Test Rename'
```

### Step 3: Call d.run_method()

```python
d.run_method('save_customization')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(d.label, 'Test Rename')
```

### Step 5: Assign d.label = 'Test Rename 2'

```python
d.label = 'Test Rename 2'
```

### Step 6: Call d.run_method()

```python
d.run_method('save_customization')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(d.label, 'Test Rename 2')
```

### Step 8: Call d.run_method()

```python
d.run_method('save_customization')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(d.label, 'Test Rename 2')
```

### Step 10: Assign d.label = ''

```python
d.label = ''
```

### Step 11: Call d.run_method()

```python
d.run_method('save_customization')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(d.label, '')
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
d.label = 'Test Rename'
d.run_method('save_customization')
self.assertEqual(d.label, 'Test Rename')
d.label = 'Test Rename 2'
d.run_method('save_customization')
self.assertEqual(d.label, 'Test Rename 2')
d.run_method('save_customization')
self.assertEqual(d.label, 'Test Rename 2')
d.label = ''
d.run_method('save_customization')
self.assertEqual(d.label, '')
```

## Next Steps


---

*Source: test_customize_form.py:364 | Complexity: Advanced | Last updated: 2026-02-04*