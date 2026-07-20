# How To: Monthly Budget Crossed Stop2

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test monthly budget crossed stop2

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.utils`
- `erpnext.accounts.doctype.budget.budget`
- `erpnext.accounts.doctype.journal_entry.test_journal_entry`
- `erpnext.accounts.utils`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.tests.utils`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.accounts.doctype.cost_center_allocation.test_cost_center_allocation`


## Step-by-Step Guide

### Step 1: Call set_total_expense_zero()

```python
set_total_expense_zero(nowdate(), 'project')
```

### Step 2: Assign budget = make_budget(...)

```python
budget = make_budget(budget_against='Project', do_not_save=False, submit_budget=True)
```

### Step 3: Call frappe.db.set_value()

```python
frappe.db.set_value('Budget', budget.name, 'action_if_accumulated_monthly_budget_exceeded', 'Stop')
```

### Step 4: Assign project = frappe.get_value(...)

```python
project = frappe.get_value('Project', {'project_name': '_Test Project'})
```

### Step 5: Assign accumulated_limit = get_accumulated_monthly_budget(...)

```python
accumulated_limit = get_accumulated_monthly_budget(budget.name, nowdate())
```

### Step 6: Assign jv = make_journal_entry(...)

```python
jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', accumulated_limit + 1, '_Test Cost Center - _TC', project=project, posting_date=nowdate())
```

### Step 7: Call self.assertRaises()

```python
self.assertRaises(BudgetError, jv.submit)
```

### Step 8: Call budget.load_from_db()

```python
budget.load_from_db()
```

### Step 9: Call budget.cancel()

```python
budget.cancel()
```


## Complete Example

```python
# Workflow
set_total_expense_zero(nowdate(), 'project')
budget = make_budget(budget_against='Project', do_not_save=False, submit_budget=True)
frappe.db.set_value('Budget', budget.name, 'action_if_accumulated_monthly_budget_exceeded', 'Stop')
project = frappe.get_value('Project', {'project_name': '_Test Project'})
accumulated_limit = get_accumulated_monthly_budget(budget.name, nowdate())
jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', accumulated_limit + 1, '_Test Cost Center - _TC', project=project, posting_date=nowdate())
self.assertRaises(BudgetError, jv.submit)
budget.load_from_db()
budget.cancel()
```

## Next Steps


---

*Source: test_budget.py:179 | Complexity: Advanced | Last updated: 2026-02-03*