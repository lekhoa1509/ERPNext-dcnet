# How To: Item Type Field Change

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Check if critical fields like `is_stock_item`, `has_batch_no` are not changed if transactions exist.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `json`
- `frappe`
- `frappe.custom.doctype.property_setter.property_setter`
- `frappe.test_runner`
- `frappe.tests`
- `frappe.utils`
- `erpnext.controllers.item_variant`
- `erpnext.stock.doctype.item.item`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.get_item_details`
- `erpnext.assets.doctype.asset.test_asset`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `time`
- `erpnext.stock.stock_balance`
- `erpnext.stock.stock_ledger`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.dashboard.item_dashboard`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.controllers.queries`
- `erpnext.stock.doctype.warehouse.test_warehouse`

**Setup Required:**
```python
super().setUp()
frappe.flags.attribute_values = None
```

## Step-by-Step Guide

### Step 1: 'Check if critical fields like `is_stock_item`, `has_batch_no` are not changed if transactions exist.'

```python
'Check if critical fields like `is_stock_item`, `has_batch_no` are not changed if transactions exist.'
```

### Step 2: Assign transaction_creators = value

```python
transaction_creators = [lambda i: make_purchase_receipt(item_code=i), lambda i: make_purchase_invoice(item_code=i, update_stock=1), lambda i: make_stock_entry(item_code=i, qty=1, target='_Test Warehouse - _TC'), lambda i: create_delivery_note(item_code=i)]
```

### Step 3: Assign properties = value

```python
properties = {'has_batch_no': 0, 'allow_negative_stock': 1, 'valuation_rate': 10}
```

### Step 4: Assign item = make_item(...)

```python
item = make_item(properties=properties)
```

### Step 5: Assign transaction = transaction_creator(...)

```python
transaction = transaction_creator(item.name)
```

### Step 6: Assign item.has_batch_no = 1

```python
item.has_batch_no = 1
```

### Step 7: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, item.save)
```

### Step 8: Call transaction.cancel()

```python
transaction.cancel()
```

### Step 9: Call item.reload()

```python
item.reload()
```

### Step 10: Assign item.has_batch_no = 1

```python
item.has_batch_no = 1
```

### Step 11: Call item.save()

```python
item.save()
```


## Complete Example

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

# Workflow
'Check if critical fields like `is_stock_item`, `has_batch_no` are not changed if transactions exist.'
from erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice import make_purchase_invoice
from erpnext.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
from erpnext.stock.doctype.purchase_receipt.test_purchase_receipt import make_purchase_receipt
from erpnext.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry
transaction_creators = [lambda i: make_purchase_receipt(item_code=i), lambda i: make_purchase_invoice(item_code=i, update_stock=1), lambda i: make_stock_entry(item_code=i, qty=1, target='_Test Warehouse - _TC'), lambda i: create_delivery_note(item_code=i)]
properties = {'has_batch_no': 0, 'allow_negative_stock': 1, 'valuation_rate': 10}
for transaction_creator in transaction_creators:
    item = make_item(properties=properties)
    transaction = transaction_creator(item.name)
    item.has_batch_no = 1
    self.assertRaises(frappe.ValidationError, item.save)
    transaction.cancel()
    item.reload()
    item.has_batch_no = 1
    item.save()
```

## Next Steps


---

*Source: test_item.py:815 | Complexity: Advanced | Last updated: 2026-02-04*