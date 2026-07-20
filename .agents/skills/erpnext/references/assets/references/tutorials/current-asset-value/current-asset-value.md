# How To: Current Asset Value

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test current asset value

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.assets.doctype.asset.asset`
- `erpnext.assets.doctype.asset.depreciation`
- `erpnext.assets.doctype.asset.test_asset`
- `erpnext.assets.doctype.asset_depreciation_schedule.asset_depreciation_schedule`
- `erpnext.assets.doctype.asset_repair.test_asset_repair`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`


## Step-by-Step Guide

### Step 1: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=100000.0, location='Test Location')
```

### Step 2: Assign asset_name = frappe.db.get_value(...)

```python
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
```

### Step 3: Assign asset_doc = frappe.get_doc(...)

```python
asset_doc = frappe.get_doc('Asset', asset_name)
```

### Step 4: Assign month_end_date = get_last_day(...)

```python
month_end_date = get_last_day(nowdate())
```

### Step 5: Assign purchase_date = value

```python
purchase_date = nowdate() if nowdate() != month_end_date else add_days(nowdate(), -15)
```

### Step 6: Assign asset_doc.available_for_use_date = purchase_date

```python
asset_doc.available_for_use_date = purchase_date
```

### Step 7: Assign asset_doc.purchase_date = purchase_date

```python
asset_doc.purchase_date = purchase_date
```

### Step 8: Assign asset_doc.calculate_depreciation = 1

```python
asset_doc.calculate_depreciation = 1
```

### Step 9: Call asset_doc.append()

```python
asset_doc.append('finance_books', {'expected_value_after_useful_life': 200, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10, 'depreciation_start_date': month_end_date})
```

### Step 10: Call asset_doc.submit()

```python
asset_doc.submit()
```

### Step 11: Assign current_value = get_asset_value_after_depreciation(...)

```python
current_value = get_asset_value_after_depreciation(asset_doc.name)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(current_value, 100000.0)
```


## Complete Example

```python
# Workflow
pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=100000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset_doc = frappe.get_doc('Asset', asset_name)
month_end_date = get_last_day(nowdate())
purchase_date = nowdate() if nowdate() != month_end_date else add_days(nowdate(), -15)
asset_doc.available_for_use_date = purchase_date
asset_doc.purchase_date = purchase_date
asset_doc.calculate_depreciation = 1
asset_doc.append('finance_books', {'expected_value_after_useful_life': 200, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10, 'depreciation_start_date': month_end_date})
asset_doc.submit()
current_value = get_asset_value_after_depreciation(asset_doc.name)
self.assertEqual(current_value, 100000.0)
```

## Next Steps


---

*Source: test_asset_value_adjustment.py:25 | Complexity: Advanced | Last updated: 2026-02-04*