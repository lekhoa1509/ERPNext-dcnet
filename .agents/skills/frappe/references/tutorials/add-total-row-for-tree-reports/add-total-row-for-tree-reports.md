# How To: Add Total Row For Tree Reports

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test add total row for tree reports

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

### Step 1: Assign report_settings = value

```python
report_settings = {'tree': True, 'parent_field': 'parent_value'}
```

### Step 2: Assign columns = value

```python
columns = [{'fieldname': 'parent_column', 'label': 'Parent Column', 'fieldtype': 'Data', 'width': 10}, {'fieldname': 'column_1', 'label': 'Column 1', 'fieldtype': 'Float', 'width': 10}, {'fieldname': 'column_2', 'label': 'Column 2', 'fieldtype': 'Float', 'width': 10}]
```

### Step 3: Assign result = value

```python
result = [{'parent_column': 'Parent 1', 'column_1': 200, 'column_2': 150.5}, {'parent_column': 'Child 1', 'column_1': 100, 'column_2': 75.25, 'parent_value': 'Parent 1'}, {'parent_column': 'Child 2', 'column_1': 100, 'column_2': 75.25, 'parent_value': 'Parent 1'}]
```

### Step 4: Assign result = add_total_row(...)

```python
result = add_total_row(result, columns, meta=None, is_tree=report_settings['tree'], parent_field=report_settings['parent_field'])
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(result[-1][0], 'Total')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(result[-1][1], 200)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(result[-1][2], 150.5)
```


## Complete Example

```python
# Workflow
report_settings = {'tree': True, 'parent_field': 'parent_value'}
columns = [{'fieldname': 'parent_column', 'label': 'Parent Column', 'fieldtype': 'Data', 'width': 10}, {'fieldname': 'column_1', 'label': 'Column 1', 'fieldtype': 'Float', 'width': 10}, {'fieldname': 'column_2', 'label': 'Column 2', 'fieldtype': 'Float', 'width': 10}]
result = [{'parent_column': 'Parent 1', 'column_1': 200, 'column_2': 150.5}, {'parent_column': 'Child 1', 'column_1': 100, 'column_2': 75.25, 'parent_value': 'Parent 1'}, {'parent_column': 'Child 2', 'column_1': 100, 'column_2': 75.25, 'parent_value': 'Parent 1'}]
result = add_total_row(result, columns, meta=None, is_tree=report_settings['tree'], parent_field=report_settings['parent_field'])
self.assertEqual(result[-1][0], 'Total')
self.assertEqual(result[-1][1], 200)
self.assertEqual(result[-1][2], 150.5)
```

## Next Steps


---

*Source: test_report.py:359 | Complexity: Intermediate | Last updated: 2026-02-04*