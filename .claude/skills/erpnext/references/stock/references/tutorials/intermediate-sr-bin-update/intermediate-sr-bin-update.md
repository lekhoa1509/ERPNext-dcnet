# How To: Intermediate Sr Bin Update

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Bin should show correct qty even for backdated entries.

-------------------------------------------
| creation | Var | Doc  | Qty | balance qty
-------------------------------------------
|  1       | SR  | Reco | 10  | 10     (posting date: today+10)
|  3       | SR2 | Reco | 11  | 11     (posting date: today+11)
|  2       | DN  | DN   | 5   | 6 <-- assert in BIN  (posting date: today+12)

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

### Step 1: 'Bin should show correct qty even for backdated entries.\n\n\t\t-------------------------------------------\n\t\t| creation | Var | Doc  | Qty | balance qty\n\t\t-------------------------------------------\n\t\t|  1       | SR  | Reco | 10  | 10     (posting date: today+10)\n\t\t|  3       | SR2 | Reco | 11  | 11     (posting date: today+11)\n\t\t|  2       | DN  | DN   | 5   | 6 <-- assert in BIN  (posting date: today+12)\n\t\t'

```python
'Bin should show correct qty even for backdated entries.\n\n\t\t-------------------------------------------\n\t\t| creation | Var | Doc  | Qty | balance qty\n\t\t-------------------------------------------\n\t\t|  1       | SR  | Reco | 10  | 10     (posting date: today+10)\n\t\t|  3       | SR2 | Reco | 11  | 11     (posting date: today+11)\n\t\t|  2       | DN  | DN   | 5   | 6 <-- assert in BIN  (posting date: today+12)\n\t\t'
```

### Step 2: Call frappe.db.rollback()

```python
frappe.db.rollback()
```

### Step 3: Assign frappe.flags.dont_execute_stock_reposts = True

```python
frappe.flags.dont_execute_stock_reposts = True
```

### Step 4: Assign item_code = value

```python
item_code = self.make_item().name
```

### Step 5: Assign warehouse = '_Test Warehouse - _TC'

```python
warehouse = '_Test Warehouse - _TC'
```

### Step 6: Call create_stock_reconciliation()

```python
create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=10, rate=100, posting_date=add_days(nowdate(), 10))
```

### Step 7: Call create_delivery_note()

```python
create_delivery_note(item_code=item_code, warehouse=warehouse, qty=5, rate=120, posting_date=add_days(nowdate(), 12))
```

### Step 8: Assign old_bin_qty = frappe.db.get_value(...)

```python
old_bin_qty = frappe.db.get_value('Bin', {'item_code': item_code, 'warehouse': warehouse}, 'actual_qty')
```

### Step 9: Call create_stock_reconciliation()

```python
create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=11, rate=100, posting_date=add_days(nowdate(), 11))
```

### Step 10: Assign new_bin_qty = frappe.db.get_value(...)

```python
new_bin_qty = frappe.db.get_value('Bin', {'item_code': item_code, 'warehouse': warehouse}, 'actual_qty')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(old_bin_qty + 1, new_bin_qty)
```

### Step 12: Call frappe.db.rollback()

```python
frappe.db.rollback()
```


## Complete Example

```python
# Workflow
'Bin should show correct qty even for backdated entries.\n\n\t\t-------------------------------------------\n\t\t| creation | Var | Doc  | Qty | balance qty\n\t\t-------------------------------------------\n\t\t|  1       | SR  | Reco | 10  | 10     (posting date: today+10)\n\t\t|  3       | SR2 | Reco | 11  | 11     (posting date: today+11)\n\t\t|  2       | DN  | DN   | 5   | 6 <-- assert in BIN  (posting date: today+12)\n\t\t'
from erpnext.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
frappe.db.rollback()
frappe.flags.dont_execute_stock_reposts = True
item_code = self.make_item().name
warehouse = '_Test Warehouse - _TC'
create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=10, rate=100, posting_date=add_days(nowdate(), 10))
create_delivery_note(item_code=item_code, warehouse=warehouse, qty=5, rate=120, posting_date=add_days(nowdate(), 12))
old_bin_qty = frappe.db.get_value('Bin', {'item_code': item_code, 'warehouse': warehouse}, 'actual_qty')
create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=11, rate=100, posting_date=add_days(nowdate(), 11))
new_bin_qty = frappe.db.get_value('Bin', {'item_code': item_code, 'warehouse': warehouse}, 'actual_qty')
self.assertEqual(old_bin_qty + 1, new_bin_qty)
frappe.db.rollback()
```

## Next Steps


---

*Source: test_stock_reconciliation.py:516 | Complexity: Advanced | Last updated: 2026-02-04*