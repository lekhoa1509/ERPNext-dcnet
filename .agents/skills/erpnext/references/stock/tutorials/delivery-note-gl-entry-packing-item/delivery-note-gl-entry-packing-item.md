# How To: Delivery Note Gl Entry Packing Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test delivery note gl entry packing item

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

### Step 1: Call frappe.db.get_value()

```python
frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
```

### Step 2: Call make_stock_entry()

```python
make_stock_entry(item_code='_Test Item', target='Stores - TCP1', qty=10, basic_rate=100)
```

### Step 3: Call make_stock_entry()

```python
make_stock_entry(item_code='_Test Item Home Desktop 100', target='Stores - TCP1', qty=10, basic_rate=100)
```

### Step 4: Assign stock_in_hand_account = get_inventory_account(...)

```python
stock_in_hand_account = get_inventory_account('_Test Company with perpetual inventory')
```

### Step 5: Assign prev_bal = get_balance_on(...)

```python
prev_bal = get_balance_on(stock_in_hand_account)
```

### Step 6: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(item_code='_Test Product Bundle Item', company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', cost_center='Main - TCP1', expense_account='Cost of Goods Sold - TCP1')
```

### Step 7: Assign stock_value_diff_rm1 = abs(...)

```python
stock_value_diff_rm1 = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name, 'item_code': '_Test Item'}, 'stock_value_difference'))
```

### Step 8: Assign stock_value_diff_rm2 = abs(...)

```python
stock_value_diff_rm2 = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name, 'item_code': '_Test Item Home Desktop 100'}, 'stock_value_difference'))
```

### Step 9: Assign stock_value_diff = value

```python
stock_value_diff = stock_value_diff_rm1 + stock_value_diff_rm2
```

### Step 10: Assign gl_entries = get_gl_entries(...)

```python
gl_entries = get_gl_entries('Delivery Note', dn.name)
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(gl_entries)
```

### Step 12: Assign expected_values = value

```python
expected_values = {stock_in_hand_account: [0.0, stock_value_diff], 'Cost of Goods Sold - TCP1': [stock_value_diff, 0.0]}
```

### Step 13: Assign bal = get_balance_on(...)

```python
bal = get_balance_on(stock_in_hand_account)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(flt(bal, 2), flt(prev_bal - stock_value_diff, 2))
```

### Step 15: Call dn.cancel()

```python
dn.cancel()
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual([gle.debit, gle.credit], expected_values.get(gle.account))
```


## Complete Example

```python
# Workflow
frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
make_stock_entry(item_code='_Test Item', target='Stores - TCP1', qty=10, basic_rate=100)
make_stock_entry(item_code='_Test Item Home Desktop 100', target='Stores - TCP1', qty=10, basic_rate=100)
stock_in_hand_account = get_inventory_account('_Test Company with perpetual inventory')
prev_bal = get_balance_on(stock_in_hand_account)
dn = create_delivery_note(item_code='_Test Product Bundle Item', company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', cost_center='Main - TCP1', expense_account='Cost of Goods Sold - TCP1')
stock_value_diff_rm1 = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name, 'item_code': '_Test Item'}, 'stock_value_difference'))
stock_value_diff_rm2 = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name, 'item_code': '_Test Item Home Desktop 100'}, 'stock_value_difference'))
stock_value_diff = stock_value_diff_rm1 + stock_value_diff_rm2
gl_entries = get_gl_entries('Delivery Note', dn.name)
self.assertTrue(gl_entries)
expected_values = {stock_in_hand_account: [0.0, stock_value_diff], 'Cost of Goods Sold - TCP1': [stock_value_diff, 0.0]}
for _i, gle in enumerate(gl_entries):
    self.assertEqual([gle.debit, gle.credit], expected_values.get(gle.account))
bal = get_balance_on(stock_in_hand_account)
self.assertEqual(flt(bal, 2), flt(prev_bal - stock_value_diff, 2))
dn.cancel()
```

## Next Steps


---

*Source: test_delivery_note.py:96 | Complexity: Advanced | Last updated: 2026-02-04*