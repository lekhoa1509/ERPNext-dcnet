# How To: Return Against Sales Order

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test return against sales order

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `json`
- `unittest.mock`
- `frappe`
- `frappe.permissions`
- `frappe.core.doctype.user_permission.test_user_permission`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.test.accounts_mixin`
- `erpnext.controllers.accounts_controller`
- `erpnext.maintenance.doctype.maintenance_schedule.test_maintenance_schedule`
- `erpnext.maintenance.doctype.maintenance_visit.test_maintenance_visit`
- `erpnext.manufacturing.doctype.blanket_order.test_blanket_order`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.get_item_details`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `frappe.custom.doctype.property_setter.property_setter`
- `frappe.model.meta`
- `frappe.model.workflow`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.controllers.item_variant`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.doctype.work_order.test_work_order`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.stock.doctype.material_request.material_request`
- `erpnext.accounts.doctype.shipping_rule.test_shipping_rule`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.payment_request.payment_request`
- `erpnext.stock.doctype.pick_list.pick_list`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.selling.doctype.sales_order.sales_order`

**Setup Required:**
```python
self.create_customer('_Test Customer Credit')
```

## Step-by-Step Guide

### Step 1: Assign so = make_sales_order(...)

```python
so = make_sales_order()
```

### Step 2: Assign dn = create_dn_against_so(...)

```python
dn = create_dn_against_so(so.name, 6)
```

### Step 3: Call so.load_from_db()

```python
so.load_from_db()
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(so.get('items')[0].delivered_qty, 6)
```

### Step 5: Assign si2 = make_sales_invoice(...)

```python
si2 = make_sales_invoice(so.name)
```

### Step 6: Call si2.set()

```python
si2.set('update_stock', 1)
```

### Step 7: Assign unknown.qty = 3

```python
si2.get('items')[0].qty = 3
```

### Step 8: Call si2.insert()

```python
si2.insert()
```

### Step 9: Call si2.submit()

```python
si2.submit()
```

### Step 10: Call so.load_from_db()

```python
so.load_from_db()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(so.get('items')[0].delivered_qty, 9)
```

### Step 12: Assign dn1 = create_delivery_note(...)

```python
dn1 = create_delivery_note(is_return=1, return_against=dn.name, qty=-3, do_not_submit=True)
```

### Step 13: Assign unknown.against_sales_order = value

```python
dn1.items[0].against_sales_order = so.name
```

### Step 14: Assign unknown.so_detail = value

```python
dn1.items[0].so_detail = so.items[0].name
```

### Step 15: Call dn1.submit()

```python
dn1.submit()
```

### Step 16: Assign si1 = create_sales_invoice(...)

```python
si1 = create_sales_invoice(is_return=1, return_against=si2.name, qty=-1, update_stock=1, do_not_submit=True)
```

### Step 17: Assign unknown.sales_order = value

```python
si1.items[0].sales_order = so.name
```

### Step 18: Assign unknown.so_detail = value

```python
si1.items[0].so_detail = so.items[0].name
```

### Step 19: Call si1.submit()

```python
si1.submit()
```

### Step 20: Call so.load_from_db()

```python
so.load_from_db()
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(so.get('items')[0].delivered_qty, 5)
```


## Complete Example

```python
# Setup
self.create_customer('_Test Customer Credit')

# Workflow
so = make_sales_order()
dn = create_dn_against_so(so.name, 6)
so.load_from_db()
self.assertEqual(so.get('items')[0].delivered_qty, 6)
si2 = make_sales_invoice(so.name)
si2.set('update_stock', 1)
si2.get('items')[0].qty = 3
si2.insert()
si2.submit()
so.load_from_db()
self.assertEqual(so.get('items')[0].delivered_qty, 9)
from erpnext.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
from erpnext.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
dn1 = create_delivery_note(is_return=1, return_against=dn.name, qty=-3, do_not_submit=True)
dn1.items[0].against_sales_order = so.name
dn1.items[0].so_detail = so.items[0].name
dn1.submit()
si1 = create_sales_invoice(is_return=1, return_against=si2.name, qty=-1, update_stock=1, do_not_submit=True)
si1.items[0].sales_order = so.name
si1.items[0].so_detail = so.items[0].name
si1.submit()
so.load_from_db()
self.assertEqual(so.get('items')[0].delivered_qty, 5)
```

## Next Steps


---

*Source: test_sales_order.py:271 | Complexity: Advanced | Last updated: 2026-02-04*