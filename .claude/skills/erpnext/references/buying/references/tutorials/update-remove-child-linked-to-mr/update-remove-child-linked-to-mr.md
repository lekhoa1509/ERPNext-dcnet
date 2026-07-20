# How To: Update Remove Child Linked To Mr

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test impact on linked PO and MR on deleting/updating row.

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

### Step 1: 'Test impact on linked PO and MR on deleting/updating row.'

```python
'Test impact on linked PO and MR on deleting/updating row.'
```

### Step 2: Assign mr = make_material_request(...)

```python
mr = make_material_request(qty=10)
```

### Step 3: Assign po = make_purchase_order(...)

```python
po = make_purchase_order(mr.name)
```

### Step 4: Assign po.supplier = '_Test Supplier'

```python
po.supplier = '_Test Supplier'
```

### Step 5: Call po.save()

```python
po.save()
```

### Step 6: Call po.submit()

```python
po.submit()
```

### Step 7: Assign first_item_of_po = value

```python
first_item_of_po = po.get('items')[0]
```

### Step 8: Assign existing_ordered_qty = get_ordered_qty(...)

```python
existing_ordered_qty = get_ordered_qty()
```

### Step 9: Assign existing_requested_qty = get_requested_qty(...)

```python
existing_requested_qty = get_requested_qty()
```

### Step 10: Assign trans_item = json.dumps(...)

```python
trans_item = json.dumps([{'item_code': first_item_of_po.item_code, 'rate': first_item_of_po.rate, 'qty': 7, 'docname': first_item_of_po.name}, {'item_code': '_Test Item 2', 'rate': 200, 'qty': 2}])
```

### Step 11: Call update_child_qty_rate()

```python
update_child_qty_rate('Purchase Order', trans_item, po.name)
```

### Step 12: Call mr.reload()

```python
mr.reload()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(get_requested_qty(), existing_requested_qty + 3)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(mr.items[0].ordered_qty, 7)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(get_ordered_qty(), existing_ordered_qty - 3)
```

### Step 16: Assign trans_item = json.dumps(...)

```python
trans_item = json.dumps([{'item_code': '_Test Item 2', 'rate': 200, 'qty': 2}])
```

### Step 17: Call update_child_qty_rate()

```python
update_child_qty_rate('Purchase Order', trans_item, po.name)
```

### Step 18: Call mr.reload()

```python
mr.reload()
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(get_requested_qty(), existing_requested_qty + 10)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(mr.items[0].ordered_qty, 0)
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(get_ordered_qty(), existing_ordered_qty - 10)
```


## Complete Example

```python
# Workflow
'Test impact on linked PO and MR on deleting/updating row.'
mr = make_material_request(qty=10)
po = make_purchase_order(mr.name)
po.supplier = '_Test Supplier'
po.save()
po.submit()
first_item_of_po = po.get('items')[0]
existing_ordered_qty = get_ordered_qty()
existing_requested_qty = get_requested_qty()
trans_item = json.dumps([{'item_code': first_item_of_po.item_code, 'rate': first_item_of_po.rate, 'qty': 7, 'docname': first_item_of_po.name}, {'item_code': '_Test Item 2', 'rate': 200, 'qty': 2}])
update_child_qty_rate('Purchase Order', trans_item, po.name)
mr.reload()
self.assertEqual(get_requested_qty(), existing_requested_qty + 3)
self.assertEqual(mr.items[0].ordered_qty, 7)
self.assertEqual(get_ordered_qty(), existing_ordered_qty - 3)
trans_item = json.dumps([{'item_code': '_Test Item 2', 'rate': 200, 'qty': 2}])
update_child_qty_rate('Purchase Order', trans_item, po.name)
mr.reload()
self.assertEqual(get_requested_qty(), existing_requested_qty + 10)
self.assertEqual(mr.items[0].ordered_qty, 0)
self.assertEqual(get_ordered_qty(), existing_ordered_qty - 10)
```

## Next Steps


---

*Source: test_purchase_order.py:129 | Complexity: Advanced | Last updated: 2026-02-04*