# How To: Xlsx Data With Filters

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test building xlsx data along with filters

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

### Step 1: 'Test building xlsx data along with filters'

```python
'Test building xlsx data along with filters'
```

### Step 2: Assign data = create_mock_data(...)

```python
data = create_mock_data()
```

### Step 3: Assign data.filters = value

```python
data.filters = {'Label 1': 'Filter Value', 'Label 2': None, 'Label 3': list(range(5))}
```

### Step 4: Assign visible_idx = value

```python
visible_idx = [0, 2, 3]
```

### Step 5: Assign unknown = build_xlsx_data(...)

```python
xlsx_data, _column_widths, header_index = build_xlsx_data(data, visible_idx, include_indentation=False, include_filters=True)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(header_index, 3)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(xlsx_data), 7)
```

### Step 8: Call self.assertListEqual()

```python
self.assertListEqual(xlsx_data[:2], [['Label 1', 'Filter Value'], ['Label 3', '0, 1, 2, 3, 4']])
```


## Complete Example

```python
# Workflow
'Test building xlsx data along with filters'
data = create_mock_data()
data.filters = {'Label 1': 'Filter Value', 'Label 2': None, 'Label 3': list(range(5))}
visible_idx = [0, 2, 3]
xlsx_data, _column_widths, header_index = build_xlsx_data(data, visible_idx, include_indentation=False, include_filters=True)
self.assertEqual(header_index, 3)
self.assertEqual(len(xlsx_data), 7)
self.assertListEqual(xlsx_data[:2], [['Label 1', 'Filter Value'], ['Label 3', '0, 1, 2, 3, 4']])
```

## Next Steps


---

*Source: test_query_report.py:45 | Complexity: Advanced | Last updated: 2026-02-04*