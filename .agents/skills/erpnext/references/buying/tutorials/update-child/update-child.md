# How To: Update Child

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test update child

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

### Step 1: Assign mr = make_material_request(...)

```python
mr = make_material_request(qty=10)
```

### Step 2: Assign po = make_purchase_order(...)

```python
po = make_purchase_order(mr.name)
```

### Step 3: Assign po.supplier = '_Test Supplier'

```python
po.supplier = '_Test Supplier'
```

### Step 4: Assign unknown.qty = 4

```python
po.items[0].qty = 4
```

### Step 5: Call po.save()

```python
po.save()
```

### Step 6: Call po.submit()

```python
po.submit()
```

### Step 7: Call create_pr_against_po()

```python
create_pr_against_po(po.name)
```

### Step 8: Call make_pi_from_po()

```python
make_pi_from_po(po.name)
```

### Step 9: Assign existing_ordered_qty = get_ordered_qty(...)

```python
existing_ordered_qty = get_ordered_qty()
```

### Step 10: Assign existing_requested_qty = get_requested_qty(...)

```python
existing_requested_qty = get_requested_qty()
```

### Step 11: Assign trans_item = json.dumps(...)

```python
trans_item = json.dumps([{'item_code': '_Test Item', 'rate': 200, 'qty': 7, 'docname': po.items[0].name}])
```

### Step 12: Call update_child_qty_rate()

```python
update_child_qty_rate('Purchase Order', trans_item, po.name)
```

### Step 13: Call mr.reload()

```python
mr.reload()
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(mr.items[0].ordered_qty, 7)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(mr.per_ordered, 70)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(get_requested_qty(), existing_requested_qty - 3)
```

### Step 17: Call po.reload()

```python
po.reload()
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(po.get('items')[0].rate, 200)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(po.get('items')[0].qty, 7)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(po.get('items')[0].amount, 1400)
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(get_ordered_qty(), existing_ordered_qty + 3)
```


## Complete Example

```python
# Workflow
mr = make_material_request(qty=10)
po = make_purchase_order(mr.name)
po.supplier = '_Test Supplier'
po.items[0].qty = 4
po.save()
po.submit()
create_pr_against_po(po.name)
make_pi_from_po(po.name)
existing_ordered_qty = get_ordered_qty()
existing_requested_qty = get_requested_qty()
trans_item = json.dumps([{'item_code': '_Test Item', 'rate': 200, 'qty': 7, 'docname': po.items[0].name}])
update_child_qty_rate('Purchase Order', trans_item, po.name)
mr.reload()
self.assertEqual(mr.items[0].ordered_qty, 7)
self.assertEqual(mr.per_ordered, 70)
self.assertEqual(get_requested_qty(), existing_requested_qty - 3)
po.reload()
self.assertEqual(po.get('items')[0].rate, 200)
self.assertEqual(po.get('items')[0].qty, 7)
self.assertEqual(po.get('items')[0].amount, 1400)
self.assertEqual(get_ordered_qty(), existing_ordered_qty + 3)
```

## Next Steps


---

*Source: test_purchase_order.py:174 | Complexity: Advanced | Last updated: 2026-02-04*