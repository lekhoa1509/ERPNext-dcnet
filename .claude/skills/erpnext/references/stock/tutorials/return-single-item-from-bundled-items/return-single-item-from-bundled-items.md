# How To: Return Single Item From Bundled Items

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test return single item from bundled items

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

### Step 2: Call create_stock_reconciliation()

```python
create_stock_reconciliation(item_code='_Test Item', warehouse='Stores - TCP1', qty=50, rate=100, company=company, expense_account='Stock Adjustment - TCP1')
```

### Step 3: Call create_stock_reconciliation()

```python
create_stock_reconciliation(item_code='_Test Item Home Desktop 100', warehouse='Stores - TCP1', qty=50, rate=100, company=company, expense_account='Stock Adjustment - TCP1')
```

### Step 4: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(item_code='_Test Product Bundle Item', qty=5, rate=500, company=company, warehouse='Stores - TCP1', expense_account='Cost of Goods Sold - TCP1', cost_center='Main - TCP1')
```

### Step 5: Assign actual_qty_1 = get_qty_after_transaction(...)

```python
actual_qty_1 = get_qty_after_transaction(warehouse='Stores - TCP1')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(actual_qty_1, 25)
```

### Step 7: Assign outgoing_rate = value

```python
outgoing_rate = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name, 'item_code': '_Test Item'}, 'stock_value_difference') / 25
```

### Step 8: Assign dn1 = create_delivery_note(...)

```python
dn1 = create_delivery_note(is_return=1, return_against=dn.name, qty=-10, rate=500, company=company, warehouse='Stores - TCP1', expense_account='Cost of Goods Sold - TCP1', cost_center='Main - TCP1')
```

### Step 9: Assign actual_qty_2 = get_qty_after_transaction(...)

```python
actual_qty_2 = get_qty_after_transaction(warehouse='Stores - TCP1')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(actual_qty_2, 35)
```

### Step 11: Assign unknown = frappe.db.get_value(...)

```python
incoming_rate, stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn1.name}, ['incoming_rate', 'stock_value_difference'])
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(flt(incoming_rate, 3), abs(flt(outgoing_rate, 3)))
```

### Step 13: Assign stock_in_hand_account = get_inventory_account(...)

```python
stock_in_hand_account = get_inventory_account(company, dn1.items[0].warehouse)
```

### Step 14: Assign gle_warehouse_amount = frappe.db.get_value(...)

```python
gle_warehouse_amount = frappe.db.get_value('GL Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn1.name, 'account': stock_in_hand_account}, 'debit')
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(gle_warehouse_amount, stock_value_difference)
```


## Complete Example

```python
# Workflow
company = frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
create_stock_reconciliation(item_code='_Test Item', warehouse='Stores - TCP1', qty=50, rate=100, company=company, expense_account='Stock Adjustment - TCP1')
create_stock_reconciliation(item_code='_Test Item Home Desktop 100', warehouse='Stores - TCP1', qty=50, rate=100, company=company, expense_account='Stock Adjustment - TCP1')
dn = create_delivery_note(item_code='_Test Product Bundle Item', qty=5, rate=500, company=company, warehouse='Stores - TCP1', expense_account='Cost of Goods Sold - TCP1', cost_center='Main - TCP1')
actual_qty_1 = get_qty_after_transaction(warehouse='Stores - TCP1')
self.assertEqual(actual_qty_1, 25)
outgoing_rate = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name, 'item_code': '_Test Item'}, 'stock_value_difference') / 25
dn1 = create_delivery_note(is_return=1, return_against=dn.name, qty=-10, rate=500, company=company, warehouse='Stores - TCP1', expense_account='Cost of Goods Sold - TCP1', cost_center='Main - TCP1')
actual_qty_2 = get_qty_after_transaction(warehouse='Stores - TCP1')
self.assertEqual(actual_qty_2, 35)
incoming_rate, stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn1.name}, ['incoming_rate', 'stock_value_difference'])
self.assertEqual(flt(incoming_rate, 3), abs(flt(outgoing_rate, 3)))
stock_in_hand_account = get_inventory_account(company, dn1.items[0].warehouse)
gle_warehouse_amount = frappe.db.get_value('GL Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn1.name, 'account': stock_in_hand_account}, 'debit')
self.assertEqual(gle_warehouse_amount, stock_value_difference)
```

## Next Steps


---

*Source: test_delivery_note.py:558 | Complexity: Advanced | Last updated: 2026-02-04*