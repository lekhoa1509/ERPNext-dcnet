# How To: Purchase Order Invoice Receipt Workflow

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test purchase order invoice receipt workflow

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

### Step 2: Assign pi = make_pi_from_po(...)

```python
pi = make_pi_from_po(po.name)
```

### Step 3: Call pi.submit()

```python
pi.submit()
```

### Step 4: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(pi.name)
```

### Step 5: Call pr.submit()

```python
pr.submit()
```

### Step 6: Call pi.load_from_db()

```python
pi.load_from_db()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(pi.per_received, 100.0)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(pi.items[0].qty, pi.items[0].received_qty)
```

### Step 9: Call po.load_from_db()

```python
po.load_from_db()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(po.per_received, 100.0)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(po.per_billed, 100.0)
```

### Step 12: Call pr.cancel()

```python
pr.cancel()
```

### Step 13: Call pi.load_from_db()

```python
pi.load_from_db()
```

### Step 14: Call pi.cancel()

```python
pi.cancel()
```

### Step 15: Call po.load_from_db()

```python
po.load_from_db()
```

### Step 16: Call po.cancel()

```python
po.cancel()
```


## Complete Example

```python
# Workflow
from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import make_purchase_receipt
po = create_purchase_order()
pi = make_pi_from_po(po.name)
pi.submit()
pr = make_purchase_receipt(pi.name)
pr.submit()
pi.load_from_db()
self.assertEqual(pi.per_received, 100.0)
self.assertEqual(pi.items[0].qty, pi.items[0].received_qty)
po.load_from_db()
self.assertEqual(po.per_received, 100.0)
self.assertEqual(po.per_billed, 100.0)
pr.cancel()
pi.load_from_db()
pi.cancel()
po.load_from_db()
po.cancel()
```

## Next Steps


---

*Source: test_purchase_order.py:495 | Complexity: Advanced | Last updated: 2026-02-04*