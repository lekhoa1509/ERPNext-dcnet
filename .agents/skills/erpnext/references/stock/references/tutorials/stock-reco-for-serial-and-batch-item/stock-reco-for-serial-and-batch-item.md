# How To: Stock Reco For Serial And Batch Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test stock reco for serial and batch item

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

### Step 1: Assign item = create_item(...)

```python
item = create_item('_TestBatchSerialItemReco')
```

### Step 2: Assign item.has_batch_no = 1

```python
item.has_batch_no = 1
```

### Step 3: Assign item.create_new_batch = 1

```python
item.create_new_batch = 1
```

### Step 4: Assign item.has_serial_no = 1

```python
item.has_serial_no = 1
```

### Step 5: Assign item.batch_number_series = 'TBS-BATCH-.##'

```python
item.batch_number_series = 'TBS-BATCH-.##'
```

### Step 6: Assign item.serial_no_series = 'TBS-.####'

```python
item.serial_no_series = 'TBS-.####'
```

### Step 7: Call item.save()

```python
item.save()
```

### Step 8: Assign warehouse = '_Test Warehouse for Stock Reco2 - _TC'

```python
warehouse = '_Test Warehouse for Stock Reco2 - _TC'
```

### Step 9: Assign sr = create_stock_reconciliation(...)

```python
sr = create_stock_reconciliation(item_code=item.item_code, warehouse=warehouse, qty=1, rate=100)
```

### Step 10: Assign batch_no = get_batch_from_bundle(...)

```python
batch_no = get_batch_from_bundle(sr.items[0].serial_and_batch_bundle)
```

### Step 11: Assign serial_nos = get_serial_nos_from_bundle(...)

```python
serial_nos = get_serial_nos_from_bundle(sr.items[0].serial_and_batch_bundle)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(len(serial_nos), 1)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Serial No', serial_nos[0], 'batch_no'), batch_no)
```

### Step 14: Call sr.cancel()

```python
sr.cancel()
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Serial No', serial_nos[0], 'warehouse'), None)
```


## Complete Example

```python
# Workflow
item = create_item('_TestBatchSerialItemReco')
item.has_batch_no = 1
item.create_new_batch = 1
item.has_serial_no = 1
item.batch_number_series = 'TBS-BATCH-.##'
item.serial_no_series = 'TBS-.####'
item.save()
warehouse = '_Test Warehouse for Stock Reco2 - _TC'
sr = create_stock_reconciliation(item_code=item.item_code, warehouse=warehouse, qty=1, rate=100)
batch_no = get_batch_from_bundle(sr.items[0].serial_and_batch_bundle)
serial_nos = get_serial_nos_from_bundle(sr.items[0].serial_and_batch_bundle)
self.assertEqual(len(serial_nos), 1)
self.assertEqual(frappe.db.get_value('Serial No', serial_nos[0], 'batch_no'), batch_no)
sr.cancel()
self.assertEqual(frappe.db.get_value('Serial No', serial_nos[0], 'warehouse'), None)
```

## Next Steps


---

*Source: test_stock_reconciliation.py:275 | Complexity: Advanced | Last updated: 2026-02-04*