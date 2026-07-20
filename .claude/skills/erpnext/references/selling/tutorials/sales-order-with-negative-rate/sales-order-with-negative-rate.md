# How To: Sales Order With Negative Rate

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test if negative rate is allowed in Sales Order via doc submission and update items

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

### Step 1: '\n\t\tTest if negative rate is allowed in Sales Order via doc submission and update items\n\t\t'

```python
'\n\t\tTest if negative rate is allowed in Sales Order via doc submission and update items\n\t\t'
```

### Step 2: Assign so = make_sales_order(...)

```python
so = make_sales_order(qty=1, rate=100, do_not_save=True)
```

### Step 3: Call so.append()

```python
so.append('items', {'item_code': '_Test Item', 'qty': 1, 'rate': -10})
```

### Step 4: Call so.save()

```python
so.save()
```

### Step 5: Call so.submit()

```python
so.submit()
```

### Step 6: Assign first_item = value

```python
first_item = so.get('items')[0]
```

### Step 7: Assign second_item = value

```python
second_item = so.get('items')[1]
```

### Step 8: Assign trans_item = json.dumps(...)

```python
trans_item = json.dumps([{'item_code': first_item.item_code, 'rate': first_item.rate, 'qty': first_item.qty, 'docname': first_item.name}, {'item_code': second_item.item_code, 'rate': -20, 'qty': second_item.qty, 'docname': second_item.name}])
```

### Step 9: Call update_child_qty_rate()

```python
update_child_qty_rate('Sales Order', trans_item, so.name)
```


## Complete Example

```python
# Setup
self.create_customer('_Test Customer Credit')

# Workflow
'\n\t\tTest if negative rate is allowed in Sales Order via doc submission and update items\n\t\t'
so = make_sales_order(qty=1, rate=100, do_not_save=True)
so.append('items', {'item_code': '_Test Item', 'qty': 1, 'rate': -10})
so.save()
so.submit()
first_item = so.get('items')[0]
second_item = so.get('items')[1]
trans_item = json.dumps([{'item_code': first_item.item_code, 'rate': first_item.rate, 'qty': first_item.qty, 'docname': first_item.name}, {'item_code': second_item.item_code, 'rate': -20, 'qty': second_item.qty, 'docname': second_item.name}])
update_child_qty_rate('Sales Order', trans_item, so.name)
```

## Next Steps


---

*Source: test_sales_order.py:61 | Complexity: Advanced | Last updated: 2026-02-04*