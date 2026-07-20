# How To: Capitalize Only Service Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test capitalize only service item

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

### Step 1: Assign company = '_Test Company'

```python
company = '_Test Company'
```

### Step 2: Assign service_rate = 500

```python
service_rate = 500
```

### Step 3: Assign service_qty = 2

```python
service_qty = 2
```

### Step 4: Assign service_amount = 1000

```python
service_amount = 1000
```

### Step 5: Assign total_amount = 1000

```python
total_amount = 1000
```

### Step 6: Assign wip_composite_asset = create_asset(...)

```python
wip_composite_asset = create_asset(asset_name='Asset Capitalization WIP Composite Asset', is_composite_asset=1, warehouse='Stores - TCP1', company=company)
```

### Step 7: Assign asset_capitalization = create_asset_capitalization(...)

```python
asset_capitalization = create_asset_capitalization(target_asset=wip_composite_asset.name, target_asset_location='Test Location', service_qty=service_qty, service_rate=service_rate, service_expense_account='Expenses Included In Asset Valuation - _TC', company=company, submit=1)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(asset_capitalization.service_items[0].amount, service_amount)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(asset_capitalization.service_items_total, service_amount)
```

### Step 10: Assign target_asset = frappe.get_doc(...)

```python
target_asset = frappe.get_doc('Asset', asset_capitalization.target_asset)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(target_asset.net_purchase_amount, total_amount)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(target_asset.purchase_amount, total_amount)
```

### Step 13: Assign expected_gle = value

```python
expected_gle = {'CWIP Account - _TC': 1000.0, 'Expenses Included In Asset Valuation - _TC': -1000.0}
```

### Step 14: Assign actual_gle = get_actual_gle_dict(...)

```python
actual_gle = get_actual_gle_dict(asset_capitalization.name)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(actual_gle, expected_gle)
```

### Step 16: Call asset_capitalization.cancel()

```python
asset_capitalization.cancel()
```

### Step 17: Call self.assertFalse()

```python
self.assertFalse(get_actual_gle_dict(asset_capitalization.name))
```

### Step 18: Call self.assertFalse()

```python
self.assertFalse(get_actual_sle_dict(asset_capitalization.name))
```


## Complete Example

```python
# Workflow
company = '_Test Company'
service_rate = 500
service_qty = 2
service_amount = 1000
total_amount = 1000
wip_composite_asset = create_asset(asset_name='Asset Capitalization WIP Composite Asset', is_composite_asset=1, warehouse='Stores - TCP1', company=company)
asset_capitalization = create_asset_capitalization(target_asset=wip_composite_asset.name, target_asset_location='Test Location', service_qty=service_qty, service_rate=service_rate, service_expense_account='Expenses Included In Asset Valuation - _TC', company=company, submit=1)
self.assertEqual(asset_capitalization.service_items[0].amount, service_amount)
self.assertEqual(asset_capitalization.service_items_total, service_amount)
target_asset = frappe.get_doc('Asset', asset_capitalization.target_asset)
self.assertEqual(target_asset.net_purchase_amount, total_amount)
self.assertEqual(target_asset.purchase_amount, total_amount)
expected_gle = {'CWIP Account - _TC': 1000.0, 'Expenses Included In Asset Valuation - _TC': -1000.0}
actual_gle = get_actual_gle_dict(asset_capitalization.name)
self.assertEqual(actual_gle, expected_gle)
asset_capitalization.cancel()
self.assertFalse(get_actual_gle_dict(asset_capitalization.name))
self.assertFalse(get_actual_sle_dict(asset_capitalization.name))
```

## Next Steps


---

*Source: test_asset_capitalization.py:300 | Complexity: Advanced | Last updated: 2026-02-04*