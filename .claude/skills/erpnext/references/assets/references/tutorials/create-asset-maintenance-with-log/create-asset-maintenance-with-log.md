# How To: Create Asset Maintenance With Log

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test create asset maintenance with log

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.assets.doctype.asset_maintenance.asset_maintenance`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`


## Step-by-Step Guide

### Step 1: Assign month_end_date = get_last_day(...)

```python
month_end_date = get_last_day(nowdate())
```

### Step 2: Assign purchase_date = value

```python
purchase_date = nowdate() if nowdate() != month_end_date else add_days(nowdate(), -15)
```

### Step 3: Assign self.asset_doc.available_for_use_date = purchase_date

```python
self.asset_doc.available_for_use_date = purchase_date
```

### Step 4: Assign self.asset_doc.purchase_date = purchase_date

```python
self.asset_doc.purchase_date = purchase_date
```

### Step 5: Assign self.asset_doc.calculate_depreciation = 1

```python
self.asset_doc.calculate_depreciation = 1
```

### Step 6: Call self.asset_doc.append()

```python
self.asset_doc.append('finance_books', {'expected_value_after_useful_life': 200, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10, 'depreciation_start_date': month_end_date})
```

### Step 7: Call self.asset_doc.save()

```python
self.asset_doc.save()
```

### Step 8: Assign asset_maintenance = frappe.get_doc.insert(...)

```python
asset_maintenance = frappe.get_doc({'doctype': 'Asset Maintenance', 'asset_name': self.asset_name, 'maintenance_team': 'Team Awesome', 'company': '_Test Company', 'asset_maintenance_tasks': get_maintenance_tasks()}).insert()
```

### Step 9: Assign next_due_date = calculate_next_due_date(...)

```python
next_due_date = calculate_next_due_date(nowdate(), 'Monthly')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)
```

### Step 11: Assign asset_maintenance_log = frappe.db.get_value(...)

```python
asset_maintenance_log = frappe.db.get_value('Asset Maintenance Log', {'asset_maintenance': asset_maintenance.name, 'task_name': 'Change Oil'}, 'name')
```

### Step 12: Assign asset_maintenance_log_doc = frappe.get_doc(...)

```python
asset_maintenance_log_doc = frappe.get_doc('Asset Maintenance Log', asset_maintenance_log)
```

### Step 13: Call asset_maintenance_log_doc.update()

```python
asset_maintenance_log_doc.update({'completion_date': add_days(nowdate(), 2), 'maintenance_status': 'Completed'})
```

### Step 14: Call asset_maintenance_log_doc.save()

```python
asset_maintenance_log_doc.save()
```

### Step 15: Assign next_due_date = calculate_next_due_date(...)

```python
next_due_date = calculate_next_due_date(asset_maintenance_log_doc.completion_date, 'Monthly')
```

### Step 16: Call asset_maintenance.reload()

```python
asset_maintenance.reload()
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)
```


## Complete Example

```python
# Workflow
month_end_date = get_last_day(nowdate())
purchase_date = nowdate() if nowdate() != month_end_date else add_days(nowdate(), -15)
self.asset_doc.available_for_use_date = purchase_date
self.asset_doc.purchase_date = purchase_date
self.asset_doc.calculate_depreciation = 1
self.asset_doc.append('finance_books', {'expected_value_after_useful_life': 200, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10, 'depreciation_start_date': month_end_date})
self.asset_doc.save()
asset_maintenance = frappe.get_doc({'doctype': 'Asset Maintenance', 'asset_name': self.asset_name, 'maintenance_team': 'Team Awesome', 'company': '_Test Company', 'asset_maintenance_tasks': get_maintenance_tasks()}).insert()
next_due_date = calculate_next_due_date(nowdate(), 'Monthly')
self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)
asset_maintenance_log = frappe.db.get_value('Asset Maintenance Log', {'asset_maintenance': asset_maintenance.name, 'task_name': 'Change Oil'}, 'name')
asset_maintenance_log_doc = frappe.get_doc('Asset Maintenance Log', asset_maintenance_log)
asset_maintenance_log_doc.update({'completion_date': add_days(nowdate(), 2), 'maintenance_status': 'Completed'})
asset_maintenance_log_doc.save()
next_due_date = calculate_next_due_date(asset_maintenance_log_doc.completion_date, 'Monthly')
asset_maintenance.reload()
self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)
```

## Next Steps


---

*Source: test_asset_maintenance.py:21 | Complexity: Advanced | Last updated: 2026-02-04*