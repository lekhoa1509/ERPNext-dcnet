# How To: Serial And Batch Bundle Company

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test serial and batch bundle company

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.serial_batch_bundle`
- `erpnext.stock.serial_batch_bundle`
- `erpnext.stock.serial_batch_bundle`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`


## Step-by-Step Guide

### Step 1: Assign item = value

```python
item = make_item('Test Serial and Batch Bundle Company Item', properties={'has_serial_no': 1, 'serial_no_series': 'TT-SER-VAL-.#####'}).name
```

### Step 2: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code=item, warehouse='_Test Warehouse - _TC', qty=3, rate=500, do_not_submit=True)
```

### Step 3: Assign entries = value

```python
entries = []
```

### Step 4: Assign item_row = value

```python
item_row = pr.items[0]
```

### Step 5: Assign item_row.type_of_transaction = 'Inward'

```python
item_row.type_of_transaction = 'Inward'
```

### Step 6: Assign item_row.is_rejected = 0

```python
item_row.is_rejected = 0
```

### Step 7: Assign sn_doc = add_serial_batch_ledgers(...)

```python
sn_doc = add_serial_batch_ledgers(entries, item_row, pr, '_Test Warehouse - _TC')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(sn_doc.company, '_Test Company')
```

### Step 9: Call entries.append()

```python
entries.append(frappe._dict({'serial_no': serial_no, 'qty': 1}))
```

### Step 10: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'Serial No', 'serial_no': serial_no, 'item_code': item}).insert(ignore_permissions=True)
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.purchase_receipt.test_purchase_receipt import make_purchase_receipt
item = make_item('Test Serial and Batch Bundle Company Item', properties={'has_serial_no': 1, 'serial_no_series': 'TT-SER-VAL-.#####'}).name
pr = make_purchase_receipt(item_code=item, warehouse='_Test Warehouse - _TC', qty=3, rate=500, do_not_submit=True)
entries = []
for serial_no in ['TT-SER-VAL-00001', 'TT-SER-VAL-00002', 'TT-SER-VAL-00003']:
    entries.append(frappe._dict({'serial_no': serial_no, 'qty': 1}))
    if not frappe.db.exists('Serial No', serial_no):
        frappe.get_doc({'doctype': 'Serial No', 'serial_no': serial_no, 'item_code': item}).insert(ignore_permissions=True)
item_row = pr.items[0]
item_row.type_of_transaction = 'Inward'
item_row.is_rejected = 0
sn_doc = add_serial_batch_ledgers(entries, item_row, pr, '_Test Warehouse - _TC')
self.assertEqual(sn_doc.company, '_Test Company')
```

## Next Steps


---

*Source: test_serial_and_batch_bundle.py:550 | Complexity: Advanced | Last updated: 2026-02-04*