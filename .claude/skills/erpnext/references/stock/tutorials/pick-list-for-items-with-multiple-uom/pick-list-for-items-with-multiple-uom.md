# How To: Pick List For Items With Multiple Uom

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test pick list for items with multiple UOM

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

### Step 1: Assign item_code = value

```python
item_code = make_item(uoms=[{'uom': 'Nos', 'conversion_factor': 1}, {'uom': 'Hand', 'conversion_factor': 5}, {'uom': 'Unit', 'conversion_factor': 0.5}]).name
```

### Step 2: Assign purchase_receipt = make_purchase_receipt(...)

```python
purchase_receipt = make_purchase_receipt(item_code=item_code, qty=10)
```

### Step 3: Call purchase_receipt.submit()

```python
purchase_receipt.submit()
```

### Step 4: Assign sales_order = frappe.get_doc.insert(...)

```python
sales_order = frappe.get_doc({'doctype': 'Sales Order', 'customer': '_Test Customer', 'company': '_Test Company', 'items': [{'item_code': item_code, 'qty': 1, 'uom': 'Hand', 'delivery_date': frappe.utils.today(), 'warehouse': '_Test Warehouse - _TC'}, {'item_code': item_code, 'qty': 1, 'conversion_factor': 1, 'delivery_date': frappe.utils.today(), 'warehouse': '_Test Warehouse - _TC'}]}).insert()
```

### Step 5: Call sales_order.submit()

```python
sales_order.submit()
```

### Step 6: Assign pick_list = frappe.get_doc(...)

```python
pick_list = frappe.get_doc({'doctype': 'Pick List', 'company': '_Test Company', 'customer': '_Test Customer', 'items_based_on': 'Sales Order', 'purpose': 'Delivery', 'locations': [{'item_code': item_code, 'qty': 2, 'stock_qty': 1, 'uom': 'Unit', 'conversion_factor': 0.5, 'sales_order': sales_order.name, 'sales_order_item': sales_order.items[0].name}, {'item_code': item_code, 'qty': 1, 'stock_qty': 1, 'conversion_factor': 1, 'sales_order': sales_order.name, 'sales_order_item': sales_order.items[1].name}]})
```

### Step 7: Call pick_list.set_item_locations()

```python
pick_list.set_item_locations()
```

### Step 8: Call pick_list.submit()

```python
pick_list.submit()
```

### Step 9: Assign delivery_note = create_delivery_note(...)

```python
delivery_note = create_delivery_note(pick_list.name)
```

### Step 10: Call pick_list.load_from_db()

```python
pick_list.load_from_db()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(pick_list.locations[0].picked_qty, delivery_note.items[0].qty * delivery_note.items[0].conversion_factor)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(pick_list.locations[1].qty, delivery_note.items[1].qty)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(sales_order.items[0].conversion_factor, delivery_note.items[0].conversion_factor)
```

### Step 14: Call pick_list.cancel()

```python
pick_list.cancel()
```

### Step 15: Call sales_order.cancel()

```python
sales_order.cancel()
```

### Step 16: Call purchase_receipt.cancel()

```python
purchase_receipt.cancel()
```


## Complete Example

```python
# Workflow
item_code = make_item(uoms=[{'uom': 'Nos', 'conversion_factor': 1}, {'uom': 'Hand', 'conversion_factor': 5}, {'uom': 'Unit', 'conversion_factor': 0.5}]).name
purchase_receipt = make_purchase_receipt(item_code=item_code, qty=10)
purchase_receipt.submit()
sales_order = frappe.get_doc({'doctype': 'Sales Order', 'customer': '_Test Customer', 'company': '_Test Company', 'items': [{'item_code': item_code, 'qty': 1, 'uom': 'Hand', 'delivery_date': frappe.utils.today(), 'warehouse': '_Test Warehouse - _TC'}, {'item_code': item_code, 'qty': 1, 'conversion_factor': 1, 'delivery_date': frappe.utils.today(), 'warehouse': '_Test Warehouse - _TC'}]}).insert()
sales_order.submit()
pick_list = frappe.get_doc({'doctype': 'Pick List', 'company': '_Test Company', 'customer': '_Test Customer', 'items_based_on': 'Sales Order', 'purpose': 'Delivery', 'locations': [{'item_code': item_code, 'qty': 2, 'stock_qty': 1, 'uom': 'Unit', 'conversion_factor': 0.5, 'sales_order': sales_order.name, 'sales_order_item': sales_order.items[0].name}, {'item_code': item_code, 'qty': 1, 'stock_qty': 1, 'conversion_factor': 1, 'sales_order': sales_order.name, 'sales_order_item': sales_order.items[1].name}]})
pick_list.set_item_locations()
pick_list.submit()
delivery_note = create_delivery_note(pick_list.name)
pick_list.load_from_db()
self.assertEqual(pick_list.locations[0].picked_qty, delivery_note.items[0].qty * delivery_note.items[0].conversion_factor)
self.assertEqual(pick_list.locations[1].qty, delivery_note.items[1].qty)
self.assertEqual(sales_order.items[0].conversion_factor, delivery_note.items[0].conversion_factor)
pick_list.cancel()
sales_order.cancel()
purchase_receipt.cancel()
```

## Next Steps


---

*Source: test_pick_list.py:401 | Complexity: Advanced | Last updated: 2026-02-04*