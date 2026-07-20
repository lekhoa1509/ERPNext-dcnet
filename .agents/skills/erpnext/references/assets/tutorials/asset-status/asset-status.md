# How To: Asset Status

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test asset status

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.query_builder.functions`
- `frappe.tests`
- `frappe.utils`
- `erpnext.assets.doctype.asset.asset`
- `erpnext.assets.doctype.asset.test_asset`
- `erpnext.assets.doctype.asset_depreciation_schedule.asset_depreciation_schedule`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`


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

### Step 4: Assign si = make_sales_invoice(...)

```python
si = make_sales_invoice(asset=asset.name, item_code='Macbook Pro', company='_Test Company', sell_qty=asset.asset_quantity)
```

### Step 5: Assign si.customer = '_Test Customer'

```python
si.customer = '_Test Customer'
```

### Step 6: Assign si.due_date = date

```python
si.due_date = date
```

### Step 7: Assign unknown.rate = 25000

```python
si.get('items')[0].rate = 25000
```

### Step 8: Call si.insert()

```python
si.insert()
```

### Step 9: Call si.submit()

```python
si.submit()
```

### Step 10: Call asset.reload()

```python
asset.reload()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')
```

### Step 12: Assign asset_repair = frappe.new_doc(...)

```python
asset_repair = frappe.new_doc('Asset Repair')
```

### Step 13: Call asset_repair.update()

```python
asset_repair.update({'company': '_Test Company', 'asset': asset.name, 'asset_name': asset.asset_name})
```

### Step 14: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, asset_repair.save)
```


## Complete Example

```python
# Workflow
date = nowdate()
purchase_date = add_months(get_first_day(date), -2)
asset = create_asset(calculate_depreciation=1, available_for_use_date=purchase_date, purchase_date=purchase_date, expected_value_after_useful_life=10000, total_number_of_depreciations=10, frequency_of_depreciation=1, submit=1)
si = make_sales_invoice(asset=asset.name, item_code='Macbook Pro', company='_Test Company', sell_qty=asset.asset_quantity)
si.customer = '_Test Customer'
si.due_date = date
si.get('items')[0].rate = 25000
si.insert()
si.submit()
asset.reload()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')
asset_repair = frappe.new_doc('Asset Repair')
asset_repair.update({'company': '_Test Company', 'asset': asset.name, 'asset_name': asset.asset_name})
self.assertRaises(frappe.ValidationError, asset_repair.save)
```

## Next Steps


---

*Source: test_asset_repair.py:39 | Complexity: Advanced | Last updated: 2026-02-04*