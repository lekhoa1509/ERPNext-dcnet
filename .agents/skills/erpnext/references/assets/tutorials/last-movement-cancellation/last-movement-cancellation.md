# How To: Last Movement Cancellation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test last movement cancellation

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.assets.doctype.asset.test_asset`
- `erpnext.setup.doctype.employee.test_employee`
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

### Step 3: Assign asset = frappe.get_doc(...)

```python
asset = frappe.get_doc('Asset', asset_name)
```

### Step 4: Assign asset.calculate_depreciation = 1

```python
asset.calculate_depreciation = 1
```

### Step 5: Assign asset.available_for_use_date = '2020-06-06'

```python
asset.available_for_use_date = '2020-06-06'
```

### Step 6: Assign asset.purchase_date = '2020-06-06'

```python
asset.purchase_date = '2020-06-06'
```

### Step 7: Call asset.append()

```python
asset.append('finance_books', {'expected_value_after_useful_life': 10000, 'next_depreciation_date': '2020-12-31', 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10})
```

### Step 8: Assign movement = frappe.get_doc(...)

```python
movement = frappe.get_doc({'doctype': 'Asset Movement', 'reference_name': pr.name})
```

### Step 9: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, movement.cancel)
```

### Step 10: Assign movement1 = create_asset_movement(...)

```python
movement1 = create_asset_movement(purpose='Transfer', company=asset.company, assets=[{'asset': asset.name, 'source_location': 'Test Location', 'target_location': 'Test Location 2'}], reference_doctype='Purchase Receipt', reference_name=pr.name)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
```

### Step 12: Call movement1.cancel()

```python
movement1.cancel()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')
```

### Step 14: Call asset.submit()

```python
asset.submit()
```

### Step 15: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'Location', 'location_name': 'Test Location 2'}).insert()
```


## Complete Example

```python
# Workflow
pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=100000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset = frappe.get_doc('Asset', asset_name)
asset.calculate_depreciation = 1
asset.available_for_use_date = '2020-06-06'
asset.purchase_date = '2020-06-06'
asset.append('finance_books', {'expected_value_after_useful_life': 10000, 'next_depreciation_date': '2020-12-31', 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10})
if asset.docstatus == 0:
    asset.submit()
if not frappe.db.exists('Location', 'Test Location 2'):
    frappe.get_doc({'doctype': 'Location', 'location_name': 'Test Location 2'}).insert()
movement = frappe.get_doc({'doctype': 'Asset Movement', 'reference_name': pr.name})
self.assertRaises(frappe.ValidationError, movement.cancel)
movement1 = create_asset_movement(purpose='Transfer', company=asset.company, assets=[{'asset': asset.name, 'source_location': 'Test Location', 'target_location': 'Test Location 2'}], reference_doctype='Purchase Receipt', reference_name=pr.name)
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
movement1.cancel()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')
```

## Next Steps


---

*Source: test_asset_movement.py:104 | Complexity: Advanced | Last updated: 2026-02-04*