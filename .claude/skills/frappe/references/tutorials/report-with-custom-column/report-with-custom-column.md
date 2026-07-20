# How To: Report With Custom Column

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test report with custom column

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

### Step 2: Assign response = run(...)

```python
response = run('Permitted Documents For User', filters={'user': 'Administrator', 'doctype': 'User'}, custom_columns=[{'fieldname': 'email', 'fieldtype': 'Data', 'label': 'Email', 'insert_after_index': 0, 'link_field': 'name', 'doctype': 'User', 'options': 'Email', 'width': 100, 'id': 'email', 'name': 'Email'}])
```

### Step 3: Assign result = response.get(...)

```python
result = response.get('result')
```

### Step 4: Assign columns = response.get(...)

```python
columns = response.get('columns')
```

### Step 5: Call self.assertListEqual()

```python
self.assertListEqual(['name', 'email', 'user_type'], [column.get('fieldname') for column in columns])
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
response = run('Permitted Documents For User', filters={'user': 'Administrator', 'doctype': 'User'}, custom_columns=[{'fieldname': 'email', 'fieldtype': 'Data', 'label': 'Email', 'insert_after_index': 0, 'link_field': 'name', 'doctype': 'User', 'options': 'Email', 'width': 100, 'id': 'email', 'name': 'Email'}])
result = response.get('result')
columns = response.get('columns')
self.assertListEqual(['name', 'email', 'user_type'], [column.get('fieldname') for column in columns])
admin_dict = frappe.core.utils.find(result, lambda d: d['name'] == 'Administrator')
self.assertDictEqual({'name': 'Administrator', 'user_type': 'System User', 'email': 'admin@example.com'}, admin_dict)
```

## Next Steps


---

*Source: test_report.py:141 | Complexity: Intermediate | Last updated: 2026-02-04*