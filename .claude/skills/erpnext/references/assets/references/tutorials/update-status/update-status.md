# How To: Update Status

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test update status

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

### Step 1: Assign asset = create_asset(...)

```python
asset = create_asset(submit=1)
```

### Step 2: Assign initial_status = value

```python
initial_status = asset.status
```

### Step 3: Assign asset_repair = create_asset_repair(...)

```python
asset_repair = create_asset_repair(asset=asset)
```

### Step 4: Assign asset_repair.repair_status = 'Completed'

```python
asset_repair.repair_status = 'Completed'
```

### Step 5: Call asset_repair.save()

```python
asset_repair.save()
```

### Step 6: Assign asset_status = frappe.db.get_value(...)

```python
asset_status = frappe.db.get_value('Asset', asset_repair.asset, 'status')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(asset_status, initial_status)
```

### Step 8: Call asset.reload()

```python
asset.reload()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(asset.status, 'Out of Order')
```


## Complete Example

```python
# Workflow
asset = create_asset(submit=1)
initial_status = asset.status
asset_repair = create_asset_repair(asset=asset)
if asset_repair.repair_status == 'Pending':
    asset.reload()
    self.assertEqual(asset.status, 'Out of Order')
asset_repair.repair_status = 'Completed'
asset_repair.save()
asset_status = frappe.db.get_value('Asset', asset_repair.asset, 'status')
self.assertEqual(asset_status, initial_status)
```

## Next Steps


---

*Source: test_asset_repair.py:68 | Complexity: Advanced | Last updated: 2026-02-04*