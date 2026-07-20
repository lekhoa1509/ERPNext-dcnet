# How To: Check Stock Uom With Bin No Sle

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test check stock uom with bin no sle

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

### Step 1: Assign item = create_item(...)

```python
item = create_item('_Item with bin qty')
```

### Step 2: Assign item.stock_uom = 'Gram'

```python
item.stock_uom = 'Gram'
```

### Step 3: Call item.save()

```python
item.save()
```

### Step 4: Call update_bin_qty()

```python
update_bin_qty(item.item_code, '_Test Warehouse - _TC', {'reserved_qty': 10})
```

### Step 5: Assign item.stock_uom = 'Kilometer'

```python
item.stock_uom = 'Kilometer'
```

### Step 6: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, item.save)
```

### Step 7: Call update_bin_qty()

```python
update_bin_qty(item.item_code, '_Test Warehouse - _TC', {'reserved_qty': 0})
```

### Step 8: Call item.load_from_db()

```python
item.load_from_db()
```

### Step 9: Assign item.stock_uom = 'Kilometer'

```python
item.stock_uom = 'Kilometer'
```

### Step 10: Call item.save()

```python
item.save()
```

### Step 11: Call self.fail()

```python
self.fail(f'UoM change not allowed even though no SLE / BIN with positive qty exists: {e}')
```


## Complete Example

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

# Workflow
from erpnext.stock.stock_balance import update_bin_qty
item = create_item('_Item with bin qty')
item.stock_uom = 'Gram'
item.save()
update_bin_qty(item.item_code, '_Test Warehouse - _TC', {'reserved_qty': 10})
item.stock_uom = 'Kilometer'
self.assertRaises(frappe.ValidationError, item.save)
update_bin_qty(item.item_code, '_Test Warehouse - _TC', {'reserved_qty': 0})
item.load_from_db()
item.stock_uom = 'Kilometer'
try:
    item.save()
except frappe.ValidationError as e:
    self.fail(f'UoM change not allowed even though no SLE / BIN with positive qty exists: {e}')
```

## Next Steps


---

*Source: test_item.py:705 | Complexity: Advanced | Last updated: 2026-02-04*