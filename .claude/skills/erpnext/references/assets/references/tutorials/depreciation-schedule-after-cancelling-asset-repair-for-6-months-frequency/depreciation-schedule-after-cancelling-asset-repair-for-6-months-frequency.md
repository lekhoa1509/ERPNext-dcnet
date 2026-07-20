# How To: Depreciation Schedule After Cancelling Asset Repair For 6 Months Frequency

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test depreciation schedule after cancelling asset repair for 6 months frequency

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
asset = create_asset(item_code='Macbook Pro', net_purchase_amount=500, calculate_depreciation=1, depreciation_method='Straight Line', available_for_use_date='2023-01-01', depreciation_start_date='2023-06-30', frequency_of_depreciation=6, total_number_of_depreciations=4, submit=1)
```

### Step 2: Assign expected_depreciation_before_repair = value

```python
expected_depreciation_before_repair = [['2023-06-30', 125.0, 125.0], ['2023-12-31', 125.0, 250.0], ['2024-06-30', 125.0, 375.0], ['2024-12-31', 125.0, 500.0]]
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
expected_depreciation_after_repair = [['2023-06-30', 150.0, 150.0], ['2023-12-31', 150.0, 300.0], ['2024-06-30', 150.0, 450.0], ['2024-12-31', 150.0, 600.0]]
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
asset = create_asset(item_code='Macbook Pro', net_purchase_amount=500, calculate_depreciation=1, depreciation_method='Straight Line', available_for_use_date='2023-01-01', depreciation_start_date='2023-06-30', frequency_of_depreciation=6, total_number_of_depreciations=4, submit=1)
expected_depreciation_before_repair = [['2023-06-30', 125.0, 125.0], ['2023-12-31', 125.0, 250.0], ['2024-06-30', 125.0, 375.0], ['2024-12-31', 125.0, 500.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_repair)
asset_repair = create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', failure_date='2023-04-01', pi_repair_cost1=60, pi_repair_cost2=40, increase_in_asset_life=0, submit=1)
self.assertEqual(asset_repair.total_repair_cost, 100)
expected_depreciation_after_repair = [['2023-06-30', 150.0, 150.0], ['2023-12-31', 150.0, 300.0], ['2024-06-30', 150.0, 450.0], ['2024-12-31', 150.0, 600.0]]
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

*Source: test_asset_depreciation_schedule.py:457 | Complexity: Advanced | Last updated: 2026-02-04*