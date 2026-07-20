# How To: Repack Multiple Fg

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test `is_finished_item` for one item repacked into two items.

## Prerequisites

**Required Modules:**
- `frappe.permissions`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.controllers.accounts_controller`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.material_request.material_request`
- `erpnext.stock.doctype.material_request.test_material_request`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.serial_no.serial_no`
- `erpnext.stock.doctype.stock_entry.stock_entry`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.stock_ledger_entry.stock_ledger_entry`
- `erpnext.stock.doctype.stock_reconciliation.stock_reconciliation`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.stock_ledger`
- `erpnext.stock.doctype.batch.test_batch`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.reorder_item`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.stock.doctype.batch.test_batch`
- `erpnext.stock.doctype.batch.test_batch`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.repost_item_valuation.repost_item_valuation`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.controllers.stock_controller`
- `erpnext.stock.doctype.batch.test_batch`
- `erpnext.stock.reorder_item`
- `erpnext.stock.reorder_item`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.stock.doctype.stock_entry.stock_entry`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.stock.utils`


## Step-by-Step Guide

### Step 1: 'Test `is_finished_item` for one item repacked into two items.'

```python
'Test `is_finished_item` for one item repacked into two items.'
```

### Step 2: Call make_stock_entry()

```python
make_stock_entry(item_code='_Test Item', target='_Test Warehouse - _TC', qty=100, basic_rate=100)
```

### Step 3: Assign repack = frappe.copy_doc(...)

```python
repack = frappe.copy_doc(self.globalTestRecords['Stock Entry'][3])
```

### Step 4: Assign repack.posting_date = nowdate(...)

```python
repack.posting_date = nowdate()
```

### Step 5: Assign repack.posting_time = nowtime(...)

```python
repack.posting_time = nowtime()
```

### Step 6: Assign unknown.qty = 100.0

```python
repack.items[0].qty = 100.0
```

### Step 7: Assign unknown.transfer_qty = 100.0

```python
repack.items[0].transfer_qty = 100.0
```

### Step 8: Assign unknown.qty = 50.0

```python
repack.items[1].qty = 50.0
```

### Step 9: Call repack.append()

```python
repack.append('items', {'conversion_factor': 1.0, 'cost_center': '_Test Cost Center - _TC', 'doctype': 'Stock Entry Detail', 'expense_account': 'Stock Adjustment - _TC', 'basic_rate': 150, 'item_code': '_Test Item 2', 'parentfield': 'items', 'qty': 50.0, 'stock_uom': '_Test UOM', 't_warehouse': '_Test Warehouse - _TC', 'transfer_qty': 50.0, 'uom': '_Test UOM'})
```

### Step 10: Call repack.set_stock_entry_type()

```python
repack.set_stock_entry_type()
```

### Step 11: Call repack.insert()

```python
repack.insert()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(repack.items[1].is_finished_item, 1)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(repack.items[2].is_finished_item, 1)
```

### Step 14: Assign unknown.is_finished_item = 0

```python
repack.items[1].is_finished_item = 0
```

### Step 15: Assign unknown.is_finished_item = 0

```python
repack.items[2].is_finished_item = 0
```

### Step 16: Call self.assertRaises()

```python
self.assertRaises(FinishedGoodError, repack.validate_finished_goods)
```

### Step 17: Call repack.delete()

```python
repack.delete()
```

### Step 18: Assign row.set_basic_rate_manually = 1

```python
row.set_basic_rate_manually = 1
```


## Complete Example

```python
# Workflow
'Test `is_finished_item` for one item repacked into two items.'
make_stock_entry(item_code='_Test Item', target='_Test Warehouse - _TC', qty=100, basic_rate=100)
repack = frappe.copy_doc(self.globalTestRecords['Stock Entry'][3])
repack.posting_date = nowdate()
repack.posting_time = nowtime()
repack.items[0].qty = 100.0
repack.items[0].transfer_qty = 100.0
repack.items[1].qty = 50.0
repack.append('items', {'conversion_factor': 1.0, 'cost_center': '_Test Cost Center - _TC', 'doctype': 'Stock Entry Detail', 'expense_account': 'Stock Adjustment - _TC', 'basic_rate': 150, 'item_code': '_Test Item 2', 'parentfield': 'items', 'qty': 50.0, 'stock_uom': '_Test UOM', 't_warehouse': '_Test Warehouse - _TC', 'transfer_qty': 50.0, 'uom': '_Test UOM'})
repack.set_stock_entry_type()
for row in repack.items:
    if row.t_warehouse:
        row.set_basic_rate_manually = 1
repack.insert()
self.assertEqual(repack.items[1].is_finished_item, 1)
self.assertEqual(repack.items[2].is_finished_item, 1)
repack.items[1].is_finished_item = 0
repack.items[2].is_finished_item = 0
self.assertRaises(FinishedGoodError, repack.validate_finished_goods)
repack.delete()
```

## Next Steps


---

*Source: test_stock_entry.py:385 | Complexity: Advanced | Last updated: 2026-02-04*