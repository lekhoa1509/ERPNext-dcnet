# How To: Capitalization With Wip Composite Asset

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test capitalization with wip composite asset

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.assets.doctype.asset.depreciation`
- `erpnext.assets.doctype.asset.test_asset`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`

**Required Fixtures:**
- `api_client` fixture


## Step-by-Step Guide

### Step 1: Assign company = '_Test Company with perpetual inventory'

```python
company = '_Test Company with perpetual inventory'
```

### Step 2: Call set_depreciation_settings_in_company()

```python
set_depreciation_settings_in_company(company=company)
```

### Step 3: Assign name = frappe.db.get_value(...)

```python
name = frappe.db.get_value('Asset Category Account', filters={'parent': 'Computers', 'company_name': company}, fieldname=['name'])
```

### Step 4: Call frappe.db.set_value()

```python
frappe.db.set_value('Asset Category Account', name, 'capital_work_in_progress_account', '')
```

### Step 5: Assign stock_rate = 1000

```python
stock_rate = 1000
```

### Step 6: Assign stock_qty = 2

```python
stock_qty = 2
```

### Step 7: Assign stock_amount = 2000

```python
stock_amount = 2000
```

### Step 8: Assign total_amount = 2000

```python
total_amount = 2000
```

### Step 9: Assign wip_composite_asset = create_asset(...)

```python
wip_composite_asset = create_asset(asset_name='Asset Capitalization WIP Composite Asset', is_composite_asset=1, warehouse='Stores - TCP1', company=company)
```

### Step 10: Assign asset_capitalization = create_asset_capitalization(...)

```python
asset_capitalization = create_asset_capitalization(target_asset=wip_composite_asset.name, target_asset_location='Test Location', stock_qty=stock_qty, stock_rate=stock_rate, service_expense_account='Expenses Included In Asset Valuation - TCP1', company=company, submit=1)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(asset_capitalization.target_qty, 1)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(asset_capitalization.stock_items[0].valuation_rate, stock_rate)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(asset_capitalization.stock_items[0].amount, stock_amount)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(asset_capitalization.stock_items_total, stock_amount)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(asset_capitalization.total_value, total_amount)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(asset_capitalization.target_incoming_rate, total_amount)
```

### Step 17: Assign target_asset = frappe.get_doc(...)

```python
target_asset = frappe.get_doc('Asset', asset_capitalization.target_asset)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(target_asset.net_purchase_amount, total_amount)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(target_asset.purchase_amount, total_amount)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(target_asset.status, 'Work In Progress')
```

### Step 21: Assign expected_gle = value

```python
expected_gle = {'_Test Fixed Asset - TCP1': 2000, '_Test Warehouse - TCP1': -2000}
```

### Step 22: Assign actual_gle = get_actual_gle_dict(...)

```python
actual_gle = get_actual_gle_dict(asset_capitalization.name)
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(actual_gle, expected_gle)
```

### Step 24: Assign expected_sle = value

```python
expected_sle = {('Capitalization Source Stock Item', '_Test Warehouse - TCP1'): {'actual_qty': -stock_qty, 'stock_value_difference': -stock_amount}}
```

### Step 25: Assign actual_sle = get_actual_sle_dict(...)

```python
actual_sle = get_actual_sle_dict(asset_capitalization.name)
```

### Step 26: Call self.assertEqual()

```python
self.assertEqual(actual_sle, expected_sle)
```

### Step 27: Call asset_capitalization.cancel()

```python
asset_capitalization.cancel()
```

### Step 28: Call self.assertFalse()

```python
self.assertFalse(get_actual_gle_dict(asset_capitalization.name))
```

### Step 29: Call self.assertFalse()

```python
self.assertFalse(get_actual_sle_dict(asset_capitalization.name))
```


## Complete Example

```python
# Workflow
company = '_Test Company with perpetual inventory'
set_depreciation_settings_in_company(company=company)
name = frappe.db.get_value('Asset Category Account', filters={'parent': 'Computers', 'company_name': company}, fieldname=['name'])
frappe.db.set_value('Asset Category Account', name, 'capital_work_in_progress_account', '')
stock_rate = 1000
stock_qty = 2
stock_amount = 2000
total_amount = 2000
wip_composite_asset = create_asset(asset_name='Asset Capitalization WIP Composite Asset', is_composite_asset=1, warehouse='Stores - TCP1', company=company)
asset_capitalization = create_asset_capitalization(target_asset=wip_composite_asset.name, target_asset_location='Test Location', stock_qty=stock_qty, stock_rate=stock_rate, service_expense_account='Expenses Included In Asset Valuation - TCP1', company=company, submit=1)
self.assertEqual(asset_capitalization.target_qty, 1)
self.assertEqual(asset_capitalization.stock_items[0].valuation_rate, stock_rate)
self.assertEqual(asset_capitalization.stock_items[0].amount, stock_amount)
self.assertEqual(asset_capitalization.stock_items_total, stock_amount)
self.assertEqual(asset_capitalization.total_value, total_amount)
self.assertEqual(asset_capitalization.target_incoming_rate, total_amount)
target_asset = frappe.get_doc('Asset', asset_capitalization.target_asset)
self.assertEqual(target_asset.net_purchase_amount, total_amount)
self.assertEqual(target_asset.purchase_amount, total_amount)
self.assertEqual(target_asset.status, 'Work In Progress')
expected_gle = {'_Test Fixed Asset - TCP1': 2000, '_Test Warehouse - TCP1': -2000}
actual_gle = get_actual_gle_dict(asset_capitalization.name)
self.assertEqual(actual_gle, expected_gle)
expected_sle = {('Capitalization Source Stock Item', '_Test Warehouse - TCP1'): {'actual_qty': -stock_qty, 'stock_value_difference': -stock_amount}}
actual_sle = get_actual_sle_dict(asset_capitalization.name)
self.assertEqual(actual_sle, expected_sle)
asset_capitalization.cancel()
self.assertFalse(get_actual_gle_dict(asset_capitalization.name))
self.assertFalse(get_actual_sle_dict(asset_capitalization.name))
```

## Next Steps


---

*Source: test_asset_capitalization.py:226 | Complexity: Advanced | Last updated: 2026-02-04*