# How To: Auto Email

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test auto email

## Prerequisites

**Required Modules:**
- `json`
- `io`
- `pypdf`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.data`


## Step-by-Step Guide

### Step 1: Call frappe.delete_doc()

```python
frappe.delete_doc('Auto Email Report', 'Permitted Documents For User')
```

### Step 2: Assign auto_email_report = get_auto_email_report(...)

```python
auto_email_report = get_auto_email_report()
```

### Step 3: Assign data = auto_email_report.get_report_content(...)

```python
data = auto_email_report.get_report_content()
```

### Step 4: Call self.assertTrue()

```python
self.assertTrue(is_html(data))
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(str(get_link_to_form('Module Def', 'Core')) in data)
```

### Step 6: Assign auto_email_report.format = 'CSV'

```python
auto_email_report.format = 'CSV'
```

### Step 7: Assign data = auto_email_report.get_report_content(...)

```python
data = auto_email_report.get_report_content()
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue('"Language","Core"' in data)
```

### Step 9: Assign auto_email_report.format = 'XLSX'

```python
auto_email_report.format = 'XLSX'
```

### Step 10: Assign data = auto_email_report.get_report_content(...)

```python
data = auto_email_report.get_report_content()
```

### Step 11: Assign auto_email_report.format = 'PDF'

```python
auto_email_report.format = 'PDF'
```

### Step 12: Assign data = auto_email_report.get_report_content(...)

```python
data = auto_email_report.get_report_content()
```

### Step 13: Call PdfReader()

```python
PdfReader(stream=BytesIO(data))
```


## Complete Example

```python
# Workflow
frappe.delete_doc('Auto Email Report', 'Permitted Documents For User')
auto_email_report = get_auto_email_report()
data = auto_email_report.get_report_content()
self.assertTrue(is_html(data))
self.assertTrue(str(get_link_to_form('Module Def', 'Core')) in data)
auto_email_report.format = 'CSV'
data = auto_email_report.get_report_content()
self.assertTrue('"Language","Core"' in data)
auto_email_report.format = 'XLSX'
data = auto_email_report.get_report_content()
auto_email_report.format = 'PDF'
data = auto_email_report.get_report_content()
PdfReader(stream=BytesIO(data))
```

## Next Steps


---

*Source: test_auto_email_report.py:15 | Complexity: Advanced | Last updated: 2026-02-04*