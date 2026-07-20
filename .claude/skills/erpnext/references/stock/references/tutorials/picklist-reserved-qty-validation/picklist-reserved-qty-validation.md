# How To: Picklist Reserved Qty Validation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test picklist reserved qty validation

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.packed_item.test_packed_item`
- `erpnext.stock.doctype.pick_list.pick_list`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.stock_reconciliation.stock_reconciliation`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.pick_list.pick_list`
- `json`
- `frappe.model.mapper`


## Step-by-Step Guide

### Step 1: Assign warehouse = '_Test Warehouse - _TC'

```python
warehouse = '_Test Warehouse - _TC'
```

### Step 2: Assign test_stock_item = '_Test Stock Item'

```python
test_stock_item = '_Test Stock Item'
```

### Step 3: Call make_stock_entry()

```python
make_stock_entry(item_code=test_stock_item, to_warehouse=warehouse, qty=15)
```

### Step 4: Assign sales_order_1 = make_sales_order(...)

```python
sales_order_1 = make_sales_order(item_code=test_stock_item, warehouse=warehouse, qty=10)
```

### Step 5: Assign picklist_1 = create_pick_list(...)

```python
picklist_1 = create_pick_list(sales_order_1.name)
```

### Step 6: Call picklist_1.submit()

```python
picklist_1.submit()
```

### Step 7: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(picklist_1.name)
```

### Step 8: Assign unknown.qty = 5

```python
dn.items[0].qty = 5
```

### Step 9: Call dn.save()

```python
dn.save()
```

### Step 10: Call dn.submit()

```python
dn.submit()
```

### Step 11: Call picklist_1.reload()

```python
picklist_1.reload()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(picklist_1.status, 'Partly Delivered')
```

### Step 13: Assign sales_order_2 = make_sales_order(...)

```python
sales_order_2 = make_sales_order(item_code=test_stock_item, warehouse=warehouse, qty=10)
```

### Step 14: Assign picklist_2 = create_pick_list(...)

```python
picklist_2 = create_pick_list(sales_order_2.name)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(picklist_2.locations[0].qty, 5)
```

### Step 16: Call create_item()

```python
create_item(item_code=test_stock_item, is_stock_item=1)
```


## Complete Example

```python
# Workflow
from erpnext.selling.doctype.sales_order.test_sales_order import make_sales_order
warehouse = '_Test Warehouse - _TC'
test_stock_item = '_Test Stock Item'
if not frappe.db.exists('Item', test_stock_item):
    create_item(item_code=test_stock_item, is_stock_item=1)
make_stock_entry(item_code=test_stock_item, to_warehouse=warehouse, qty=15)
sales_order_1 = make_sales_order(item_code=test_stock_item, warehouse=warehouse, qty=10)
picklist_1 = create_pick_list(sales_order_1.name)
picklist_1.submit()
dn = create_delivery_note(picklist_1.name)
dn.items[0].qty = 5
dn.save()
dn.submit()
picklist_1.reload()
self.assertEqual(picklist_1.status, 'Partly Delivered')
sales_order_2 = make_sales_order(item_code=test_stock_item, warehouse=warehouse, qty=10)
picklist_2 = create_pick_list(sales_order_2.name)
self.assertEqual(picklist_2.locations[0].qty, 5)
```

## Next Steps


---

*Source: test_pick_list.py:648 | Complexity: Advanced | Last updated: 2026-02-04*