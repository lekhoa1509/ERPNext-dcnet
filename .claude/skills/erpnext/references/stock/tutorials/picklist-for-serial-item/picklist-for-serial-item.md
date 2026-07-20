# How To: Picklist For Serial Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test picklist for serial item

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

### Step 2: Assign item = value

```python
item = make_item(properties={'is_stock_item': 1, 'has_serial_no': 1, 'serial_no_series': 'SN-PICKLT-.######'}).name
```

### Step 3: Call make_stock_entry()

```python
make_stock_entry(item=item, to_warehouse=warehouse, qty=50, basic_rate=100)
```

### Step 4: Assign so = make_sales_order(...)

```python
so = make_sales_order(item_code=item, qty=25.0, rate=100)
```

### Step 5: Assign pl = create_pick_list(...)

```python
pl = create_pick_list(so.name)
```

### Step 6: Call pl.submit()

```python
pl.submit()
```

### Step 7: Assign picked_serial_nos = value

```python
picked_serial_nos = []
```

### Step 8: Assign so1 = make_sales_order(...)

```python
so1 = make_sales_order(item_code=item, qty=10.0, rate=100)
```

### Step 9: Assign pl1 = create_pick_list(...)

```python
pl1 = create_pick_list(so1.name)
```

### Step 10: Call pl1.submit()

```python
pl1.submit()
```

### Step 11: Call pl1.cancel()

```python
pl1.cancel()
```

### Step 12: Call pl.cancel()

```python
pl.cancel()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(loc.qty, 25.0)
```

### Step 14: Call self.assertTrue()

```python
self.assertTrue(loc.serial_and_batch_bundle)
```

### Step 15: Assign data = frappe.get_all(...)

```python
data = frappe.get_all('Serial and Batch Entry', fields=['serial_no'], filters={'parent': loc.serial_and_batch_bundle})
```

### Step 16: Assign picked_serial_nos = value

```python
picked_serial_nos = [d.serial_no for d in data]
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(len(picked_serial_nos), 25)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(loc.qty, 10.0)
```

### Step 19: Call self.assertTrue()

```python
self.assertTrue(loc.serial_and_batch_bundle)
```

### Step 20: Assign data = frappe.get_all(...)

```python
data = frappe.get_all('Serial and Batch Entry', fields=['qty', 'batch_no'], filters={'parent': loc.serial_and_batch_bundle})
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(len(data), 10)
```

### Step 22: Call self.assertTrue()

```python
self.assertTrue(d.serial_no not in picked_serial_nos)
```


## Complete Example

```python
# Workflow
warehouse = '_Test Warehouse - _TC'
item = make_item(properties={'is_stock_item': 1, 'has_serial_no': 1, 'serial_no_series': 'SN-PICKLT-.######'}).name
make_stock_entry(item=item, to_warehouse=warehouse, qty=50, basic_rate=100)
so = make_sales_order(item_code=item, qty=25.0, rate=100)
pl = create_pick_list(so.name)
pl.submit()
picked_serial_nos = []
for loc in pl.locations:
    self.assertEqual(loc.qty, 25.0)
    self.assertTrue(loc.serial_and_batch_bundle)
    data = frappe.get_all('Serial and Batch Entry', fields=['serial_no'], filters={'parent': loc.serial_and_batch_bundle})
    picked_serial_nos = [d.serial_no for d in data]
    self.assertEqual(len(picked_serial_nos), 25)
so1 = make_sales_order(item_code=item, qty=10.0, rate=100)
pl1 = create_pick_list(so1.name)
pl1.submit()
for loc in pl1.locations:
    self.assertEqual(loc.qty, 10.0)
    self.assertTrue(loc.serial_and_batch_bundle)
    data = frappe.get_all('Serial and Batch Entry', fields=['qty', 'batch_no'], filters={'parent': loc.serial_and_batch_bundle})
    self.assertEqual(len(data), 10)
    for d in data:
        self.assertTrue(d.serial_no not in picked_serial_nos)
pl1.cancel()
pl.cancel()
```

## Next Steps


---

*Source: test_pick_list.py:765 | Complexity: Advanced | Last updated: 2026-02-04*