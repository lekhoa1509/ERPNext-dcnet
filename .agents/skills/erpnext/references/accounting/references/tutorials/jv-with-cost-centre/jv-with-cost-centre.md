# How To: Jv With Cost Centre

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test jv with cost centre

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

### Step 1: Assign cost_center = '_Test Cost Center for BS Account - _TC'

```python
cost_center = '_Test Cost Center for BS Account - _TC'
```

### Step 2: Call create_cost_center()

```python
create_cost_center(cost_center_name='_Test Cost Center for BS Account', company='_Test Company')
```

### Step 3: Assign jv = make_journal_entry(...)

```python
jv = make_journal_entry('_Test Cash - _TC', '_Test Bank - _TC', 100, cost_center=cost_center, save=False)
```

### Step 4: Assign jv.voucher_type = 'Bank Entry'

```python
jv.voucher_type = 'Bank Entry'
```

### Step 5: Assign jv.multi_currency = 0

```python
jv.multi_currency = 0
```

### Step 6: Assign jv.cheque_no = '112233'

```python
jv.cheque_no = '112233'
```

### Step 7: Assign jv.cheque_date = nowdate(...)

```python
jv.cheque_date = nowdate()
```

### Step 8: Call jv.insert()

```python
jv.insert()
```

### Step 9: Call jv.submit()

```python
jv.submit()
```

### Step 10: Assign self.voucher_no = value

```python
self.voucher_no = jv.name
```

### Step 11: Assign self.fields = value

```python
self.fields = ['account', 'cost_center']
```

### Step 12: Assign self.expected_gle = value

```python
self.expected_gle = [{'account': '_Test Bank - _TC', 'cost_center': cost_center}, {'account': '_Test Cash - _TC', 'cost_center': cost_center}]
```

### Step 13: Call self.check_gl_entries()

```python
self.check_gl_entries()
```


## Complete Example

```python
# Workflow
from erpnext.accounts.doctype.cost_center.test_cost_center import create_cost_center
cost_center = '_Test Cost Center for BS Account - _TC'
create_cost_center(cost_center_name='_Test Cost Center for BS Account', company='_Test Company')
jv = make_journal_entry('_Test Cash - _TC', '_Test Bank - _TC', 100, cost_center=cost_center, save=False)
jv.voucher_type = 'Bank Entry'
jv.multi_currency = 0
jv.cheque_no = '112233'
jv.cheque_date = nowdate()
jv.insert()
jv.submit()
self.voucher_no = jv.name
self.fields = ['account', 'cost_center']
self.expected_gle = [{'account': '_Test Bank - _TC', 'cost_center': cost_center}, {'account': '_Test Cash - _TC', 'cost_center': cost_center}]
self.check_gl_entries()
```

## Next Steps


---

*Source: test_journal_entry.py:314 | Complexity: Advanced | Last updated: 2026-02-03*