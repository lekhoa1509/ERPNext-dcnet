# How To: Ordered Qty Against Pi With Update Stock

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test ordered qty against pi with update stock

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

### Step 1: Assign existing_ordered_qty = get_ordered_qty(...)

```python
existing_ordered_qty = get_ordered_qty()
```

### Step 2: Assign po = create_purchase_order(...)

```python
po = create_purchase_order()
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(get_ordered_qty(), existing_ordered_qty + 10)
```

### Step 4: Call frappe.db.set_value()

```python
frappe.db.set_value('Item', '_Test Item', 'over_delivery_receipt_allowance', 50)
```

### Step 5: Call frappe.db.set_value()

```python
frappe.db.set_value('Item', '_Test Item', 'over_billing_allowance', 20)
```

### Step 6: Assign pi = make_pi_from_po(...)

```python
pi = make_pi_from_po(po.name)
```

### Step 7: Assign pi.update_stock = 1

```python
pi.update_stock = 1
```

### Step 8: Assign unknown.qty = 12

```python
pi.items[0].qty = 12
```

### Step 9: Call pi.insert()

```python
pi.insert()
```

### Step 10: Call pi.submit()

```python
pi.submit()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(get_ordered_qty(), existing_ordered_qty)
```

### Step 12: Call po.load_from_db()

```python
po.load_from_db()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(po.get('items')[0].received_qty, 12)
```

### Step 14: Call pi.cancel()

```python
pi.cancel()
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(get_ordered_qty(), existing_ordered_qty + 10)
```

### Step 16: Call po.load_from_db()

```python
po.load_from_db()
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(po.get('items')[0].received_qty, 0)
```

### Step 18: Call frappe.db.set_value()

```python
frappe.db.set_value('Item', '_Test Item', 'over_delivery_receipt_allowance', 0)
```

### Step 19: Call frappe.db.set_value()

```python
frappe.db.set_value('Item', '_Test Item', 'over_billing_allowance', 0)
```

### Step 20: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Accounts Settings', 'over_billing_allowance', 0)
```


## Complete Example

```python
# Workflow
existing_ordered_qty = get_ordered_qty()
po = create_purchase_order()
self.assertEqual(get_ordered_qty(), existing_ordered_qty + 10)
frappe.db.set_value('Item', '_Test Item', 'over_delivery_receipt_allowance', 50)
frappe.db.set_value('Item', '_Test Item', 'over_billing_allowance', 20)
pi = make_pi_from_po(po.name)
pi.update_stock = 1
pi.items[0].qty = 12
pi.insert()
pi.submit()
self.assertEqual(get_ordered_qty(), existing_ordered_qty)
po.load_from_db()
self.assertEqual(po.get('items')[0].received_qty, 12)
pi.cancel()
self.assertEqual(get_ordered_qty(), existing_ordered_qty + 10)
po.load_from_db()
self.assertEqual(po.get('items')[0].received_qty, 0)
frappe.db.set_value('Item', '_Test Item', 'over_delivery_receipt_allowance', 0)
frappe.db.set_value('Item', '_Test Item', 'over_billing_allowance', 0)
frappe.db.set_single_value('Accounts Settings', 'over_billing_allowance', 0)
```

## Next Steps


---

*Source: test_purchase_order.py:99 | Complexity: Advanced | Last updated: 2026-02-04*