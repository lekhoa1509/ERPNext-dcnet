# How To: Purchase Of Grouped Asset

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test purchase of grouped asset

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

### Step 1: Call create_fixed_asset_item()

```python
create_fixed_asset_item('Rack', is_grouped_asset=1)
```

### Step 2: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code='Rack', qty=3, rate=100000.0, location='Test Location')
```

### Step 3: Assign asset_name = frappe.db.get_value(...)

```python
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
```

### Step 4: Assign asset = frappe.get_doc(...)

```python
asset = frappe.get_doc('Asset', asset_name)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(asset.asset_quantity, 3)
```

### Step 6: Assign asset.calculate_depreciation = 1

```python
asset.calculate_depreciation = 1
```

### Step 7: Assign month_end_date = get_last_day(...)

```python
month_end_date = get_last_day(nowdate())
```

### Step 8: Assign purchase_date = value

```python
purchase_date = nowdate() if nowdate() != month_end_date else add_days(nowdate(), -15)
```

### Step 9: Assign asset.available_for_use_date = purchase_date

```python
asset.available_for_use_date = purchase_date
```

### Step 10: Assign asset.purchase_date = purchase_date

```python
asset.purchase_date = purchase_date
```

### Step 11: Call asset.append()

```python
asset.append('finance_books', {'expected_value_after_useful_life': 10000, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10, 'depreciation_start_date': month_end_date})
```

### Step 12: Call asset.submit()

```python
asset.submit()
```


## Complete Example

```python
# Workflow
create_fixed_asset_item('Rack', is_grouped_asset=1)
pr = make_purchase_receipt(item_code='Rack', qty=3, rate=100000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset = frappe.get_doc('Asset', asset_name)
self.assertEqual(asset.asset_quantity, 3)
asset.calculate_depreciation = 1
month_end_date = get_last_day(nowdate())
purchase_date = nowdate() if nowdate() != month_end_date else add_days(nowdate(), -15)
asset.available_for_use_date = purchase_date
asset.purchase_date = purchase_date
asset.append('finance_books', {'expected_value_after_useful_life': 10000, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10, 'depreciation_start_date': month_end_date})
asset.submit()
```

## Next Steps


---

*Source: test_asset.py:158 | Complexity: Advanced | Last updated: 2026-02-04*