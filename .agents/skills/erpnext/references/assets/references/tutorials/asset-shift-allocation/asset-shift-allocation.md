# How To: Asset Shift Allocation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test asset shift allocation

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.assets.doctype.asset.test_asset`
- `erpnext.assets.doctype.asset_depreciation_schedule.asset_depreciation_schedule`


## Step-by-Step Guide

### Step 1: Assign asset = create_asset(...)

```python
asset = create_asset(calculate_depreciation=1, available_for_use_date='2023-01-01', purchase_date='2023-01-01', net_purchase_amount=120000, depreciation_start_date='2023-01-31', total_number_of_depreciations=12, frequency_of_depreciation=1, shift_based=1, submit=1)
```

### Step 2: Assign expected_schedules = value

```python
expected_schedules = [['2023-01-31', 10000.0, 10000.0, 'Single'], ['2023-02-28', 10000.0, 20000.0, 'Single'], ['2023-03-31', 10000.0, 30000.0, 'Single'], ['2023-04-30', 10000.0, 40000.0, 'Single'], ['2023-05-31', 10000.0, 50000.0, 'Single'], ['2023-06-30', 10000.0, 60000.0, 'Single'], ['2023-07-31', 10000.0, 70000.0, 'Single'], ['2023-08-31', 10000.0, 80000.0, 'Single'], ['2023-09-30', 10000.0, 90000.0, 'Single'], ['2023-10-31', 10000.0, 100000.0, 'Single'], ['2023-11-30', 10000.0, 110000.0, 'Single'], ['2023-12-31', 10000.0, 120000.0, 'Single']]
```

### Step 3: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount, d.shift] for d in get_depr_schedule(asset.name, 'Active')]
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_schedules)
```

### Step 5: Assign asset_shift_allocation = frappe.get_doc.insert(...)

```python
asset_shift_allocation = frappe.get_doc({'doctype': 'Asset Shift Allocation', 'asset': asset.name}).insert()
```

### Step 6: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount, d.shift] for d in asset_shift_allocation.get('depreciation_schedule')]
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_schedules)
```

### Step 8: Assign asset_shift_allocation = frappe.get_doc(...)

```python
asset_shift_allocation = frappe.get_doc('Asset Shift Allocation', asset_shift_allocation.name)
```

### Step 9: Assign unknown.shift = 'Triple'

```python
asset_shift_allocation.depreciation_schedule[4].shift = 'Triple'
```

### Step 10: Call asset_shift_allocation.save()

```python
asset_shift_allocation.save()
```

### Step 11: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount, d.shift] for d in asset_shift_allocation.get('depreciation_schedule')]
```

### Step 12: Assign expected_schedules = value

```python
expected_schedules = [['2023-01-31', 10000.0, 10000.0, 'Single'], ['2023-02-28', 10000.0, 20000.0, 'Single'], ['2023-03-31', 10000.0, 30000.0, 'Single'], ['2023-04-30', 10000.0, 40000.0, 'Single'], ['2023-05-31', 20000.0, 60000.0, 'Triple'], ['2023-06-30', 10000.0, 70000.0, 'Single'], ['2023-07-31', 10000.0, 80000.0, 'Single'], ['2023-08-31', 10000.0, 90000.0, 'Single'], ['2023-09-30', 10000.0, 100000.0, 'Single'], ['2023-10-31', 10000.0, 110000.0, 'Single'], ['2023-11-30', 10000.0, 120000.0, 'Single']]
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_schedules)
```

### Step 14: Call asset_shift_allocation.submit()

```python
asset_shift_allocation.submit()
```

### Step 15: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount, d.shift] for d in get_depr_schedule(asset.name, 'Active')]
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_schedules)
```


## Complete Example

```python
# Workflow
asset = create_asset(calculate_depreciation=1, available_for_use_date='2023-01-01', purchase_date='2023-01-01', net_purchase_amount=120000, depreciation_start_date='2023-01-31', total_number_of_depreciations=12, frequency_of_depreciation=1, shift_based=1, submit=1)
expected_schedules = [['2023-01-31', 10000.0, 10000.0, 'Single'], ['2023-02-28', 10000.0, 20000.0, 'Single'], ['2023-03-31', 10000.0, 30000.0, 'Single'], ['2023-04-30', 10000.0, 40000.0, 'Single'], ['2023-05-31', 10000.0, 50000.0, 'Single'], ['2023-06-30', 10000.0, 60000.0, 'Single'], ['2023-07-31', 10000.0, 70000.0, 'Single'], ['2023-08-31', 10000.0, 80000.0, 'Single'], ['2023-09-30', 10000.0, 90000.0, 'Single'], ['2023-10-31', 10000.0, 100000.0, 'Single'], ['2023-11-30', 10000.0, 110000.0, 'Single'], ['2023-12-31', 10000.0, 120000.0, 'Single']]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount, d.shift] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_schedules)
asset_shift_allocation = frappe.get_doc({'doctype': 'Asset Shift Allocation', 'asset': asset.name}).insert()
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount, d.shift] for d in asset_shift_allocation.get('depreciation_schedule')]
self.assertEqual(schedules, expected_schedules)
asset_shift_allocation = frappe.get_doc('Asset Shift Allocation', asset_shift_allocation.name)
asset_shift_allocation.depreciation_schedule[4].shift = 'Triple'
asset_shift_allocation.save()
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount, d.shift] for d in asset_shift_allocation.get('depreciation_schedule')]
expected_schedules = [['2023-01-31', 10000.0, 10000.0, 'Single'], ['2023-02-28', 10000.0, 20000.0, 'Single'], ['2023-03-31', 10000.0, 30000.0, 'Single'], ['2023-04-30', 10000.0, 40000.0, 'Single'], ['2023-05-31', 20000.0, 60000.0, 'Triple'], ['2023-06-30', 10000.0, 70000.0, 'Single'], ['2023-07-31', 10000.0, 80000.0, 'Single'], ['2023-08-31', 10000.0, 90000.0, 'Single'], ['2023-09-30', 10000.0, 100000.0, 'Single'], ['2023-10-31', 10000.0, 110000.0, 'Single'], ['2023-11-30', 10000.0, 120000.0, 'Single']]
self.assertEqual(schedules, expected_schedules)
asset_shift_allocation.submit()
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount, d.shift] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_schedules)
```

## Next Steps


---

*Source: test_asset_shift_allocation.py:24 | Complexity: Advanced | Last updated: 2026-02-04*