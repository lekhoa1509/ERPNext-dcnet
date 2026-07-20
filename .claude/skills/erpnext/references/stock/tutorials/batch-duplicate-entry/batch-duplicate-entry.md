# How To: Batch Duplicate Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test batch duplicate entry

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
item_code = make_item(properties={'has_batch_no': 1}).name
```

### Step 2: Assign batch_id = 'TEST-BATTCCH-VAL-00001'

```python
batch_id = 'TEST-BATTCCH-VAL-00001'
```

### Step 3: Assign batch_nos = value

```python
batch_nos = [{'batch_no': batch_id, 'qty': 1}]
```

### Step 4: Call make_batch_nos()

```python
make_batch_nos(item_code, batch_nos)
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('Batch', batch_id))
```

### Step 6: Assign use_batchwise_valuation = frappe.db.get_value(...)

```python
use_batchwise_valuation = frappe.db.get_value('Batch', batch_id, 'use_batchwise_valuation')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(use_batchwise_valuation, 1)
```

### Step 8: Assign batch_id = 'TEST-BATTCCH-VAL-00001'

```python
batch_id = 'TEST-BATTCCH-VAL-00001'
```

### Step 9: Assign batch_nos = value

```python
batch_nos = [{'batch_no': batch_id, 'qty': 1}]
```

### Step 10: Call make_batch_nos()

```python
make_batch_nos(item_code, batch_nos)
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('Batch', batch_id))
```


## Complete Example

```python
# Workflow
item_code = make_item(properties={'has_batch_no': 1}).name
batch_id = 'TEST-BATTCCH-VAL-00001'
batch_nos = [{'batch_no': batch_id, 'qty': 1}]
make_batch_nos(item_code, batch_nos)
self.assertTrue(frappe.db.exists('Batch', batch_id))
use_batchwise_valuation = frappe.db.get_value('Batch', batch_id, 'use_batchwise_valuation')
self.assertEqual(use_batchwise_valuation, 1)
batch_id = 'TEST-BATTCCH-VAL-00001'
batch_nos = [{'batch_no': batch_id, 'qty': 1}]
make_batch_nos(item_code, batch_nos)
self.assertTrue(frappe.db.exists('Batch', batch_id))
```

## Next Steps


---

*Source: test_serial_and_batch_bundle.py:608 | Complexity: Advanced | Last updated: 2026-02-04*