# How To: Return For Serialized Items

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test return for serialized items

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

### Step 1: Assign se = make_serialized_item(...)

```python
se = make_serialized_item(self)
```

### Step 2: Assign serial_no = value

```python
serial_no = [get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)[0]]
```

### Step 3: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(item_code='_Test Serialized Item With Series', rate=500, serial_no=serial_no)
```

### Step 4: Call self.check_serial_no_values()

```python
self.check_serial_no_values(serial_no, {'warehouse': ''})
```

### Step 5: Assign dn1 = create_delivery_note(...)

```python
dn1 = create_delivery_note(item_code='_Test Serialized Item With Series', is_return=1, return_against=dn.name, qty=-1, rate=500, serial_no=serial_no)
```

### Step 6: Call self.check_serial_no_values()

```python
self.check_serial_no_values(serial_no, {'warehouse': '_Test Warehouse - _TC'})
```

### Step 7: Call dn1.cancel()

```python
dn1.cancel()
```

### Step 8: Call self.check_serial_no_values()

```python
self.check_serial_no_values(serial_no, {'warehouse': ''})
```

### Step 9: Call dn.cancel()

```python
dn.cancel()
```

### Step 10: Call self.check_serial_no_values()

```python
self.check_serial_no_values(serial_no, {'warehouse': '_Test Warehouse - _TC'})
```


## Complete Example

```python
# Workflow
se = make_serialized_item(self)
serial_no = [get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)[0]]
dn = create_delivery_note(item_code='_Test Serialized Item With Series', rate=500, serial_no=serial_no)
self.check_serial_no_values(serial_no, {'warehouse': ''})
dn1 = create_delivery_note(item_code='_Test Serialized Item With Series', is_return=1, return_against=dn.name, qty=-1, rate=500, serial_no=serial_no)
self.check_serial_no_values(serial_no, {'warehouse': '_Test Warehouse - _TC'})
dn1.cancel()
self.check_serial_no_values(serial_no, {'warehouse': ''})
dn.cancel()
self.check_serial_no_values(serial_no, {'warehouse': '_Test Warehouse - _TC'})
```

## Next Steps


---

*Source: test_delivery_note.py:750 | Complexity: Advanced | Last updated: 2026-02-04*