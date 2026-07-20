# How To: Script Report With Columns

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test script report with columns

## Prerequisites

**Required Modules:**
- `json`
- `os`
- `textwrap`
- `frappe`
- `frappe.core.doctype.user_permission.test_user_permission`
- `frappe.custom.doctype.customize_form.customize_form`
- `frappe.desk.query_report`
- `frappe.desk.reportview`
- `frappe.desk.reportview`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign report_name = 'Test Script Report With Columns'

```python
report_name = 'Test Script Report With Columns'
```

### Step 2: Assign report = frappe.get_doc.insert(...)

```python
report = frappe.get_doc({'doctype': 'Report', 'ref_doctype': 'User', 'report_name': report_name, 'report_type': 'Script Report', 'is_standard': 'No', 'columns': [dict(fieldname='type', label='Type', fieldtype='Data'), dict(fieldname='value', label='Value', fieldtype='Int')]}).insert(ignore_permissions=True)
```

### Step 3: Assign report.report_script = '\ntotals = {}\nfor user in frappe.get_all(\'User\', fields = [\'name\', \'user_type\', \'creation\']):\n    if not user.user_type in totals:\n        totals[user.user_type] = 0\n    totals[user.user_type] = totals[user.user_type] + 1\n\nresult = [\n        {"type":key, "value": value} for key, value in totals.items()\n    ]\n'

```python
report.report_script = '\ntotals = {}\nfor user in frappe.get_all(\'User\', fields = [\'name\', \'user_type\', \'creation\']):\n    if not user.user_type in totals:\n        totals[user.user_type] = 0\n    totals[user.user_type] = totals[user.user_type] + 1\n\nresult = [\n        {"type":key, "value": value} for key, value in totals.items()\n    ]\n'
```

### Step 4: Call report.save()

```python
report.save()
```

### Step 5: Assign data = report.get_data(...)

```python
data = report.get_data()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(data[0][0]['label'], 'Type')
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue('System User' in [d.get('type') for d in data[1]])
```

### Step 8: Call frappe.delete_doc()

```python
frappe.delete_doc('Report', report_name)
```


## Complete Example

```python
# Workflow
report_name = 'Test Script Report With Columns'
if frappe.db.exists('Report', report_name):
    frappe.delete_doc('Report', report_name)
report = frappe.get_doc({'doctype': 'Report', 'ref_doctype': 'User', 'report_name': report_name, 'report_type': 'Script Report', 'is_standard': 'No', 'columns': [dict(fieldname='type', label='Type', fieldtype='Data'), dict(fieldname='value', label='Value', fieldtype='Int')]}).insert(ignore_permissions=True)
report.report_script = '\ntotals = {}\nfor user in frappe.get_all(\'User\', fields = [\'name\', \'user_type\', \'creation\']):\n    if not user.user_type in totals:\n        totals[user.user_type] = 0\n    totals[user.user_type] = totals[user.user_type] + 1\n\nresult = [\n        {"type":key, "value": value} for key, value in totals.items()\n    ]\n'
report.save()
data = report.get_data()
self.assertEqual(data[0][0]['label'], 'Type')
self.assertTrue('System User' in [d.get('type') for d in data[1]])
```

## Next Steps


---

*Source: test_report.py:295 | Complexity: Advanced | Last updated: 2026-02-04*