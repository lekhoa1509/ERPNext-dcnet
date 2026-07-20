# How To: Dynamic Date Filters

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test dynamic date filters

## Prerequisites

**Required Modules:**
- `json`
- `io`
- `pypdf`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.data`


## Step-by-Step Guide

### Step 1: Assign auto_email_report = get_auto_email_report(...)

```python
auto_email_report = get_auto_email_report()
```

### Step 2: Assign auto_email_report.dynamic_date_period = 'Weekly'

```python
auto_email_report.dynamic_date_period = 'Weekly'
```

### Step 3: Assign auto_email_report.from_date_field = 'from_date'

```python
auto_email_report.from_date_field = 'from_date'
```

### Step 4: Assign auto_email_report.to_date_field = 'to_date'

```python
auto_email_report.to_date_field = 'to_date'
```

### Step 5: Call auto_email_report.prepare_dynamic_filters()

```python
auto_email_report.prepare_dynamic_filters()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(auto_email_report.filters['from_date'], add_to_date(today(), weeks=-1))
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(auto_email_report.filters['to_date'], today())
```


## Complete Example

```python
# Workflow
auto_email_report = get_auto_email_report()
auto_email_report.dynamic_date_period = 'Weekly'
auto_email_report.from_date_field = 'from_date'
auto_email_report.to_date_field = 'to_date'
auto_email_report.prepare_dynamic_filters()
self.assertEqual(auto_email_report.filters['from_date'], add_to_date(today(), weeks=-1))
self.assertEqual(auto_email_report.filters['to_date'], today())
```

## Next Steps


---

*Source: test_auto_email_report.py:39 | Complexity: Intermediate | Last updated: 2026-02-04*