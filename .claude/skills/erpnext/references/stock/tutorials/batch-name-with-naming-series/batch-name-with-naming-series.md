# How To: Batch Name With Naming Series

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test batch name with naming series

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

### Step 1: Assign stock_settings = frappe.get_single(...)

```python
stock_settings = frappe.get_single('Stock Settings')
```

### Step 2: Assign use_naming_series = cint(...)

```python
use_naming_series = cint(stock_settings.use_naming_series)
```

### Step 3: Assign batch = self.make_new_batch(...)

```python
batch = self.make_new_batch('_Test Stock Item For Batch Test1')
```

### Step 4: Assign batch_name = value

```python
batch_name = batch.name
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(batch_name.startswith('BATCH-'))
```

### Step 6: Call batch.delete()

```python
batch.delete()
```

### Step 7: Assign batch = self.make_new_batch(...)

```python
batch = self.make_new_batch('_Test Stock Item For Batch Test2')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(batch_name, batch.name)
```

### Step 9: Call frappe.set_value()

```python
frappe.set_value('Stock Settings', 'Stock Settings', 'use_naming_series', 1)
```

### Step 10: Call frappe.set_value()

```python
frappe.set_value('Stock Settings', 'Stock Settings', 'use_naming_series', 0)
```


## Complete Example

```python
# Workflow
stock_settings = frappe.get_single('Stock Settings')
use_naming_series = cint(stock_settings.use_naming_series)
if not use_naming_series:
    frappe.set_value('Stock Settings', 'Stock Settings', 'use_naming_series', 1)
batch = self.make_new_batch('_Test Stock Item For Batch Test1')
batch_name = batch.name
self.assertTrue(batch_name.startswith('BATCH-'))
batch.delete()
batch = self.make_new_batch('_Test Stock Item For Batch Test2')
self.assertEqual(batch_name, batch.name)
if not use_naming_series:
    frappe.set_value('Stock Settings', 'Stock Settings', 'use_naming_series', 0)
```

## Next Steps


---

*Source: test_batch.py:406 | Complexity: Advanced | Last updated: 2026-02-04*