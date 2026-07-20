# How To: Custom Report

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test custom report

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

### Step 1: Call reset_customization()

```python
reset_customization('User')
```

### Step 2: Assign custom_report_name = save_report(...)

```python
custom_report_name = save_report('Permitted Documents For User', 'Permitted Documents For User Custom', json.dumps([{'fieldname': 'email', 'fieldtype': 'Data', 'label': 'Email', 'insert_after_index': 0, 'link_field': 'name', 'doctype': 'User', 'options': 'Email', 'width': 100, 'id': 'email', 'name': 'Email'}]), json.dumps({'user': 'Administrator', 'doctype': 'User'}))
```

### Step 3: Assign custom_report = frappe.get_doc(...)

```python
custom_report = frappe.get_doc('Report', custom_report_name)
```

### Step 4: Assign unknown = custom_report.run_query_report(...)

```python
columns, result = custom_report.run_query_report(user=frappe.session.user)
```

### Step 5: Call self.assertListEqual()

```python
self.assertListEqual(['email'], [column.get('fieldname') for column in columns])
```

### Step 6: Assign admin_dict = frappe.core.utils.find(...)

```python
admin_dict = frappe.core.utils.find(result, lambda d: d['name'] == 'Administrator')
```

### Step 7: Call self.assertDictEqual()

```python
self.assertDictEqual({'name': 'Administrator', 'user_type': 'System User', 'email': 'admin@example.com'}, admin_dict)
```


## Complete Example

```python
# Workflow
reset_customization('User')
custom_report_name = save_report('Permitted Documents For User', 'Permitted Documents For User Custom', json.dumps([{'fieldname': 'email', 'fieldtype': 'Data', 'label': 'Email', 'insert_after_index': 0, 'link_field': 'name', 'doctype': 'User', 'options': 'Email', 'width': 100, 'id': 'email', 'name': 'Email'}]), json.dumps({'user': 'Administrator', 'doctype': 'User'}))
custom_report = frappe.get_doc('Report', custom_report_name)
columns, result = custom_report.run_query_report(user=frappe.session.user)
self.assertListEqual(['email'], [column.get('fieldname') for column in columns])
admin_dict = frappe.core.utils.find(result, lambda d: d['name'] == 'Administrator')
self.assertDictEqual({'name': 'Administrator', 'user_type': 'System User', 'email': 'admin@example.com'}, admin_dict)
```

## Next Steps


---

*Source: test_report.py:104 | Complexity: Intermediate | Last updated: 2026-02-04*