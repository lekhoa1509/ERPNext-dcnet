# How To: Backdated Stock Reco Future Negative Stock

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test if a backdated stock reco causes future negative stock and is blocked.
-------------------------------------------
Var             | Doc   |       Qty     | Balance
-------------------------------------------
PR1             | PR    |       10      |       10              (posting date: today-2)
SR3             | Reco  |       0       |       1               (posting date: today-1) [backdated & blocked]
DN2             | DN    |       -2      |       8(-1)   (posting date: today)

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

### Step 1: '\n\t\tTest if a backdated stock reco causes future negative stock and is blocked.\n\t\t-------------------------------------------\n\t\tVar\t\t| Doc\t|\tQty\t| Balance\n\t\t-------------------------------------------\n\t\tPR1\t\t| PR\t|\t10\t|\t10\t\t(posting date: today-2)\n\t\tSR3\t\t| Reco\t|\t0\t|\t1\t\t(posting date: today-1) [backdated & blocked]\n\t\tDN2\t\t| DN\t|\t-2\t|\t8(-1)\t(posting date: today)\n\t\t'

```python
'\n\t\tTest if a backdated stock reco causes future negative stock and is blocked.\n\t\t-------------------------------------------\n\t\tVar\t\t| Doc\t|\tQty\t| Balance\n\t\t-------------------------------------------\n\t\tPR1\t\t| PR\t|\t10\t|\t10\t\t(posting date: today-2)\n\t\tSR3\t\t| Reco\t|\t0\t|\t1\t\t(posting date: today-1) [backdated & blocked]\n\t\tDN2\t\t| DN\t|\t-2\t|\t8(-1)\t(posting date: today)\n\t\t'
```

### Step 2: Assign item_code = value

```python
item_code = self.make_item().name
```

### Step 3: Assign warehouse = '_Test Warehouse - _TC'

```python
warehouse = '_Test Warehouse - _TC'
```

### Step 4: Assign pr1 = make_purchase_receipt(...)

```python
pr1 = make_purchase_receipt(item_code=item_code, warehouse=warehouse, qty=10, rate=100, posting_date=add_days(nowdate(), -2))
```

### Step 5: Assign dn2 = create_delivery_note(...)

```python
dn2 = create_delivery_note(item_code=item_code, warehouse=warehouse, qty=2, rate=120, posting_date=nowdate())
```

### Step 6: Assign pr1_balance = frappe.db.get_value(...)

```python
pr1_balance = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': pr1.name, 'is_cancelled': 0}, 'qty_after_transaction')
```

### Step 7: Assign dn2_balance = frappe.db.get_value(...)

```python
dn2_balance = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': dn2.name, 'is_cancelled': 0}, 'qty_after_transaction')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(pr1_balance, 10)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(dn2_balance, 8)
```

### Step 10: Assign sr3 = create_stock_reconciliation(...)

```python
sr3 = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=1, rate=100, posting_date=add_days(nowdate(), -1), do_not_submit=True)
```

### Step 11: Call self.assertRaises()

```python
self.assertRaises(NegativeStockError, sr3.submit)
```

### Step 12: Call sr3.cancel()

```python
sr3.cancel()
```

### Step 13: Call dn2.cancel()

```python
dn2.cancel()
```

### Step 14: Call pr1.cancel()

```python
pr1.cancel()
```


## Complete Example

```python
# Workflow
'\n\t\tTest if a backdated stock reco causes future negative stock and is blocked.\n\t\t-------------------------------------------\n\t\tVar\t\t| Doc\t|\tQty\t| Balance\n\t\t-------------------------------------------\n\t\tPR1\t\t| PR\t|\t10\t|\t10\t\t(posting date: today-2)\n\t\tSR3\t\t| Reco\t|\t0\t|\t1\t\t(posting date: today-1) [backdated & blocked]\n\t\tDN2\t\t| DN\t|\t-2\t|\t8(-1)\t(posting date: today)\n\t\t'
from erpnext.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
from erpnext.stock.stock_ledger import NegativeStockError
item_code = self.make_item().name
warehouse = '_Test Warehouse - _TC'
pr1 = make_purchase_receipt(item_code=item_code, warehouse=warehouse, qty=10, rate=100, posting_date=add_days(nowdate(), -2))
dn2 = create_delivery_note(item_code=item_code, warehouse=warehouse, qty=2, rate=120, posting_date=nowdate())
pr1_balance = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': pr1.name, 'is_cancelled': 0}, 'qty_after_transaction')
dn2_balance = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': dn2.name, 'is_cancelled': 0}, 'qty_after_transaction')
self.assertEqual(pr1_balance, 10)
self.assertEqual(dn2_balance, 8)
sr3 = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=1, rate=100, posting_date=add_days(nowdate(), -1), do_not_submit=True)
self.assertRaises(NegativeStockError, sr3.submit)
sr3.cancel()
dn2.cancel()
pr1.cancel()
```

## Next Steps


---

*Source: test_stock_reconciliation.py:427 | Complexity: Advanced | Last updated: 2026-02-04*