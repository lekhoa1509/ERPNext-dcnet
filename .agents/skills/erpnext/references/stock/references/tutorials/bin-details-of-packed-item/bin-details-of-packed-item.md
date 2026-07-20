# How To: Bin Details Of Packed Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bin details of packed item

## Prerequisites

**Required Modules:**
- `json`
- `collections`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.accounts.utils`
- `erpnext.controllers.accounts_controller`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_trip.test_delivery_trip`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.stock_ledger`
- `frappe.model.naming`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.serial_no.serial_no`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.stock.stock_balance`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.stock.doctype.serial_no.serial_no`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.item.test_item`


## Step-by-Step Guide

### Step 1: Call make_item()

```python
make_item('_Packed Item New 1', {'is_stock_item': 1})
```

### Step 2: Call make_product_bundle()

```python
make_product_bundle('_Test Product Bundle Item New', ['_Packed Item New 1'], 2)
```

### Step 3: Assign si = create_delivery_note(...)

```python
si = create_delivery_note(item_code='_Test Product Bundle Item New', update_stock=1, warehouse='_Test Warehouse - _TC', transaction_date=add_days(nowdate(), -1), do_not_submit=1)
```

### Step 4: Call make_stock_entry()

```python
make_stock_entry(item='_Packed Item New 1', target='_Test Warehouse - _TC', qty=120, rate=100)
```

### Step 5: Assign bin_details = frappe.db.get_value(...)

```python
bin_details = frappe.db.get_value('Bin', {'item_code': '_Packed Item New 1', 'warehouse': '_Test Warehouse - _TC'}, ['actual_qty', 'projected_qty', 'ordered_qty'], as_dict=1)
```

### Step 6: Assign si.transaction_date = nowdate(...)

```python
si.transaction_date = nowdate()
```

### Step 7: Call si.save()

```python
si.save()
```

### Step 8: Assign packed_item = value

```python
packed_item = si.packed_items[0]
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(flt(bin_details.actual_qty), flt(packed_item.actual_qty))
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(flt(bin_details.projected_qty), flt(packed_item.projected_qty))
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(flt(bin_details.ordered_qty), flt(packed_item.ordered_qty))
```

### Step 12: Assign bundle_item = make_item(...)

```python
bundle_item = make_item('_Test Product Bundle Item New', {'is_stock_item': 0})
```

### Step 13: Call bundle_item.append()

```python
bundle_item.append('item_defaults', {'company': '_Test Company', 'default_warehouse': '_Test Warehouse - _TC'})
```

### Step 14: Call bundle_item.save()

```python
bundle_item.save(ignore_permissions=True)
```


## Complete Example

```python
# Workflow
from erpnext.selling.doctype.product_bundle.test_product_bundle import make_product_bundle
from erpnext.stock.doctype.item.test_item import make_item
if not frappe.db.exists('Item', '_Test Product Bundle Item New'):
    bundle_item = make_item('_Test Product Bundle Item New', {'is_stock_item': 0})
    bundle_item.append('item_defaults', {'company': '_Test Company', 'default_warehouse': '_Test Warehouse - _TC'})
    bundle_item.save(ignore_permissions=True)
make_item('_Packed Item New 1', {'is_stock_item': 1})
make_product_bundle('_Test Product Bundle Item New', ['_Packed Item New 1'], 2)
si = create_delivery_note(item_code='_Test Product Bundle Item New', update_stock=1, warehouse='_Test Warehouse - _TC', transaction_date=add_days(nowdate(), -1), do_not_submit=1)
make_stock_entry(item='_Packed Item New 1', target='_Test Warehouse - _TC', qty=120, rate=100)
bin_details = frappe.db.get_value('Bin', {'item_code': '_Packed Item New 1', 'warehouse': '_Test Warehouse - _TC'}, ['actual_qty', 'projected_qty', 'ordered_qty'], as_dict=1)
si.transaction_date = nowdate()
si.save()
packed_item = si.packed_items[0]
self.assertEqual(flt(bin_details.actual_qty), flt(packed_item.actual_qty))
self.assertEqual(flt(bin_details.projected_qty), flt(packed_item.projected_qty))
self.assertEqual(flt(bin_details.ordered_qty), flt(packed_item.ordered_qty))
```

## Next Steps


---

*Source: test_delivery_note.py:710 | Complexity: Advanced | Last updated: 2026-02-04*