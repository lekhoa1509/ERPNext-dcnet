# How To: Xlsx Export With Composite Cell Value

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test excel export using rows with composite cell value

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.utils`
- `frappe.desk.query_report`
- `frappe.tests`
- `frappe.utils.xlsxutils`
- `csv`
- `io`


## Step-by-Step Guide

### Step 1: 'Test excel export using rows with composite cell value'

```python
'Test excel export using rows with composite cell value'
```

### Step 2: Assign data = frappe._dict(...)

```python
data = frappe._dict()
```

### Step 3: Assign data.columns = value

```python
data.columns = [{'label': 'Column A', 'fieldname': 'column_a', 'fieldtype': 'Float'}, {'label': 'Column B', 'fieldname': 'column_b', 'width': 150, 'fieldtype': 'Data'}]
```

### Step 4: Assign data.result = value

```python
data.result = [[1.0, 'Dummy 1'], {'column_a': 22.1, 'column_b': ['Dummy 1', 'Dummy 2']}]
```

### Step 5: Assign visible_idx = value

```python
visible_idx = [0, 1]
```

### Step 6: Assign unknown = build_xlsx_data(...)

```python
xlsx_data, column_widths, header_index = build_xlsx_data(data, visible_idx, include_indentation=0)
```

### Step 7: Call make_xlsx()

```python
make_xlsx(xlsx_data, 'Query Report', column_widths=column_widths, header_index=header_index)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(type(row[1]), str)
```


## Complete Example

```python
# Workflow
'Test excel export using rows with composite cell value'
data = frappe._dict()
data.columns = [{'label': 'Column A', 'fieldname': 'column_a', 'fieldtype': 'Float'}, {'label': 'Column B', 'fieldname': 'column_b', 'width': 150, 'fieldtype': 'Data'}]
data.result = [[1.0, 'Dummy 1'], {'column_a': 22.1, 'column_b': ['Dummy 1', 'Dummy 2']}]
visible_idx = [0, 1]
xlsx_data, column_widths, header_index = build_xlsx_data(data, visible_idx, include_indentation=0)
make_xlsx(xlsx_data, 'Query Report', column_widths=column_widths, header_index=header_index)
for row in xlsx_data:
    self.assertEqual(type(row[1]), str)
```

## Next Steps


---

*Source: test_query_report.py:68 | Complexity: Advanced | Last updated: 2026-02-04*