# How To: Monthly Budget Against Parent Group Cost Center

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test monthly budget against parent group cost center

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

### Step 1: Assign cost_center = '_Test Cost Center 3 - _TC'

```python
cost_center = '_Test Cost Center 3 - _TC'
```

### Step 2: Assign budget = make_budget(...)

```python
budget = make_budget(budget_against='Cost Center', cost_center=cost_center, do_not_save=False, submit_budget=True)
```

### Step 3: Call frappe.db.set_value()

```python
frappe.db.set_value('Budget', budget.name, 'action_if_accumulated_monthly_budget_exceeded', 'Stop')
```

### Step 4: Assign accumulated_limit = get_accumulated_monthly_budget(...)

```python
accumulated_limit = get_accumulated_monthly_budget(budget.name, nowdate())
```

### Step 5: Assign jv = make_journal_entry(...)

```python
jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', accumulated_limit + 1, cost_center, posting_date=nowdate())
```

### Step 6: Call self.assertRaises()

```python
self.assertRaises(BudgetError, jv.submit)
```

### Step 7: Call budget.load_from_db()

```python
budget.load_from_db()
```

### Step 8: Call budget.cancel()

```python
budget.cancel()
```

### Step 9: Call jv.cancel()

```python
jv.cancel()
```

### Step 10: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'Cost Center', 'cost_center_name': '_Test Cost Center 3', 'parent_cost_center': '_Test Company - _TC', 'company': '_Test Company', 'is_group': 0}).insert(ignore_permissions=True)
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
cost_center = '_Test Cost Center 3 - _TC'
if not frappe.db.exists('Cost Center', cost_center):
    frappe.get_doc({'doctype': 'Cost Center', 'cost_center_name': '_Test Cost Center 3', 'parent_cost_center': '_Test Company - _TC', 'company': '_Test Company', 'is_group': 0}).insert(ignore_permissions=True)
budget = make_budget(budget_against='Cost Center', cost_center=cost_center, do_not_save=False, submit_budget=True)
frappe.db.set_value('Budget', budget.name, 'action_if_accumulated_monthly_budget_exceeded', 'Stop')
accumulated_limit = get_accumulated_monthly_budget(budget.name, nowdate())
jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', accumulated_limit + 1, cost_center, posting_date=nowdate())
self.assertRaises(BudgetError, jv.submit)
budget.load_from_db()
budget.cancel()
jv.cancel()
```

## Next Steps


---

*Source: test_budget.py:331 | Complexity: Advanced | Last updated: 2026-02-03*