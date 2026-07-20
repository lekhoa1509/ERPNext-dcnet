# How To: Stock Reco For Serialized Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test stock reco for serialized item

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

### Step 2: Assign serial_item_code = 'Stock-Reco-Serial-Item-1'

```python
serial_item_code = 'Stock-Reco-Serial-Item-1'
```

### Step 3: Assign serial_warehouse = '_Test Warehouse for Stock Reco1 - _TC'

```python
serial_warehouse = '_Test Warehouse for Stock Reco1 - _TC'
```

### Step 4: Assign sr = create_stock_reconciliation(...)

```python
sr = create_stock_reconciliation(item_code=serial_item_code, warehouse=serial_warehouse, qty=5, rate=200)
```

### Step 5: Assign serial_nos = frappe.get_doc.get_serial_nos(...)

```python
serial_nos = frappe.get_doc('Serial and Batch Bundle', sr.items[0].serial_and_batch_bundle).get_serial_nos()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(serial_nos), 5)
```

### Step 7: Assign args = value

```python
args = {'item_code': serial_item_code, 'warehouse': serial_warehouse, 'qty': -5, 'posting_date': add_days(sr.posting_date, 1), 'posting_time': nowtime(), 'serial_and_batch_bundle': sr.items[0].serial_and_batch_bundle}
```

### Step 8: Assign valuation_rate = get_incoming_rate(...)

```python
valuation_rate = get_incoming_rate(args)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(valuation_rate, 200)
```

### Step 10: Call to_delete_records.append()

```python
to_delete_records.append(sr.name)
```

### Step 11: Assign sr = create_stock_reconciliation(...)

```python
sr = create_stock_reconciliation(item_code=serial_item_code, warehouse=serial_warehouse, qty=5, rate=300, serial_no=serial_nos)
```

### Step 12: Assign sn_doc = frappe.get_doc(...)

```python
sn_doc = frappe.get_doc('Serial and Batch Bundle', sr.items[0].serial_and_batch_bundle)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(len(sn_doc.get_serial_nos()), 5)
```

### Step 14: Assign args = value

```python
args = {'item_code': serial_item_code, 'warehouse': serial_warehouse, 'qty': -5, 'posting_date': add_days(sr.posting_date, 1), 'posting_time': nowtime(), 'serial_and_batch_bundle': sr.items[0].serial_and_batch_bundle}
```

### Step 15: Assign valuation_rate = get_incoming_rate(...)

```python
valuation_rate = get_incoming_rate(args)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(valuation_rate, 300)
```

### Step 17: Call to_delete_records.append()

```python
to_delete_records.append(sr.name)
```

### Step 18: Call to_delete_records.reverse()

```python
to_delete_records.reverse()
```

### Step 19: Assign stock_doc = frappe.get_doc(...)

```python
stock_doc = frappe.get_doc('Stock Reconciliation', d)
```

### Step 20: Call stock_doc.cancel()

```python
stock_doc.cancel()
```


## Complete Example

```python
# Workflow
to_delete_records = []
serial_item_code = 'Stock-Reco-Serial-Item-1'
serial_warehouse = '_Test Warehouse for Stock Reco1 - _TC'
sr = create_stock_reconciliation(item_code=serial_item_code, warehouse=serial_warehouse, qty=5, rate=200)
serial_nos = frappe.get_doc('Serial and Batch Bundle', sr.items[0].serial_and_batch_bundle).get_serial_nos()
self.assertEqual(len(serial_nos), 5)
args = {'item_code': serial_item_code, 'warehouse': serial_warehouse, 'qty': -5, 'posting_date': add_days(sr.posting_date, 1), 'posting_time': nowtime(), 'serial_and_batch_bundle': sr.items[0].serial_and_batch_bundle}
valuation_rate = get_incoming_rate(args)
self.assertEqual(valuation_rate, 200)
to_delete_records.append(sr.name)
sr = create_stock_reconciliation(item_code=serial_item_code, warehouse=serial_warehouse, qty=5, rate=300, serial_no=serial_nos)
sn_doc = frappe.get_doc('Serial and Batch Bundle', sr.items[0].serial_and_batch_bundle)
self.assertEqual(len(sn_doc.get_serial_nos()), 5)
args = {'item_code': serial_item_code, 'warehouse': serial_warehouse, 'qty': -5, 'posting_date': add_days(sr.posting_date, 1), 'posting_time': nowtime(), 'serial_and_batch_bundle': sr.items[0].serial_and_batch_bundle}
valuation_rate = get_incoming_rate(args)
self.assertEqual(valuation_rate, 300)
to_delete_records.append(sr.name)
to_delete_records.reverse()
for d in to_delete_records:
    stock_doc = frappe.get_doc('Stock Reconciliation', d)
    stock_doc.cancel()
```

## Next Steps


---

*Source: test_stock_reconciliation.py:160 | Complexity: Advanced | Last updated: 2026-02-04*