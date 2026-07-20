# How To: Picklist For Batch Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test picklist for batch item

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
item = make_item(properties={'is_stock_item': 1, 'has_batch_no': 1, 'batch_number_series': 'PICKLT-.######'}).name
```

### Step 3: Call make_stock_entry()

```python
make_stock_entry(item=item, to_warehouse=warehouse, qty=50, basic_rate=100, batches=frappe._dict({'PICKLT-000001': 30, 'PICKLT-000002': 20}))
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

### Step 7: Call pl.save()

```python
pl.save()
```

### Step 8: Call pl.submit()

```python
pl.submit()
```

### Step 9: Assign so1 = make_sales_order(...)

```python
so1 = make_sales_order(item_code=item, qty=10.0, rate=100)
```

### Step 10: Assign pl1 = create_pick_list(...)

```python
pl1 = create_pick_list(so1.name)
```

### Step 11: Call pl1.submit()

```python
pl1.submit()
```

### Step 12: Call pl1.cancel()

```python
pl1.cancel()
```

### Step 13: Call pl.cancel()

```python
pl.cancel()
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(loc.qty, 25.0)
```

### Step 15: Call self.assertTrue()

```python
self.assertTrue(loc.serial_and_batch_bundle)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(loc.qty, 5.0)
```

### Step 17: Call self.assertTrue()

```python
self.assertTrue(loc.serial_and_batch_bundle)
```

### Step 18: Assign data = frappe.get_all(...)

```python
data = frappe.get_all('Serial and Batch Entry', fields=['qty', 'batch_no'], filters={'parent': loc.serial_and_batch_bundle})
```

### Step 19: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'Batch', 'batch_id': batch_id, 'item': item}).insert()
```

### Step 20: Call self.assertTrue()

```python
self.assertTrue(d.batch_no in ['PICKLT-000001', 'PICKLT-000002'])
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(d.qty, 5.0 * -1)
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(d.qty, 5.0 * -1)
```


## Complete Example

```python
# Workflow
warehouse = '_Test Warehouse - _TC'
item = make_item(properties={'is_stock_item': 1, 'has_batch_no': 1, 'batch_number_series': 'PICKLT-.######'}).name
for batch_id in ['PICKLT-000001', 'PICKLT-000002']:
    if not frappe.db.exists('Batch', batch_id):
        frappe.get_doc({'doctype': 'Batch', 'batch_id': batch_id, 'item': item}).insert()
make_stock_entry(item=item, to_warehouse=warehouse, qty=50, basic_rate=100, batches=frappe._dict({'PICKLT-000001': 30, 'PICKLT-000002': 20}))
so = make_sales_order(item_code=item, qty=25.0, rate=100)
pl = create_pick_list(so.name)
pl.submit()
for loc in pl.locations:
    self.assertEqual(loc.qty, 25.0)
    self.assertTrue(loc.serial_and_batch_bundle)
pl.save()
pl.submit()
so1 = make_sales_order(item_code=item, qty=10.0, rate=100)
pl1 = create_pick_list(so1.name)
pl1.submit()
for loc in pl1.locations:
    self.assertEqual(loc.qty, 5.0)
    self.assertTrue(loc.serial_and_batch_bundle)
    data = frappe.get_all('Serial and Batch Entry', fields=['qty', 'batch_no'], filters={'parent': loc.serial_and_batch_bundle})
    for d in data:
        self.assertTrue(d.batch_no in ['PICKLT-000001', 'PICKLT-000002'])
        if d.batch_no == 'PICKLT-000001':
            self.assertEqual(d.qty, 5.0 * -1)
        elif d.batch_no == 'PICKLT-000002':
            self.assertEqual(d.qty, 5.0 * -1)
pl1.cancel()
pl.cancel()
```

## Next Steps


---

*Source: test_pick_list.py:704 | Complexity: Advanced | Last updated: 2026-02-04*