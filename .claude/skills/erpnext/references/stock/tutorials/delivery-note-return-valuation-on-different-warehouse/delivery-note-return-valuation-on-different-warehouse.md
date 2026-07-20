# How To: Delivery Note Return Valuation On Different Warehouse

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test delivery note return valuation on different warehouse

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

### Step 1: Assign company = frappe.db.get_value(...)

```python
company = frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
```

### Step 2: Assign item_code = 'Test Return Valuation For DN'

```python
item_code = 'Test Return Valuation For DN'
```

### Step 3: Call make_item()

```python
make_item('Test Return Valuation For DN', {'is_stock_item': 1})
```

### Step 4: Assign return_warehouse = create_warehouse(...)

```python
return_warehouse = create_warehouse('Returned Test Warehouse', company=company)
```

### Step 5: Call make_stock_entry()

```python
make_stock_entry(item_code=item_code, target='Stores - TCP1', qty=5, basic_rate=150)
```

### Step 6: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(item_code=item_code, qty=5, rate=500, warehouse='Stores - TCP1', company=company, expense_account='Cost of Goods Sold - TCP1', cost_center='Main - TCP1')
```

### Step 7: Call dn.submit()

```python
dn.submit()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(dn.items[0].incoming_rate, 150)
```

### Step 9: Assign return_dn = make_return_doc(...)

```python
return_dn = make_return_doc(dn.doctype, dn.name)
```

### Step 10: Assign unknown.warehouse = return_warehouse

```python
return_dn.items[0].warehouse = return_warehouse
```

### Step 11: Call return_dn.save.submit()

```python
return_dn.save().submit()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(return_dn.items[0].incoming_rate, 150)
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.warehouse.test_warehouse import create_warehouse
company = frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
item_code = 'Test Return Valuation For DN'
make_item('Test Return Valuation For DN', {'is_stock_item': 1})
return_warehouse = create_warehouse('Returned Test Warehouse', company=company)
make_stock_entry(item_code=item_code, target='Stores - TCP1', qty=5, basic_rate=150)
dn = create_delivery_note(item_code=item_code, qty=5, rate=500, warehouse='Stores - TCP1', company=company, expense_account='Cost of Goods Sold - TCP1', cost_center='Main - TCP1')
dn.submit()
self.assertEqual(dn.items[0].incoming_rate, 150)
from erpnext.controllers.sales_and_purchase_return import make_return_doc
return_dn = make_return_doc(dn.doctype, dn.name)
return_dn.items[0].warehouse = return_warehouse
return_dn.save().submit()
self.assertEqual(return_dn.items[0].incoming_rate, 150)
```

## Next Steps


---

*Source: test_delivery_note.py:435 | Complexity: Advanced | Last updated: 2026-02-04*