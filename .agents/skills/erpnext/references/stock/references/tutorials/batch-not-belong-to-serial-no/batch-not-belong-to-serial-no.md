# How To: Batch Not Belong To Serial No

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test batch not belong to serial no

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

### Step 1: Assign serial_and_batch_code = 'New Serial No Valuation 1'

```python
serial_and_batch_code = 'New Serial No Valuation 1'
```

### Step 2: Call make_item()

```python
make_item(serial_and_batch_code, {'has_serial_no': 1, 'serial_no_series': 'TEST-SER-VALL-.#####', 'is_stock_item': 1, 'has_batch_no': 1, 'create_new_batch': 1, 'batch_number_series': 'TEST-SNBAT-VAL-.#####'})
```

### Step 3: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code=serial_and_batch_code, warehouse='_Test Warehouse - _TC', qty=1, rate=500)
```

### Step 4: Assign serial_no = value

```python
serial_no = get_serial_nos_from_bundle(pr.items[0].serial_and_batch_bundle)[0]
```

### Step 5: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code=serial_and_batch_code, warehouse='_Test Warehouse - _TC', qty=1, rate=300)
```

### Step 6: Assign batch_no = get_batch_from_bundle(...)

```python
batch_no = get_batch_from_bundle(pr.items[0].serial_and_batch_bundle)
```

### Step 7: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc({'doctype': 'Serial and Batch Bundle', 'item_code': serial_and_batch_code, 'warehouse': '_Test Warehouse - _TC', 'voucher_type': 'Stock Entry', 'posting_date': today(), 'posting_time': nowtime(), 'qty': -1, 'type_of_transaction': 'Outward'})
```

### Step 8: Call doc.append()

```python
doc.append('entries', {'batch_no': batch_no, 'serial_no': serial_no, 'qty': -1})
```

### Step 9: Call self.assertRaises()

```python
self.assertRaises(frappe.exceptions.ValidationError, doc.save)
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.purchase_receipt.test_purchase_receipt import make_purchase_receipt
serial_and_batch_code = 'New Serial No Valuation 1'
make_item(serial_and_batch_code, {'has_serial_no': 1, 'serial_no_series': 'TEST-SER-VALL-.#####', 'is_stock_item': 1, 'has_batch_no': 1, 'create_new_batch': 1, 'batch_number_series': 'TEST-SNBAT-VAL-.#####'})
pr = make_purchase_receipt(item_code=serial_and_batch_code, warehouse='_Test Warehouse - _TC', qty=1, rate=500)
serial_no = get_serial_nos_from_bundle(pr.items[0].serial_and_batch_bundle)[0]
pr = make_purchase_receipt(item_code=serial_and_batch_code, warehouse='_Test Warehouse - _TC', qty=1, rate=300)
batch_no = get_batch_from_bundle(pr.items[0].serial_and_batch_bundle)
doc = frappe.get_doc({'doctype': 'Serial and Batch Bundle', 'item_code': serial_and_batch_code, 'warehouse': '_Test Warehouse - _TC', 'voucher_type': 'Stock Entry', 'posting_date': today(), 'posting_time': nowtime(), 'qty': -1, 'type_of_transaction': 'Outward'})
doc.append('entries', {'batch_no': batch_no, 'serial_no': serial_no, 'qty': -1})
self.assertRaises(frappe.exceptions.ValidationError, doc.save)
```

## Next Steps


---

*Source: test_serial_and_batch_bundle.py:445 | Complexity: Advanced | Last updated: 2026-02-04*