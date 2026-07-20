# How To: Delivery Of Bundled Items To Target Warehouse

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test delivery of bundled items to target warehouse

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

### Step 2: Assign customer_name = create_internal_customer(...)

```python
customer_name = create_internal_customer(customer_name='_Test Internal Customer 2', represents_company='_Test Company with perpetual inventory', allowed_to_interact_with='_Test Company with perpetual inventory')
```

### Step 3: Call set_valuation_method()

```python
set_valuation_method('_Test Item', 'FIFO')
```

### Step 4: Call set_valuation_method()

```python
set_valuation_method('_Test Item Home Desktop 100', 'FIFO')
```

### Step 5: Assign target_warehouse = value

```python
target_warehouse = get_warehouse(company=company, abbr='TCP1', warehouse_name='_Test Customer Warehouse').name
```

### Step 6: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(item_code='_Test Product Bundle Item', company='_Test Company with perpetual inventory', customer=customer_name, cost_center='Main - TCP1', expense_account='Cost of Goods Sold - TCP1', qty=5, rate=500, warehouse='Stores - TCP1', target_warehouse=target_warehouse)
```

### Step 7: Assign actual_qty_at_source = get_qty_after_transaction(...)

```python
actual_qty_at_source = get_qty_after_transaction(warehouse='Stores - TCP1')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(actual_qty_at_source, 475)
```

### Step 9: Assign actual_qty_at_target = get_qty_after_transaction(...)

```python
actual_qty_at_target = get_qty_after_transaction(warehouse=target_warehouse)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(actual_qty_at_target, 525)
```

### Step 11: Assign stock_value_difference = frappe.db.get_value(...)

```python
stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name, 'item_code': '_Test Item', 'warehouse': 'Stores - TCP1'}, 'stock_value_difference')
```

### Step 12: Assign stock_value_difference1 = frappe.db.get_value(...)

```python
stock_value_difference1 = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name, 'item_code': '_Test Item', 'warehouse': target_warehouse}, 'stock_value_difference')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(abs(stock_value_difference), stock_value_difference1)
```

### Step 14: Assign gl_entries = get_gl_entries(...)

```python
gl_entries = get_gl_entries('Delivery Note', dn.name)
```

### Step 15: Call self.assertTrue()

```python
self.assertTrue(gl_entries)
```

### Step 16: Assign stock_value_difference = abs(...)

```python
stock_value_difference = abs(frappe.db.sql("select sum(stock_value_difference)\n\t\t\tfrom `tabStock Ledger Entry` where voucher_type='Delivery Note' and voucher_no=%s\n\t\t\tand warehouse='Stores - TCP1'", dn.name)[0][0])
```

### Step 17: Assign expected_values = value

```python
expected_values = {'Stock In Hand - TCP1': [0.0, stock_value_difference], target_warehouse: [stock_value_difference, 0.0]}
```

### Step 18: Call frappe.db.rollback()

```python
frappe.db.rollback()
```

### Step 19: Call create_stock_reconciliation()

```python
create_stock_reconciliation(item_code='_Test Item', warehouse=warehouse, company=company, expense_account='Stock Adjustment - TCP1', qty=500, rate=100)
```

### Step 20: Call create_stock_reconciliation()

```python
create_stock_reconciliation(item_code='_Test Item Home Desktop 100', company=company, expense_account='Stock Adjustment - TCP1', warehouse=warehouse, qty=500, rate=100)
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual([gle.debit, gle.credit], expected_values.get(gle.account))
```


## Complete Example

```python
# Workflow
from erpnext.selling.doctype.customer.test_customer import create_internal_customer
company = frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
customer_name = create_internal_customer(customer_name='_Test Internal Customer 2', represents_company='_Test Company with perpetual inventory', allowed_to_interact_with='_Test Company with perpetual inventory')
set_valuation_method('_Test Item', 'FIFO')
set_valuation_method('_Test Item Home Desktop 100', 'FIFO')
target_warehouse = get_warehouse(company=company, abbr='TCP1', warehouse_name='_Test Customer Warehouse').name
for warehouse in ('Stores - TCP1', target_warehouse):
    create_stock_reconciliation(item_code='_Test Item', warehouse=warehouse, company=company, expense_account='Stock Adjustment - TCP1', qty=500, rate=100)
    create_stock_reconciliation(item_code='_Test Item Home Desktop 100', company=company, expense_account='Stock Adjustment - TCP1', warehouse=warehouse, qty=500, rate=100)
dn = create_delivery_note(item_code='_Test Product Bundle Item', company='_Test Company with perpetual inventory', customer=customer_name, cost_center='Main - TCP1', expense_account='Cost of Goods Sold - TCP1', qty=5, rate=500, warehouse='Stores - TCP1', target_warehouse=target_warehouse)
actual_qty_at_source = get_qty_after_transaction(warehouse='Stores - TCP1')
self.assertEqual(actual_qty_at_source, 475)
actual_qty_at_target = get_qty_after_transaction(warehouse=target_warehouse)
self.assertEqual(actual_qty_at_target, 525)
stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name, 'item_code': '_Test Item', 'warehouse': 'Stores - TCP1'}, 'stock_value_difference')
stock_value_difference1 = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name, 'item_code': '_Test Item', 'warehouse': target_warehouse}, 'stock_value_difference')
self.assertEqual(abs(stock_value_difference), stock_value_difference1)
gl_entries = get_gl_entries('Delivery Note', dn.name)
self.assertTrue(gl_entries)
stock_value_difference = abs(frappe.db.sql("select sum(stock_value_difference)\n\t\t\tfrom `tabStock Ledger Entry` where voucher_type='Delivery Note' and voucher_no=%s\n\t\t\tand warehouse='Stores - TCP1'", dn.name)[0][0])
expected_values = {'Stock In Hand - TCP1': [0.0, stock_value_difference], target_warehouse: [stock_value_difference, 0.0]}
for _i, gle in enumerate(gl_entries):
    self.assertEqual([gle.debit, gle.credit], expected_values.get(gle.account))
frappe.db.rollback()
```

## Next Steps


---

*Source: test_delivery_note.py:826 | Complexity: Advanced | Last updated: 2026-02-04*