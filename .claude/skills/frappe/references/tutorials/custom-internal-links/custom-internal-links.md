# How To: Custom Internal Links

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test custom internal links

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

### Step 1: Call frappe.clear_cache()

```python
frappe.clear_cache()
```

### Step 2: Assign d = self.get_customize_form(...)

```python
d = self.get_customize_form('User Group')
```

### Step 3: Call d.append()

```python
d.append('links', dict(link_doctype='User Group Member', parent_doctype='User Group', link_fieldname='user', table_fieldname='user_group_members', group='Tests', custom=1))
```

### Step 4: Call d.run_method()

```python
d.run_method('save_customization')
```

### Step 5: Call frappe.clear_cache()

```python
frappe.clear_cache()
```

### Step 6: Assign user_group = frappe.get_meta(...)

```python
user_group = frappe.get_meta('User Group')
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue([d.name for d in user_group.links if d.link_doctype == 'User Group Member'])
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue([d.name for d in user_group.links if d.parent_doctype == 'User Group'])
```

### Step 9: Assign d = self.get_customize_form(...)

```python
d = self.get_customize_form('User Group')
```

### Step 10: Assign d.links = value

```python
d.links = []
```

### Step 11: Call d.run_method()

```python
d.run_method('save_customization')
```

### Step 12: Call frappe.clear_cache()

```python
frappe.clear_cache()
```

### Step 13: Assign user_group = frappe.get_meta(...)

```python
user_group = frappe.get_meta('Event')
```

### Step 14: Call self.assertFalse()

```python
self.assertFalse([d.name for d in user_group.links or [] if d.link_doctype == 'User Group Member'])
```


## Complete Example

```python
# Setup
self.insert_custom_field()
frappe.db.delete('Property Setter', dict(doc_type='Event'))
frappe.db.commit()
frappe.clear_cache(doctype='Event')

# Workflow
frappe.clear_cache()
d = self.get_customize_form('User Group')
d.append('links', dict(link_doctype='User Group Member', parent_doctype='User Group', link_fieldname='user', table_fieldname='user_group_members', group='Tests', custom=1))
d.run_method('save_customization')
frappe.clear_cache()
user_group = frappe.get_meta('User Group')
self.assertTrue([d.name for d in user_group.links if d.link_doctype == 'User Group Member'])
self.assertTrue([d.name for d in user_group.links if d.parent_doctype == 'User Group'])
d = self.get_customize_form('User Group')
d.links = []
d.run_method('save_customization')
frappe.clear_cache()
user_group = frappe.get_meta('Event')
self.assertFalse([d.name for d in user_group.links or [] if d.link_doctype == 'User Group Member'])
```

## Next Steps


---

*Source: test_customize_form.py:302 | Complexity: Advanced | Last updated: 2026-02-04*