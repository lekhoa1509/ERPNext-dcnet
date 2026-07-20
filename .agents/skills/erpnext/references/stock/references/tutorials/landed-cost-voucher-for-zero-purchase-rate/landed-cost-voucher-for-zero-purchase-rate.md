# How To: Landed Cost Voucher For Zero Purchase Rate

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
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

### Step 4: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code=item.name, warehouse=warehouse, qty=10, rate=0, posting_date=add_days(frappe.utils.nowdate(), -2))
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': pr.name, 'is_cancelled': 0}, 'stock_value_difference'), 0)
```

### Step 6: Assign lcv = make_landed_cost_voucher(...)

```python
lcv = make_landed_cost_voucher(company=pr.company, receipt_document_type='Purchase Receipt', receipt_document=pr.name, charges=100, distribute_charges_based_on='Distribute Manually', do_not_save=True)
```

### Step 7: Call lcv.get_items_from_purchase_receipts()

```python
lcv.get_items_from_purchase_receipts()
```

### Step 8: Assign unknown.applicable_charges = 100

```python
lcv.items[0].applicable_charges = 100
```

### Step 9: Call lcv.save()

```python
lcv.save()
```

### Step 10: Call lcv.submit()

```python
lcv.submit()
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': pr.name, 'is_cancelled': 0}))
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': pr.name, 'is_cancelled': 0}, 'stock_value_difference'), 100)
```


## Complete Example

```python
# Workflow
'Test impact of LCV on future stock balances.'
from erpnext.stock.doctype.item.test_item import make_item
item = make_item('LCV Stock Item', {'is_stock_item': 1})
warehouse = 'Stores - _TC'
pr = make_purchase_receipt(item_code=item.name, warehouse=warehouse, qty=10, rate=0, posting_date=add_days(frappe.utils.nowdate(), -2))
self.assertEqual(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': pr.name, 'is_cancelled': 0}, 'stock_value_difference'), 0)
lcv = make_landed_cost_voucher(company=pr.company, receipt_document_type='Purchase Receipt', receipt_document=pr.name, charges=100, distribute_charges_based_on='Distribute Manually', do_not_save=True)
lcv.get_items_from_purchase_receipts()
lcv.items[0].applicable_charges = 100
lcv.save()
lcv.submit()
self.assertTrue(frappe.db.exists('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': pr.name, 'is_cancelled': 0}))
self.assertEqual(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': pr.name, 'is_cancelled': 0}, 'stock_value_difference'), 100)
```

## Next Steps


---

*Source: test_landed_cost_voucher.py:181 | Complexity: Advanced | Last updated: 2026-02-04*