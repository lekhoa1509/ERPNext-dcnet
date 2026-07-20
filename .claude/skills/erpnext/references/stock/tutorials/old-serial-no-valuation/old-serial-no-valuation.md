# How To: Old Serial No Valuation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test old serial no valuation

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

### Step 1: Assign serial_no_item_code = 'Old Serial No Item Valuation 1'

```python
serial_no_item_code = 'Old Serial No Item Valuation 1'
```

### Step 2: Call make_item()

```python
make_item(serial_no_item_code, {'has_serial_no': 1, 'serial_no_series': 'TEST-SER-VALL-.#####', 'is_stock_item': 1})
```

### Step 3: Call make_purchase_receipt()

```python
make_purchase_receipt(item_code=serial_no_item_code, warehouse='_Test Warehouse - _TC', qty=1, rate=500)
```

### Step 4: Assign frappe.flags.ignore_serial_batch_bundle_validation = True

```python
frappe.flags.ignore_serial_batch_bundle_validation = True
```

### Step 5: Assign frappe.flags.use_serial_and_batch_fields = True

```python
frappe.flags.use_serial_and_batch_fields = True
```

### Step 6: Assign serial_no_id = 'Old Serial No 1'

```python
serial_no_id = 'Old Serial No 1'
```

### Step 7: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc({'doctype': 'Stock Ledger Entry', 'posting_date': today(), 'posting_time': nowtime(), 'serial_no': serial_no_id, 'incoming_rate': 100, 'qty_after_transaction': 1, 'stock_value_difference': 100, 'balance_value': 100, 'valuation_rate': 100, 'actual_qty': 1, 'item_code': serial_no_item_code, 'warehouse': '_Test Warehouse - _TC', 'company': '_Test Company'})
```

### Step 8: Assign doc.flags.ignore_permissions = True

```python
doc.flags.ignore_permissions = True
```

### Step 9: Assign doc.flags.ignore_mandatory = True

```python
doc.flags.ignore_mandatory = True
```

### Step 10: Assign doc.flags.ignore_links = True

```python
doc.flags.ignore_links = True
```

### Step 11: Assign doc.flags.ignore_validate = True

```python
doc.flags.ignore_validate = True
```

### Step 12: Call doc.submit()

```python
doc.submit()
```

### Step 13: Assign bundle_doc = make_serial_batch_bundle(...)

```python
bundle_doc = make_serial_batch_bundle({'item_code': serial_no_item_code, 'warehouse': '_Test Warehouse - _TC', 'voucher_type': 'Stock Entry', 'posting_date': today(), 'posting_time': nowtime(), 'qty': -1, 'serial_nos': [serial_no_id], 'type_of_transaction': 'Outward', 'do_not_submit': True})
```

### Step 14: Call bundle_doc.reload()

```python
bundle_doc.reload()
```

### Step 15: Assign frappe.flags.ignore_serial_batch_bundle_validation = False

```python
frappe.flags.ignore_serial_batch_bundle_validation = False
```

### Step 16: Assign frappe.flags.use_serial_and_batch_fields = False

```python
frappe.flags.use_serial_and_batch_fields = False
```

### Step 17: Assign sn_doc = frappe.get_doc.insert(...)

```python
sn_doc = frappe.get_doc({'doctype': 'Serial No', 'serial_no': serial_no_id, 'item_code': serial_no_item_code, 'company': '_Test Company'}).insert(ignore_permissions=True)
```

### Step 18: Call sn_doc.db_set()

```python
sn_doc.db_set({'warehouse': '_Test Warehouse - _TC', 'purchase_rate': 100})
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(flt(row.stock_value_difference, 2), -100.0)
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.purchase_receipt.test_purchase_receipt import make_purchase_receipt
serial_no_item_code = 'Old Serial No Item Valuation 1'
make_item(serial_no_item_code, {'has_serial_no': 1, 'serial_no_series': 'TEST-SER-VALL-.#####', 'is_stock_item': 1})
make_purchase_receipt(item_code=serial_no_item_code, warehouse='_Test Warehouse - _TC', qty=1, rate=500)
frappe.flags.ignore_serial_batch_bundle_validation = True
frappe.flags.use_serial_and_batch_fields = True
serial_no_id = 'Old Serial No 1'
if not frappe.db.exists('Serial No', serial_no_id):
    sn_doc = frappe.get_doc({'doctype': 'Serial No', 'serial_no': serial_no_id, 'item_code': serial_no_item_code, 'company': '_Test Company'}).insert(ignore_permissions=True)
    sn_doc.db_set({'warehouse': '_Test Warehouse - _TC', 'purchase_rate': 100})
doc = frappe.get_doc({'doctype': 'Stock Ledger Entry', 'posting_date': today(), 'posting_time': nowtime(), 'serial_no': serial_no_id, 'incoming_rate': 100, 'qty_after_transaction': 1, 'stock_value_difference': 100, 'balance_value': 100, 'valuation_rate': 100, 'actual_qty': 1, 'item_code': serial_no_item_code, 'warehouse': '_Test Warehouse - _TC', 'company': '_Test Company'})
doc.flags.ignore_permissions = True
doc.flags.ignore_mandatory = True
doc.flags.ignore_links = True
doc.flags.ignore_validate = True
doc.submit()
bundle_doc = make_serial_batch_bundle({'item_code': serial_no_item_code, 'warehouse': '_Test Warehouse - _TC', 'voucher_type': 'Stock Entry', 'posting_date': today(), 'posting_time': nowtime(), 'qty': -1, 'serial_nos': [serial_no_id], 'type_of_transaction': 'Outward', 'do_not_submit': True})
bundle_doc.reload()
for row in bundle_doc.entries:
    self.assertEqual(flt(row.stock_value_difference, 2), -100.0)
frappe.flags.ignore_serial_batch_bundle_validation = False
frappe.flags.use_serial_and_batch_fields = False
```

## Next Steps


---

*Source: test_serial_and_batch_bundle.py:362 | Complexity: Advanced | Last updated: 2026-02-04*