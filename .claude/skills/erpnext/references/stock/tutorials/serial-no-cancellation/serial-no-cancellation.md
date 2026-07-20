# How To: Serial No Cancellation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test serial no cancellation

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
item = create_item('Stock-Reco-Serial-Item-9', is_stock_item=1)
```

### Step 2: Assign item_code = value

```python
item_code = item.name
```

### Step 3: Assign warehouse = '_Test Warehouse - _TC'

```python
warehouse = '_Test Warehouse - _TC'
```

### Step 4: Assign se1 = make_stock_entry(...)

```python
se1 = make_stock_entry(item_code=item_code, target=warehouse, qty=10, basic_rate=700)
```

### Step 5: Assign serial_nos = get_serial_nos_from_bundle(...)

```python
serial_nos = get_serial_nos_from_bundle(se1.items[0].serial_and_batch_bundle)
```

### Step 6: Call serial_nos.pop()

```python
serial_nos.pop()
```

### Step 7: Assign new_serial_nos = serial_nos

```python
new_serial_nos = serial_nos
```

### Step 8: Assign sr = create_stock_reconciliation(...)

```python
sr = create_stock_reconciliation(item_code=item.name, warehouse=warehouse, serial_no=new_serial_nos, qty=9)
```

### Step 9: Call sr.cancel()

```python
sr.cancel()
```

### Step 10: Assign active_sr_no = frappe.get_all(...)

```python
active_sr_no = frappe.get_all('Serial No', filters={'item_code': item_code, 'warehouse': warehouse, 'status': 'Active'})
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(len(active_sr_no), 10)
```

### Step 12: Assign item.has_serial_no = 1

```python
item.has_serial_no = 1
```

### Step 13: Assign item.serial_no_series = 'PSRS9.####'

```python
item.serial_no_series = 'PSRS9.####'
```

### Step 14: Call item.save()

```python
item.save()
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.stock_entry.test_stock_entry import make_stock_entry
item = create_item('Stock-Reco-Serial-Item-9', is_stock_item=1)
if not item.has_serial_no:
    item.has_serial_no = 1
    item.serial_no_series = 'PSRS9.####'
    item.save()
item_code = item.name
warehouse = '_Test Warehouse - _TC'
se1 = make_stock_entry(item_code=item_code, target=warehouse, qty=10, basic_rate=700)
serial_nos = get_serial_nos_from_bundle(se1.items[0].serial_and_batch_bundle)
serial_nos.pop()
new_serial_nos = serial_nos
sr = create_stock_reconciliation(item_code=item.name, warehouse=warehouse, serial_no=new_serial_nos, qty=9)
sr.cancel()
active_sr_no = frappe.get_all('Serial No', filters={'item_code': item_code, 'warehouse': warehouse, 'status': 'Active'})
self.assertEqual(len(active_sr_no), 10)
```

## Next Steps


---

*Source: test_stock_reconciliation.py:579 | Complexity: Advanced | Last updated: 2026-02-04*