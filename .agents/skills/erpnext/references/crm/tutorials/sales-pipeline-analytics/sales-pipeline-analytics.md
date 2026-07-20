# How To: Sales Pipeline Analytics

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test sales pipeline analytics

## Prerequisites

**Required Modules:**
- `unittest`
- `frappe`
- `frappe.tests`
- `erpnext.crm.report.sales_pipeline_analytics.sales_pipeline_analytics`


## Step-by-Step Guide

### Step 1: Assign self.from_date = '2021-01-01'

```python
self.from_date = '2021-01-01'
```

### Step 2: Assign self.to_date = '2021-12-31'

```python
self.to_date = '2021-12-31'
```

### Step 3: Call self.check_for_monthly_and_number()

```python
self.check_for_monthly_and_number()
```

### Step 4: Call self.check_for_monthly_and_amount()

```python
self.check_for_monthly_and_amount()
```

### Step 5: Call self.check_for_quarterly_and_number()

```python
self.check_for_quarterly_and_number()
```

### Step 6: Call self.check_for_quarterly_and_amount()

```python
self.check_for_quarterly_and_amount()
```

### Step 7: Call self.check_for_all_filters()

```python
self.check_for_all_filters()
```


## Complete Example

```python
# Workflow
self.from_date = '2021-01-01'
self.to_date = '2021-12-31'
self.check_for_monthly_and_number()
self.check_for_monthly_and_amount()
self.check_for_quarterly_and_number()
self.check_for_quarterly_and_amount()
self.check_for_all_filters()
```

## Next Steps


---

*Source: test_sales_pipeline_analytics.py:15 | Complexity: Intermediate | Last updated: 2026-02-04*