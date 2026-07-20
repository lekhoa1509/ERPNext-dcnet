# How To: Depreciation Schedule After Cancelling Asset Value Adjustent For Existing Asset

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test depreciation schedule after cancelling asset value adjustent for existing asset

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
asset = create_asset(item_code='Macbook Pro', net_purchase_amount=500, calculate_depreciation=1, depreciation_method='Straight Line', available_for_use_date='2023-01-15', depreciation_start_date='2023-03-31', frequency_of_depreciation=1, total_number_of_depreciations=12, is_existing_asset=1, opening_accumulated_depreciation=64.52, opening_number_of_booked_depreciations=2, submit=1)
```

### Step 2: Assign expected_depreciation_before_adjustment = value

```python
expected_depreciation_before_adjustment = [['2023-03-31', 41.39, 105.91], ['2023-04-30', 41.39, 147.3], ['2023-05-31', 41.39, 188.69], ['2023-06-30', 41.39, 230.08], ['2023-07-31', 41.39, 271.47], ['2023-08-31', 41.39, 312.86], ['2023-09-30', 41.39, 354.25], ['2023-10-31', 41.39, 395.64], ['2023-11-30', 41.39, 437.03], ['2023-12-31', 41.39, 478.42], ['2024-01-15', 21.58, 500.0]]
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
asset_value_adjustment = make_asset_value_adjustment(asset=asset.name, date='2023-04-01', current_asset_value=current_asset_value, new_asset_value=600)
```

### Step 7: Call asset_value_adjustment.submit()

```python
asset_value_adjustment.submit()
```

### Step 8: Assign expected_depreciation_after_adjustment = value

```python
expected_depreciation_after_adjustment = [['2023-03-31', 57.03, 121.55], ['2023-04-30', 57.03, 178.58], ['2023-05-31', 57.03, 235.61], ['2023-06-30', 57.03, 292.64], ['2023-07-31', 57.03, 349.67], ['2023-08-31', 57.03, 406.7], ['2023-09-30', 57.03, 463.73], ['2023-10-31', 57.03, 520.76], ['2023-11-30', 57.03, 577.79], ['2023-12-31', 57.03, 634.82], ['2024-01-15', 29.7, 664.52]]
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

### Step 12: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_depreciation_before_adjustment)
```


## Complete Example

```python
# Setup
create_asset_data()

# Workflow
asset = create_asset(item_code='Macbook Pro', net_purchase_amount=500, calculate_depreciation=1, depreciation_method='Straight Line', available_for_use_date='2023-01-15', depreciation_start_date='2023-03-31', frequency_of_depreciation=1, total_number_of_depreciations=12, is_existing_asset=1, opening_accumulated_depreciation=64.52, opening_number_of_booked_depreciations=2, submit=1)
expected_depreciation_before_adjustment = [['2023-03-31', 41.39, 105.91], ['2023-04-30', 41.39, 147.3], ['2023-05-31', 41.39, 188.69], ['2023-06-30', 41.39, 230.08], ['2023-07-31', 41.39, 271.47], ['2023-08-31', 41.39, 312.86], ['2023-09-30', 41.39, 354.25], ['2023-10-31', 41.39, 395.64], ['2023-11-30', 41.39, 437.03], ['2023-12-31', 41.39, 478.42], ['2024-01-15', 21.58, 500.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_adjustment)
current_asset_value = asset.finance_books[0].value_after_depreciation
asset_value_adjustment = make_asset_value_adjustment(asset=asset.name, date='2023-04-01', current_asset_value=current_asset_value, new_asset_value=600)
asset_value_adjustment.submit()
expected_depreciation_after_adjustment = [['2023-03-31', 57.03, 121.55], ['2023-04-30', 57.03, 178.58], ['2023-05-31', 57.03, 235.61], ['2023-06-30', 57.03, 292.64], ['2023-07-31', 57.03, 349.67], ['2023-08-31', 57.03, 406.7], ['2023-09-30', 57.03, 463.73], ['2023-10-31', 57.03, 520.76], ['2023-11-30', 57.03, 577.79], ['2023-12-31', 57.03, 634.82], ['2024-01-15', 29.7, 664.52]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_adjustment)
asset_value_adjustment.cancel()
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_adjustment)
```

## Next Steps


---

*Source: test_asset_depreciation_schedule.py:844 | Complexity: Advanced | Last updated: 2026-02-04*