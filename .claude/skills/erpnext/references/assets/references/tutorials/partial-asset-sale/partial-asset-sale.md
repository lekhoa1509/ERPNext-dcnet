# How To: Partial Asset Sale

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test partial asset sale

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

### Step 3: Assign depreciation_start_date = add_months(...)

```python
depreciation_start_date = add_months(get_last_day(date), -2)
```

### Step 4: Assign asset = create_asset(...)

```python
asset = create_asset(item_code='Macbook Pro', is_existing_asset=1, calculate_depreciation=1, available_for_use_date=purchase_date, purchase_date=purchase_date, depreciation_start_date=depreciation_start_date, net_purchase_amount=1000000.0, purchase_amount=1000000.0, asset_quantity=10, total_number_of_depreciations=12, frequency_of_depreciation=1, submit=1)
```

### Step 5: Assign asset_depr_schedule_before_sale = get_asset_depr_schedule_doc(...)

```python
asset_depr_schedule_before_sale = get_asset_depr_schedule_doc(asset.name, 'Active')
```

### Step 6: Call post_depreciation_entries()

```python
post_depreciation_entries(date)
```

### Step 7: Call asset.reload()

```python
asset.reload()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(asset.asset_quantity, 10)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(asset.net_purchase_amount, 1000000)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(asset.status, 'Partially Depreciated')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(asset_depr_schedule_before_sale.depreciation_schedule[0].get('depreciation_amount'), 83333.33)
```

### Step 12: Assign si = make_sales_invoice(...)

```python
si = make_sales_invoice(asset=asset.name, item_code='Macbook Pro', company='_Test Company', sell_qty=5)
```

### Step 13: Assign si.customer = '_Test Customer'

```python
si.customer = '_Test Customer'
```

### Step 14: Assign si.due_date = date

```python
si.due_date = date
```

### Step 15: Assign unknown.rate = 25000

```python
si.get('items')[0].rate = 25000
```

### Step 16: Call si.insert()

```python
si.insert()
```

### Step 17: Call si.submit()

```python
si.submit()
```

### Step 18: Call asset.reload()

```python
asset.reload()
```

### Step 19: Assign asset_depr_schedule_after_sale = get_asset_depr_schedule_doc(...)

```python
asset_depr_schedule_after_sale = get_asset_depr_schedule_doc(asset.name, 'Active')
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(asset.asset_quantity, 5)
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(asset.net_purchase_amount, 500000)
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(asset.status, 'Sold')
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(asset_depr_schedule_after_sale.depreciation_schedule[0].get('depreciation_amount'), 41666.66)
```


## Complete Example

```python
# Workflow
date = nowdate()
purchase_date = add_months(get_first_day(date), -2)
depreciation_start_date = add_months(get_last_day(date), -2)
asset = create_asset(item_code='Macbook Pro', is_existing_asset=1, calculate_depreciation=1, available_for_use_date=purchase_date, purchase_date=purchase_date, depreciation_start_date=depreciation_start_date, net_purchase_amount=1000000.0, purchase_amount=1000000.0, asset_quantity=10, total_number_of_depreciations=12, frequency_of_depreciation=1, submit=1)
asset_depr_schedule_before_sale = get_asset_depr_schedule_doc(asset.name, 'Active')
post_depreciation_entries(date)
asset.reload()
self.assertEqual(asset.asset_quantity, 10)
self.assertEqual(asset.net_purchase_amount, 1000000)
self.assertEqual(asset.status, 'Partially Depreciated')
self.assertEqual(asset_depr_schedule_before_sale.depreciation_schedule[0].get('depreciation_amount'), 83333.33)
si = make_sales_invoice(asset=asset.name, item_code='Macbook Pro', company='_Test Company', sell_qty=5)
si.customer = '_Test Customer'
si.due_date = date
si.get('items')[0].rate = 25000
si.insert()
si.submit()
asset.reload()
asset_depr_schedule_after_sale = get_asset_depr_schedule_doc(asset.name, 'Active')
self.assertEqual(asset.asset_quantity, 5)
self.assertEqual(asset.net_purchase_amount, 500000)
self.assertEqual(asset.status, 'Sold')
self.assertEqual(asset_depr_schedule_after_sale.depreciation_schedule[0].get('depreciation_amount'), 41666.66)
```

## Next Steps


---

*Source: test_asset.py:704 | Complexity: Advanced | Last updated: 2026-02-04*