# How To: Cwip Accounting

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test cwip accounting

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Call frappe.db.get_value()

```python
frappe.db.get_value('Company', '_Test Company', 'capital_work_in_progress_account')
```

### Step 2: Call frappe.db.set_value()

```python
frappe.db.set_value('Company', '_Test Company', 'capital_work_in_progress_account', '')
```

### Step 3: Assign asset_category = frappe.new_doc(...)

```python
asset_category = frappe.new_doc('Asset Category')
```

### Step 4: Assign asset_category.asset_category_name = 'Computers'

```python
asset_category.asset_category_name = 'Computers'
```

### Step 5: Assign asset_category.enable_cwip_accounting = 1

```python
asset_category.enable_cwip_accounting = 1
```

### Step 6: Assign asset_category.total_number_of_depreciations = 3

```python
asset_category.total_number_of_depreciations = 3
```

### Step 7: Assign asset_category.frequency_of_depreciation = 3

```python
asset_category.frequency_of_depreciation = 3
```

### Step 8: Call asset_category.append()

```python
asset_category.append('accounts', {'company_name': '_Test Company', 'fixed_asset_account': '_Test Fixed Asset - _TC', 'accumulated_depreciation_account': '_Test Accumulated Depreciations - _TC', 'depreciation_expense_account': '_Test Depreciations - _TC'})
```

### Step 9: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, asset_category.insert)
```


## Complete Example

```python
# Workflow
frappe.db.get_value('Company', '_Test Company', 'capital_work_in_progress_account')
frappe.db.set_value('Company', '_Test Company', 'capital_work_in_progress_account', '')
asset_category = frappe.new_doc('Asset Category')
asset_category.asset_category_name = 'Computers'
asset_category.enable_cwip_accounting = 1
asset_category.total_number_of_depreciations = 3
asset_category.frequency_of_depreciation = 3
asset_category.append('accounts', {'company_name': '_Test Company', 'fixed_asset_account': '_Test Fixed Asset - _TC', 'accumulated_depreciation_account': '_Test Accumulated Depreciations - _TC', 'depreciation_expense_account': '_Test Depreciations - _TC'})
self.assertRaises(frappe.ValidationError, asset_category.insert)
```

## Next Steps


---

*Source: test_asset_category.py:32 | Complexity: Advanced | Last updated: 2026-02-04*