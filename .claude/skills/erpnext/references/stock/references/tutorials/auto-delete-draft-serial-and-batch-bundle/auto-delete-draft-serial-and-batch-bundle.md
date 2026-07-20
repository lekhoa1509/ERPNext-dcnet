# How To: Auto Delete Draft Serial And Batch Bundle

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test auto delete draft serial and batch bundle

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

### Step 1: Assign serial_and_batch_code = 'New Serial No Auto Delete 1'

```python
serial_and_batch_code = 'New Serial No Auto Delete 1'
```

### Step 2: Call make_item()

```python
make_item(serial_and_batch_code, {'has_serial_no': 1, 'serial_no_series': 'TEST-SER-VALL-.#####', 'is_stock_item': 1})
```

### Step 3: Assign ste = make_stock_entry(...)

```python
ste = make_stock_entry(item_code=serial_and_batch_code, target='_Test Warehouse - _TC', qty=1, rate=500, do_not_submit=True)
```

### Step 4: Assign serial_no = 'SN-TEST-AUTO-DEL'

```python
serial_no = 'SN-TEST-AUTO-DEL'
```

### Step 5: Assign bundle_doc = make_serial_batch_bundle(...)

```python
bundle_doc = make_serial_batch_bundle({'item_code': serial_and_batch_code, 'warehouse': '_Test Warehouse - _TC', 'voucher_type': 'Stock Entry', 'posting_date': ste.posting_date, 'posting_time': ste.posting_time, 'qty': 1, 'serial_nos': [serial_no], 'type_of_transaction': 'Inward', 'do_not_submit': True})
```

### Step 6: Call bundle_doc.reload()

```python
bundle_doc.reload()
```

### Step 7: Assign unknown.serial_and_batch_bundle = value

```python
ste.items[0].serial_and_batch_bundle = bundle_doc.name
```

### Step 8: Call ste.save()

```python
ste.save()
```

### Step 9: Call ste.reload()

```python
ste.reload()
```

### Step 10: Call ste.delete()

```python
ste.delete()
```

### Step 11: Call self.assertFalse()

```python
self.assertFalse(frappe.db.exists('Serial and Batch Bundle', bundle_doc.name))
```

### Step 12: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'Serial No', 'serial_no': serial_no, 'item_code': serial_and_batch_code, 'company': '_Test Company'}).insert(ignore_permissions=True)
```


## Complete Example

```python
# Workflow
serial_and_batch_code = 'New Serial No Auto Delete 1'
make_item(serial_and_batch_code, {'has_serial_no': 1, 'serial_no_series': 'TEST-SER-VALL-.#####', 'is_stock_item': 1})
ste = make_stock_entry(item_code=serial_and_batch_code, target='_Test Warehouse - _TC', qty=1, rate=500, do_not_submit=True)
serial_no = 'SN-TEST-AUTO-DEL'
if not frappe.db.exists('Serial No', serial_no):
    frappe.get_doc({'doctype': 'Serial No', 'serial_no': serial_no, 'item_code': serial_and_batch_code, 'company': '_Test Company'}).insert(ignore_permissions=True)
bundle_doc = make_serial_batch_bundle({'item_code': serial_and_batch_code, 'warehouse': '_Test Warehouse - _TC', 'voucher_type': 'Stock Entry', 'posting_date': ste.posting_date, 'posting_time': ste.posting_time, 'qty': 1, 'serial_nos': [serial_no], 'type_of_transaction': 'Inward', 'do_not_submit': True})
bundle_doc.reload()
ste.items[0].serial_and_batch_bundle = bundle_doc.name
ste.save()
ste.reload()
ste.delete()
self.assertFalse(frappe.db.exists('Serial and Batch Bundle', bundle_doc.name))
```

## Next Steps


---

*Source: test_serial_and_batch_bundle.py:498 | Complexity: Advanced | Last updated: 2026-02-04*