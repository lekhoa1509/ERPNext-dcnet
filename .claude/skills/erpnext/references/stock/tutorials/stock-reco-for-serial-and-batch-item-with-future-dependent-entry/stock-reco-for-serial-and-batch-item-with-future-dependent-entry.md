# How To: Stock Reco For Serial And Batch Item With Future Dependent Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Behaviour: 1) Create Stock Reconciliation, which will be the origin document
of a new batch having a serial no
2) Create a Stock Entry that adds a serial no to the same batch following this
Stock Reconciliation
3) Cancel Stock Entry
Expected Result: 3) Serial No only in the Stock Entry is Inactive and Batch qty decreases

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

### Step 1: '\n\t\tBehaviour: 1) Create Stock Reconciliation, which will be the origin document\n\t\tof a new batch having a serial no\n\t\t2) Create a Stock Entry that adds a serial no to the same batch following this\n\t\tStock Reconciliation\n\t\t3) Cancel Stock Entry\n\t\tExpected Result: 3) Serial No only in the Stock Entry is Inactive and Batch qty decreases\n\t\t'

```python
'\n\t\tBehaviour: 1) Create Stock Reconciliation, which will be the origin document\n\t\tof a new batch having a serial no\n\t\t2) Create a Stock Entry that adds a serial no to the same batch following this\n\t\tStock Reconciliation\n\t\t3) Cancel Stock Entry\n\t\tExpected Result: 3) Serial No only in the Stock Entry is Inactive and Batch qty decreases\n\t\t'
```

### Step 2: Assign item = create_item(...)

```python
item = create_item('_TestBatchSerialItemDependentReco')
```

### Step 3: Assign item.has_batch_no = 1

```python
item.has_batch_no = 1
```

### Step 4: Assign item.create_new_batch = 1

```python
item.create_new_batch = 1
```

### Step 5: Assign item.has_serial_no = 1

```python
item.has_serial_no = 1
```

### Step 6: Assign item.batch_number_series = 'TBSD-BATCH-.##'

```python
item.batch_number_series = 'TBSD-BATCH-.##'
```

### Step 7: Assign item.serial_no_series = 'TBSD-.####'

```python
item.serial_no_series = 'TBSD-.####'
```

### Step 8: Call item.save()

```python
item.save()
```

### Step 9: Assign warehouse = '_Test Warehouse for Stock Reco2 - _TC'

```python
warehouse = '_Test Warehouse for Stock Reco2 - _TC'
```

### Step 10: Assign stock_reco = create_stock_reconciliation(...)

```python
stock_reco = create_stock_reconciliation(item_code=item.item_code, warehouse=warehouse, qty=1, rate=100)
```

### Step 11: Assign batch_no = get_batch_from_bundle(...)

```python
batch_no = get_batch_from_bundle(stock_reco.items[0].serial_and_batch_bundle)
```

### Step 12: Assign reco_serial_no = value

```python
reco_serial_no = get_serial_nos_from_bundle(stock_reco.items[0].serial_and_batch_bundle)[0]
```

### Step 13: Assign stock_entry = make_stock_entry(...)

```python
stock_entry = make_stock_entry(item_code=item.item_code, target=warehouse, qty=1, basic_rate=100, batch_no=batch_no)
```

### Step 14: Assign serial_no_2 = value

```python
serial_no_2 = get_serial_nos_from_bundle(stock_entry.items[0].serial_and_batch_bundle)[0]
```

### Step 15: Assign batch_qty = get_batch_qty(...)

```python
batch_qty = get_batch_qty(batch_no, warehouse, item.item_code)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(batch_qty, 2)
```

### Step 17: Call stock_entry.cancel()

```python
stock_entry.cancel()
```

### Step 18: Assign batch_qty = get_batch_qty(...)

```python
batch_qty = get_batch_qty(batch_no, warehouse, item.item_code)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(batch_qty, 1)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Serial No', reco_serial_no, 'batch_no'), batch_no)
```

### Step 21: Call self.assertTrue()

```python
self.assertTrue(frappe.db.get_value('Serial No', reco_serial_no, 'warehouse'))
```

### Step 22: Call self.assertFalse()

```python
self.assertFalse(frappe.db.get_value('Serial No', serial_no_2, 'warehouse'))
```

### Step 23: Call stock_reco.cancel()

```python
stock_reco.cancel()
```


## Complete Example

```python
# Workflow
'\n\t\tBehaviour: 1) Create Stock Reconciliation, which will be the origin document\n\t\tof a new batch having a serial no\n\t\t2) Create a Stock Entry that adds a serial no to the same batch following this\n\t\tStock Reconciliation\n\t\t3) Cancel Stock Entry\n\t\tExpected Result: 3) Serial No only in the Stock Entry is Inactive and Batch qty decreases\n\t\t'
from erpnext.stock.doctype.batch.batch import get_batch_qty
from erpnext.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry
item = create_item('_TestBatchSerialItemDependentReco')
item.has_batch_no = 1
item.create_new_batch = 1
item.has_serial_no = 1
item.batch_number_series = 'TBSD-BATCH-.##'
item.serial_no_series = 'TBSD-.####'
item.save()
warehouse = '_Test Warehouse for Stock Reco2 - _TC'
stock_reco = create_stock_reconciliation(item_code=item.item_code, warehouse=warehouse, qty=1, rate=100)
batch_no = get_batch_from_bundle(stock_reco.items[0].serial_and_batch_bundle)
reco_serial_no = get_serial_nos_from_bundle(stock_reco.items[0].serial_and_batch_bundle)[0]
stock_entry = make_stock_entry(item_code=item.item_code, target=warehouse, qty=1, basic_rate=100, batch_no=batch_no)
serial_no_2 = get_serial_nos_from_bundle(stock_entry.items[0].serial_and_batch_bundle)[0]
batch_qty = get_batch_qty(batch_no, warehouse, item.item_code)
self.assertEqual(batch_qty, 2)
stock_entry.cancel()
batch_qty = get_batch_qty(batch_no, warehouse, item.item_code)
self.assertEqual(batch_qty, 1)
self.assertEqual(frappe.db.get_value('Serial No', reco_serial_no, 'batch_no'), batch_no)
self.assertTrue(frappe.db.get_value('Serial No', reco_serial_no, 'warehouse'))
self.assertFalse(frappe.db.get_value('Serial No', serial_no_2, 'warehouse'))
stock_reco.cancel()
```

## Next Steps


---

*Source: test_stock_reconciliation.py:298 | Complexity: Advanced | Last updated: 2026-02-04*