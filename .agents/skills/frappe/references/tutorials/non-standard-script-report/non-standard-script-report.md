# How To: Non Standard Script Report

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test non standard script report

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

### Step 1: Assign report_name = 'Test Non Standard Script Report'

```python
report_name = 'Test Non Standard Script Report'
```

### Step 2: Assign report.report_script = '\ntotals = {}\nfor user in frappe.get_all(\'User\', fields = [\'name\', \'user_type\', \'creation\']):\n    if not user.user_type in totals:\n        totals[user.user_type] = 0\n    totals[user.user_type] = totals[user.user_type] + 1\n\ndata = [\n    [\n        {\'fieldname\': \'type\', \'label\': \'Type\'},\n        {\'fieldname\': \'value\', \'label\': \'Value\'}\n    ],\n    [\n        {"type":key, "value": value} for key, value in totals.items()\n    ]\n]\n'

```python
report.report_script = '\ntotals = {}\nfor user in frappe.get_all(\'User\', fields = [\'name\', \'user_type\', \'creation\']):\n    if not user.user_type in totals:\n        totals[user.user_type] = 0\n    totals[user.user_type] = totals[user.user_type] + 1\n\ndata = [\n    [\n        {\'fieldname\': \'type\', \'label\': \'Type\'},\n        {\'fieldname\': \'value\', \'label\': \'Value\'}\n    ],\n    [\n        {"type":key, "value": value} for key, value in totals.items()\n    ]\n]\n'
```

### Step 3: Call report.save()

```python
report.save()
```

### Step 4: Assign data = report.get_data(...)

```python
data = report.get_data()
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(data[0][0]['label'], 'Type')
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue('System User' in [d.get('type') for d in data[1]])
```

### Step 7: Assign report = frappe.get_doc.insert(...)

```python
report = frappe.get_doc({'doctype': 'Report', 'ref_doctype': 'User', 'report_name': report_name, 'report_type': 'Script Report', 'is_standard': 'No'}).insert(ignore_permissions=True)
```

### Step 8: Assign report = frappe.get_doc(...)

```python
report = frappe.get_doc('Report', report_name)
```


## Complete Example

```python
# Workflow
report_name = 'Test Non Standard Script Report'
if not frappe.db.exists('Report', report_name):
    report = frappe.get_doc({'doctype': 'Report', 'ref_doctype': 'User', 'report_name': report_name, 'report_type': 'Script Report', 'is_standard': 'No'}).insert(ignore_permissions=True)
else:
    report = frappe.get_doc('Report', report_name)
report.report_script = '\ntotals = {}\nfor user in frappe.get_all(\'User\', fields = [\'name\', \'user_type\', \'creation\']):\n    if not user.user_type in totals:\n        totals[user.user_type] = 0\n    totals[user.user_type] = totals[user.user_type] + 1\n\ndata = [\n    [\n        {\'fieldname\': \'type\', \'label\': \'Type\'},\n        {\'fieldname\': \'value\', \'label\': \'Value\'}\n    ],\n    [\n        {"type":key, "value": value} for key, value in totals.items()\n    ]\n]\n'
report.save()
data = report.get_data()
self.assertEqual(data[0][0]['label'], 'Type')
self.assertTrue('System User' in [d.get('type') for d in data[1]])
```

## Next Steps


---

*Source: test_report.py:254 | Complexity: Advanced | Last updated: 2026-02-04*