# How To: Serial No Duplicate Entry

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test serial no duplicate entry

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

### Step 1: Assign item_code = value

```python
item_code = make_item(properties={'has_serial_no': 1}).name
```

### Step 2: Assign serial_no_id = 'TEST-SNID-VAL-00001'

```python
serial_no_id = 'TEST-SNID-VAL-00001'
```

### Step 3: Assign serial_nos = value

```python
serial_nos = [{'serial_no': serial_no_id, 'qty': 1}]
```

### Step 4: Call make_serial_nos()

```python
make_serial_nos(item_code, serial_nos)
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('Serial No', serial_no_id))
```

### Step 6: Assign serial_no_id = 'TEST-SNID-VAL-00001'

```python
serial_no_id = 'TEST-SNID-VAL-00001'
```

### Step 7: Assign serial_nos = value

```python
serial_nos = [{'batch_no': serial_no_id, 'qty': 1}]
```

### Step 8: Call make_serial_nos()

```python
make_serial_nos(item_code, serial_nos)
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('Serial No', serial_no_id))
```


## Complete Example

```python
# Workflow
item_code = make_item(properties={'has_serial_no': 1}).name
serial_no_id = 'TEST-SNID-VAL-00001'
serial_nos = [{'serial_no': serial_no_id, 'qty': 1}]
make_serial_nos(item_code, serial_nos)
self.assertTrue(frappe.db.exists('Serial No', serial_no_id))
serial_no_id = 'TEST-SNID-VAL-00001'
serial_nos = [{'batch_no': serial_no_id, 'qty': 1}]
make_serial_nos(item_code, serial_nos)
self.assertTrue(frappe.db.exists('Serial No', serial_no_id))
```

## Next Steps


---

*Source: test_serial_and_batch_bundle.py:626 | Complexity: Advanced | Last updated: 2026-02-04*