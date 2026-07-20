# How To: Gle Made By Asset Sale

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test gle made by asset sale

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

### Step 1: Assign date = nowdate(...)

```python
date = nowdate()
```

### Step 2: Assign purchase_date = add_months(...)

```python
purchase_date = add_months(get_first_day(date), -2)
```

### Step 3: Assign asset = create_asset(...)

```python
asset = create_asset(calculate_depreciation=1, available_for_use_date=purchase_date, purchase_date=purchase_date, expected_value_after_useful_life=10000, total_number_of_depreciations=10, frequency_of_depreciation=1, submit=1)
```

### Step 4: Assign first_asset_depr_schedule = get_asset_depr_schedule_doc(...)

```python
first_asset_depr_schedule = get_asset_depr_schedule_doc(asset.name, 'Active')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(first_asset_depr_schedule.status, 'Active')
```

### Step 6: Call post_depreciation_entries()

```python
post_depreciation_entries(date=add_months(purchase_date, 2))
```

### Step 7: Assign si = make_sales_invoice(...)

```python
si = make_sales_invoice(asset=asset.name, item_code='Macbook Pro', company='_Test Company', sell_qty=asset.asset_quantity)
```

### Step 8: Assign si.customer = '_Test Customer'

```python
si.customer = '_Test Customer'
```

### Step 9: Assign si.due_date = date

```python
si.due_date = date
```

### Step 10: Assign unknown.rate = 25000

```python
si.get('items')[0].rate = 25000
```

### Step 11: Call si.insert()

```python
si.insert()
```

### Step 12: Call si.submit()

```python
si.submit()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')
```

### Step 14: Call first_asset_depr_schedule.load_from_db()

```python
first_asset_depr_schedule.load_from_db()
```

### Step 15: Assign second_asset_depr_schedule = get_asset_depr_schedule_doc(...)

```python
second_asset_depr_schedule = get_asset_depr_schedule_doc(asset.name, 'Active')
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(second_asset_depr_schedule.status, 'Active')
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(first_asset_depr_schedule.status, 'Cancelled')
```

### Step 18: Call asset.load_from_db()

```python
asset.load_from_db()
```

### Step 19: Assign accumulated_depr_amount = flt(...)

```python
accumulated_depr_amount = flt(asset.net_purchase_amount - asset.finance_books[0].value_after_depreciation, asset.precision('net_purchase_amount'))
```

### Step 20: Assign pro_rata_amount = flt(...)

```python
pro_rata_amount = flt(accumulated_depr_amount - 18000)
```

### Step 21: Assign expected_gle = value

```python
expected_gle = (('_Test Accumulated Depreciations - _TC', flt(accumulated_depr_amount, asset.precision('net_purchase_amount')), 0.0), ('_Test Fixed Asset - _TC', 0.0, 100000.0), ('_Test Gain/Loss on Asset Disposal - _TC', flt(57000.0 - pro_rata_amount, asset.precision('net_purchase_amount')), 0.0), ('Debtors - _TC', 25000.0, 0.0))
```

### Step 22: Assign gle = get_gl_entries(...)

```python
gle = get_gl_entries('Sales Invoice', si.name)
```

### Step 23: Call self.assertSequenceEqual()

```python
self.assertSequenceEqual(gle, expected_gle)
```

### Step 24: Call si.cancel()

```python
si.cancel()
```

### Step 25: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Partially Depreciated')
```


## Complete Example

```python
# Workflow
date = nowdate()
purchase_date = add_months(get_first_day(date), -2)
asset = create_asset(calculate_depreciation=1, available_for_use_date=purchase_date, purchase_date=purchase_date, expected_value_after_useful_life=10000, total_number_of_depreciations=10, frequency_of_depreciation=1, submit=1)
first_asset_depr_schedule = get_asset_depr_schedule_doc(asset.name, 'Active')
self.assertEqual(first_asset_depr_schedule.status, 'Active')
post_depreciation_entries(date=add_months(purchase_date, 2))
si = make_sales_invoice(asset=asset.name, item_code='Macbook Pro', company='_Test Company', sell_qty=asset.asset_quantity)
si.customer = '_Test Customer'
si.due_date = date
si.get('items')[0].rate = 25000
si.insert()
si.submit()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')
first_asset_depr_schedule.load_from_db()
second_asset_depr_schedule = get_asset_depr_schedule_doc(asset.name, 'Active')
self.assertEqual(second_asset_depr_schedule.status, 'Active')
self.assertEqual(first_asset_depr_schedule.status, 'Cancelled')
asset.load_from_db()
accumulated_depr_amount = flt(asset.net_purchase_amount - asset.finance_books[0].value_after_depreciation, asset.precision('net_purchase_amount'))
pro_rata_amount = flt(accumulated_depr_amount - 18000)
expected_gle = (('_Test Accumulated Depreciations - _TC', flt(accumulated_depr_amount, asset.precision('net_purchase_amount')), 0.0), ('_Test Fixed Asset - _TC', 0.0, 100000.0), ('_Test Gain/Loss on Asset Disposal - _TC', flt(57000.0 - pro_rata_amount, asset.precision('net_purchase_amount')), 0.0), ('Debtors - _TC', 25000.0, 0.0))
gle = get_gl_entries('Sales Invoice', si.name)
self.assertSequenceEqual(gle, expected_gle)
si.cancel()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Partially Depreciated')
```

## Next Steps


---

*Source: test_asset.py:313 | Complexity: Advanced | Last updated: 2026-02-04*