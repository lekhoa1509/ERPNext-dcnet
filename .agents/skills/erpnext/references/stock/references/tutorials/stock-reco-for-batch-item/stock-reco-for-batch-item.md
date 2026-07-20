# How To: Stock Reco For Batch Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test stock reco for batch item

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

### Step 1: Assign to_delete_records = value

```python
to_delete_records = []
```

### Step 2: Assign item_code = 'Stock-Reco-batch-Item-123'

```python
item_code = 'Stock-Reco-batch-Item-123'
```

### Step 3: Assign warehouse = '_Test Warehouse for Stock Reco2 - _TC'

```python
warehouse = '_Test Warehouse for Stock Reco2 - _TC'
```

### Step 4: Call self.make_item()

```python
self.make_item(item_code, frappe._dict({'is_stock_item': 1, 'has_batch_no': 1, 'create_new_batch': 1, 'batch_number_series': 'SRBI123-.#####'}))
```

### Step 5: Assign sr = create_stock_reconciliation(...)

```python
sr = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=5, rate=200, do_not_save=1)
```

### Step 6: Call sr.save()

```python
sr.save()
```

### Step 7: Call sr.submit()

```python
sr.submit()
```

### Step 8: Call sr.load_from_db()

```python
sr.load_from_db()
```

### Step 9: Assign batch_no = get_batch_from_bundle(...)

```python
batch_no = get_batch_from_bundle(sr.items[0].serial_and_batch_bundle)
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(batch_no)
```

### Step 11: Call to_delete_records.append()

```python
to_delete_records.append(sr.name)
```

### Step 12: Assign sr1 = create_stock_reconciliation(...)

```python
sr1 = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=6, rate=300, batch_no=batch_no)
```

### Step 13: Assign args = value

```python
args = {'item_code': item_code, 'warehouse': warehouse, 'posting_date': nowdate(), 'posting_time': nowtime(), 'serial_and_batch_bundle': sr1.items[0].serial_and_batch_bundle}
```

### Step 14: Assign valuation_rate = get_incoming_rate(...)

```python
valuation_rate = get_incoming_rate(args)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(valuation_rate, 300)
```

### Step 16: Call to_delete_records.append()

```python
to_delete_records.append(sr1.name)
```

### Step 17: Assign sr2 = create_stock_reconciliation(...)

```python
sr2 = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=0, rate=0, batch_no=batch_no)
```

### Step 18: Assign stock_value = get_stock_value_on(...)

```python
stock_value = get_stock_value_on(warehouse, nowdate(), item_code)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(stock_value, 0)
```

### Step 20: Call to_delete_records.append()

```python
to_delete_records.append(sr2.name)
```

### Step 21: Call to_delete_records.reverse()

```python
to_delete_records.reverse()
```

### Step 22: Assign stock_doc = frappe.get_doc(...)

```python
stock_doc = frappe.get_doc('Stock Reconciliation', d)
```

### Step 23: Call stock_doc.cancel()

```python
stock_doc.cancel()
```


## Complete Example

```python
# Workflow
to_delete_records = []
item_code = 'Stock-Reco-batch-Item-123'
warehouse = '_Test Warehouse for Stock Reco2 - _TC'
self.make_item(item_code, frappe._dict({'is_stock_item': 1, 'has_batch_no': 1, 'create_new_batch': 1, 'batch_number_series': 'SRBI123-.#####'}))
sr = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=5, rate=200, do_not_save=1)
sr.save()
sr.submit()
sr.load_from_db()
batch_no = get_batch_from_bundle(sr.items[0].serial_and_batch_bundle)
self.assertTrue(batch_no)
to_delete_records.append(sr.name)
sr1 = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=6, rate=300, batch_no=batch_no)
args = {'item_code': item_code, 'warehouse': warehouse, 'posting_date': nowdate(), 'posting_time': nowtime(), 'serial_and_batch_bundle': sr1.items[0].serial_and_batch_bundle}
valuation_rate = get_incoming_rate(args)
self.assertEqual(valuation_rate, 300)
to_delete_records.append(sr1.name)
sr2 = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=0, rate=0, batch_no=batch_no)
stock_value = get_stock_value_on(warehouse, nowdate(), item_code)
self.assertEqual(stock_value, 0)
to_delete_records.append(sr2.name)
to_delete_records.reverse()
for d in to_delete_records:
    stock_doc = frappe.get_doc('Stock Reconciliation', d)
    stock_doc.cancel()
```

## Next Steps


---

*Source: test_stock_reconciliation.py:217 | Complexity: Advanced | Last updated: 2026-02-04*