# How To: Validate Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test validate item

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.data`
- `erpnext.accounts.doctype.journal_entry.test_journal_entry`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.assets.doctype.asset.asset`
- `erpnext.assets.doctype.asset.depreciation`
- `erpnext.assets.doctype.asset_depreciation_schedule.asset_depreciation_schedule`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.assets.doctype.asset_capitalization.test_asset_capitalization`


## Step-by-Step Guide

### Step 1: Assign asset = create_asset(...)

```python
asset = create_asset(item_code='MacBook Pro', do_not_save=1)
```

### Step 2: Assign item = frappe.get_doc(...)

```python
item = frappe.get_doc('Item', 'MacBook Pro')
```

### Step 3: Assign item.disabled = 1

```python
item.disabled = 1
```

### Step 4: Call item.save()

```python
item.save()
```

### Step 5: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, asset.save)
```

### Step 6: Assign item.disabled = 0

```python
item.disabled = 0
```

### Step 7: Assign item.is_fixed_asset = 0

```python
item.is_fixed_asset = 0
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, asset.save)
```

### Step 9: Assign item.is_fixed_asset = 1

```python
item.is_fixed_asset = 1
```

### Step 10: Assign item.is_stock_item = 1

```python
item.is_stock_item = 1
```

### Step 11: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, asset.save)
```


## Complete Example

```python
# Workflow
asset = create_asset(item_code='MacBook Pro', do_not_save=1)
item = frappe.get_doc('Item', 'MacBook Pro')
item.disabled = 1
item.save()
self.assertRaises(frappe.ValidationError, asset.save)
item.disabled = 0
item.is_fixed_asset = 0
self.assertRaises(frappe.ValidationError, asset.save)
item.is_fixed_asset = 1
item.is_stock_item = 1
self.assertRaises(frappe.ValidationError, asset.save)
```

## Next Steps


---

*Source: test_asset.py:93 | Complexity: Advanced | Last updated: 2026-02-04*