# How To: Depreciation Schedule After Sale Of Asset

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test depreciation schedule after sale of asset

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

### Step 13: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(item_code='Macbook Pro', asset=asset.name, qty=1, rate=300, posting_date=getdate('2022-04-01'))
```

### Step 14: Call asset.load_from_db()

```python
asset.load_from_db()
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')
```

### Step 16: Assign expected_depreciation_after_sale = value

```python
expected_depreciation_after_sale = [['2021-12-31', 200.0, 200.0], ['2022-04-01', 62.33, 262.33]]
```

### Step 17: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_depreciation_after_sale)
```

### Step 19: Call si.cancel()

```python
si.cancel()
```

### Step 20: Call asset.reload()

```python
asset.reload()
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Partially Depreciated')
```

### Step 22: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_depreciation_after_adjustment)
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
si = create_sales_invoice(item_code='Macbook Pro', asset=asset.name, qty=1, rate=300, posting_date=getdate('2022-04-01'))
asset.load_from_db()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')
expected_depreciation_after_sale = [['2021-12-31', 200.0, 200.0], ['2022-04-01', 62.33, 262.33]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_sale)
si.cancel()
asset.reload()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Partially Depreciated')
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_adjustment)
```

## Next Steps


---

*Source: test_asset_depreciation_schedule.py:1007 | Complexity: Advanced | Last updated: 2026-02-04*