# How To: Delivery Note Internal Transfer Serial No Status

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test delivery note internal transfer serial no status

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

### Step 1: Assign item = value

```python
item = make_item('_Test Item for Internal Transfer With Serial No Status', properties={'has_serial_no': 1, 'is_stock_item': 1, 'serial_no_series': 'INT-SN-.####'}).name
```

### Step 2: Assign warehouse = '_Test Warehouse - _TC'

```python
warehouse = '_Test Warehouse - _TC'
```

### Step 3: Assign target = 'Stores - _TC'

```python
target = 'Stores - _TC'
```

### Step 4: Assign company = '_Test Company'

```python
company = '_Test Company'
```

### Step 5: Assign customer = create_internal_customer(...)

```python
customer = create_internal_customer(represents_company=company)
```

### Step 6: Assign rate = 42

```python
rate = 42
```

### Step 7: Assign se = make_stock_entry(...)

```python
se = make_stock_entry(target=warehouse, qty=5, basic_rate=rate, item_code=item)
```

### Step 8: Assign serial_nos = get_serial_nos_from_bundle(...)

```python
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
```

### Step 9: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(item_code=item, company=company, customer=customer, qty=5, rate=500, warehouse=warehouse, target_warehouse=target, ignore_pricing_rule=0, use_serial_batch_fields=1, serial_no='\n'.join(serial_nos))
```

### Step 10: Call dn.cancel()

```python
dn.cancel()
```

### Step 11: Assign sn = frappe.db.get_value(...)

```python
sn = frappe.db.get_value('Serial No', serial_no, ['status', 'warehouse'], as_dict=1)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(sn.status, 'Active')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(sn.warehouse, target)
```

### Step 14: Assign sn = frappe.db.get_value(...)

```python
sn = frappe.db.get_value('Serial No', serial_no, ['status', 'warehouse'], as_dict=1)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(sn.status, 'Active')
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(sn.warehouse, warehouse)
```


## Complete Example

```python
# Workflow
from erpnext.selling.doctype.customer.test_customer import create_internal_customer
item = make_item('_Test Item for Internal Transfer With Serial No Status', properties={'has_serial_no': 1, 'is_stock_item': 1, 'serial_no_series': 'INT-SN-.####'}).name
warehouse = '_Test Warehouse - _TC'
target = 'Stores - _TC'
company = '_Test Company'
customer = create_internal_customer(represents_company=company)
rate = 42
se = make_stock_entry(target=warehouse, qty=5, basic_rate=rate, item_code=item)
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
dn = create_delivery_note(item_code=item, company=company, customer=customer, qty=5, rate=500, warehouse=warehouse, target_warehouse=target, ignore_pricing_rule=0, use_serial_batch_fields=1, serial_no='\n'.join(serial_nos))
for serial_no in serial_nos:
    sn = frappe.db.get_value('Serial No', serial_no, ['status', 'warehouse'], as_dict=1)
    self.assertEqual(sn.status, 'Active')
    self.assertEqual(sn.warehouse, target)
dn.cancel()
for serial_no in serial_nos:
    sn = frappe.db.get_value('Serial No', serial_no, ['status', 'warehouse'], as_dict=1)
    self.assertEqual(sn.status, 'Active')
    self.assertEqual(sn.warehouse, warehouse)
```

## Next Steps


---

*Source: test_delivery_note.py:784 | Complexity: Advanced | Last updated: 2026-02-04*