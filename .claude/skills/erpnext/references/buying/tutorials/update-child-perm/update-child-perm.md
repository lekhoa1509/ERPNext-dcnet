# How To: Update Child Perm

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test update child perm

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
po = create_purchase_order(item_code='_Test Item', qty=4)
```

### Step 2: Assign user = 'test@example.com'

```python
user = 'test@example.com'
```

### Step 3: Assign test_user = frappe.get_doc(...)

```python
test_user = frappe.get_doc('User', user)
```

### Step 4: Call test_user.add_roles()

```python
test_user.add_roles('Accounts User')
```

### Step 5: Assign trans_item = json.dumps(...)

```python
trans_item = json.dumps([{'item_code': '_Test Item', 'rate': 200, 'qty': 7, 'docname': po.items[0].name}])
```

### Step 6: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, update_child_qty_rate, 'Purchase Order', trans_item, po.name)
```

### Step 7: Assign trans_item = json.dumps(...)

```python
trans_item = json.dumps([{'item_code': '_Test Item', 'rate': 100, 'qty': 2}])
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, update_child_qty_rate, 'Purchase Order', trans_item, po.name)
```


## Complete Example

```python
# Workflow
po = create_purchase_order(item_code='_Test Item', qty=4)
user = 'test@example.com'
test_user = frappe.get_doc('User', user)
test_user.add_roles('Accounts User')
with self.set_user(user):
    trans_item = json.dumps([{'item_code': '_Test Item', 'rate': 200, 'qty': 7, 'docname': po.items[0].name}])
    self.assertRaises(frappe.ValidationError, update_child_qty_rate, 'Purchase Order', trans_item, po.name)
    trans_item = json.dumps([{'item_code': '_Test Item', 'rate': 100, 'qty': 2}])
    self.assertRaises(frappe.ValidationError, update_child_qty_rate, 'Purchase Order', trans_item, po.name)
```

## Next Steps


---

*Source: test_purchase_order.py:292 | Complexity: Advanced | Last updated: 2026-02-04*