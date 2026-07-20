# How To: Is Fixed Asset Set

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test is fixed asset set

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
asset = create_asset(is_existing_asset=1)
```

### Step 2: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc('Purchase Invoice')
```

### Step 3: Assign doc.company = '_Test Company'

```python
doc.company = '_Test Company'
```

### Step 4: Assign doc.supplier = '_Test Supplier'

```python
doc.supplier = '_Test Supplier'
```

### Step 5: Call doc.append()

```python
doc.append('items', {'item_code': 'Macbook Pro', 'qty': 1, 'asset': asset.name})
```

### Step 6: Call doc.set_missing_values()

```python
doc.set_missing_values()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(doc.items[0].is_fixed_asset, 1)
```


## Complete Example

```python
# Workflow
asset = create_asset(is_existing_asset=1)
doc = frappe.new_doc('Purchase Invoice')
doc.company = '_Test Company'
doc.supplier = '_Test Supplier'
doc.append('items', {'item_code': 'Macbook Pro', 'qty': 1, 'asset': asset.name})
doc.set_missing_values()
self.assertEqual(doc.items[0].is_fixed_asset, 1)
```

## Next Steps


---

*Source: test_asset.py:184 | Complexity: Intermediate | Last updated: 2026-02-04*