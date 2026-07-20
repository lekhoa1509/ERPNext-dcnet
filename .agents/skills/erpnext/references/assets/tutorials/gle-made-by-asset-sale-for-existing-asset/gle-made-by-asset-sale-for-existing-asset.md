# How To: Gle Made By Asset Sale For Existing Asset

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test gle made by asset sale for existing asset

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.data`
- `erpnext.accounts.doctype.journal_entry.test_journal_entry`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.assets.doctype.asset.asset`
- `erpnext.assets.doctype.asset.depreciation`
- `erpnext.assets.doctype.asset_depreciation_schedule.asset_depreciation_schedule`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.assets.doctype.asset_capitalization.test_asset_capitalization`


## Step-by-Step Guide

### Step 1: Assign asset = create_asset(...)

```python
asset = create_asset(calculate_depreciation=1, available_for_use_date='2020-04-01', purchase_date='2020-04-01', expected_value_after_useful_life=0, total_number_of_depreciations=5, opening_number_of_booked_depreciations=2, frequency_of_depreciation=12, depreciation_start_date='2023-03-31', opening_accumulated_depreciation=24000, net_purchase_amount=60000, submit=1)
```

### Step 2: Assign expected_depr_values = value

```python
expected_depr_values = [['2023-03-31', 12000, 36000], ['2024-03-31', 12000, 48000], ['2025-03-31', 12000, 60000]]
```

### Step 3: Assign first_asset_depr_schedule = get_depr_schedule(...)

```python
first_asset_depr_schedule = get_depr_schedule(asset.name, 'Active')
```

### Step 4: Call post_depreciation_entries()

```python
post_depreciation_entries(date='2023-03-31')
```

### Step 5: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(item_code='Macbook Pro', asset=asset.name, qty=1, rate=40000, posting_date=getdate('2023-05-23'))
```

### Step 6: Call asset.load_from_db()

```python
asset.load_from_db()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')
```

### Step 8: Assign expected_values = value

```python
expected_values = [['2023-03-31', 12000, 36000], ['2023-05-23', 1737.7, 37737.7]]
```

### Step 9: Assign second_asset_depr_schedule = get_depr_schedule(...)

```python
second_asset_depr_schedule = get_depr_schedule(asset.name, 'Active')
```

### Step 10: Assign expected_gle = value

```python
expected_gle = (('_Test Accumulated Depreciations - _TC', 37737.7, 0.0), ('_Test Fixed Asset - _TC', 0.0, 60000.0), ('_Test Gain/Loss on Asset Disposal - _TC', 0.0, 17737.7), ('Debtors - _TC', 40000.0, 0.0))
```

### Step 11: Assign gle = get_gl_entries(...)

```python
gle = get_gl_entries('Sales Invoice', si.name)
```

### Step 12: Call self.assertSequenceEqual()

```python
self.assertSequenceEqual(gle, expected_gle)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(getdate(expected_depr_values[i][0]), schedule.schedule_date)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(expected_depr_values[i][1], schedule.depreciation_amount)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(expected_depr_values[i][2], schedule.accumulated_depreciation_amount)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(getdate(expected_values[i][0]), schedule.schedule_date)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(expected_values[i][1], schedule.depreciation_amount)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(expected_values[i][2], schedule.accumulated_depreciation_amount)
```

### Step 19: Call self.assertTrue()

```python
self.assertTrue(schedule.journal_entry)
```


## Complete Example

```python
# Workflow
from erpnext.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
asset = create_asset(calculate_depreciation=1, available_for_use_date='2020-04-01', purchase_date='2020-04-01', expected_value_after_useful_life=0, total_number_of_depreciations=5, opening_number_of_booked_depreciations=2, frequency_of_depreciation=12, depreciation_start_date='2023-03-31', opening_accumulated_depreciation=24000, net_purchase_amount=60000, submit=1)
expected_depr_values = [['2023-03-31', 12000, 36000], ['2024-03-31', 12000, 48000], ['2025-03-31', 12000, 60000]]
first_asset_depr_schedule = get_depr_schedule(asset.name, 'Active')
for i, schedule in enumerate(first_asset_depr_schedule):
    self.assertEqual(getdate(expected_depr_values[i][0]), schedule.schedule_date)
    self.assertEqual(expected_depr_values[i][1], schedule.depreciation_amount)
    self.assertEqual(expected_depr_values[i][2], schedule.accumulated_depreciation_amount)
post_depreciation_entries(date='2023-03-31')
si = create_sales_invoice(item_code='Macbook Pro', asset=asset.name, qty=1, rate=40000, posting_date=getdate('2023-05-23'))
asset.load_from_db()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')
expected_values = [['2023-03-31', 12000, 36000], ['2023-05-23', 1737.7, 37737.7]]
second_asset_depr_schedule = get_depr_schedule(asset.name, 'Active')
for i, schedule in enumerate(second_asset_depr_schedule):
    self.assertEqual(getdate(expected_values[i][0]), schedule.schedule_date)
    self.assertEqual(expected_values[i][1], schedule.depreciation_amount)
    self.assertEqual(expected_values[i][2], schedule.accumulated_depreciation_amount)
    self.assertTrue(schedule.journal_entry)
expected_gle = (('_Test Accumulated Depreciations - _TC', 37737.7, 0.0), ('_Test Fixed Asset - _TC', 0.0, 60000.0), ('_Test Gain/Loss on Asset Disposal - _TC', 0.0, 17737.7), ('Debtors - _TC', 40000.0, 0.0))
gle = get_gl_entries('Sales Invoice', si.name)
self.assertSequenceEqual(gle, expected_gle)
```

## Next Steps


---

*Source: test_asset.py:376 | Complexity: Advanced | Last updated: 2026-02-04*