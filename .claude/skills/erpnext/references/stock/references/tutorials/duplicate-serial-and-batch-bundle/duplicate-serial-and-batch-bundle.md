# How To: Duplicate Serial And Batch Bundle

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test duplicate serial and batch bundle

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
item_code = make_item(properties={'is_stock_item': 1, 'has_serial_no': 1}).name
```

### Step 2: Assign serial_no = value

```python
serial_no = f'{item_code}-001'
```

### Step 3: Assign serial_nos = value

```python
serial_nos = [{'serial_no': serial_no, 'qty': 1}]
```

### Step 4: Call make_serial_nos()

```python
make_serial_nos(item_code, serial_nos)
```

### Step 5: Assign pr1 = make_purchase_receipt(...)

```python
pr1 = make_purchase_receipt(item=item_code, qty=1, rate=500, serial_no=[serial_no])
```

### Step 6: Assign pr2 = make_purchase_receipt(...)

```python
pr2 = make_purchase_receipt(item=item_code, qty=1, rate=500, do_not_save=True)
```

### Step 7: Call pr1.reload()

```python
pr1.reload()
```

### Step 8: Assign unknown.serial_and_batch_bundle = value

```python
pr2.items[0].serial_and_batch_bundle = pr1.items[0].serial_and_batch_bundle
```

### Step 9: Call self.assertRaises()

```python
self.assertRaises(frappe.exceptions.ValidationError, pr2.save)
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.purchase_receipt.test_purchase_receipt import make_purchase_receipt
item_code = make_item(properties={'is_stock_item': 1, 'has_serial_no': 1}).name
serial_no = f'{item_code}-001'
serial_nos = [{'serial_no': serial_no, 'qty': 1}]
make_serial_nos(item_code, serial_nos)
pr1 = make_purchase_receipt(item=item_code, qty=1, rate=500, serial_no=[serial_no])
pr2 = make_purchase_receipt(item=item_code, qty=1, rate=500, do_not_save=True)
pr1.reload()
pr2.items[0].serial_and_batch_bundle = pr1.items[0].serial_and_batch_bundle
self.assertRaises(frappe.exceptions.ValidationError, pr2.save)
```

## Next Steps


---

*Source: test_serial_and_batch_bundle.py:645 | Complexity: Advanced | Last updated: 2026-02-04*