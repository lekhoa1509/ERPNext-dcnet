# How To: Update Batch Properties

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test update batch properties

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

### Step 1: Assign item_code = '_TestBatchWiseVal'

```python
item_code = '_TestBatchWiseVal'
```

### Step 2: Call self.make_batch_item()

```python
self.make_batch_item(item_code)
```

### Step 3: Assign se = make_stock_entry(...)

```python
se = make_stock_entry(item_code=item_code, qty=100, rate=10, target='_Test Warehouse - _TC')
```

### Step 4: Assign batch_no = get_batch_from_bundle(...)

```python
batch_no = get_batch_from_bundle(se.items[0].serial_and_batch_bundle)
```

### Step 5: Assign batch = frappe.get_doc(...)

```python
batch = frappe.get_doc('Batch', batch_no)
```

### Step 6: Assign expiry_date = add_to_date(...)

```python
expiry_date = add_to_date(batch.manufacturing_date, days=30)
```

### Step 7: Assign batch.expiry_date = expiry_date

```python
batch.expiry_date = expiry_date
```

### Step 8: Call batch.save()

```python
batch.save()
```

### Step 9: Call batch.reload()

```python
batch.reload()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(getdate(batch.expiry_date), getdate(expiry_date))
```


## Complete Example

```python
# Workflow
item_code = '_TestBatchWiseVal'
self.make_batch_item(item_code)
se = make_stock_entry(item_code=item_code, qty=100, rate=10, target='_Test Warehouse - _TC')
batch_no = get_batch_from_bundle(se.items[0].serial_and_batch_bundle)
batch = frappe.get_doc('Batch', batch_no)
expiry_date = add_to_date(batch.manufacturing_date, days=30)
batch.expiry_date = expiry_date
batch.save()
batch.reload()
self.assertEqual(getdate(batch.expiry_date), getdate(expiry_date))
```

## Next Steps


---

*Source: test_batch.py:536 | Complexity: Advanced | Last updated: 2026-02-04*