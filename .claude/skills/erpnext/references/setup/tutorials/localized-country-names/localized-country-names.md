# How To: Localized Country Names

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test localized country names

## Prerequisites

**Required Modules:**
- `contextlib`
- `datetime`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.setup.doctype.holiday_list.holiday_list`


## Step-by-Step Guide

### Step 1: Assign lang = value

```python
lang = frappe.local.lang
```

### Step 2: Assign frappe.local.lang = 'en-gb'

```python
frappe.local.lang = 'en-gb'
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(local_country_name('IN'), 'India')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(local_country_name('DE'), 'Germany')
```

### Step 5: Assign frappe.local.lang = 'de'

```python
frappe.local.lang = 'de'
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(local_country_name('DE'), 'Deutschland')
```

### Step 7: Assign frappe.local.lang = lang

```python
frappe.local.lang = lang
```


## Complete Example

```python
# Workflow
lang = frappe.local.lang
frappe.local.lang = 'en-gb'
self.assertEqual(local_country_name('IN'), 'India')
self.assertEqual(local_country_name('DE'), 'Germany')
frappe.local.lang = 'de'
self.assertEqual(local_country_name('DE'), 'Deutschland')
frappe.local.lang = lang
```

## Next Steps


---

*Source: test_holiday_list.py:103 | Complexity: Advanced | Last updated: 2026-02-04*