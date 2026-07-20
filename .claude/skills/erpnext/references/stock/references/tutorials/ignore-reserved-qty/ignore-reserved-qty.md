# How To: Ignore Reserved Qty

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test ignore reserved qty

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.exceptions`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.data`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.get_item_details`
- `erpnext.stock.serial_batch_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`


## Step-by-Step Guide

### Step 1: Assign batch_item_name = 'Reserve Batch Item'

```python
batch_item_name = 'Reserve Batch Item'
```

### Step 2: Assign batch_id = 'Reserve Batch 1'

```python
batch_id = 'Reserve Batch 1'
```

### Step 3: Call self.make_batch_item()

```python
self.make_batch_item(batch_item_name)
```

### Step 4: Call self.make_new_batch_and_entry()

```python
self.make_new_batch_and_entry(batch_item_name, batch_id, '_Test Warehouse - _TC')
```

### Step 5: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Stock Settings', 'enable_stock_reservation', 1)
```

### Step 6: Assign sales_order = make_sales_order(...)

```python
sales_order = make_sales_order(item_code=batch_item_name, warehouse='_Test Warehouse - _TC', qty=50, rate=20)
```

### Step 7: Assign pl = create_pick_list(...)

```python
pl = create_pick_list(sales_order.name)
```

### Step 8: Call pl.submit()

```python
pl.submit()
```

### Step 9: Call pl.create_stock_reservation_entries()

```python
pl.create_stock_reservation_entries(notify=False)
```

### Step 10: Assign batch = frappe.get_doc(...)

```python
batch = frappe.get_doc('Batch', batch_id)
```

### Step 11: Call batch.recalculate_batch_qty()

```python
batch.recalculate_batch_qty()
```

### Step 12: Call batch.reload()

```python
batch.reload()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(batch.batch_qty, 90)
```


## Complete Example

```python
# Workflow
from erpnext.selling.doctype.sales_order.sales_order import create_pick_list
from erpnext.selling.doctype.sales_order.test_sales_order import make_sales_order
batch_item_name = 'Reserve Batch Item'
batch_id = 'Reserve Batch 1'
self.make_batch_item(batch_item_name)
self.make_new_batch_and_entry(batch_item_name, batch_id, '_Test Warehouse - _TC')
frappe.db.set_single_value('Stock Settings', 'enable_stock_reservation', 1)
sales_order = make_sales_order(item_code=batch_item_name, warehouse='_Test Warehouse - _TC', qty=50, rate=20)
pl = create_pick_list(sales_order.name)
pl.submit()
pl.create_stock_reservation_entries(notify=False)
batch = frappe.get_doc('Batch', batch_id)
batch.recalculate_batch_qty()
batch.reload()
self.assertEqual(batch.batch_qty, 90)
```

## Next Steps


---

*Source: test_batch.py:315 | Complexity: Advanced | Last updated: 2026-02-04*