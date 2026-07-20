# How To: Custom Action

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test custom action

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

### Step 1: Assign test_route = '/desk/List/DocType'

```python
test_route = '/desk/List/DocType'
```

### Step 2: Assign d = self.get_customize_form(...)

```python
d = self.get_customize_form('Event')
```

### Step 3: Call d.append()

```python
d.append('actions', dict(label='Test Action', action_type='Route', action=test_route))
```

### Step 4: Call d.run_method()

```python
d.run_method('save_customization')
```

### Step 5: Call frappe.clear_cache()

```python
frappe.clear_cache()
```

### Step 6: Assign event = frappe.get_meta(...)

```python
event = frappe.get_meta('Event')
```

### Step 7: Assign action = value

```python
action = [d for d in event.actions if d.label == 'Test Action']
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(len(action), 1)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(action[0].action, test_route)
```

### Step 10: Assign d = self.get_customize_form(...)

```python
d = self.get_customize_form('Event')
```

### Step 11: Assign d.actions = value

```python
d.actions = []
```

### Step 12: Call d.run_method()

```python
d.run_method('save_customization')
```

### Step 13: Call frappe.clear_cache()

```python
frappe.clear_cache()
```

### Step 14: Assign event = frappe.get_meta(...)

```python
event = frappe.get_meta('Event')
```

### Step 15: Assign action = value

```python
action = [d for d in event.actions if d.label == 'Test Action']
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(len(action), 0)
```


## Complete Example

```python
# Setup
self.insert_custom_field()
frappe.db.delete('Property Setter', dict(doc_type='Event'))
frappe.db.commit()
frappe.clear_cache(doctype='Event')

# Workflow
test_route = '/desk/List/DocType'
d = self.get_customize_form('Event')
d.append('actions', dict(label='Test Action', action_type='Route', action=test_route))
d.run_method('save_customization')
frappe.clear_cache()
event = frappe.get_meta('Event')
action = [d for d in event.actions if d.label == 'Test Action']
self.assertEqual(len(action), 1)
self.assertEqual(action[0].action, test_route)
d = self.get_customize_form('Event')
d.actions = []
d.run_method('save_customization')
frappe.clear_cache()
event = frappe.get_meta('Event')
action = [d for d in event.actions if d.label == 'Test Action']
self.assertEqual(len(action), 0)
```

## Next Steps


---

*Source: test_customize_form.py:337 | Complexity: Advanced | Last updated: 2026-02-04*