# How To: Client Validate Link And Fetch

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test client validate link and fetch

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.client`
- `frappe.desk.doctype.note.note`
- `frappe.client`
- `frappe.handler`
- `frappe.handler`
- `frappe.handler`
- `requests`
- `frappe.auth`
- `frappe.client`
- `frappe.client`
- `frappe.client`
- `frappe.client`
- `frappe.client`


## Step-by-Step Guide

### Step 1: Call self.assertTrue()

```python
self.assertTrue(validate_link_and_fetch('Role', 'System Manager'))
```

### Step 2: Assign result = validate_link_and_fetch(...)

```python
result = validate_link_and_fetch('Role', 'System Manager', fields_to_fetch=['desk_access'])
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(result.get('name'), 'System Manager')
```

### Step 4: Call self.assertIn()

```python
self.assertIn('desk_access', result)
```

### Step 5: Assign result = validate_link_and_fetch(...)

```python
result = validate_link_and_fetch('Role', 'Non Existent Role')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(result, {})
```

### Step 7: Assign result = validate_link_and_fetch(...)

```python
result = validate_link_and_fetch('Role', 'System Manager', filters={'desk_access': 0})
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(result, {})
```

### Step 9: Assign result = validate_link_and_fetch(...)

```python
result = validate_link_and_fetch('Role', 'System Manager', filters={'desk_access': 1})
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(result.get('name'), 'System Manager')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(validate_link_and_fetch('Role', 'system manager'), {'name': 'System Manager'})
```

### Step 12: Call validate_link_and_fetch()

```python
validate_link_and_fetch('Role', 'System Manager')
```


## Complete Example

```python
# Workflow
from frappe.client import validate_link_and_fetch
self.assertTrue(validate_link_and_fetch('Role', 'System Manager'))
if frappe.db.db_type == 'mariadb':
    self.assertEqual(validate_link_and_fetch('Role', 'system manager'), {'name': 'System Manager'})
result = validate_link_and_fetch('Role', 'System Manager', fields_to_fetch=['desk_access'])
self.assertEqual(result.get('name'), 'System Manager')
self.assertIn('desk_access', result)
result = validate_link_and_fetch('Role', 'Non Existent Role')
self.assertEqual(result, {})
result = validate_link_and_fetch('Role', 'System Manager', filters={'desk_access': 0})
self.assertEqual(result, {})
result = validate_link_and_fetch('Role', 'System Manager', filters={'desk_access': 1})
self.assertEqual(result.get('name'), 'System Manager')
with self.set_user('Guest'), self.assertRaises(frappe.PermissionError):
    validate_link_and_fetch('Role', 'System Manager')
```

## Next Steps


---

*Source: test_client.py:158 | Complexity: Advanced | Last updated: 2026-02-04*