# How To: Daily Prorata Based Depreciation Schedule After Cancelling Asset Repair

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test daily prorata based depreciation schedule after cancelling asset repair

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
asset = create_asset(item_code='Macbook Pro', net_purchase_amount=500, calculate_depreciation=1, depreciation_method='Straight Line', available_for_use_date='2023-01-01', depreciation_start_date='2023-01-31', daily_prorata_based=1, frequency_of_depreciation=1, total_number_of_depreciations=12, submit=1)
```

### Step 2: Assign expected_depreciation_before_repair = value

```python
expected_depreciation_before_repair = [['2023-01-31', 42.47, 42.47], ['2023-02-28', 38.36, 80.83], ['2023-03-31', 42.47, 123.3], ['2023-04-30', 41.1, 164.4], ['2023-05-31', 42.47, 206.87], ['2023-06-30', 41.1, 247.97], ['2023-07-31', 42.47, 290.44], ['2023-08-31', 42.47, 332.91], ['2023-09-30', 41.1, 374.01], ['2023-10-31', 42.47, 416.48], ['2023-11-30', 41.1, 457.58], ['2023-12-31', 42.42, 500.0]]
```

### Step 3: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_depreciation_before_repair)
```

### Step 5: Assign asset_repair = create_asset_repair(...)

```python
asset_repair = create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', failure_date='2023-04-01', pi_repair_cost1=60, pi_repair_cost2=40, increase_in_asset_life=0, submit=1)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(asset_repair.total_repair_cost, 100)
```

### Step 7: Assign expected_depreciation_after_repair = value

```python
expected_depreciation_after_repair = [['2023-01-31', 50.96, 50.96], ['2023-02-28', 46.03, 96.99], ['2023-03-31', 50.96, 147.95], ['2023-04-30', 49.32, 197.27], ['2023-05-31', 50.96, 248.23], ['2023-06-30', 49.32, 297.55], ['2023-07-31', 50.96, 348.51], ['2023-08-31', 50.96, 399.47], ['2023-09-30', 49.32, 448.79], ['2023-10-31', 50.96, 499.75], ['2023-11-30', 49.32, 549.07], ['2023-12-31', 50.93, 600.0]]
```

### Step 8: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_depreciation_after_repair)
```

### Step 10: Call asset.reload()

```python
asset.reload()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(asset.finance_books[0].value_after_depreciation, 600)
```

### Step 12: Call asset_repair.cancel()

```python
asset_repair.cancel()
```

### Step 13: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_depreciation_before_repair)
```

### Step 15: Call asset.reload()

```python
asset.reload()
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(asset.finance_books[0].value_after_depreciation, 500)
```


## Complete Example

```python
# Setup
create_asset_data()

# Workflow
asset = create_asset(item_code='Macbook Pro', net_purchase_amount=500, calculate_depreciation=1, depreciation_method='Straight Line', available_for_use_date='2023-01-01', depreciation_start_date='2023-01-31', daily_prorata_based=1, frequency_of_depreciation=1, total_number_of_depreciations=12, submit=1)
expected_depreciation_before_repair = [['2023-01-31', 42.47, 42.47], ['2023-02-28', 38.36, 80.83], ['2023-03-31', 42.47, 123.3], ['2023-04-30', 41.1, 164.4], ['2023-05-31', 42.47, 206.87], ['2023-06-30', 41.1, 247.97], ['2023-07-31', 42.47, 290.44], ['2023-08-31', 42.47, 332.91], ['2023-09-30', 41.1, 374.01], ['2023-10-31', 42.47, 416.48], ['2023-11-30', 41.1, 457.58], ['2023-12-31', 42.42, 500.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_repair)
asset_repair = create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', failure_date='2023-04-01', pi_repair_cost1=60, pi_repair_cost2=40, increase_in_asset_life=0, submit=1)
self.assertEqual(asset_repair.total_repair_cost, 100)
expected_depreciation_after_repair = [['2023-01-31', 50.96, 50.96], ['2023-02-28', 46.03, 96.99], ['2023-03-31', 50.96, 147.95], ['2023-04-30', 49.32, 197.27], ['2023-05-31', 50.96, 248.23], ['2023-06-30', 49.32, 297.55], ['2023-07-31', 50.96, 348.51], ['2023-08-31', 50.96, 399.47], ['2023-09-30', 49.32, 448.79], ['2023-10-31', 50.96, 499.75], ['2023-11-30', 49.32, 549.07], ['2023-12-31', 50.93, 600.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_repair)
asset.reload()
self.assertEqual(asset.finance_books[0].value_after_depreciation, 600)
asset_repair.cancel()
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_repair)
asset.reload()
self.assertEqual(asset.finance_books[0].value_after_depreciation, 500)
```

## Next Steps


---

*Source: test_asset_depreciation_schedule.py:662 | Complexity: Advanced | Last updated: 2026-02-04*