# How To: Depreciation Schedule After Cancelling Asset Value Adjustent

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test depreciation schedule after cancelling asset value adjustent

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.assets.doctype.asset.depreciation`
- `erpnext.assets.doctype.asset.test_asset`
- `erpnext.assets.doctype.asset_depreciation_schedule.asset_depreciation_schedule`
- `erpnext.assets.doctype.asset_repair.test_asset_repair`
- `erpnext.assets.doctype.asset_value_adjustment.test_asset_value_adjustment`
- `erpnext.controllers.sales_and_purchase_return`

**Setup Required:**
```python
create_asset_data()
```

## Step-by-Step Guide

### Step 1: Assign asset = create_asset(...)

```python
asset = create_asset(item_code='Macbook Pro', net_purchase_amount=1000, calculate_depreciation=1, depreciation_method='Straight Line', available_for_use_date='2023-01-01', depreciation_start_date='2023-01-31', frequency_of_depreciation=1, total_number_of_depreciations=12, submit=1)
```

### Step 2: Assign expected_depreciation_before_adjustment = value

```python
expected_depreciation_before_adjustment = [['2023-01-31', 83.33, 83.33], ['2023-02-28', 83.33, 166.66], ['2023-03-31', 83.33, 249.99], ['2023-04-30', 83.33, 333.32], ['2023-05-31', 83.33, 416.65], ['2023-06-30', 83.33, 499.98], ['2023-07-31', 83.33, 583.31], ['2023-08-31', 83.33, 666.64], ['2023-09-30', 83.33, 749.97], ['2023-10-31', 83.33, 833.3], ['2023-11-30', 83.33, 916.63], ['2023-12-31', 83.37, 1000.0]]
```

### Step 3: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_depreciation_before_adjustment)
```

### Step 5: Assign current_asset_value = value

```python
current_asset_value = asset.finance_books[0].value_after_depreciation
```

### Step 6: Assign asset_value_adjustment = make_asset_value_adjustment(...)

```python
asset_value_adjustment = make_asset_value_adjustment(asset=asset.name, date='2023-04-01', current_asset_value=current_asset_value, new_asset_value=1200)
```

### Step 7: Call asset_value_adjustment.submit()

```python
asset_value_adjustment.submit()
```

### Step 8: Assign expected_depreciation_after_adjustment = value

```python
expected_depreciation_after_adjustment = [['2023-01-31', 100.0, 100.0], ['2023-02-28', 100.0, 200.0], ['2023-03-31', 100.0, 300.0], ['2023-04-30', 100.0, 400.0], ['2023-05-31', 100.0, 500.0], ['2023-06-30', 100.0, 600.0], ['2023-07-31', 100.0, 700.0], ['2023-08-31', 100.0, 800.0], ['2023-09-30', 100.0, 900.0], ['2023-10-31', 100.0, 1000.0], ['2023-11-30', 100.0, 1100.0], ['2023-12-31', 100.0, 1200.0]]
```

### Step 9: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_depreciation_after_adjustment)
```

### Step 11: Call asset_value_adjustment.cancel()

```python
asset_value_adjustment.cancel()
```

### Step 12: Call asset.reload()

```python
asset.reload()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(asset.finance_books[0].value_after_depreciation, 1000)
```

### Step 14: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_depreciation_before_adjustment)
```


## Complete Example

```python
# Setup
create_asset_data()

# Workflow
asset = create_asset(item_code='Macbook Pro', net_purchase_amount=1000, calculate_depreciation=1, depreciation_method='Straight Line', available_for_use_date='2023-01-01', depreciation_start_date='2023-01-31', frequency_of_depreciation=1, total_number_of_depreciations=12, submit=1)
expected_depreciation_before_adjustment = [['2023-01-31', 83.33, 83.33], ['2023-02-28', 83.33, 166.66], ['2023-03-31', 83.33, 249.99], ['2023-04-30', 83.33, 333.32], ['2023-05-31', 83.33, 416.65], ['2023-06-30', 83.33, 499.98], ['2023-07-31', 83.33, 583.31], ['2023-08-31', 83.33, 666.64], ['2023-09-30', 83.33, 749.97], ['2023-10-31', 83.33, 833.3], ['2023-11-30', 83.33, 916.63], ['2023-12-31', 83.37, 1000.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_adjustment)
current_asset_value = asset.finance_books[0].value_after_depreciation
asset_value_adjustment = make_asset_value_adjustment(asset=asset.name, date='2023-04-01', current_asset_value=current_asset_value, new_asset_value=1200)
asset_value_adjustment.submit()
expected_depreciation_after_adjustment = [['2023-01-31', 100.0, 100.0], ['2023-02-28', 100.0, 200.0], ['2023-03-31', 100.0, 300.0], ['2023-04-30', 100.0, 400.0], ['2023-05-31', 100.0, 500.0], ['2023-06-30', 100.0, 600.0], ['2023-07-31', 100.0, 700.0], ['2023-08-31', 100.0, 800.0], ['2023-09-30', 100.0, 900.0], ['2023-10-31', 100.0, 1000.0], ['2023-11-30', 100.0, 1100.0], ['2023-12-31', 100.0, 1200.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_adjustment)
asset_value_adjustment.cancel()
asset.reload()
self.assertEqual(asset.finance_books[0].value_after_depreciation, 1000)
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_adjustment)
```

## Next Steps


---

*Source: test_asset_depreciation_schedule.py:742 | Complexity: Advanced | Last updated: 2026-02-04*