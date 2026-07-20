# How To: Get Period Date Ranges Yearly

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get period date ranges yearly

## Prerequisites

**Required Modules:**
- `datetime`
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils.data`
- `erpnext.accounts.utils`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.report.stock_analytics.stock_analytics`


## Step-by-Step Guide

### Step 1: Assign filters = _dict(...)

```python
filters = _dict(range='Yearly', from_date='2021-01-28', to_date='2021-02-06')
```

### Step 2: Assign ranges = get_period_date_ranges(...)

```python
ranges = get_period_date_ranges(filters)
```

### Step 3: Assign first_date = value

```python
first_date = get_fiscal_year('2021-01-28')[1]
```

### Step 4: Assign expected_ranges = value

```python
expected_ranges = [[first_date, datetime.date(2021, 2, 6)]]
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(ranges, expected_ranges)
```


## Complete Example

```python
# Workflow
filters = _dict(range='Yearly', from_date='2021-01-28', to_date='2021-02-06')
ranges = get_period_date_ranges(filters)
first_date = get_fiscal_year('2021-01-28')[1]
expected_ranges = [[first_date, datetime.date(2021, 2, 6)]]
self.assertEqual(ranges, expected_ranges)
```

## Next Steps


---

*Source: test_stock_analytics.py:70 | Complexity: Intermediate | Last updated: 2026-02-04*