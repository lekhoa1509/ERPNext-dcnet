# How To: Jv With Project

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test jv with project

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.doctype.journal_entry.journal_entry`
- `erpnext.exceptions`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.accounts.utils`
- `erpnext.accounts.doctype.journal_entry.journal_entry`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.projects.doctype.project.test_project`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.accounts.utils`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.accounts.general_ledger`
- `erpnext.accounts.general_ledger`


## Step-by-Step Guide

### Step 1: Assign jv = make_journal_entry(...)

```python
jv = make_journal_entry('_Test Cash - _TC', '_Test Bank - _TC', 100, save=False)
```

### Step 2: Assign jv.voucher_type = 'Bank Entry'

```python
jv.voucher_type = 'Bank Entry'
```

### Step 3: Assign jv.multi_currency = 0

```python
jv.multi_currency = 0
```

### Step 4: Assign jv.cheque_no = '112233'

```python
jv.cheque_no = '112233'
```

### Step 5: Assign jv.cheque_date = nowdate(...)

```python
jv.cheque_date = nowdate()
```

### Step 6: Call jv.insert()

```python
jv.insert()
```

### Step 7: Call jv.submit()

```python
jv.submit()
```

### Step 8: Assign self.voucher_no = value

```python
self.voucher_no = jv.name
```

### Step 9: Assign self.fields = value

```python
self.fields = ['account', 'project']
```

### Step 10: Assign self.expected_gle = value

```python
self.expected_gle = [{'account': '_Test Bank - _TC', 'project': project_name}, {'account': '_Test Cash - _TC', 'project': project_name}]
```

### Step 11: Call self.check_gl_entries()

```python
self.check_gl_entries()
```

### Step 12: Assign project = make_project(...)

```python
project = make_project({'project_name': 'Journal Entry Project', 'project_template_name': 'Test Project Template', 'start_date': '2020-01-01'})
```

### Step 13: Assign project_name = value

```python
project_name = project.name
```

### Step 14: Assign project_name = frappe.get_value(...)

```python
project_name = frappe.get_value('Project', {'project_name': '_Test Project'})
```

### Step 15: Assign d.project = project_name

```python
d.project = project_name
```


## Complete Example

```python
# Workflow
from erpnext.projects.doctype.project.test_project import make_project
if not frappe.db.exists('Project', {'project_name': 'Journal Entry Project'}):
    project = make_project({'project_name': 'Journal Entry Project', 'project_template_name': 'Test Project Template', 'start_date': '2020-01-01'})
    project_name = project.name
else:
    project_name = frappe.get_value('Project', {'project_name': '_Test Project'})
jv = make_journal_entry('_Test Cash - _TC', '_Test Bank - _TC', 100, save=False)
for d in jv.accounts:
    d.project = project_name
jv.voucher_type = 'Bank Entry'
jv.multi_currency = 0
jv.cheque_no = '112233'
jv.cheque_date = nowdate()
jv.insert()
jv.submit()
self.voucher_no = jv.name
self.fields = ['account', 'project']
self.expected_gle = [{'account': '_Test Bank - _TC', 'project': project_name}, {'account': '_Test Cash - _TC', 'project': project_name}]
self.check_gl_entries()
```

## Next Steps


---

*Source: test_journal_entry.py:349 | Complexity: Advanced | Last updated: 2026-02-03*