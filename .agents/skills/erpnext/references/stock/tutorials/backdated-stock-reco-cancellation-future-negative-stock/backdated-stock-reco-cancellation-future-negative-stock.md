# How To: Backdated Stock Reco Cancellation Future Negative Stock

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test if a backdated stock reco cancellation that causes future negative stock is blocked.
-------------------------------------------
Var | Doc  | Qty | Balance
-------------------------------------------
SR  | Reco | 100 | 100     (posting date: today-1) (shouldn't be cancelled after DN)
DN  | DN   | 100 |   0     (posting date: today)

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.utils`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_reconciliation.stock_reconciliation`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.stock_ledger`
- `erpnext.stock.tests.test_utils`
- `erpnext.stock.utils`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.stock_ledger`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.stock_ledger`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`


## Step-by-Step Guide

### Step 1: "\n\t\tTest if a backdated stock reco cancellation that causes future negative stock is blocked.\n\t\t-------------------------------------------\n\t\tVar | Doc  | Qty | Balance\n\t\t-------------------------------------------\n\t\tSR  | Reco | 100 | 100     (posting date: today-1) (shouldn't be cancelled after DN)\n\t\tDN  | DN   | 100 |   0     (posting date: today)\n\t\t"

```python
"\n\t\tTest if a backdated stock reco cancellation that causes future negative stock is blocked.\n\t\t-------------------------------------------\n\t\tVar | Doc  | Qty | Balance\n\t\t-------------------------------------------\n\t\tSR  | Reco | 100 | 100     (posting date: today-1) (shouldn't be cancelled after DN)\n\t\tDN  | DN   | 100 |   0     (posting date: today)\n\t\t"
```

### Step 2: Assign item_code = value

```python
item_code = self.make_item().name
```

### Step 3: Assign warehouse = '_Test Warehouse - _TC'

```python
warehouse = '_Test Warehouse - _TC'
```

### Step 4: Assign sr = create_stock_reconciliation(...)

```python
sr = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=100, rate=100, posting_date=add_days(nowdate(), -1))
```

### Step 5: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(item_code=item_code, warehouse=warehouse, qty=100, rate=120, posting_date=nowdate())
```

### Step 6: Assign dn_balance = frappe.db.get_value(...)

```python
dn_balance = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': dn.name, 'is_cancelled': 0}, 'qty_after_transaction')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(dn_balance, 0)
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(NegativeStockError, sr.cancel)
```

### Step 9: Assign repost_exists = bool(...)

```python
repost_exists = bool(frappe.db.exists('Repost Item Valuation', {'voucher_no': sr.name, 'status': 'Queued'}))
```

### Step 10: Call self.assertFalse()

```python
self.assertFalse(repost_exists, msg='Negative stock validation not working on reco cancellation')
```


## Complete Example

```python
# Workflow
"\n\t\tTest if a backdated stock reco cancellation that causes future negative stock is blocked.\n\t\t-------------------------------------------\n\t\tVar | Doc  | Qty | Balance\n\t\t-------------------------------------------\n\t\tSR  | Reco | 100 | 100     (posting date: today-1) (shouldn't be cancelled after DN)\n\t\tDN  | DN   | 100 |   0     (posting date: today)\n\t\t"
from erpnext.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
from erpnext.stock.stock_ledger import NegativeStockError
item_code = self.make_item().name
warehouse = '_Test Warehouse - _TC'
sr = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=100, rate=100, posting_date=add_days(nowdate(), -1))
dn = create_delivery_note(item_code=item_code, warehouse=warehouse, qty=100, rate=120, posting_date=nowdate())
dn_balance = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': dn.name, 'is_cancelled': 0}, 'qty_after_transaction')
self.assertEqual(dn_balance, 0)
self.assertRaises(NegativeStockError, sr.cancel)
repost_exists = bool(frappe.db.exists('Repost Item Valuation', {'voucher_no': sr.name, 'status': 'Queued'}))
self.assertFalse(repost_exists, msg='Negative stock validation not working on reco cancellation')
```

## Next Steps


---

*Source: test_stock_reconciliation.py:476 | Complexity: Advanced | Last updated: 2026-02-04*