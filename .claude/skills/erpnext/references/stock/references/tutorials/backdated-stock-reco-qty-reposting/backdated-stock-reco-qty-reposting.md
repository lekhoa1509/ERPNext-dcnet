# How To: Backdated Stock Reco Qty Reposting

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test if a backdated stock reco recalculates future qty until next reco.
-------------------------------------------
Var             | Doc   |       Qty     | Balance
-------------------------------------------
PR5     | PR    |   10  |  10   (posting date: today-4) [backdated]
SR5             | Reco  |       0       |       8       (posting date: today-4) [backdated]
PR1             | PR    |       10      |       18      (posting date: today-3)
PR2             | PR    |       1       |       19      (posting date: today-2)
SR4             | Reco  |       0       |       6       (posting date: today-1) [backdated]
PR3             | PR    |       1       |       7       (posting date: today) # can't post future PR

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

### Step 1: "\n\t\tTest if a backdated stock reco recalculates future qty until next reco.\n\t\t-------------------------------------------\n\t\tVar\t\t| Doc\t|\tQty\t| Balance\n\t\t-------------------------------------------\n\t\tPR5     | PR    |   10  |  10   (posting date: today-4) [backdated]\n\t\tSR5\t\t| Reco\t|\t0\t|\t8\t(posting date: today-4) [backdated]\n\t\tPR1\t\t| PR\t|\t10\t|\t18\t(posting date: today-3)\n\t\tPR2\t\t| PR\t|\t1\t|\t19\t(posting date: today-2)\n\t\tSR4\t\t| Reco\t|\t0\t|\t6\t(posting date: today-1) [backdated]\n\t\tPR3\t\t| PR\t|\t1\t|\t7\t(posting date: today) # can't post future PR\n\t\t"

```python
"\n\t\tTest if a backdated stock reco recalculates future qty until next reco.\n\t\t-------------------------------------------\n\t\tVar\t\t| Doc\t|\tQty\t| Balance\n\t\t-------------------------------------------\n\t\tPR5     | PR    |   10  |  10   (posting date: today-4) [backdated]\n\t\tSR5\t\t| Reco\t|\t0\t|\t8\t(posting date: today-4) [backdated]\n\t\tPR1\t\t| PR\t|\t10\t|\t18\t(posting date: today-3)\n\t\tPR2\t\t| PR\t|\t1\t|\t19\t(posting date: today-2)\n\t\tSR4\t\t| Reco\t|\t0\t|\t6\t(posting date: today-1) [backdated]\n\t\tPR3\t\t| PR\t|\t1\t|\t7\t(posting date: today) # can't post future PR\n\t\t"
```

**Verification:**
```python
assertBalance(pr1, 10)
```

### Step 2: Assign item_code = value

```python
item_code = self.make_item().name
```

**Verification:**
```python
assertBalance(pr3, 12)
```

### Step 3: Assign warehouse = '_Test Warehouse - _TC'

```python
warehouse = '_Test Warehouse - _TC'
```

**Verification:**
```python
assertBalance(pr3, 7)
```

### Step 4: Assign frappe.flags.dont_execute_stock_reposts = True

```python
frappe.flags.dont_execute_stock_reposts = True
```

**Verification:**
```python
assertBalance(pr1, 18)
```

### Step 5: Assign pr1 = make_purchase_receipt(...)

```python
pr1 = make_purchase_receipt(item_code=item_code, warehouse=warehouse, qty=10, rate=100, posting_date=add_days(nowdate(), -3))
```

**Verification:**
```python
assertBalance(pr2, 19)
```

### Step 6: Assign pr2 = make_purchase_receipt(...)

```python
pr2 = make_purchase_receipt(item_code=item_code, warehouse=warehouse, qty=1, rate=100, posting_date=add_days(nowdate(), -2))
```

**Verification:**
```python
assertBalance(sr4, 6)
```

### Step 7: Assign pr3 = make_purchase_receipt(...)

```python
pr3 = make_purchase_receipt(item_code=item_code, warehouse=warehouse, qty=1, rate=100, posting_date=nowdate())
```

**Verification:**
```python
assertBalance(pr5, 10)
```

### Step 8: Call assertBalance()

```python
assertBalance(pr1, 10)
```

**Verification:**
```python
assertBalance(sr4, 6)
```

### Step 9: Call assertBalance()

```python
assertBalance(pr3, 12)
```

**Verification:**
```python
assertBalance(sr5, 8)
```

### Step 10: Assign sr4 = create_stock_reconciliation(...)

```python
sr4 = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=6, rate=100, posting_date=add_days(nowdate(), -1))
```

**Verification:**
```python
assertBalance(pr1, 10)
```

### Step 11: Call assertBalance()

```python
assertBalance(pr3, 7)
```

**Verification:**
```python
assertBalance(pr2, 11)
```

### Step 12: Assign sr5 = create_stock_reconciliation(...)

```python
sr5 = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=8, rate=100, posting_date=add_days(nowdate(), -4))
```

**Verification:**
```python
assertBalance(sr4, 6)
```

### Step 13: Call assertBalance()

```python
assertBalance(pr1, 18)
```

### Step 14: Call assertBalance()

```python
assertBalance(pr2, 19)
```

### Step 15: Call assertBalance()

```python
assertBalance(sr4, 6)
```

### Step 16: Assign pr5 = make_purchase_receipt(...)

```python
pr5 = make_purchase_receipt(item_code=item_code, warehouse=warehouse, qty=10, rate=100, posting_date=add_days(nowdate(), -5))
```

### Step 17: Call assertBalance()

```python
assertBalance(pr5, 10)
```

### Step 18: Call assertBalance()

```python
assertBalance(sr4, 6)
```

### Step 19: Call assertBalance()

```python
assertBalance(sr5, 8)
```

### Step 20: Call sr5.cancel()

```python
sr5.cancel()
```

### Step 21: Call assertBalance()

```python
assertBalance(pr1, 10)
```

### Step 22: Call assertBalance()

```python
assertBalance(pr2, 11)
```

### Step 23: Call assertBalance()

```python
assertBalance(sr4, 6)
```

### Step 24: Assign sle_balance = frappe.db.get_value(...)

```python
sle_balance = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': doc.name, 'is_cancelled': 0}, 'qty_after_transaction')
```

### Step 25: Call self.assertEqual()

```python
self.assertEqual(sle_balance, qty_after_transaction)
```


## Complete Example

```python
# Workflow
"\n\t\tTest if a backdated stock reco recalculates future qty until next reco.\n\t\t-------------------------------------------\n\t\tVar\t\t| Doc\t|\tQty\t| Balance\n\t\t-------------------------------------------\n\t\tPR5     | PR    |   10  |  10   (posting date: today-4) [backdated]\n\t\tSR5\t\t| Reco\t|\t0\t|\t8\t(posting date: today-4) [backdated]\n\t\tPR1\t\t| PR\t|\t10\t|\t18\t(posting date: today-3)\n\t\tPR2\t\t| PR\t|\t1\t|\t19\t(posting date: today-2)\n\t\tSR4\t\t| Reco\t|\t0\t|\t6\t(posting date: today-1) [backdated]\n\t\tPR3\t\t| PR\t|\t1\t|\t7\t(posting date: today) # can't post future PR\n\t\t"
item_code = self.make_item().name
warehouse = '_Test Warehouse - _TC'
frappe.flags.dont_execute_stock_reposts = True

def assertBalance(doc, qty_after_transaction):
    sle_balance = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': doc.name, 'is_cancelled': 0}, 'qty_after_transaction')
    self.assertEqual(sle_balance, qty_after_transaction)
pr1 = make_purchase_receipt(item_code=item_code, warehouse=warehouse, qty=10, rate=100, posting_date=add_days(nowdate(), -3))
pr2 = make_purchase_receipt(item_code=item_code, warehouse=warehouse, qty=1, rate=100, posting_date=add_days(nowdate(), -2))
pr3 = make_purchase_receipt(item_code=item_code, warehouse=warehouse, qty=1, rate=100, posting_date=nowdate())
assertBalance(pr1, 10)
assertBalance(pr3, 12)
sr4 = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=6, rate=100, posting_date=add_days(nowdate(), -1))
assertBalance(pr3, 7)
sr5 = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=8, rate=100, posting_date=add_days(nowdate(), -4))
assertBalance(pr1, 18)
assertBalance(pr2, 19)
assertBalance(sr4, 6)
pr5 = make_purchase_receipt(item_code=item_code, warehouse=warehouse, qty=10, rate=100, posting_date=add_days(nowdate(), -5))
assertBalance(pr5, 10)
assertBalance(sr4, 6)
assertBalance(sr5, 8)
sr5.cancel()
assertBalance(pr1, 10)
assertBalance(pr2, 11)
assertBalance(sr4, 6)
```

## Next Steps


---

*Source: test_stock_reconciliation.py:361 | Complexity: Advanced | Last updated: 2026-02-04*