# How To: Action For Cumulative Limit

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test action for cumulative limit

## Prerequisites

- [ ] Setup code must be executed first

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

**Setup Required:**
```python
frappe.db.set_single_value('Accounts Settings', 'use_legacy_budget_controller', False)
self.company = '_Test Company'
self.fiscal_year = frappe.db.get_value('Fiscal Year', {}, 'name')
self.account = '_Test Account Cost for Goods Sold - _TC'
self.cost_center = '_Test Cost Center - _TC'
```

## Step-by-Step Guide

### Step 1: Call set_total_expense_zero()

```python
set_total_expense_zero(nowdate(), 'cost_center')
```

### Step 2: Assign budget = make_budget(...)

```python
budget = make_budget(budget_against='Cost Center', applicable_on_cumulative_expense=True, do_not_save=False, submit_budget=True)
```

### Step 3: Assign accumulated_limit = get_accumulated_monthly_budget(...)

```python
accumulated_limit = get_accumulated_monthly_budget(budget.name, nowdate())
```

### Step 4: Assign jv = make_journal_entry(...)

```python
jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', accumulated_limit - 1, '_Test Cost Center - _TC', posting_date=nowdate())
```

### Step 5: Call jv.submit()

```python
jv.submit()
```

### Step 6: Call frappe.db.set_value()

```python
frappe.db.set_value('Budget', budget.name, 'action_if_accumulated_monthly_exceeded_on_cumulative_expense', 'Stop')
```

### Step 7: Assign po = create_purchase_order(...)

```python
po = create_purchase_order(transaction_date=nowdate(), qty=1, rate=accumulated_limit + 1, do_not_submit=True)
```

### Step 8: Call po.set_missing_values()

```python
po.set_missing_values()
```

### Step 9: Call self.assertRaises()

```python
self.assertRaises(BudgetError, po.submit)
```

### Step 10: Call frappe.db.set_value()

```python
frappe.db.set_value('Budget', budget.name, 'action_if_accumulated_monthly_exceeded_on_cumulative_expense', 'Ignore')
```

### Step 11: Call po.submit()

```python
po.submit()
```

### Step 12: Call budget.load_from_db()

```python
budget.load_from_db()
```

### Step 13: Call budget.cancel()

```python
budget.cancel()
```

### Step 14: Call po.cancel()

```python
po.cancel()
```

### Step 15: Call jv.cancel()

```python
jv.cancel()
```


## Complete Example

```python
# Setup
frappe.db.set_single_value('Accounts Settings', 'use_legacy_budget_controller', False)
self.company = '_Test Company'
self.fiscal_year = frappe.db.get_value('Fiscal Year', {}, 'name')
self.account = '_Test Account Cost for Goods Sold - _TC'
self.cost_center = '_Test Cost Center - _TC'

# Workflow
set_total_expense_zero(nowdate(), 'cost_center')
budget = make_budget(budget_against='Cost Center', applicable_on_cumulative_expense=True, do_not_save=False, submit_budget=True)
accumulated_limit = get_accumulated_monthly_budget(budget.name, nowdate())
jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', accumulated_limit - 1, '_Test Cost Center - _TC', posting_date=nowdate())
jv.submit()
frappe.db.set_value('Budget', budget.name, 'action_if_accumulated_monthly_exceeded_on_cumulative_expense', 'Stop')
po = create_purchase_order(transaction_date=nowdate(), qty=1, rate=accumulated_limit + 1, do_not_submit=True)
po.set_missing_values()
self.assertRaises(BudgetError, po.submit)
frappe.db.set_value('Budget', budget.name, 'action_if_accumulated_monthly_exceeded_on_cumulative_expense', 'Ignore')
po.submit()
budget.load_from_db()
budget.cancel()
po.cancel()
jv.cancel()
```

## Next Steps


---

*Source: test_budget.py:406 | Complexity: Advanced | Last updated: 2026-02-03*