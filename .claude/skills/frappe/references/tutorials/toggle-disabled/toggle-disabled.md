# How To: Toggle Disabled

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Make sure that authorization is respected.

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

### Step 1: 'Make sure that authorization is respected.'

```python
'Make sure that authorization is respected.'
```

### Step 2: Assign reports = frappe.get_all(...)

```python
reports = frappe.get_all(doctype='Report', limit=1)
```

### Step 3: Assign report_name = value

```python
report_name = reports[0]['name']
```

### Step 4: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc('Report', report_name)
```

### Step 5: Assign status = value

```python
status = doc.disabled
```

### Step 6: Call frappe.set_user()

```python
frappe.set_user('test@example.com')
```

### Step 7: Call doc.toggle_disable()

```python
doc.toggle_disable(not status)
```

### Step 8: Call doc.reload()

```python
doc.reload()
```

### Step 9: Call self.assertNotEqual()

```python
self.assertNotEqual(status, doc.disabled)
```

### Step 10: Call frappe.set_user()

```python
frappe.set_user('test1@example.com')
```

### Step 11: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc('Report', report_name)
```

### Step 12: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 13: Call doc.toggle_disable()

```python
doc.toggle_disable(1)
```


## Complete Example

```python
# Workflow
'Make sure that authorization is respected.'
reports = frappe.get_all(doctype='Report', limit=1)
report_name = reports[0]['name']
doc = frappe.get_doc('Report', report_name)
status = doc.disabled
frappe.set_user('test@example.com')
doc.toggle_disable(not status)
doc.reload()
self.assertNotEqual(status, doc.disabled)
frappe.set_user('test1@example.com')
doc = frappe.get_doc('Report', report_name)
with self.assertRaises(frappe.exceptions.ValidationError):
    doc.toggle_disable(1)
frappe.set_user('Administrator')
```

## Next Steps


---

*Source: test_report.py:336 | Complexity: Advanced | Last updated: 2026-02-04*