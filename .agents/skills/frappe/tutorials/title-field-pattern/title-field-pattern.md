# How To: Title Field Pattern

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test title field pattern

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
d = self.get_customize_form('Web Form')
```

### Step 2: Assign df = value

```python
df = d.get('fields', {'fieldname': 'title'})[0]
```

### Step 3: Assign df.default = '{doc_type} - {introduction_test}'

```python
df.default = '{doc_type} - {introduction_test}'
```

### Step 4: Call self.assertRaises()

```python
self.assertRaises(InvalidFieldNameError, d.run_method, 'save_customization')
```

### Step 5: Assign df.default = '{doc_type} - {introduction text}'

```python
df.default = '{doc_type} - {introduction text}'
```

### Step 6: Call self.assertRaises()

```python
self.assertRaises(InvalidFieldNameError, d.run_method, 'save_customization')
```

### Step 7: Assign df.default = '{doc_type} - {introduction_text}'

```python
df.default = '{doc_type} - {introduction_text}'
```

### Step 8: Call d.run_method()

```python
d.run_method('save_customization')
```

### Step 9: Assign df.default = '{{ {doc_type} }} - {introduction_text}'

```python
df.default = '{{ {doc_type} }} - {introduction_text}'
```

### Step 10: Call d.run_method()

```python
d.run_method('save_customization')
```

### Step 11: Assign df.default = None

```python
df.default = None
```

### Step 12: Call d.run_method()

```python
d.run_method('save_customization')
```


## Complete Example

```python
# Setup
self.insert_custom_field()
frappe.db.delete('Property Setter', dict(doc_type='Event'))
frappe.db.commit()
frappe.clear_cache(doctype='Event')

# Workflow
d = self.get_customize_form('Web Form')
df = d.get('fields', {'fieldname': 'title'})[0]
df.default = '{doc_type} - {introduction_test}'
self.assertRaises(InvalidFieldNameError, d.run_method, 'save_customization')
df.default = '{doc_type} - {introduction text}'
self.assertRaises(InvalidFieldNameError, d.run_method, 'save_customization')
df.default = '{doc_type} - {introduction_text}'
d.run_method('save_customization')
df.default = '{{ {doc_type} }} - {introduction_text}'
d.run_method('save_customization')
df.default = None
d.run_method('save_customization')
```

## Next Steps


---

*Source: test_customize_form.py:203 | Complexity: Advanced | Last updated: 2026-02-04*