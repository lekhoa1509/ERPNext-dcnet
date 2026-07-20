# How To: Gl Entries With Capitalized Asset Repair

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test gl entries with capitalized asset repair

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
asset = create_asset(is_existing_asset=1, calculate_depreciation=1, submit=1)
```

### Step 2: Assign asset_repair = create_asset_repair(...)

```python
asset_repair = create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', submit=1)
```

### Step 3: Call asset.reload()

```python
asset.reload()
```

### Step 4: Assign GLEntry = qb.DocType(...)

```python
GLEntry = qb.DocType('GL Entry')
```

### Step 5: Assign res = qb.from_.select.where.run(...)

```python
res = qb.from_(GLEntry).select(Sum(GLEntry.debit_in_account_currency).as_('total_debit')).where((GLEntry.voucher_type == 'Asset Repair') & (GLEntry.voucher_no == asset_repair.name) & (GLEntry.against_voucher_type == 'Asset') & (GLEntry.against_voucher == asset.name) & (GLEntry.company == asset.company) & (GLEntry.is_cancelled == 0)).run(as_dict=True)
```

### Step 6: Assign booked_value = value

```python
booked_value = res[0].total_debit if res else 0
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(asset.additional_asset_cost, asset_repair.repair_cost)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(booked_value, asset_repair.repair_cost)
```


## Complete Example

```python
# Workflow
asset = create_asset(is_existing_asset=1, calculate_depreciation=1, submit=1)
asset_repair = create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', submit=1)
asset.reload()
GLEntry = qb.DocType('GL Entry')
res = qb.from_(GLEntry).select(Sum(GLEntry.debit_in_account_currency).as_('total_debit')).where((GLEntry.voucher_type == 'Asset Repair') & (GLEntry.voucher_no == asset_repair.name) & (GLEntry.against_voucher_type == 'Asset') & (GLEntry.against_voucher == asset.name) & (GLEntry.company == asset.company) & (GLEntry.is_cancelled == 0)).run(as_dict=True)
booked_value = res[0].total_debit if res else 0
self.assertEqual(asset.additional_asset_cost, asset_repair.repair_cost)
self.assertEqual(booked_value, asset_repair.repair_cost)
```

## Next Steps


---

*Source: test_asset_repair.py:361 | Complexity: Advanced | Last updated: 2026-02-04*