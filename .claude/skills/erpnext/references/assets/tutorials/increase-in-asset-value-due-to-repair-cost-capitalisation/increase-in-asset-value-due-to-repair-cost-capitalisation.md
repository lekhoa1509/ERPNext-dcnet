# How To: Increase In Asset Value Due To Repair Cost Capitalisation

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test increase in asset value due to repair cost capitalisation

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

**Required Fixtures:**
- `api_client` fixture


## Step-by-Step Guide

### Step 1: Assign asset = create_asset(...)

```python
asset = create_asset(calculate_depreciation=1, submit=1)
```

### Step 2: Assign initial_asset_value = get_asset_value_after_depreciation(...)

```python
initial_asset_value = get_asset_value_after_depreciation(asset.name)
```

### Step 3: Assign asset_repair = create_asset_repair(...)

```python
asset_repair = create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', submit=1, increase_in_asset_value=1)
```

### Step 4: Call asset.reload()

```python
asset.reload()
```

### Step 5: Assign increase_in_asset_value = value

```python
increase_in_asset_value = get_asset_value_after_depreciation(asset.name) - initial_asset_value
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(asset_repair.repair_cost, increase_in_asset_value)
```


## Complete Example

```python
# Workflow
asset = create_asset(calculate_depreciation=1, submit=1)
initial_asset_value = get_asset_value_after_depreciation(asset.name)
asset_repair = create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', submit=1, increase_in_asset_value=1)
asset.reload()
increase_in_asset_value = get_asset_value_after_depreciation(asset.name) - initial_asset_value
self.assertEqual(asset_repair.repair_cost, increase_in_asset_value)
```

## Next Steps


---

*Source: test_asset_repair.py:158 | Complexity: Intermediate | Last updated: 2026-02-04*