# How To: Asset Depreciation Value Adjustment

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test asset depreciation value adjustment

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.assets.doctype.asset.asset`
- `erpnext.assets.doctype.asset.depreciation`
- `erpnext.assets.doctype.asset.test_asset`
- `erpnext.assets.doctype.asset_depreciation_schedule.asset_depreciation_schedule`
- `erpnext.assets.doctype.asset_repair.test_asset_repair`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`


## Step-by-Step Guide

### Step 1: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=120000.0, location='Test Location')
```

### Step 2: Assign asset_name = frappe.db.get_value(...)

```python
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
```

### Step 3: Assign asset_doc = frappe.get_doc(...)

```python
asset_doc = frappe.get_doc('Asset', asset_name)
```

### Step 4: Assign asset_doc.calculate_depreciation = 1

```python
asset_doc.calculate_depreciation = 1
```

### Step 5: Assign asset_doc.available_for_use_date = '2023-01-15'

```python
asset_doc.available_for_use_date = '2023-01-15'
```

### Step 6: Assign asset_doc.purchase_date = '2023-01-15'

```python
asset_doc.purchase_date = '2023-01-15'
```

### Step 7: Call asset_doc.append()

```python
asset_doc.append('finance_books', {'expected_value_after_useful_life': 200, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 12, 'frequency_of_depreciation': 1, 'depreciation_start_date': '2023-01-31'})
```

### Step 8: Call asset_doc.submit()

```python
asset_doc.submit()
```

### Step 9: Assign first_asset_depr_schedule = get_asset_depr_schedule_doc(...)

```python
first_asset_depr_schedule = get_asset_depr_schedule_doc(asset_doc.name, 'Active')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(first_asset_depr_schedule.status, 'Active')
```

### Step 11: Call post_depreciation_entries()

```python
post_depreciation_entries(getdate('2023-08-21'))
```

### Step 12: Assign current_value = get_asset_value_after_depreciation(...)

```python
current_value = get_asset_value_after_depreciation(asset_doc.name)
```

### Step 13: Assign adj_doc = make_asset_value_adjustment(...)

```python
adj_doc = make_asset_value_adjustment(asset=asset_doc.name, current_asset_value=current_value, new_asset_value=50000.0, date='2023-08-21')
```

### Step 14: Call adj_doc.submit()

```python
adj_doc.submit()
```

### Step 15: Call first_asset_depr_schedule.load_from_db()

```python
first_asset_depr_schedule.load_from_db()
```

### Step 16: Assign second_asset_depr_schedule = get_asset_depr_schedule_doc(...)

```python
second_asset_depr_schedule = get_asset_depr_schedule_doc(asset_doc.name, 'Active')
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(second_asset_depr_schedule.status, 'Active')
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(first_asset_depr_schedule.status, 'Cancelled')
```

### Step 19: Assign expected_gle = value

```python
expected_gle = (('_Test Difference Account - _TC', 4625.29, 0.0), ('_Test Fixed Asset - _TC', 0.0, 4625.29))
```

### Step 20: Assign gle = frappe.db.sql(...)

```python
gle = frappe.db.sql("select account, debit, credit from `tabGL Entry`\n\t\t\twhere voucher_type='Journal Entry' and voucher_no = %s\n\t\t\torder by account", adj_doc.journal_entry)
```

### Step 21: Call self.assertSequenceEqual()

```python
self.assertSequenceEqual(gle, expected_gle)
```

### Step 22: Assign expected_schedules = value

```python
expected_schedules = [['2023-01-31', 5474.73, 5474.73], ['2023-02-28', 9983.33, 15458.06], ['2023-03-31', 9983.33, 25441.39], ['2023-04-30', 9983.33, 35424.72], ['2023-05-31', 9983.33, 45408.05], ['2023-06-30', 9983.33, 55391.38], ['2023-07-31', 9983.33, 65374.71], ['2023-08-31', 9070.36, 74445.07], ['2023-09-30', 9070.36, 83515.43], ['2023-10-31', 9070.36, 92585.79], ['2023-11-30', 9070.36, 101656.15], ['2023-12-31', 9070.36, 110726.51], ['2024-01-15', 4448.2, 115174.71]]
```

### Step 23: Assign schedules = value

```python
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in second_asset_depr_schedule.get('depreciation_schedule')]
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(schedules, expected_schedules)
```


## Complete Example

```python
# Workflow
pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=120000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset_doc = frappe.get_doc('Asset', asset_name)
asset_doc.calculate_depreciation = 1
asset_doc.available_for_use_date = '2023-01-15'
asset_doc.purchase_date = '2023-01-15'
asset_doc.append('finance_books', {'expected_value_after_useful_life': 200, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 12, 'frequency_of_depreciation': 1, 'depreciation_start_date': '2023-01-31'})
asset_doc.submit()
first_asset_depr_schedule = get_asset_depr_schedule_doc(asset_doc.name, 'Active')
self.assertEqual(first_asset_depr_schedule.status, 'Active')
post_depreciation_entries(getdate('2023-08-21'))
current_value = get_asset_value_after_depreciation(asset_doc.name)
adj_doc = make_asset_value_adjustment(asset=asset_doc.name, current_asset_value=current_value, new_asset_value=50000.0, date='2023-08-21')
adj_doc.submit()
first_asset_depr_schedule.load_from_db()
second_asset_depr_schedule = get_asset_depr_schedule_doc(asset_doc.name, 'Active')
self.assertEqual(second_asset_depr_schedule.status, 'Active')
self.assertEqual(first_asset_depr_schedule.status, 'Cancelled')
expected_gle = (('_Test Difference Account - _TC', 4625.29, 0.0), ('_Test Fixed Asset - _TC', 0.0, 4625.29))
gle = frappe.db.sql("select account, debit, credit from `tabGL Entry`\n\t\t\twhere voucher_type='Journal Entry' and voucher_no = %s\n\t\t\torder by account", adj_doc.journal_entry)
self.assertSequenceEqual(gle, expected_gle)
expected_schedules = [['2023-01-31', 5474.73, 5474.73], ['2023-02-28', 9983.33, 15458.06], ['2023-03-31', 9983.33, 25441.39], ['2023-04-30', 9983.33, 35424.72], ['2023-05-31', 9983.33, 45408.05], ['2023-06-30', 9983.33, 55391.38], ['2023-07-31', 9983.33, 65374.71], ['2023-08-31', 9070.36, 74445.07], ['2023-09-30', 9070.36, 83515.43], ['2023-10-31', 9070.36, 92585.79], ['2023-11-30', 9070.36, 101656.15], ['2023-12-31', 9070.36, 110726.51], ['2024-01-15', 4448.2, 115174.71]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in second_asset_depr_schedule.get('depreciation_schedule')]
self.assertEqual(schedules, expected_schedules)
```

## Next Steps


---

*Source: test_asset_value_adjustment.py:52 | Complexity: Advanced | Last updated: 2026-02-04*