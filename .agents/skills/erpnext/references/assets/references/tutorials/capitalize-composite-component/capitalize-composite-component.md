# How To: Capitalize Composite Component

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test capitalize composite component

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

### Step 5: Assign wip_composite_asset = create_asset(...)

```python
wip_composite_asset = create_asset(asset_name='Asset Capitalization WIP Composite Asset', is_composite_asset=1, warehouse='Stores - TCP1', company=company)
```

### Step 6: Assign consumed_asset_value = 100000

```python
consumed_asset_value = 100000
```

### Step 7: Assign consumed_asset = create_asset(...)

```python
consumed_asset = create_asset(asset_name='Asset Capitalization Consumable Asset', asset_value=consumed_asset_value, submit=1, warehouse='Stores - _TC', is_composite_component=1, company=company)
```

### Step 8: Assign asset_capitalization = create_asset_capitalization(...)

```python
asset_capitalization = create_asset_capitalization(target_asset=wip_composite_asset.name, target_asset_location='Test Location', consumed_asset=consumed_asset.name, company=company, submit=1)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(asset_capitalization.target_qty, 1)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(asset_capitalization.asset_items[0].asset_value, consumed_asset_value)
```

### Step 11: Assign actual_gle = get_actual_gle_dict(...)

```python
actual_gle = get_actual_gle_dict(asset_capitalization.name)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(actual_gle, {})
```


## Complete Example

```python
# Workflow
company = '_Test Company with perpetual inventory'
set_depreciation_settings_in_company(company=company)
name = frappe.db.get_value('Asset Category Account', filters={'parent': 'Computers', 'company_name': company}, fieldname=['name'])
frappe.db.set_value('Asset Category Account', name, 'capital_work_in_progress_account', '')
wip_composite_asset = create_asset(asset_name='Asset Capitalization WIP Composite Asset', is_composite_asset=1, warehouse='Stores - TCP1', company=company)
consumed_asset_value = 100000
consumed_asset = create_asset(asset_name='Asset Capitalization Consumable Asset', asset_value=consumed_asset_value, submit=1, warehouse='Stores - _TC', is_composite_component=1, company=company)
asset_capitalization = create_asset_capitalization(target_asset=wip_composite_asset.name, target_asset_location='Test Location', consumed_asset=consumed_asset.name, company=company, submit=1)
self.assertEqual(asset_capitalization.target_qty, 1)
self.assertEqual(asset_capitalization.asset_items[0].asset_value, consumed_asset_value)
actual_gle = get_actual_gle_dict(asset_capitalization.name)
self.assertEqual(actual_gle, {})
```

## Next Steps


---

*Source: test_asset_capitalization.py:348 | Complexity: Advanced | Last updated: 2026-02-04*