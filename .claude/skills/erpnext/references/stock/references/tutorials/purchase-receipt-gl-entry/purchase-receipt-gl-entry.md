# How To: Purchase Receipt Gl Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test purchase receipt gl entry

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `pypika`
- `erpnext`
- `erpnext.controllers`
- `erpnext.controllers.status_updater`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.buying.doctype.supplier.test_supplier`
- `erpnext.controllers.accounts_controller`
- `erpnext.controllers.buying_controller`
- `erpnext.stock`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.get_item_details`
- `erpnext.stock.utils`
- `erpnext.buying.doctype.purchase_order`
- `erpnext.buying.doctype.purchase_order`
- `erpnext.accounts.doctype.purchase_invoice.purchase_invoice`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.party`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.get_item_details`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.landed_cost_voucher.test_landed_cost_voucher`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.buying.doctype.supplier.test_supplier`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.serial_no.serial_no`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.accounts.doctype.purchase_invoice.purchase_invoice`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.landed_cost_voucher.test_landed_cost_voucher`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.report.stock_balance.stock_balance`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.landed_cost_voucher.test_landed_cost_voucher`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.stock_ledger`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.stock_ledger`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`

**Setup Required:**
```python
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)
```

## Step-by-Step Guide

### Step 1: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Work In Progress - TCP1', get_multiple_items=True, get_taxes_and_charges=True)
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual(cint(erpnext.is_perpetual_inventory_enabled(pr.company)), 1)
```

### Step 3: Assign gl_entries = get_gl_entries(...)

```python
gl_entries = get_gl_entries('Purchase Receipt', pr.name)
```

### Step 4: Call self.assertTrue()

```python
self.assertTrue(gl_entries)
```

### Step 5: Assign stock_in_hand_account = get_inventory_account(...)

```python
stock_in_hand_account = get_inventory_account(pr.company, pr.items[0].warehouse)
```

### Step 6: Assign fixed_asset_account = get_inventory_account(...)

```python
fixed_asset_account = get_inventory_account(pr.company, pr.items[1].warehouse)
```

### Step 7: Call pr.cancel()

```python
pr.cancel()
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(get_gl_entries('Purchase Receipt', pr.name))
```

### Step 9: Assign expected_values = value

```python
expected_values = {stock_in_hand_account: [750.0, 0.0], 'Stock Received But Not Billed - TCP1': [0.0, 500.0], '_Test Account Shipping Charges - TCP1': [0.0, 100.0], '_Test Account Customs Duty - TCP1': [0.0, 150.0]}
```

### Step 10: Assign expected_values = value

```python
expected_values = {stock_in_hand_account: [375.0, 0.0], fixed_asset_account: [375.0, 0.0], 'Stock Received But Not Billed - TCP1': [0.0, 500.0], '_Test Account Shipping Charges - TCP1': [0.0, 250.0]}
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(expected_values[gle.account][0], gle.debit)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(expected_values[gle.account][1], gle.credit)
```


## Complete Example

```python
# Setup
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)

# Workflow
pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Work In Progress - TCP1', get_multiple_items=True, get_taxes_and_charges=True)
self.assertEqual(cint(erpnext.is_perpetual_inventory_enabled(pr.company)), 1)
gl_entries = get_gl_entries('Purchase Receipt', pr.name)
self.assertTrue(gl_entries)
stock_in_hand_account = get_inventory_account(pr.company, pr.items[0].warehouse)
fixed_asset_account = get_inventory_account(pr.company, pr.items[1].warehouse)
if stock_in_hand_account == fixed_asset_account:
    expected_values = {stock_in_hand_account: [750.0, 0.0], 'Stock Received But Not Billed - TCP1': [0.0, 500.0], '_Test Account Shipping Charges - TCP1': [0.0, 100.0], '_Test Account Customs Duty - TCP1': [0.0, 150.0]}
else:
    expected_values = {stock_in_hand_account: [375.0, 0.0], fixed_asset_account: [375.0, 0.0], 'Stock Received But Not Billed - TCP1': [0.0, 500.0], '_Test Account Shipping Charges - TCP1': [0.0, 250.0]}
for gle in gl_entries:
    self.assertEqual(expected_values[gle.account][0], gle.debit)
    self.assertEqual(expected_values[gle.account][1], gle.credit)
pr.cancel()
self.assertTrue(get_gl_entries('Purchase Receipt', pr.name))
```

## Next Steps


---

*Source: test_purchase_receipt.py:319 | Complexity: Advanced | Last updated: 2026-02-04*