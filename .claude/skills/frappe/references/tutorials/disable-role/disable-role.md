# How To: Disable Role

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test disable role

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.core.doctype.role.role`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Call frappe.get_doc.add_roles()

```python
frappe.get_doc('User', 'test@example.com').add_roles('_Test Role 3')
```

### Step 2: Assign role = frappe.get_doc(...)

```python
role = frappe.get_doc('Role', '_Test Role 3')
```

### Step 3: Assign role.disabled = 1

```python
role.disabled = 1
```

### Step 4: Call role.save()

```python
role.save()
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue('_Test Role 3' not in frappe.get_roles('test@example.com'))
```

### Step 6: Assign role = frappe.get_doc(...)

```python
role = frappe.get_doc('Role', '_Test Role 3')
```

### Step 7: Assign role.disabled = 0

```python
role.disabled = 0
```

### Step 8: Call role.save()

```python
role.save()
```

### Step 9: Call frappe.get_doc.add_roles()

```python
frappe.get_doc('User', 'test@example.com').add_roles('_Test Role 3')
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue('_Test Role 3' in frappe.get_roles('test@example.com'))
```


## Complete Example

```python
# Workflow
frappe.get_doc('User', 'test@example.com').add_roles('_Test Role 3')
role = frappe.get_doc('Role', '_Test Role 3')
role.disabled = 1
role.save()
self.assertTrue('_Test Role 3' not in frappe.get_roles('test@example.com'))
role = frappe.get_doc('Role', '_Test Role 3')
role.disabled = 0
role.save()
frappe.get_doc('User', 'test@example.com').add_roles('_Test Role 3')
self.assertTrue('_Test Role 3' in frappe.get_roles('test@example.com'))
```

## Next Steps


---

*Source: test_role.py:10 | Complexity: Advanced | Last updated: 2026-02-04*