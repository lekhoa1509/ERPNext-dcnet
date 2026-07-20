# How To: Landed Cost Voucher Stock Impact

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test impact of LCV on future stock balances.

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

### Step 1: 'Test impact of LCV on future stock balances.'

```python
'Test impact of LCV on future stock balances.'
```

### Step 2: Assign item = make_item(...)

```python
item = make_item('LCV Stock Item', {'is_stock_item': 1})
```

### Step 3: Assign warehouse = 'Stores - _TC'

```python
warehouse = 'Stores - _TC'
```

### Step 4: Assign pr1 = make_purchase_receipt(...)

```python
pr1 = make_purchase_receipt(item_code=item.name, warehouse=warehouse, qty=500, rate=80, posting_date=add_days(frappe.utils.nowdate(), -2))
```

### Step 5: Assign pr2 = make_purchase_receipt(...)

```python
pr2 = make_purchase_receipt(item_code=item.name, warehouse=warehouse, qty=100, rate=80, posting_date=frappe.utils.nowdate())
```

### Step 6: Assign last_sle = frappe.db.get_value(...)

```python
last_sle = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pr2.doctype, 'voucher_no': pr2.name, 'item_code': item.name, 'warehouse': warehouse, 'is_cancelled': 0}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
```

### Step 7: Call create_landed_cost_voucher()

```python
create_landed_cost_voucher('Purchase Receipt', pr1.name, pr1.company)
```

### Step 8: Assign last_sle_after_landed_cost = frappe.db.get_value(...)

```python
last_sle_after_landed_cost = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pr2.doctype, 'voucher_no': pr2.name, 'item_code': item.name, 'warehouse': warehouse, 'is_cancelled': 0}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(last_sle.qty_after_transaction, last_sle_after_landed_cost.qty_after_transaction)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(last_sle_after_landed_cost.stock_value - last_sle.stock_value, 50.0)
```


## Complete Example

```python
# Workflow
'Test impact of LCV on future stock balances.'
from erpnext.stock.doctype.item.test_item import make_item
item = make_item('LCV Stock Item', {'is_stock_item': 1})
warehouse = 'Stores - _TC'
pr1 = make_purchase_receipt(item_code=item.name, warehouse=warehouse, qty=500, rate=80, posting_date=add_days(frappe.utils.nowdate(), -2))
pr2 = make_purchase_receipt(item_code=item.name, warehouse=warehouse, qty=100, rate=80, posting_date=frappe.utils.nowdate())
last_sle = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pr2.doctype, 'voucher_no': pr2.name, 'item_code': item.name, 'warehouse': warehouse, 'is_cancelled': 0}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
create_landed_cost_voucher('Purchase Receipt', pr1.name, pr1.company)
last_sle_after_landed_cost = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pr2.doctype, 'voucher_no': pr2.name, 'item_code': item.name, 'warehouse': warehouse, 'is_cancelled': 0}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
self.assertEqual(last_sle.qty_after_transaction, last_sle_after_landed_cost.qty_after_transaction)
self.assertEqual(last_sle_after_landed_cost.stock_value - last_sle.stock_value, 50.0)
```

## Next Steps


---

*Source: test_landed_cost_voucher.py:128 | Complexity: Advanced | Last updated: 2026-02-04*