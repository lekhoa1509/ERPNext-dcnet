# How To: Difference Amount

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test difference amount

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

### Step 4: Assign asset_doc.calculate_depreciation = 1

```python
asset_doc.calculate_depreciation = 1
```

### Step 5: Assign asset_doc.available_for_use_date = '2023-01-15'

```python
asset_doc.available_for_use_date = '2023-01-15'
```

### Step 6: Assign asset_doc.purchase_date = '2023-01-15'

```python
asset_doc.purchase_date = '2023-01-15'
```

### Step 7: Call asset_doc.append()

```python
asset_doc.append('finance_books', {'expected_value_after_useful_life': 200, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 12, 'frequency_of_depreciation': 1, 'depreciation_start_date': '2023-01-31'})
```

### Step 8: Call asset_doc.submit()

```python
asset_doc.submit()
```

### Step 9: Assign current_asset_value = get_asset_value_after_depreciation(...)

```python
current_asset_value = get_asset_value_after_depreciation(asset_doc.name)
```

### Step 10: Assign adj_doc = make_asset_value_adjustment(...)

```python
adj_doc = make_asset_value_adjustment(asset=asset_doc.name, current_asset_value=current_asset_value, new_asset_value=40000, date='2023-08-21')
```

### Step 11: Call adj_doc.submit()

```python
adj_doc.submit()
```

### Step 12: Assign difference_amount = value

```python
difference_amount = adj_doc.new_asset_value - adj_doc.current_asset_value
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(difference_amount, -60000)
```

### Step 14: Call asset_doc.load_from_db()

```python
asset_doc.load_from_db()
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(asset_doc.finance_books[0].value_after_depreciation, 40000.0)
```


## Complete Example

```python
# Workflow
pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=100000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset_doc = frappe.get_doc('Asset', asset_name)
asset_doc.calculate_depreciation = 1
asset_doc.available_for_use_date = '2023-01-15'
asset_doc.purchase_date = '2023-01-15'
asset_doc.append('finance_books', {'expected_value_after_useful_life': 200, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 12, 'frequency_of_depreciation': 1, 'depreciation_start_date': '2023-01-31'})
asset_doc.submit()
current_asset_value = get_asset_value_after_depreciation(asset_doc.name)
adj_doc = make_asset_value_adjustment(asset=asset_doc.name, current_asset_value=current_asset_value, new_asset_value=40000, date='2023-08-21')
adj_doc.submit()
difference_amount = adj_doc.new_asset_value - adj_doc.current_asset_value
self.assertEqual(difference_amount, -60000)
asset_doc.load_from_db()
self.assertEqual(asset_doc.finance_books[0].value_after_depreciation, 40000.0)
```

## Next Steps


---

*Source: test_asset_value_adjustment.py:267 | Complexity: Advanced | Last updated: 2026-02-04*