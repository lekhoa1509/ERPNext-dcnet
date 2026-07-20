# How To: Update Child Removing Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test update child removing item

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.data`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.party`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.controllers.accounts_controller`
- `erpnext.manufacturing.doctype.blanket_order.test_blanket_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.material_request.material_request`
- `erpnext.stock.doctype.material_request.test_material_request`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.controllers.tests.test_subcontracting_controller`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.accounts.doctype.purchase_invoice.purchase_invoice`
- `erpnext.stock.utils`
- `erpnext.utilities.transaction_base`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.controllers.tests.test_subcontracting_controller`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.controllers.tests.test_subcontracting_controller`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.payment_request.payment_request`
- `erpnext.accounts.doctype.purchase_invoice.purchase_invoice`


## Step-by-Step Guide

### Step 1: Assign po = create_purchase_order(...)

```python
po = create_purchase_order(do_not_save=1)
```

### Step 2: Assign unknown.qty = 4

```python
po.items[0].qty = 4
```

### Step 3: Call po.save()

```python
po.save()
```

### Step 4: Call po.submit()

```python
po.submit()
```

### Step 5: Call make_pr_against_po()

```python
make_pr_against_po(po.name, 2)
```

### Step 6: Call po.reload()

```python
po.reload()
```

### Step 7: Assign first_item_of_po = value

```python
first_item_of_po = po.get('items')[0]
```

### Step 8: Assign existing_ordered_qty = get_ordered_qty(...)

```python
existing_ordered_qty = get_ordered_qty()
```

### Step 9: Assign trans_item = json.dumps(...)

```python
trans_item = json.dumps([{'item_code': first_item_of_po.item_code, 'rate': first_item_of_po.rate, 'qty': first_item_of_po.qty, 'docname': first_item_of_po.name}, {'item_code': '_Test Item', 'rate': 200, 'qty': 7}])
```

### Step 10: Call update_child_qty_rate()

```python
update_child_qty_rate('Purchase Order', trans_item, po.name)
```

### Step 11: Call po.reload()

```python
po.reload()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(get_ordered_qty(), existing_ordered_qty + 7)
```

### Step 13: Assign trans_item = json.dumps(...)

```python
trans_item = json.dumps([{'item_code': '_Test Item', 'rate': 200, 'qty': 7, 'docname': po.get('items')[1].name}])
```

### Step 14: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, update_child_qty_rate, 'Purchase Order', trans_item, po.name)
```

### Step 15: Assign first_item_of_po = value

```python
first_item_of_po = po.get('items')[0]
```

### Step 16: Assign trans_item = json.dumps(...)

```python
trans_item = json.dumps([{'item_code': first_item_of_po.item_code, 'rate': first_item_of_po.rate, 'qty': first_item_of_po.qty, 'docname': first_item_of_po.name}])
```

### Step 17: Call update_child_qty_rate()

```python
update_child_qty_rate('Purchase Order', trans_item, po.name)
```

### Step 18: Call po.reload()

```python
po.reload()
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(len(po.get('items')), 1)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(po.status, 'To Receive and Bill')
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(get_ordered_qty(), existing_ordered_qty)
```


## Complete Example

```python
# Workflow
po = create_purchase_order(do_not_save=1)
po.items[0].qty = 4
po.save()
po.submit()
make_pr_against_po(po.name, 2)
po.reload()
first_item_of_po = po.get('items')[0]
existing_ordered_qty = get_ordered_qty()
trans_item = json.dumps([{'item_code': first_item_of_po.item_code, 'rate': first_item_of_po.rate, 'qty': first_item_of_po.qty, 'docname': first_item_of_po.name}, {'item_code': '_Test Item', 'rate': 200, 'qty': 7}])
update_child_qty_rate('Purchase Order', trans_item, po.name)
po.reload()
self.assertEqual(get_ordered_qty(), existing_ordered_qty + 7)
trans_item = json.dumps([{'item_code': '_Test Item', 'rate': 200, 'qty': 7, 'docname': po.get('items')[1].name}])
self.assertRaises(frappe.ValidationError, update_child_qty_rate, 'Purchase Order', trans_item, po.name)
first_item_of_po = po.get('items')[0]
trans_item = json.dumps([{'item_code': first_item_of_po.item_code, 'rate': first_item_of_po.rate, 'qty': first_item_of_po.qty, 'docname': first_item_of_po.name}])
update_child_qty_rate('Purchase Order', trans_item, po.name)
po.reload()
self.assertEqual(len(po.get('items')), 1)
self.assertEqual(po.status, 'To Receive and Bill')
self.assertEqual(get_ordered_qty(), existing_ordered_qty)
```

## Next Steps


---

*Source: test_purchase_order.py:235 | Complexity: Advanced | Last updated: 2026-02-04*