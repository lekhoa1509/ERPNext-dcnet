# How To: Depreciation On Return Of Sold Asset

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test depreciation on return of sold asset

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.assets.doctype.asset.depreciation`
- `erpnext.assets.doctype.asset.test_asset`
- `erpnext.assets.doctype.asset_depreciation_schedule.asset_depreciation_schedule`
- `erpnext.assets.doctype.asset_repair.test_asset_repair`
- `erpnext.assets.doctype.asset_value_adjustment.test_asset_value_adjustment`
- `erpnext.controllers.sales_and_purchase_return`

**Setup Required:**
```python
create_asset_data()
```

## Step-by-Step Guide

### Step 1: Call create_asset_data()

```python
create_asset_data()
```

### Step 2: Assign asset = create_asset(...)

```python
asset = create_asset(item_code='Macbook Pro', calculate_depreciation=1, submit=1)
```

### Step 3: Call post_depreciation_entries()

```python
post_depreciation_entries(getdate('2021-09-30'))
```

### Step 4: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(item_code='Macbook Pro', asset=asset.name, qty=1, rate=90000, posting_date=getdate('2021-09-30'))
```

### Step 5: Assign return_si = make_return_doc(...)

```python
return_si = make_return_doc('Sales Invoice', si.name)
```

### Step 6: Call return_si.submit()

```python
return_si.submit()
```

### Step 7: Call asset.load_from_db()

```python
asset.load_from_db()
```

### Step 8: Assign expected_values = value

```python
expected_values = [['2020-06-30', 1366.12, 1366.12, True], ['2021-06-30', 20000.0, 21366.12, True], ['2022-06-30', 20000.95, 41367.07, False], ['2023-06-30', 20000.95, 61368.02, False], ['2024-06-30', 20000.95, 81368.97, False], ['2025-06-06', 18631.03, 100000.0, False]]
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(getdate(expected_values[i][0]), schedule.schedule_date)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(expected_values[i][1], schedule.depreciation_amount)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(expected_values[i][2], schedule.accumulated_depreciation_amount)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(schedule.journal_entry, schedule.journal_entry)
```


## Complete Example

```python
# Setup
create_asset_data()

# Workflow
from erpnext.controllers.sales_and_purchase_return import make_return_doc
create_asset_data()
asset = create_asset(item_code='Macbook Pro', calculate_depreciation=1, submit=1)
post_depreciation_entries(getdate('2021-09-30'))
si = create_sales_invoice(item_code='Macbook Pro', asset=asset.name, qty=1, rate=90000, posting_date=getdate('2021-09-30'))
return_si = make_return_doc('Sales Invoice', si.name)
return_si.submit()
asset.load_from_db()
expected_values = [['2020-06-30', 1366.12, 1366.12, True], ['2021-06-30', 20000.0, 21366.12, True], ['2022-06-30', 20000.95, 41367.07, False], ['2023-06-30', 20000.95, 61368.02, False], ['2024-06-30', 20000.95, 81368.97, False], ['2025-06-06', 18631.03, 100000.0, False]]
for i, schedule in enumerate(get_depr_schedule(asset.name, 'Active')):
    self.assertEqual(getdate(expected_values[i][0]), schedule.schedule_date)
    self.assertEqual(expected_values[i][1], schedule.depreciation_amount)
    self.assertEqual(expected_values[i][2], schedule.accumulated_depreciation_amount)
    self.assertEqual(schedule.journal_entry, schedule.journal_entry)
```

## Next Steps


---

*Source: test_asset_depreciation_schedule.py:815 | Complexity: Advanced | Last updated: 2026-02-04*