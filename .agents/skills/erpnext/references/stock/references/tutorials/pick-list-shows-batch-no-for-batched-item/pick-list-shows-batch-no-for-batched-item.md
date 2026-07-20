# How To: Pick List Shows Batch No For Batched Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test pick list shows batch no for batched item

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
item = frappe.db.exists('Item', {'item_name': 'Batched Item'})
```

### Step 2: Assign pr1 = make_purchase_receipt(...)

```python
pr1 = make_purchase_receipt(item_code='Batched Item', qty=1, rate=100.0)
```

### Step 3: Call pr1.load_from_db()

```python
pr1.load_from_db()
```

### Step 4: Assign oldest_batch_no = get_batch_from_bundle(...)

```python
oldest_batch_no = get_batch_from_bundle(pr1.items[0].serial_and_batch_bundle)
```

### Step 5: Assign pr2 = make_purchase_receipt(...)

```python
pr2 = make_purchase_receipt(item_code='Batched Item', qty=2, rate=100.0)
```

### Step 6: Assign pick_list = frappe.get_doc(...)

```python
pick_list = frappe.get_doc({'doctype': 'Pick List', 'company': '_Test Company', 'purpose': 'Material Transfer', 'locations': [{'item_code': 'Batched Item', 'qty': 1, 'stock_qty': 1, 'conversion_factor': 1}]})
```

### Step 7: Call pick_list.set_item_locations()

```python
pick_list.set_item_locations()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(pick_list.locations[0].batch_no, oldest_batch_no)
```

### Step 9: Call pr1.cancel()

```python
pr1.cancel()
```

### Step 10: Call pr2.cancel()

```python
pr2.cancel()
```

### Step 11: Assign item = create_item(...)

```python
item = create_item('Batched Item')
```

### Step 12: Assign item.has_batch_no = 1

```python
item.has_batch_no = 1
```

### Step 13: Assign item.create_new_batch = 1

```python
item.create_new_batch = 1
```

### Step 14: Assign item.batch_number_series = 'B-BATCH-.##'

```python
item.batch_number_series = 'B-BATCH-.##'
```

### Step 15: Call item.save()

```python
item.save()
```

### Step 16: Assign item = frappe.get_doc(...)

```python
item = frappe.get_doc('Item', {'item_name': 'Batched Item'})
```


## Complete Example

```python
# Workflow
item = frappe.db.exists('Item', {'item_name': 'Batched Item'})
if not item:
    item = create_item('Batched Item')
    item.has_batch_no = 1
    item.create_new_batch = 1
    item.batch_number_series = 'B-BATCH-.##'
    item.save()
else:
    item = frappe.get_doc('Item', {'item_name': 'Batched Item'})
pr1 = make_purchase_receipt(item_code='Batched Item', qty=1, rate=100.0)
pr1.load_from_db()
oldest_batch_no = get_batch_from_bundle(pr1.items[0].serial_and_batch_bundle)
pr2 = make_purchase_receipt(item_code='Batched Item', qty=2, rate=100.0)
pick_list = frappe.get_doc({'doctype': 'Pick List', 'company': '_Test Company', 'purpose': 'Material Transfer', 'locations': [{'item_code': 'Batched Item', 'qty': 1, 'stock_qty': 1, 'conversion_factor': 1}]})
pick_list.set_item_locations()
self.assertEqual(pick_list.locations[0].batch_no, oldest_batch_no)
pr1.cancel()
pr2.cancel()
```

## Next Steps


---

*Source: test_pick_list.py:231 | Complexity: Advanced | Last updated: 2026-02-04*