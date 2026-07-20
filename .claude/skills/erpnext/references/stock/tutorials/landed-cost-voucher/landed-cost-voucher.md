# How To: Landed Cost Voucher

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test landed cost voucher

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

### Step 1: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)
```

### Step 2: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Work In Progress - TCP1', get_multiple_items=True, get_taxes_and_charges=True)
```

### Step 3: Assign last_sle = frappe.db.get_value(...)

```python
last_sle = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pr.doctype, 'voucher_no': pr.name, 'item_code': '_Test Item', 'warehouse': 'Stores - TCP1', 'is_cancelled': 0}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
```

### Step 4: Call create_landed_cost_voucher()

```python
create_landed_cost_voucher('Purchase Receipt', pr.name, pr.company)
```

### Step 5: Assign pr_lc_value = frappe.db.get_value(...)

```python
pr_lc_value = frappe.db.get_value('Purchase Receipt Item', {'parent': pr.name}, 'landed_cost_voucher_amount')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(pr_lc_value, 25.0)
```

### Step 7: Assign last_sle_after_landed_cost = frappe.db.get_value(...)

```python
last_sle_after_landed_cost = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pr.doctype, 'voucher_no': pr.name, 'item_code': '_Test Item', 'warehouse': 'Stores - TCP1', 'is_cancelled': 0}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(last_sle.qty_after_transaction, last_sle_after_landed_cost.qty_after_transaction)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(last_sle_after_landed_cost.stock_value - last_sle.stock_value, 25.0)
```

### Step 10: Call self.assertPurchaseReceiptLCVGLEntries()

```python
self.assertPurchaseReceiptLCVGLEntries(pr)
```

### Step 11: Call frappe.db.set_value()

```python
frappe.db.set_value('Stock Ledger Entry', {'is_cancelled': 1, 'voucher_type': pr.doctype, 'voucher_no': pr.name}, 'is_cancelled', 1, modified=add_to_date(now(), hours=1, as_datetime=True, as_string=True))
```

### Step 12: Assign unknown = pr.get_items_and_warehouses(...)

```python
items, warehouses = pr.get_items_and_warehouses()
```

### Step 13: Call update_gl_entries_after()

```python
update_gl_entries_after(pr.posting_date, pr.posting_time, warehouses, items, company=pr.company)
```

### Step 14: Call self.assertPurchaseReceiptLCVGLEntries()

```python
self.assertPurchaseReceiptLCVGLEntries(pr)
```


## Complete Example

```python
# Workflow
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)
pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Work In Progress - TCP1', get_multiple_items=True, get_taxes_and_charges=True)
last_sle = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pr.doctype, 'voucher_no': pr.name, 'item_code': '_Test Item', 'warehouse': 'Stores - TCP1', 'is_cancelled': 0}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
create_landed_cost_voucher('Purchase Receipt', pr.name, pr.company)
pr_lc_value = frappe.db.get_value('Purchase Receipt Item', {'parent': pr.name}, 'landed_cost_voucher_amount')
self.assertEqual(pr_lc_value, 25.0)
last_sle_after_landed_cost = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pr.doctype, 'voucher_no': pr.name, 'item_code': '_Test Item', 'warehouse': 'Stores - TCP1', 'is_cancelled': 0}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
self.assertEqual(last_sle.qty_after_transaction, last_sle_after_landed_cost.qty_after_transaction)
self.assertEqual(last_sle_after_landed_cost.stock_value - last_sle.stock_value, 25.0)
self.assertPurchaseReceiptLCVGLEntries(pr)
frappe.db.set_value('Stock Ledger Entry', {'is_cancelled': 1, 'voucher_type': pr.doctype, 'voucher_no': pr.name}, 'is_cancelled', 1, modified=add_to_date(now(), hours=1, as_datetime=True, as_string=True))
items, warehouses = pr.get_items_and_warehouses()
update_gl_entries_after(pr.posting_date, pr.posting_time, warehouses, items, company=pr.company)
self.assertPurchaseReceiptLCVGLEntries(pr)
```

## Next Steps


---

*Source: test_landed_cost_voucher.py:29 | Complexity: Advanced | Last updated: 2026-02-04*