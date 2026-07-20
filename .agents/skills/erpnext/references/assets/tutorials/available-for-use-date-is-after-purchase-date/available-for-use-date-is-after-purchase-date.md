# How To: Available For Use Date Is After Purchase Date

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test available for use date is after purchase date

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
asset = create_asset(item_code='Macbook Pro', calculate_depreciation=1, do_not_save=1)
```

### Step 2: Assign asset.is_existing_asset = 0

```python
asset.is_existing_asset = 0
```

### Step 3: Assign asset.purchase_date = getdate(...)

```python
asset.purchase_date = getdate('2021-10-10')
```

### Step 4: Assign asset.available_for_use_date = getdate(...)

```python
asset.available_for_use_date = getdate('2021-10-1')
```

### Step 5: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, asset.save)
```


## Complete Example

```python
# Workflow
asset = create_asset(item_code='Macbook Pro', calculate_depreciation=1, do_not_save=1)
asset.is_existing_asset = 0
asset.purchase_date = getdate('2021-10-10')
asset.available_for_use_date = getdate('2021-10-1')
self.assertRaises(frappe.ValidationError, asset.save)
```

## Next Steps


---

*Source: test_asset.py:80 | Complexity: Intermediate | Last updated: 2026-02-04*