# How To: Autocreation Of Batches

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test if auto created Serial No excludes existing serial numbers

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

### Step 1: '\n\t\tTest if auto created Serial No excludes existing serial numbers\n\t\t'

```python
'\n\t\tTest if auto created Serial No excludes existing serial numbers\n\t\t'
```

### Step 2: Assign item_code = value

```python
item_code = make_item(properties={'has_batch_no': 1, 'batch_number_series': 'BATCHEXISTING.###', 'create_new_batch': 1}).name
```

### Step 3: Assign manually_created_batch = value

```python
manually_created_batch = self.make_new_batch(item_code, batch_id='BATCHEXISTING001').name
```

### Step 4: Assign pr_1 = make_purchase_receipt(...)

```python
pr_1 = make_purchase_receipt(item_code=item_code, qty=1, batch_no=manually_created_batch)
```

### Step 5: Assign pr_2 = make_purchase_receipt(...)

```python
pr_2 = make_purchase_receipt(item_code=item_code, qty=1)
```

### Step 6: Call pr_1.load_from_db()

```python
pr_1.load_from_db()
```

### Step 7: Call pr_2.load_from_db()

```python
pr_2.load_from_db()
```

### Step 8: Call self.assertNotEqual()

```python
self.assertNotEqual(get_batch_from_bundle(pr_1.items[0].serial_and_batch_bundle), get_batch_from_bundle(pr_2.items[0].serial_and_batch_bundle))
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual('BATCHEXISTING002', get_batch_from_bundle(pr_2.items[0].serial_and_batch_bundle))
```


## Complete Example

```python
# Workflow
'\n\t\tTest if auto created Serial No excludes existing serial numbers\n\t\t'
item_code = make_item(properties={'has_batch_no': 1, 'batch_number_series': 'BATCHEXISTING.###', 'create_new_batch': 1}).name
manually_created_batch = self.make_new_batch(item_code, batch_id='BATCHEXISTING001').name
pr_1 = make_purchase_receipt(item_code=item_code, qty=1, batch_no=manually_created_batch)
pr_2 = make_purchase_receipt(item_code=item_code, qty=1)
pr_1.load_from_db()
pr_2.load_from_db()
self.assertNotEqual(get_batch_from_bundle(pr_1.items[0].serial_and_batch_bundle), get_batch_from_bundle(pr_2.items[0].serial_and_batch_bundle))
self.assertEqual('BATCHEXISTING002', get_batch_from_bundle(pr_2.items[0].serial_and_batch_bundle))
```

## Next Steps


---

*Source: test_batch.py:553 | Complexity: Advanced | Last updated: 2026-02-04*