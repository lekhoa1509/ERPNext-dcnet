# How To: Export Report Via Email

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test export report via email

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

### Step 1: Assign REPORT_NAME = 'Test CSV Report'

```python
REPORT_NAME = 'Test CSV Report'
```

### Step 2: Assign REF_DOCTYPE = 'DocType'

```python
REF_DOCTYPE = 'DocType'
```

### Step 3: Assign REPORT_COLUMNS = value

```python
REPORT_COLUMNS = ['name', 'module', 'issingle']
```

### Step 4: Assign frappe.local.form_dict = frappe._dict(...)

```python
frappe.local.form_dict = frappe._dict({'report_name': REPORT_NAME, 'file_format_type': 'CSV', 'include_indentation': 0, 'visible_idx': [0, 1, 2], 'export_in_background': 1})
```

### Step 5: Call frappe.db.delete()

```python
frappe.db.delete('Email Queue')
```

### Step 6: Call export_query()

```python
export_query()
```

### Step 7: Assign jobs = frappe.get_all(...)

```python
jobs = frappe.get_all('RQ Job')
```

### Step 8: Assign email_queue = frappe.get_all(...)

```python
email_queue = frappe.get_all('Email Queue')
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(jobs, 'Background job was not enqueued')
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(email_queue, 'Email was not enqueued')
```

### Step 11: Call frappe.delete_doc()

```python
frappe.delete_doc('Report', REPORT_NAME, delete_permanently=True)
```

### Step 12: Assign report = frappe.new_doc(...)

```python
report = frappe.new_doc('Report')
```

### Step 13: Assign report.report_name = REPORT_NAME

```python
report.report_name = REPORT_NAME
```

### Step 14: Assign report.ref_doctype = 'User'

```python
report.ref_doctype = 'User'
```

### Step 15: Assign report.report_type = 'Query Report'

```python
report.report_type = 'Query Report'
```

### Step 16: Assign report.query = frappe.qb.from_.select.limit.get_sql(...)

```python
report.query = frappe.qb.from_(REF_DOCTYPE).select(*REPORT_COLUMNS).limit(10).get_sql()
```

### Step 17: Assign report.is_standard = 'No'

```python
report.is_standard = 'No'
```

### Step 18: Call report.save()

```python
report.save()
```


## Complete Example

```python
# Workflow
REPORT_NAME = 'Test CSV Report'
REF_DOCTYPE = 'DocType'
REPORT_COLUMNS = ['name', 'module', 'issingle']
if not frappe.db.exists('Report', REPORT_NAME):
    report = frappe.new_doc('Report')
    report.report_name = REPORT_NAME
    report.ref_doctype = 'User'
    report.report_type = 'Query Report'
    report.query = frappe.qb.from_(REF_DOCTYPE).select(*REPORT_COLUMNS).limit(10).get_sql()
    report.is_standard = 'No'
    report.save()
frappe.local.form_dict = frappe._dict({'report_name': REPORT_NAME, 'file_format_type': 'CSV', 'include_indentation': 0, 'visible_idx': [0, 1, 2], 'export_in_background': 1})
frappe.db.delete('Email Queue')
export_query()
jobs = frappe.get_all('RQ Job')
email_queue = frappe.get_all('Email Queue')
self.assertTrue(jobs, 'Background job was not enqueued')
self.assertTrue(email_queue, 'Email was not enqueued')
frappe.delete_doc('Report', REPORT_NAME, delete_permanently=True)
```

## Next Steps


---

*Source: test_query_report.py:251 | Complexity: Advanced | Last updated: 2026-02-04*