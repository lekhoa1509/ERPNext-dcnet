# How To: Purchase Asset

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test purchase asset

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

### Step 5: Assign month_end_date = get_last_day(...)

```python
month_end_date = get_last_day(nowdate())
```

### Step 6: Assign purchase_date = value

```python
purchase_date = nowdate() if nowdate() != month_end_date else add_days(nowdate(), -15)
```

### Step 7: Assign asset.available_for_use_date = purchase_date

```python
asset.available_for_use_date = purchase_date
```

### Step 8: Assign asset.purchase_date = purchase_date

```python
asset.purchase_date = purchase_date
```

### Step 9: Call asset.append()

```python
asset.append('finance_books', {'expected_value_after_useful_life': 10000, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10, 'depreciation_start_date': month_end_date})
```

### Step 10: Call asset.submit()

```python
asset.submit()
```

### Step 11: Assign pi = make_invoice(...)

```python
pi = make_invoice(pr.name)
```

### Step 12: Assign pi.supplier = '_Test Supplier'

```python
pi.supplier = '_Test Supplier'
```

### Step 13: Call pi.insert()

```python
pi.insert()
```

### Step 14: Call pi.submit()

```python
pi.submit()
```

### Step 15: Call asset.load_from_db()

```python
asset.load_from_db()
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(asset.supplier, '_Test Supplier')
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(asset.purchase_date, getdate(purchase_date))
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(asset.purchase_receipt, pr.name)
```

### Step 19: Assign expected_gle = value

```python
expected_gle = (('Asset Received But Not Billed - _TC', 100000.0, 0.0), ('Creditors - _TC', 0.0, 100000.0))
```

### Step 20: Assign gle = get_gl_entries(...)

```python
gle = get_gl_entries('Purchase Invoice', pi.name)
```

### Step 21: Call self.assertSequenceEqual()

```python
self.assertSequenceEqual(gle, expected_gle)
```

### Step 22: Call pi.cancel()

```python
pi.cancel()
```

### Step 23: Call asset.cancel()

```python
asset.cancel()
```

### Step 24: Call asset.load_from_db()

```python
asset.load_from_db()
```

### Step 25: Call pr.load_from_db()

```python
pr.load_from_db()
```

### Step 26: Call pr.cancel()

```python
pr.cancel()
```

### Step 27: Call self.assertEqual()

```python
self.assertEqual(asset.docstatus, 2)
```


## Complete Example

```python
# Workflow
pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=100000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset = frappe.get_doc('Asset', asset_name)
asset.calculate_depreciation = 1
month_end_date = get_last_day(nowdate())
purchase_date = nowdate() if nowdate() != month_end_date else add_days(nowdate(), -15)
asset.available_for_use_date = purchase_date
asset.purchase_date = purchase_date
asset.append('finance_books', {'expected_value_after_useful_life': 10000, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10, 'depreciation_start_date': month_end_date})
asset.submit()
pi = make_invoice(pr.name)
pi.supplier = '_Test Supplier'
pi.insert()
pi.submit()
asset.load_from_db()
self.assertEqual(asset.supplier, '_Test Supplier')
self.assertEqual(asset.purchase_date, getdate(purchase_date))
self.assertEqual(asset.purchase_receipt, pr.name)
expected_gle = (('Asset Received But Not Billed - _TC', 100000.0, 0.0), ('Creditors - _TC', 0.0, 100000.0))
gle = get_gl_entries('Purchase Invoice', pi.name)
self.assertSequenceEqual(gle, expected_gle)
pi.cancel()
asset.cancel()
asset.load_from_db()
pr.load_from_db()
pr.cancel()
self.assertEqual(asset.docstatus, 2)
```

## Next Steps


---

*Source: test_asset.py:109 | Complexity: Advanced | Last updated: 2026-02-04*