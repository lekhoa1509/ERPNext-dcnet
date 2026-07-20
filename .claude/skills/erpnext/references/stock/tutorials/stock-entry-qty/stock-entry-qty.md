# How To: Stock Entry Qty

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test stock entry qty

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

### Step 1: Assign item_code = '_Test Item 2'

```python
item_code = '_Test Item 2'
```

### Step 2: Assign warehouse = '_Test Warehouse - _TC'

```python
warehouse = '_Test Warehouse - _TC'
```

### Step 3: Assign se = make_stock_entry(...)

```python
se = make_stock_entry(item_code=item_code, target=warehouse, qty=0, do_not_save=True)
```

### Step 4: Assign unknown.qty = 1

```python
se.items[0].qty = 1
```

### Step 5: Call se.save()

```python
se.save()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(se.items[0].qty, 1)
```

### Step 7: Call se.save()

```python
se.save()
```


## Complete Example

```python
# Workflow
item_code = '_Test Item 2'
warehouse = '_Test Warehouse - _TC'
se = make_stock_entry(item_code=item_code, target=warehouse, qty=0, do_not_save=True)
with self.assertRaises(InvalidQtyError):
    se.save()
se.items[0].qty = 1
se.save()
self.assertEqual(se.items[0].qty, 1)
```

## Next Steps


---

*Source: test_stock_entry.py:63 | Complexity: Advanced | Last updated: 2026-02-04*