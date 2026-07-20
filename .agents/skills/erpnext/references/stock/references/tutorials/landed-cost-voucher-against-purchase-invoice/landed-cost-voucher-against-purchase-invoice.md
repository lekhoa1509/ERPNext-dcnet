# How To: Landed Cost Voucher Against Purchase Invoice

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test landed cost voucher against purchase invoice

## Prerequisites

**Required Modules:**
- `copy`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.utils`
- `erpnext.assets.doctype.asset.test_asset`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.serial_batch_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.setup.doctype.currency_exchange.test_currency_exchange`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.controllers.tests.test_subcontracting_controller`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.doctype.work_order.test_work_order`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.subcontracting.doctype.subcontracting_order.subcontracting_order`


## Step-by-Step Guide

### Step 1: Assign pi = make_purchase_invoice(...)

```python
pi = make_purchase_invoice(update_stock=1, posting_date=frappe.utils.nowdate(), posting_time=frappe.utils.nowtime(), cash_bank_account='Cash - TCP1', company='_Test Company with perpetual inventory', supplier_warehouse='Work In Progress - TCP1', warehouse='Stores - TCP1', cost_center='Main - TCP1', expense_account='_Test Account Cost for Goods Sold - TCP1')
```

### Step 2: Assign last_sle = frappe.db.get_value(...)

```python
last_sle = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pi.doctype, 'voucher_no': pi.name, 'item_code': '_Test Item', 'warehouse': 'Stores - TCP1'}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
```

### Step 3: Call create_landed_cost_voucher()

```python
create_landed_cost_voucher('Purchase Invoice', pi.name, pi.company)
```

### Step 4: Assign pi_lc_value = frappe.db.get_value(...)

```python
pi_lc_value = frappe.db.get_value('Purchase Invoice Item', {'parent': pi.name}, 'landed_cost_voucher_amount')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(pi_lc_value, 50.0)
```

### Step 6: Assign last_sle_after_landed_cost = frappe.db.get_value(...)

```python
last_sle_after_landed_cost = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pi.doctype, 'voucher_no': pi.name, 'item_code': '_Test Item', 'warehouse': 'Stores - TCP1'}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(last_sle.qty_after_transaction, last_sle_after_landed_cost.qty_after_transaction)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(last_sle_after_landed_cost.stock_value - last_sle.stock_value, 50.0)
```

### Step 9: Assign gl_entries = get_gl_entries(...)

```python
gl_entries = get_gl_entries('Purchase Invoice', pi.name)
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(gl_entries)
```

### Step 11: Assign stock_in_hand_account = get_inventory_account(...)

```python
stock_in_hand_account = get_inventory_account(pi.company, pi.get('items')[0].warehouse)
```

### Step 12: Assign expected_values = value

```python
expected_values = {stock_in_hand_account: [300.0, 0.0], 'Creditors - TCP1': [0.0, 250.0], 'Expenses Included In Valuation - TCP1': [0.0, 50.0]}
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(expected_values[gle.account][0], gle.debit)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(expected_values[gle.account][1], gle.credit)
```


## Complete Example

```python
# Workflow
pi = make_purchase_invoice(update_stock=1, posting_date=frappe.utils.nowdate(), posting_time=frappe.utils.nowtime(), cash_bank_account='Cash - TCP1', company='_Test Company with perpetual inventory', supplier_warehouse='Work In Progress - TCP1', warehouse='Stores - TCP1', cost_center='Main - TCP1', expense_account='_Test Account Cost for Goods Sold - TCP1')
last_sle = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pi.doctype, 'voucher_no': pi.name, 'item_code': '_Test Item', 'warehouse': 'Stores - TCP1'}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
create_landed_cost_voucher('Purchase Invoice', pi.name, pi.company)
pi_lc_value = frappe.db.get_value('Purchase Invoice Item', {'parent': pi.name}, 'landed_cost_voucher_amount')
self.assertEqual(pi_lc_value, 50.0)
last_sle_after_landed_cost = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pi.doctype, 'voucher_no': pi.name, 'item_code': '_Test Item', 'warehouse': 'Stores - TCP1'}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
self.assertEqual(last_sle.qty_after_transaction, last_sle_after_landed_cost.qty_after_transaction)
self.assertEqual(last_sle_after_landed_cost.stock_value - last_sle.stock_value, 50.0)
gl_entries = get_gl_entries('Purchase Invoice', pi.name)
self.assertTrue(gl_entries)
stock_in_hand_account = get_inventory_account(pi.company, pi.get('items')[0].warehouse)
expected_values = {stock_in_hand_account: [300.0, 0.0], 'Creditors - TCP1': [0.0, 250.0], 'Expenses Included In Valuation - TCP1': [0.0, 50.0]}
for gle in gl_entries:
    if not gle.get('is_cancelled'):
        self.assertEqual(expected_values[gle.account][0], gle.debit)
        self.assertEqual(expected_values[gle.account][1], gle.credit)
```

## Next Steps


---

*Source: test_landed_cost_voucher.py:234 | Complexity: Advanced | Last updated: 2026-02-04*