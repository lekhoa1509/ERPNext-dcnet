# How To: Auto Cancel Serial And Batch

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test auto cancel serial and batch

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
item_code = make_item(properties={'has_serial_no': 1, 'serial_no_series': 'ATC-TT-SER-VAL-.#####'}).name
```

### Step 2: Assign se = make_stock_entry(...)

```python
se = make_stock_entry(item_code=item_code, target='_Test Warehouse - _TC', qty=5, rate=500)
```

### Step 3: Assign bundle = value

```python
bundle = se.items[0].serial_and_batch_bundle
```

### Step 4: Assign docstatus = frappe.db.get_value(...)

```python
docstatus = frappe.db.get_value('Serial and Batch Bundle', bundle, 'docstatus')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(docstatus, 1)
```

### Step 6: Call se.cancel()

```python
se.cancel()
```

### Step 7: Assign docstatus = frappe.db.get_value(...)

```python
docstatus = frappe.db.get_value('Serial and Batch Bundle', bundle, 'docstatus')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(docstatus, 2)
```


## Complete Example

```python
# Workflow
item_code = make_item(properties={'has_serial_no': 1, 'serial_no_series': 'ATC-TT-SER-VAL-.#####'}).name
se = make_stock_entry(item_code=item_code, target='_Test Warehouse - _TC', qty=5, rate=500)
bundle = se.items[0].serial_and_batch_bundle
docstatus = frappe.db.get_value('Serial and Batch Bundle', bundle, 'docstatus')
self.assertEqual(docstatus, 1)
se.cancel()
docstatus = frappe.db.get_value('Serial and Batch Bundle', bundle, 'docstatus')
self.assertEqual(docstatus, 2)
```

## Next Steps


---

*Source: test_serial_and_batch_bundle.py:588 | Complexity: Advanced | Last updated: 2026-02-04*