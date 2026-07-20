# How To: Increase In Asset Life

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test increase in asset life

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
asset = create_asset(calculate_depreciation=1, submit=1)
```

### Step 2: Assign first_asset_depr_schedule = get_asset_depr_schedule_doc(...)

```python
first_asset_depr_schedule = get_asset_depr_schedule_doc(asset.name, 'Active')
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(first_asset_depr_schedule.status, 'Active')
```

### Step 4: Assign initial_num_of_depreciations = num_of_depreciations(...)

```python
initial_num_of_depreciations = num_of_depreciations(asset)
```

### Step 5: Call create_asset_repair()

```python
create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', submit=1, increase_in_asset_life=1)
```

### Step 6: Call asset.reload()

```python
asset.reload()
```

### Step 7: Call first_asset_depr_schedule.load_from_db()

```python
first_asset_depr_schedule.load_from_db()
```

### Step 8: Assign second_asset_depr_schedule = get_asset_depr_schedule_doc(...)

```python
second_asset_depr_schedule = get_asset_depr_schedule_doc(asset.name, 'Active')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(second_asset_depr_schedule.status, 'Active')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(first_asset_depr_schedule.status, 'Cancelled')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(initial_num_of_depreciations + 1, num_of_depreciations(asset))
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(second_asset_depr_schedule.get('depreciation_schedule')[-1].accumulated_depreciation_amount, asset.finance_books[0].value_after_depreciation)
```


## Complete Example

```python
# Workflow
asset = create_asset(calculate_depreciation=1, submit=1)
first_asset_depr_schedule = get_asset_depr_schedule_doc(asset.name, 'Active')
self.assertEqual(first_asset_depr_schedule.status, 'Active')
initial_num_of_depreciations = num_of_depreciations(asset)
create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', submit=1, increase_in_asset_life=1)
asset.reload()
first_asset_depr_schedule.load_from_db()
second_asset_depr_schedule = get_asset_depr_schedule_doc(asset.name, 'Active')
self.assertEqual(second_asset_depr_schedule.status, 'Active')
self.assertEqual(first_asset_depr_schedule.status, 'Cancelled')
self.assertEqual(initial_num_of_depreciations + 1, num_of_depreciations(asset))
self.assertEqual(second_asset_depr_schedule.get('depreciation_schedule')[-1].accumulated_depreciation_amount, asset.finance_books[0].value_after_depreciation)
```

## Next Steps


---

*Source: test_asset_repair.py:327 | Complexity: Advanced | Last updated: 2026-02-04*