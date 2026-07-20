# How To: Monthly Budget On Cancellation1

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test monthly budget on cancellation1

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
budget = make_budget(budget_against='Cost Center', do_not_save=False, submit_budget=True)
```

### Step 3: Assign month = value

```python
month = now_datetime().month
```

### Step 4: Call frappe.db.set_value()

```python
frappe.db.set_value('Budget', budget.name, 'action_if_accumulated_monthly_budget_exceeded', 'Stop')
```

### Step 5: Call self.assertRaises()

```python
self.assertRaises(BudgetError, jv.cancel)
```

### Step 6: Call budget.load_from_db()

```python
budget.load_from_db()
```

### Step 7: Call budget.cancel()

```python
budget.cancel()
```

### Step 8: Assign month = 9

```python
month = 9
```

### Step 9: Assign jv = make_journal_entry(...)

```python
jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 20000, '_Test Cost Center - _TC', posting_date=nowdate(), submit=True)
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(frappe.db.get_value('GL Entry', {'voucher_type': 'Journal Entry', 'voucher_no': jv.name}))
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
budget = make_budget(budget_against='Cost Center', do_not_save=False, submit_budget=True)
month = now_datetime().month
if month > 9:
    month = 9
for _i in range(month + 1):
    jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 20000, '_Test Cost Center - _TC', posting_date=nowdate(), submit=True)
    self.assertTrue(frappe.db.get_value('GL Entry', {'voucher_type': 'Journal Entry', 'voucher_no': jv.name}))
frappe.db.set_value('Budget', budget.name, 'action_if_accumulated_monthly_budget_exceeded', 'Stop')
self.assertRaises(BudgetError, jv.cancel)
budget.load_from_db()
budget.cancel()
```

## Next Steps


---

*Source: test_budget.py:242 | Complexity: Advanced | Last updated: 2026-02-03*