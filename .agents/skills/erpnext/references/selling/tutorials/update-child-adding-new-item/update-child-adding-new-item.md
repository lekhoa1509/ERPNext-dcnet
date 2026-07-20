# How To: Update Child Adding New Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test update child adding new item

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
so = make_sales_order(item_code='_Test Item', qty=4)
```

### Step 2: Call create_dn_against_so()

```python
create_dn_against_so(so.name, 4)
```

### Step 3: Call make_sales_invoice()

```python
make_sales_invoice(so.name)
```

### Step 4: Assign prev_total = so.get(...)

```python
prev_total = so.get('base_total')
```

### Step 5: Assign prev_total_in_words = so.get(...)

```python
prev_total_in_words = so.get('base_in_words')
```

### Step 6: Assign reserved_qty_for_second_item = get_reserved_qty(...)

```python
reserved_qty_for_second_item = get_reserved_qty('_Test Item 2')
```

### Step 7: Assign first_item_of_so = value

```python
first_item_of_so = so.get('items')[0]
```

### Step 8: Assign trans_item = json.dumps(...)

```python
trans_item = json.dumps([{'item_code': first_item_of_so.item_code, 'rate': first_item_of_so.rate, 'qty': first_item_of_so.qty, 'docname': first_item_of_so.name}, {'item_code': '_Test Item 2', 'rate': 200, 'qty': 7}])
```

### Step 9: Call update_child_qty_rate()

```python
update_child_qty_rate('Sales Order', trans_item, so.name)
```

### Step 10: Call so.reload()

```python
so.reload()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(so.get('items')[-1].item_code, '_Test Item 2')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(so.get('items')[-1].rate, 200)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(so.get('items')[-1].qty, 7)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(so.get('items')[-1].amount, 1400)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(get_reserved_qty('_Test Item 2'), reserved_qty_for_second_item + 7)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(so.status, 'To Deliver and Bill')
```

### Step 17: Assign updated_total = so.get(...)

```python
updated_total = so.get('base_total')
```

### Step 18: Assign updated_total_in_words = so.get(...)

```python
updated_total_in_words = so.get('base_in_words')
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(updated_total, prev_total + 1400)
```

### Step 20: Call self.assertNotEqual()

```python
self.assertNotEqual(updated_total_in_words, prev_total_in_words)
```


## Complete Example

```python
# Setup
self.create_customer('_Test Customer Credit')

# Workflow
so = make_sales_order(item_code='_Test Item', qty=4)
create_dn_against_so(so.name, 4)
make_sales_invoice(so.name)
prev_total = so.get('base_total')
prev_total_in_words = so.get('base_in_words')
reserved_qty_for_second_item = get_reserved_qty('_Test Item 2')
first_item_of_so = so.get('items')[0]
trans_item = json.dumps([{'item_code': first_item_of_so.item_code, 'rate': first_item_of_so.rate, 'qty': first_item_of_so.qty, 'docname': first_item_of_so.name}, {'item_code': '_Test Item 2', 'rate': 200, 'qty': 7}])
update_child_qty_rate('Sales Order', trans_item, so.name)
so.reload()
self.assertEqual(so.get('items')[-1].item_code, '_Test Item 2')
self.assertEqual(so.get('items')[-1].rate, 200)
self.assertEqual(so.get('items')[-1].qty, 7)
self.assertEqual(so.get('items')[-1].amount, 1400)
self.assertEqual(get_reserved_qty('_Test Item 2'), reserved_qty_for_second_item + 7)
self.assertEqual(so.status, 'To Deliver and Bill')
updated_total = so.get('base_total')
updated_total_in_words = so.get('base_in_words')
self.assertEqual(updated_total, prev_total + 1400)
self.assertNotEqual(updated_total_in_words, prev_total_in_words)
```

## Next Steps


---

*Source: test_sales_order.py:455 | Complexity: Advanced | Last updated: 2026-02-04*