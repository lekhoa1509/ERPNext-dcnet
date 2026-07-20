# How To: Offsetting Entries For Accounting Dimensions

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Checks if Trial Balance Report is balanced when filtered using a particular Accounting Dimension

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.report.trial_balance.trial_balance`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.accounts.utils`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`


## Step-by-Step Guide

### Step 1: '\n\t\tChecks if Trial Balance Report is balanced when filtered using a particular Accounting Dimension\n\t\t'

```python
'\n\t\tChecks if Trial Balance Report is balanced when filtered using a particular Accounting Dimension\n\t\t'
```

### Step 2: Call frappe.db.sql()

```python
frappe.db.sql("delete from `tabSales Invoice` where company='Trial Balance Company'")
```

### Step 3: Call frappe.db.sql()

```python
frappe.db.sql("delete from `tabGL Entry` where company='Trial Balance Company'")
```

### Step 4: Assign branch1 = frappe.new_doc(...)

```python
branch1 = frappe.new_doc('Branch')
```

### Step 5: Assign branch1.branch = 'Location 1'

```python
branch1.branch = 'Location 1'
```

### Step 6: Call branch1.insert()

```python
branch1.insert(ignore_if_duplicate=True)
```

### Step 7: Assign branch2 = frappe.new_doc(...)

```python
branch2 = frappe.new_doc('Branch')
```

### Step 8: Assign branch2.branch = 'Location 2'

```python
branch2.branch = 'Location 2'
```

### Step 9: Call branch2.insert()

```python
branch2.insert(ignore_if_duplicate=True)
```

### Step 10: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(company=self.company, debit_to='Debtors - TBC', cost_center='Test Cost Center - TBC', income_account='Sales - TBC', do_not_submit=1)
```

### Step 11: Assign si.branch = 'Location 1'

```python
si.branch = 'Location 1'
```

### Step 12: Assign unknown.branch = 'Location 2'

```python
si.items[0].branch = 'Location 2'
```

### Step 13: Call si.save()

```python
si.save()
```

### Step 14: Call si.submit()

```python
si.submit()
```

### Step 15: Assign filters = frappe._dict(...)

```python
filters = frappe._dict({'company': self.company, 'fiscal_year': self.fiscal_year, 'branch': ['Location 1']})
```

### Step 16: Assign total_row = value

```python
total_row = execute(filters)[1][-1]
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(total_row['debit'], total_row['credit'])
```


## Complete Example

```python
# Workflow
'\n\t\tChecks if Trial Balance Report is balanced when filtered using a particular Accounting Dimension\n\t\t'
from erpnext.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
frappe.db.sql("delete from `tabSales Invoice` where company='Trial Balance Company'")
frappe.db.sql("delete from `tabGL Entry` where company='Trial Balance Company'")
branch1 = frappe.new_doc('Branch')
branch1.branch = 'Location 1'
branch1.insert(ignore_if_duplicate=True)
branch2 = frappe.new_doc('Branch')
branch2.branch = 'Location 2'
branch2.insert(ignore_if_duplicate=True)
si = create_sales_invoice(company=self.company, debit_to='Debtors - TBC', cost_center='Test Cost Center - TBC', income_account='Sales - TBC', do_not_submit=1)
si.branch = 'Location 1'
si.items[0].branch = 'Location 2'
si.save()
si.submit()
filters = frappe._dict({'company': self.company, 'fiscal_year': self.fiscal_year, 'branch': ['Location 1']})
total_row = execute(filters)[1][-1]
self.assertEqual(total_row['debit'], total_row['credit'])
```

## Next Steps


---

*Source: test_trial_balance.py:31 | Complexity: Advanced | Last updated: 2026-02-03*