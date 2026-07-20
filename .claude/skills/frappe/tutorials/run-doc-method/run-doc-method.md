# How To: Run Doc Method

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test run doc method

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.client`
- `frappe.desk.doctype.note.note`
- `frappe.client`
- `frappe.handler`
- `frappe.handler`
- `frappe.handler`
- `requests`
- `frappe.auth`
- `frappe.client`
- `frappe.client`
- `frappe.client`
- `frappe.client`
- `frappe.client`


## Step-by-Step Guide

### Step 1: Assign report = frappe.get_doc.insert(...)

```python
report = frappe.get_doc({'doctype': 'Report', 'ref_doctype': 'User', 'report_name': frappe.generate_hash(), 'report_type': 'Query Report', 'is_standard': 'No', 'roles': [{'role': 'System Manager'}]}).insert()
```

### Step 2: Assign frappe.local.request = frappe._dict(...)

```python
frappe.local.request = frappe._dict()
```

### Step 3: Assign frappe.local.request.method = 'GET'

```python
frappe.local.request.method = 'GET'
```

### Step 4: Assign frappe.local.form_dict = frappe._dict(...)

```python
frappe.local.form_dict = frappe._dict({'dt': report.doctype, 'dn': report.name, 'method': 'toggle_disable', 'cmd': 'run_doc_method', 'args': 0})
```

### Step 5: Call execute_cmd()

```python
execute_cmd(frappe.local.form_dict.cmd)
```

### Step 6: Assign frappe.local.form_dict = frappe._dict(...)

```python
frappe.local.form_dict = frappe._dict({'dt': report.doctype, 'dn': report.name, 'method': 'create_report_py', 'cmd': 'run_doc_method', 'args': 0})
```

### Step 7: Call self.assertRaises()

```python
self.assertRaises(frappe.PermissionError, execute_cmd, frappe.local.form_dict.cmd)
```


## Complete Example

```python
# Workflow
from frappe.handler import execute_cmd
report = frappe.get_doc({'doctype': 'Report', 'ref_doctype': 'User', 'report_name': frappe.generate_hash(), 'report_type': 'Query Report', 'is_standard': 'No', 'roles': [{'role': 'System Manager'}]}).insert()
frappe.local.request = frappe._dict()
frappe.local.request.method = 'GET'
frappe.local.form_dict = frappe._dict({'dt': report.doctype, 'dn': report.name, 'method': 'toggle_disable', 'cmd': 'run_doc_method', 'args': 0})
execute_cmd(frappe.local.form_dict.cmd)
frappe.local.form_dict = frappe._dict({'dt': report.doctype, 'dn': report.name, 'method': 'create_report_py', 'cmd': 'run_doc_method', 'args': 0})
self.assertRaises(frappe.PermissionError, execute_cmd, frappe.local.form_dict.cmd)
```

## Next Steps


---

*Source: test_client.py:74 | Complexity: Intermediate | Last updated: 2026-02-04*