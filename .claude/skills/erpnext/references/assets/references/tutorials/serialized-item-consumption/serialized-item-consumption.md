# How To: Serialized Item Consumption

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test serialized item consumption

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

### Step 1: Assign stock_entry = make_serialized_item(...)

```python
stock_entry = make_serialized_item(self)
```

### Step 2: Assign bundle_id = value

```python
bundle_id = stock_entry.get('items')[0].serial_and_batch_bundle
```

### Step 3: Assign serial_nos = get_serial_nos_from_bundle(...)

```python
serial_nos = get_serial_nos_from_bundle(bundle_id)
```

### Step 4: Assign serial_no = value

```python
serial_no = serial_nos[0]
```

### Step 5: Call create_asset_repair()

```python
create_asset_repair(stock_consumption=1, item_code=stock_entry.get('items')[0].item_code, warehouse='_Test Warehouse - _TC', serial_no=[serial_no], submit=1)
```

### Step 6: Assign asset_repair = create_asset_repair(...)

```python
asset_repair = create_asset_repair(stock_consumption=1, warehouse='_Test Warehouse - _TC', item_code=stock_entry.get('items')[0].item_code)
```

### Step 7: Assign asset_repair.repair_status = 'Completed'

```python
asset_repair.repair_status = 'Completed'
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, asset_repair.submit)
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.stock_entry.test_stock_entry import make_serialized_item
stock_entry = make_serialized_item(self)
bundle_id = stock_entry.get('items')[0].serial_and_batch_bundle
serial_nos = get_serial_nos_from_bundle(bundle_id)
serial_no = serial_nos[0]
create_asset_repair(stock_consumption=1, item_code=stock_entry.get('items')[0].item_code, warehouse='_Test Warehouse - _TC', serial_no=[serial_no], submit=1)
asset_repair = create_asset_repair(stock_consumption=1, warehouse='_Test Warehouse - _TC', item_code=stock_entry.get('items')[0].item_code)
asset_repair.repair_status = 'Completed'
self.assertRaises(frappe.ValidationError, asset_repair.submit)
```

## Next Steps


---

*Source: test_asset_repair.py:122 | Complexity: Advanced | Last updated: 2026-02-04*