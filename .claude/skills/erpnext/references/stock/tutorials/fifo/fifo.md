# How To: Fifo

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test fifo

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

### Step 1: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Stock Settings', 'allow_negative_stock', 1)
```

### Step 2: Assign item_code = '_Test Item 2'

```python
item_code = '_Test Item 2'
```

### Step 3: Assign warehouse = '_Test Warehouse - _TC'

```python
warehouse = '_Test Warehouse - _TC'
```

### Step 4: Call create_stock_reconciliation()

```python
create_stock_reconciliation(item_code='_Test Item 2', warehouse='_Test Warehouse - _TC', qty=0, rate=100)
```

### Step 5: Call make_stock_entry()

```python
make_stock_entry(item_code=item_code, target=warehouse, qty=1, basic_rate=10)
```

### Step 6: Assign sle = value

```python
sle = get_sle(item_code=item_code, warehouse=warehouse)[0]
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual([[1, 10]], frappe.safe_eval(sle.stock_queue))
```

### Step 8: Call make_stock_entry()

```python
make_stock_entry(item_code=item_code, source=warehouse, qty=2, basic_rate=10)
```

### Step 9: Assign sle = value

```python
sle = get_sle(item_code=item_code, warehouse=warehouse)[0]
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual([[-1, 10]], frappe.safe_eval(sle.stock_queue))
```

### Step 11: Call make_stock_entry()

```python
make_stock_entry(item_code=item_code, source=warehouse, qty=1)
```

### Step 12: Assign sle = value

```python
sle = get_sle(item_code=item_code, warehouse=warehouse)[0]
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual([[-2, 10]], frappe.safe_eval(sle.stock_queue))
```

### Step 14: Call make_stock_entry()

```python
make_stock_entry(item_code=item_code, target=warehouse, qty=3, basic_rate=20)
```

### Step 15: Assign sle = value

```python
sle = get_sle(item_code=item_code, warehouse=warehouse)[0]
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual([[1, 20]], frappe.safe_eval(sle.stock_queue))
```

### Step 17: Call make_stock_entry()

```python
make_stock_entry(item_code=item_code, target=warehouse, qty=1, basic_rate=30)
```

### Step 18: Assign sle = value

```python
sle = get_sle(item_code=item_code, warehouse=warehouse)[0]
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual([[1, 20], [1, 30]], frappe.safe_eval(sle.stock_queue))
```

### Step 20: Call frappe.db.set_default()

```python
frappe.db.set_default('allow_negative_stock', 0)
```


## Complete Example

```python
# Workflow
frappe.db.set_single_value('Stock Settings', 'allow_negative_stock', 1)
item_code = '_Test Item 2'
warehouse = '_Test Warehouse - _TC'
create_stock_reconciliation(item_code='_Test Item 2', warehouse='_Test Warehouse - _TC', qty=0, rate=100)
make_stock_entry(item_code=item_code, target=warehouse, qty=1, basic_rate=10)
sle = get_sle(item_code=item_code, warehouse=warehouse)[0]
self.assertEqual([[1, 10]], frappe.safe_eval(sle.stock_queue))
make_stock_entry(item_code=item_code, source=warehouse, qty=2, basic_rate=10)
sle = get_sle(item_code=item_code, warehouse=warehouse)[0]
self.assertEqual([[-1, 10]], frappe.safe_eval(sle.stock_queue))
make_stock_entry(item_code=item_code, source=warehouse, qty=1)
sle = get_sle(item_code=item_code, warehouse=warehouse)[0]
self.assertEqual([[-2, 10]], frappe.safe_eval(sle.stock_queue))
make_stock_entry(item_code=item_code, target=warehouse, qty=3, basic_rate=20)
sle = get_sle(item_code=item_code, warehouse=warehouse)[0]
self.assertEqual([[1, 20]], frappe.safe_eval(sle.stock_queue))
make_stock_entry(item_code=item_code, target=warehouse, qty=1, basic_rate=30)
sle = get_sle(item_code=item_code, warehouse=warehouse)[0]
self.assertEqual([[1, 20], [1, 30]], frappe.safe_eval(sle.stock_queue))
frappe.db.set_default('allow_negative_stock', 0)
```

## Next Steps


---

*Source: test_stock_entry.py:75 | Complexity: Advanced | Last updated: 2026-02-04*