# How To: Csv

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test csv

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.desk.reportview`
- `frappe.tests`
- `csv`
- `io`


## Step-by-Step Guide

### Step 1: Assign frappe.local.form_dict = frappe._dict(...)

```python
frappe.local.form_dict = frappe._dict(doctype='DocType', file_format_type='CSV', fields=('name', 'module', 'issingle'), filters={'issingle': 1, 'module': 'Core'})
```

### Step 2: Assign frappe.local.form_dict.csv_delimiter = delimiter

```python
frappe.local.form_dict.csv_delimiter = delimiter
```

### Step 3: Assign frappe.local.form_dict.csv_quoting = quoting

```python
frappe.local.form_dict.csv_quoting = quoting
```

### Step 4: Call export_query()

```python
export_query()
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(frappe.response['filename'].endswith('.csv'))
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(frappe.response['type'], 'binary')
```

### Step 7: Assign reader = DictReader(...)

```python
reader = DictReader(result, delimiter=delimiter, quoting=quoting)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(int(row['Is Single']), 1)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(row['Module'], 'Core')
```


## Complete Example

```python
# Workflow
from csv import QUOTE_ALL, QUOTE_MINIMAL, QUOTE_NONE, QUOTE_NONNUMERIC, DictReader
from io import StringIO
frappe.local.form_dict = frappe._dict(doctype='DocType', file_format_type='CSV', fields=('name', 'module', 'issingle'), filters={'issingle': 1, 'module': 'Core'})
for delimiter in (',', ';', '\t', '|'):
    frappe.local.form_dict.csv_delimiter = delimiter
    for quoting in (QUOTE_ALL, QUOTE_MINIMAL, QUOTE_NONE, QUOTE_NONNUMERIC):
        frappe.local.form_dict.csv_quoting = quoting
        export_query()
        self.assertTrue(frappe.response['filename'].endswith('.csv'))
        self.assertEqual(frappe.response['type'], 'binary')
        with StringIO(frappe.response['filecontent'].decode('utf-8')) as result:
            reader = DictReader(result, delimiter=delimiter, quoting=quoting)
            for row in reader:
                self.assertEqual(int(row['Is Single']), 1)
                self.assertEqual(row['Module'], 'Core')
```

## Next Steps


---

*Source: test_reportview.py:10 | Complexity: Advanced | Last updated: 2026-02-04*