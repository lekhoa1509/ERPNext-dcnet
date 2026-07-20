# How To: Return Against Purchase Order

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test return against purchase order

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
po = create_purchase_order()
```

### Step 2: Assign pr = make_pr_against_po(...)

```python
pr = make_pr_against_po(po.name, 6)
```

### Step 3: Call po.load_from_db()

```python
po.load_from_db()
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(po.get('items')[0].received_qty, 6)
```

### Step 5: Assign pi2 = make_pi_from_po(...)

```python
pi2 = make_pi_from_po(po.name)
```

### Step 6: Call pi2.set()

```python
pi2.set('update_stock', 1)
```

### Step 7: Assign unknown.qty = 3

```python
pi2.get('items')[0].qty = 3
```

### Step 8: Call pi2.insert()

```python
pi2.insert()
```

### Step 9: Call pi2.submit()

```python
pi2.submit()
```

### Step 10: Call po.load_from_db()

```python
po.load_from_db()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(po.get('items')[0].received_qty, 9)
```

### Step 12: Assign pr1 = make_purchase_receipt_return(...)

```python
pr1 = make_purchase_receipt_return(is_return=1, return_against=pr.name, qty=-3, do_not_submit=True)
```

### Step 13: Assign unknown.purchase_order = value

```python
pr1.items[0].purchase_order = po.name
```

### Step 14: Assign unknown.purchase_order_item = value

```python
pr1.items[0].purchase_order_item = po.items[0].name
```

### Step 15: Call pr1.submit()

```python
pr1.submit()
```

### Step 16: Assign pi1 = make_purchase_invoice_return(...)

```python
pi1 = make_purchase_invoice_return(is_return=1, return_against=pi2.name, qty=-1, update_stock=1, do_not_submit=True)
```

### Step 17: Assign unknown.purchase_order = value

```python
pi1.items[0].purchase_order = po.name
```

### Step 18: Assign unknown.po_detail = value

```python
pi1.items[0].po_detail = po.items[0].name
```

### Step 19: Call pi1.submit()

```python
pi1.submit()
```

### Step 20: Call po.load_from_db()

```python
po.load_from_db()
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(po.get('items')[0].received_qty, 5)
```


## Complete Example

```python
# Workflow
po = create_purchase_order()
pr = make_pr_against_po(po.name, 6)
po.load_from_db()
self.assertEqual(po.get('items')[0].received_qty, 6)
pi2 = make_pi_from_po(po.name)
pi2.set('update_stock', 1)
pi2.get('items')[0].qty = 3
pi2.insert()
pi2.submit()
po.load_from_db()
self.assertEqual(po.get('items')[0].received_qty, 9)
from erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice import make_purchase_invoice as make_purchase_invoice_return
from erpnext.stock.doctype.purchase_receipt.test_purchase_receipt import make_purchase_receipt as make_purchase_receipt_return
pr1 = make_purchase_receipt_return(is_return=1, return_against=pr.name, qty=-3, do_not_submit=True)
pr1.items[0].purchase_order = po.name
pr1.items[0].purchase_order_item = po.items[0].name
pr1.submit()
pi1 = make_purchase_invoice_return(is_return=1, return_against=pi2.name, qty=-1, update_stock=1, do_not_submit=True)
pi1.items[0].purchase_order = po.name
pi1.items[0].po_detail = po.items[0].name
pi1.submit()
po.load_from_db()
self.assertEqual(po.get('items')[0].received_qty, 5)
```

## Next Steps


---

*Source: test_purchase_order.py:455 | Complexity: Advanced | Last updated: 2026-02-04*