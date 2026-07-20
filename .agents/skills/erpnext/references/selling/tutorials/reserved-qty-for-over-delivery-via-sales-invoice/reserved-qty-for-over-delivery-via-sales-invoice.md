# How To: Reserved Qty For Over Delivery Via Sales Invoice

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test reserved qty for over delivery via sales invoice

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

### Step 1: Call make_stock_entry()

```python
make_stock_entry(target='_Test Warehouse - _TC', qty=10, rate=100)
```

### Step 2: Call frappe.db.set_value()

```python
frappe.db.set_value('Item', '_Test Item', 'over_delivery_receipt_allowance', 50)
```

### Step 3: Call frappe.db.set_value()

```python
frappe.db.set_value('Item', '_Test Item', 'over_billing_allowance', 20)
```

### Step 4: Assign existing_reserved_qty = get_reserved_qty(...)

```python
existing_reserved_qty = get_reserved_qty()
```

### Step 5: Assign so = make_sales_order(...)

```python
so = make_sales_order()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(get_reserved_qty(), existing_reserved_qty + 10)
```

### Step 7: Assign si = make_sales_invoice(...)

```python
si = make_sales_invoice(so.name)
```

### Step 8: Assign si.update_stock = 1

```python
si.update_stock = 1
```

### Step 9: Assign unknown.qty = 12

```python
si.get('items')[0].qty = 12
```

### Step 10: Call si.insert()

```python
si.insert()
```

### Step 11: Call si.submit()

```python
si.submit()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(get_reserved_qty(), existing_reserved_qty)
```

### Step 13: Call so.load_from_db()

```python
so.load_from_db()
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(so.get('items')[0].delivered_qty, 12)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(so.per_delivered, 100)
```

### Step 16: Call si.cancel()

```python
si.cancel()
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(get_reserved_qty(), existing_reserved_qty + 10)
```

### Step 18: Call so.load_from_db()

```python
so.load_from_db()
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(so.get('items')[0].delivered_qty, 0)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(so.per_delivered, 0)
```


## Complete Example

```python
# Setup
self.create_customer('_Test Customer Credit')

# Workflow
make_stock_entry(target='_Test Warehouse - _TC', qty=10, rate=100)
frappe.db.set_value('Item', '_Test Item', 'over_delivery_receipt_allowance', 50)
frappe.db.set_value('Item', '_Test Item', 'over_billing_allowance', 20)
existing_reserved_qty = get_reserved_qty()
so = make_sales_order()
self.assertEqual(get_reserved_qty(), existing_reserved_qty + 10)
si = make_sales_invoice(so.name)
si.update_stock = 1
si.get('items')[0].qty = 12
si.insert()
si.submit()
self.assertEqual(get_reserved_qty(), existing_reserved_qty)
so.load_from_db()
self.assertEqual(so.get('items')[0].delivered_qty, 12)
self.assertEqual(so.per_delivered, 100)
si.cancel()
self.assertEqual(get_reserved_qty(), existing_reserved_qty + 10)
so.load_from_db()
self.assertEqual(so.get('items')[0].delivered_qty, 0)
self.assertEqual(so.per_delivered, 0)
```

## Next Steps


---

*Source: test_sales_order.py:353 | Complexity: Advanced | Last updated: 2026-02-04*