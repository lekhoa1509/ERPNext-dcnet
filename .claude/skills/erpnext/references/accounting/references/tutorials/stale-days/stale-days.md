# How To: Stale Days

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test stale days

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign cur_settings = frappe.get_doc(...)

```python
cur_settings = frappe.get_doc('Accounts Settings', 'Accounts Settings')
```

### Step 2: Assign cur_settings.allow_stale = 0

```python
cur_settings.allow_stale = 0
```

### Step 3: Assign cur_settings.stale_days = 0

```python
cur_settings.stale_days = 0
```

### Step 4: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, cur_settings.save)
```

### Step 5: Assign cur_settings.stale_days = value

```python
cur_settings.stale_days = -1
```

### Step 6: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, cur_settings.save)
```


## Complete Example

```python
# Workflow
cur_settings = frappe.get_doc('Accounts Settings', 'Accounts Settings')
cur_settings.allow_stale = 0
cur_settings.stale_days = 0
self.assertRaises(frappe.ValidationError, cur_settings.save)
cur_settings.stale_days = -1
self.assertRaises(frappe.ValidationError, cur_settings.save)
```

## Next Steps


---

*Source: test_accounts_settings.py:13 | Complexity: Intermediate | Last updated: 2026-02-03*