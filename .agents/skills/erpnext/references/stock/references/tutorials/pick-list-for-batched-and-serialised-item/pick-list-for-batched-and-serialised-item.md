# How To: Pick List For Batched And Serialised Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test pick list for batched and serialised item

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

### Step 1: Assign item = frappe.db.exists(...)

```python
item = frappe.db.exists('Item', {'item_name': 'Batched and Serialised Item'})
```

### Step 2: Assign pr1 = make_purchase_receipt(...)

```python
pr1 = make_purchase_receipt(item_code='Batched and Serialised Item', qty=2, rate=100.0)
```

### Step 3: Call pr1.load_from_db()

```python
pr1.load_from_db()
```

### Step 4: Assign oldest_batch_no = get_batch_from_bundle(...)

```python
oldest_batch_no = get_batch_from_bundle(pr1.items[0].serial_and_batch_bundle)
```

### Step 5: Assign oldest_serial_nos = get_serial_nos_from_bundle(...)

```python
oldest_serial_nos = get_serial_nos_from_bundle(pr1.items[0].serial_and_batch_bundle)
```

### Step 6: Assign pr2 = make_purchase_receipt(...)

```python
pr2 = make_purchase_receipt(item_code='Batched and Serialised Item', qty=2, rate=100.0)
```

### Step 7: Assign pick_list = frappe.get_doc(...)

```python
pick_list = frappe.get_doc({'doctype': 'Pick List', 'company': '_Test Company', 'purpose': 'Material Transfer', 'locations': [{'item_code': 'Batched and Serialised Item', 'qty': 2, 'stock_qty': 2, 'conversion_factor': 1}]})
```

### Step 8: Call pick_list.set_item_locations()

```python
pick_list.set_item_locations()
```

### Step 9: Call pick_list.submit()

```python
pick_list.submit()
```

### Step 10: Call pick_list.reload()

```python
pick_list.reload()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(get_batch_from_bundle(pick_list.locations[0].serial_and_batch_bundle), oldest_batch_no)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(get_serial_nos_from_bundle(pick_list.locations[0].serial_and_batch_bundle), oldest_serial_nos)
```

### Step 13: Call pick_list.cancel()

```python
pick_list.cancel()
```

### Step 14: Call pr1.cancel()

```python
pr1.cancel()
```

### Step 15: Call pr2.cancel()

```python
pr2.cancel()
```

### Step 16: Assign item = create_item(...)

```python
item = create_item('Batched and Serialised Item')
```

### Step 17: Assign item.has_batch_no = 1

```python
item.has_batch_no = 1
```

### Step 18: Assign item.create_new_batch = 1

```python
item.create_new_batch = 1
```

### Step 19: Assign item.has_serial_no = 1

```python
item.has_serial_no = 1
```

### Step 20: Assign item.batch_number_series = 'B-BATCH-.##'

```python
item.batch_number_series = 'B-BATCH-.##'
```

### Step 21: Assign item.serial_no_series = 'S-.####'

```python
item.serial_no_series = 'S-.####'
```

### Step 22: Call item.save()

```python
item.save()
```

### Step 23: Assign item = frappe.get_doc(...)

```python
item = frappe.get_doc('Item', {'item_name': 'Batched and Serialised Item'})
```


## Complete Example

```python
# Workflow
item = frappe.db.exists('Item', {'item_name': 'Batched and Serialised Item'})
if not item:
    item = create_item('Batched and Serialised Item')
    item.has_batch_no = 1
    item.create_new_batch = 1
    item.has_serial_no = 1
    item.batch_number_series = 'B-BATCH-.##'
    item.serial_no_series = 'S-.####'
    item.save()
else:
    item = frappe.get_doc('Item', {'item_name': 'Batched and Serialised Item'})
pr1 = make_purchase_receipt(item_code='Batched and Serialised Item', qty=2, rate=100.0)
pr1.load_from_db()
oldest_batch_no = get_batch_from_bundle(pr1.items[0].serial_and_batch_bundle)
oldest_serial_nos = get_serial_nos_from_bundle(pr1.items[0].serial_and_batch_bundle)
pr2 = make_purchase_receipt(item_code='Batched and Serialised Item', qty=2, rate=100.0)
pick_list = frappe.get_doc({'doctype': 'Pick List', 'company': '_Test Company', 'purpose': 'Material Transfer', 'locations': [{'item_code': 'Batched and Serialised Item', 'qty': 2, 'stock_qty': 2, 'conversion_factor': 1}]})
pick_list.set_item_locations()
pick_list.submit()
pick_list.reload()
self.assertEqual(get_batch_from_bundle(pick_list.locations[0].serial_and_batch_bundle), oldest_batch_no)
self.assertEqual(get_serial_nos_from_bundle(pick_list.locations[0].serial_and_batch_bundle), oldest_serial_nos)
pick_list.cancel()
pr1.cancel()
pr2.cancel()
```

## Next Steps


---

*Source: test_pick_list.py:271 | Complexity: Advanced | Last updated: 2026-02-04*