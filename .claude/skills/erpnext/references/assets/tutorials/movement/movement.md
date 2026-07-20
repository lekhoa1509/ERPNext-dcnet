# How To: Movement

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test movement

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

### Step 8: Call create_asset_movement()

```python
create_asset_movement(purpose='Transfer', company=asset.company, assets=[{'asset': asset.name, 'source_location': 'Test Location', 'target_location': 'Test Location 2'}], reference_doctype='Purchase Receipt', reference_name=pr.name)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
```

### Step 10: Assign movement1 = create_asset_movement(...)

```python
movement1 = create_asset_movement(purpose='Transfer', company=asset.company, assets=[{'asset': asset.name, 'source_location': 'Test Location 2', 'target_location': 'Test Location'}], reference_doctype='Purchase Receipt', reference_name=pr.name)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')
```

### Step 12: Call movement1.cancel()

```python
movement1.cancel()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
```

### Step 14: Assign employee = make_employee(...)

```python
employee = make_employee('testassetmovemp@example.com', company='_Test Company')
```

### Step 15: Call create_asset_movement()

```python
create_asset_movement(purpose='Issue', company=asset.company, assets=[{'asset': asset.name, 'source_location': 'Test Location 2', 'to_employee': employee}], reference_doctype='Purchase Receipt', reference_name=pr.name)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'custodian'), employee)
```

### Step 18: Call create_asset_movement()

```python
create_asset_movement(purpose='Receipt', company=asset.company, assets=[{'asset': asset.name, 'from_employee': employee, 'target_location': 'Test Location'}], reference_doctype='Purchase Receipt', reference_name=pr.name)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')
```

### Step 20: Call asset.submit()

```python
asset.submit()
```

### Step 21: Call frappe.get_doc.insert()

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
create_asset_movement(purpose='Transfer', company=asset.company, assets=[{'asset': asset.name, 'source_location': 'Test Location', 'target_location': 'Test Location 2'}], reference_doctype='Purchase Receipt', reference_name=pr.name)
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
movement1 = create_asset_movement(purpose='Transfer', company=asset.company, assets=[{'asset': asset.name, 'source_location': 'Test Location 2', 'target_location': 'Test Location'}], reference_doctype='Purchase Receipt', reference_name=pr.name)
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')
movement1.cancel()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
employee = make_employee('testassetmovemp@example.com', company='_Test Company')
create_asset_movement(purpose='Issue', company=asset.company, assets=[{'asset': asset.name, 'source_location': 'Test Location 2', 'to_employee': employee}], reference_doctype='Purchase Receipt', reference_name=pr.name)
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'custodian'), employee)
create_asset_movement(purpose='Receipt', company=asset.company, assets=[{'asset': asset.name, 'from_employee': employee, 'target_location': 'Test Location'}], reference_doctype='Purchase Receipt', reference_name=pr.name)
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')
```

## Next Steps


---

*Source: test_asset_movement.py:21 | Complexity: Advanced | Last updated: 2026-02-04*