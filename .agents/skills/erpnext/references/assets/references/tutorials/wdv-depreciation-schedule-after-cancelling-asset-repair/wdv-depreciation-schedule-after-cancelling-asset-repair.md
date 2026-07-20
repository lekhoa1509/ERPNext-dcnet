# How To: Wdv Depreciation Schedule After Cancelling Asset Repair

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test wdv depreciation schedule after cancelling asset repair

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
asset = create_asset(item_code='Macbook Pro', net_purchase_amount=500, calculate_depreciation=1, depreciation_method='Written Down Value', available_for_use_date='2023-04-01', depreciation_start_date='2023-12-31', frequency_of_depreciation=12, total_number_of_depreciations=4, rate_of_depreciation=40, submit=1)
```

### Step 2: Assign expected_depreciation_before_repair = value

```python
expected_depreciation_before_repair = [['2023-12-31', 150.68, 150.68], ['2024-12-31', 139.73, 290.41], ['2025-12-31', 83.84, 374.25], ['2026-12-31', 50.3, 424.55], ['2027-04-01', 75.45, 500.0]]
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
asset_repair = create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', failure_date='2024-01-01', pi_repair_cost1=60, pi_repair_cost2=40, increase_in_asset_life=0, submit=1)
```

### Step 6: Assign expected_depreciation_after_repair = value

```python
expected_depreciation_after_repair = [['2023-12-31', 180.82, 180.82], ['2024-12-31', 167.67, 348.49], ['2025-12-31', 100.6, 449.09], ['2026-12-31', 60.36, 509.45], ['2027-04-01', 90.55, 600.0]]
```

### Step 7: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_depreciation_after_repair)
```

### Step 9: Call asset_repair.cancel()

```python
asset_repair.cancel()
```

### Step 10: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_depreciation_before_repair)
```


## Complete Example

```python
# Setup
create_asset_data()

# Workflow
asset = create_asset(item_code='Macbook Pro', net_purchase_amount=500, calculate_depreciation=1, depreciation_method='Written Down Value', available_for_use_date='2023-04-01', depreciation_start_date='2023-12-31', frequency_of_depreciation=12, total_number_of_depreciations=4, rate_of_depreciation=40, submit=1)
expected_depreciation_before_repair = [['2023-12-31', 150.68, 150.68], ['2024-12-31', 139.73, 290.41], ['2025-12-31', 83.84, 374.25], ['2026-12-31', 50.3, 424.55], ['2027-04-01', 75.45, 500.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_repair)
asset_repair = create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', failure_date='2024-01-01', pi_repair_cost1=60, pi_repair_cost2=40, increase_in_asset_life=0, submit=1)
expected_depreciation_after_repair = [['2023-12-31', 180.82, 180.82], ['2024-12-31', 167.67, 348.49], ['2025-12-31', 100.6, 449.09], ['2026-12-31', 60.36, 509.45], ['2027-04-01', 90.55, 600.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_repair)
asset_repair.cancel()
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_repair)
```

## Next Steps


---

*Source: test_asset_depreciation_schedule.py:601 | Complexity: Advanced | Last updated: 2026-02-04*