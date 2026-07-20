# How To: Total Batch Qty

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test total batch qty

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.exceptions`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.data`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.get_item_details`
- `erpnext.stock.serial_batch_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.batch.batch`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`


## Step-by-Step Guide

### Step 1: Call self.make_batch_item()

```python
self.make_batch_item('ITEM-BATCH-3')
```

### Step 2: Assign existing_batch_qty = flt(...)

```python
existing_batch_qty = flt(frappe.db.get_value('Batch', 'B100', 'batch_qty'))
```

### Step 3: Assign stock_entry = self.make_new_batch_and_entry(...)

```python
stock_entry = self.make_new_batch_and_entry('ITEM-BATCH-3', 'B100', '_Test Warehouse - _TC')
```

### Step 4: Assign current_batch_qty = flt(...)

```python
current_batch_qty = flt(frappe.db.get_value('Batch', 'B100', 'batch_qty'))
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(current_batch_qty, existing_batch_qty + 90)
```

### Step 6: Call stock_entry.cancel()

```python
stock_entry.cancel()
```

### Step 7: Assign current_batch_qty = flt(...)

```python
current_batch_qty = flt(frappe.db.get_value('Batch', 'B100', 'batch_qty'))
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(current_batch_qty, existing_batch_qty)
```


## Complete Example

```python
# Workflow
self.make_batch_item('ITEM-BATCH-3')
existing_batch_qty = flt(frappe.db.get_value('Batch', 'B100', 'batch_qty'))
stock_entry = self.make_new_batch_and_entry('ITEM-BATCH-3', 'B100', '_Test Warehouse - _TC')
current_batch_qty = flt(frappe.db.get_value('Batch', 'B100', 'batch_qty'))
self.assertEqual(current_batch_qty, existing_batch_qty + 90)
stock_entry.cancel()
current_batch_qty = flt(frappe.db.get_value('Batch', 'B100', 'batch_qty'))
self.assertEqual(current_batch_qty, existing_batch_qty)
```

## Next Steps


---

*Source: test_batch.py:347 | Complexity: Advanced | Last updated: 2026-02-04*