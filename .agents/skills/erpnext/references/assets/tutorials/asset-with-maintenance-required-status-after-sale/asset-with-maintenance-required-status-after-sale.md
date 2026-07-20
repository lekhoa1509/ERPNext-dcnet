# How To: Asset With Maintenance Required Status After Sale

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test asset with maintenance required status after sale

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
asset = create_asset(calculate_depreciation=1, available_for_use_date='2020-06-06', purchase_date='2020-01-01', expected_value_after_useful_life=10000, total_number_of_depreciations=3, frequency_of_depreciation=10, maintenance_required=1, depreciation_start_date='2020-12-31', submit=1)
```

### Step 2: Call post_depreciation_entries()

```python
post_depreciation_entries(date='2021-01-01')
```

### Step 3: Assign si = make_sales_invoice(...)

```python
si = make_sales_invoice(asset=asset.name, item_code='Macbook Pro', company='_Test Company', sell_qty=asset.asset_quantity)
```

### Step 4: Assign si.customer = '_Test Customer'

```python
si.customer = '_Test Customer'
```

### Step 5: Assign si.due_date = nowdate(...)

```python
si.due_date = nowdate()
```

### Step 6: Assign unknown.rate = 25000

```python
si.get('items')[0].rate = 25000
```

### Step 7: Call si.insert()

```python
si.insert()
```

### Step 8: Call si.submit()

```python
si.submit()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')
```

### Step 10: Call update_maintenance_status()

```python
update_maintenance_status()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')
```


## Complete Example

```python
# Workflow
asset = create_asset(calculate_depreciation=1, available_for_use_date='2020-06-06', purchase_date='2020-01-01', expected_value_after_useful_life=10000, total_number_of_depreciations=3, frequency_of_depreciation=10, maintenance_required=1, depreciation_start_date='2020-12-31', submit=1)
post_depreciation_entries(date='2021-01-01')
si = make_sales_invoice(asset=asset.name, item_code='Macbook Pro', company='_Test Company', sell_qty=asset.asset_quantity)
si.customer = '_Test Customer'
si.due_date = nowdate()
si.get('items')[0].rate = 25000
si.insert()
si.submit()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')
update_maintenance_status()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')
```

## Next Steps


---

*Source: test_asset.py:447 | Complexity: Advanced | Last updated: 2026-02-04*