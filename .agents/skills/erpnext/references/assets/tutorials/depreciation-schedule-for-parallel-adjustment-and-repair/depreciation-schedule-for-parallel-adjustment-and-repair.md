# How To: Depreciation Schedule For Parallel Adjustment And Repair

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test depreciation schedule for parallel adjustment and repair

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
asset = create_asset(item_code='Macbook Pro', net_purchase_amount=600, calculate_depreciation=1, depreciation_method='Straight Line', available_for_use_date='2021-01-01', depreciation_start_date='2021-12-31', frequency_of_depreciation=12, total_number_of_depreciations=3, is_existing_asset=1, submit=1)
```

### Step 2: Call post_depreciation_entries()

```python
post_depreciation_entries(date='2021-12-31')
```

### Step 3: Call asset.reload()

```python
asset.reload()
```

### Step 4: Assign expected_depreciation_before_adjustment = value

```python
expected_depreciation_before_adjustment = [['2021-12-31', 200, 200], ['2022-12-31', 200, 400], ['2023-12-31', 200, 600]]
```

### Step 5: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_depreciation_before_adjustment)
```

### Step 7: Assign current_asset_value = value

```python
current_asset_value = asset.finance_books[0].value_after_depreciation
```

### Step 8: Assign asset_value_adjustment = make_asset_value_adjustment(...)

```python
asset_value_adjustment = make_asset_value_adjustment(asset=asset.name, date='2022-01-15', current_asset_value=current_asset_value, new_asset_value=500)
```

### Step 9: Call asset_value_adjustment.submit()

```python
asset_value_adjustment.submit()
```

### Step 10: Assign expected_depreciation_after_adjustment = value

```python
expected_depreciation_after_adjustment = [['2021-12-31', 200, 200], ['2022-12-31', 250, 450], ['2023-12-31', 250, 700]]
```

### Step 11: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_depreciation_after_adjustment)
```

### Step 13: Assign asset_repair = create_asset_repair(...)

```python
asset_repair = create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', failure_date='2022-01-20', pi_repair_cost1=60, pi_repair_cost2=40, increase_in_asset_life=0, submit=1)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(asset_repair.total_repair_cost, 100)
```

### Step 15: Assign expected_depreciation_after_repair = value

```python
expected_depreciation_after_repair = [['2021-12-31', 200, 200], ['2022-12-31', 300, 500], ['2023-12-31', 300, 800]]
```

### Step 16: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_depreciation_after_repair)
```

### Step 18: Call asset.reload()

```python
asset.reload()
```

### Step 19: Call asset_value_adjustment.cancel()

```python
asset_value_adjustment.cancel()
```

### Step 20: Assign expected_depreciation_after_cancelling_adjustment = value

```python
expected_depreciation_after_cancelling_adjustment = [['2021-12-31', 200, 200], ['2022-12-31', 250, 450], ['2023-12-31', 250, 700]]
```

### Step 21: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_depreciation_after_cancelling_adjustment)
```


## Complete Example

```python
# Setup
create_asset_data()

# Workflow
asset = create_asset(item_code='Macbook Pro', net_purchase_amount=600, calculate_depreciation=1, depreciation_method='Straight Line', available_for_use_date='2021-01-01', depreciation_start_date='2021-12-31', frequency_of_depreciation=12, total_number_of_depreciations=3, is_existing_asset=1, submit=1)
post_depreciation_entries(date='2021-12-31')
asset.reload()
expected_depreciation_before_adjustment = [['2021-12-31', 200, 200], ['2022-12-31', 200, 400], ['2023-12-31', 200, 600]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_adjustment)
current_asset_value = asset.finance_books[0].value_after_depreciation
asset_value_adjustment = make_asset_value_adjustment(asset=asset.name, date='2022-01-15', current_asset_value=current_asset_value, new_asset_value=500)
asset_value_adjustment.submit()
expected_depreciation_after_adjustment = [['2021-12-31', 200, 200], ['2022-12-31', 250, 450], ['2023-12-31', 250, 700]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_adjustment)
asset_repair = create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', failure_date='2022-01-20', pi_repair_cost1=60, pi_repair_cost2=40, increase_in_asset_life=0, submit=1)
self.assertEqual(asset_repair.total_repair_cost, 100)
expected_depreciation_after_repair = [['2021-12-31', 200, 200], ['2022-12-31', 300, 500], ['2023-12-31', 300, 800]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_repair)
asset.reload()
asset_value_adjustment.cancel()
expected_depreciation_after_cancelling_adjustment = [['2021-12-31', 200, 200], ['2022-12-31', 250, 450], ['2023-12-31', 250, 700]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_cancelling_adjustment)
```

## Next Steps


---

*Source: test_asset_depreciation_schedule.py:918 | Complexity: Advanced | Last updated: 2026-02-04*