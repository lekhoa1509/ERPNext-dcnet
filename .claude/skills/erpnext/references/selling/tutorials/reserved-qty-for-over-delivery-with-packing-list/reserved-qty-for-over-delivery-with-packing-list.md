# How To: Reserved Qty For Over Delivery With Packing List

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test reserved qty for over delivery with packing list

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

### Step 2: Call make_stock_entry()

```python
make_stock_entry(item='_Test Item Home Desktop 100', target='_Test Warehouse - _TC', qty=10, rate=100)
```

### Step 3: Call frappe.db.set_value()

```python
frappe.db.set_value('Item', '_Test Product Bundle Item', 'over_delivery_receipt_allowance', 50)
```

### Step 4: Assign existing_reserved_qty_item1 = get_reserved_qty(...)

```python
existing_reserved_qty_item1 = get_reserved_qty('_Test Item')
```

### Step 5: Assign existing_reserved_qty_item2 = get_reserved_qty(...)

```python
existing_reserved_qty_item2 = get_reserved_qty('_Test Item Home Desktop 100')
```

### Step 6: Assign so = make_sales_order(...)

```python
so = make_sales_order(item_code='_Test Product Bundle Item')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(get_reserved_qty('_Test Item'), existing_reserved_qty_item1 + 50)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(get_reserved_qty('_Test Item Home Desktop 100'), existing_reserved_qty_item2 + 20)
```

### Step 9: Assign dn = create_dn_against_so(...)

```python
dn = create_dn_against_so(so.name, 15)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(get_reserved_qty('_Test Item'), existing_reserved_qty_item1)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(get_reserved_qty('_Test Item Home Desktop 100'), existing_reserved_qty_item2)
```

### Step 12: Call dn.cancel()

```python
dn.cancel()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(get_reserved_qty('_Test Item'), existing_reserved_qty_item1 + 50)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(get_reserved_qty('_Test Item Home Desktop 100'), existing_reserved_qty_item2 + 20)
```


## Complete Example

```python
# Setup
self.create_customer('_Test Customer Credit')

# Workflow
make_stock_entry(target='_Test Warehouse - _TC', qty=10, rate=100)
make_stock_entry(item='_Test Item Home Desktop 100', target='_Test Warehouse - _TC', qty=10, rate=100)
frappe.db.set_value('Item', '_Test Product Bundle Item', 'over_delivery_receipt_allowance', 50)
existing_reserved_qty_item1 = get_reserved_qty('_Test Item')
existing_reserved_qty_item2 = get_reserved_qty('_Test Item Home Desktop 100')
so = make_sales_order(item_code='_Test Product Bundle Item')
self.assertEqual(get_reserved_qty('_Test Item'), existing_reserved_qty_item1 + 50)
self.assertEqual(get_reserved_qty('_Test Item Home Desktop 100'), existing_reserved_qty_item2 + 20)
dn = create_dn_against_so(so.name, 15)
self.assertEqual(get_reserved_qty('_Test Item'), existing_reserved_qty_item1)
self.assertEqual(get_reserved_qty('_Test Item Home Desktop 100'), existing_reserved_qty_item2)
dn.cancel()
self.assertEqual(get_reserved_qty('_Test Item'), existing_reserved_qty_item1 + 50)
self.assertEqual(get_reserved_qty('_Test Item Home Desktop 100'), existing_reserved_qty_item2 + 20)
```

## Next Steps


---

*Source: test_sales_order.py:431 | Complexity: Advanced | Last updated: 2026-02-04*