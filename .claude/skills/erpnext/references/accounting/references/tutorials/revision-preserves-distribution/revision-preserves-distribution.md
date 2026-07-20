# How To: Revision Preserves Distribution

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test revision preserves distribution

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
set_total_expense_zero(nowdate(), 'cost_center', '_Test Cost Center - _TC')
```

### Step 2: Assign budget = make_budget(...)

```python
budget = make_budget(budget_against='Cost Center', budget_amount=120000, do_not_save=False, submit_budget=True)
```

### Step 3: Assign revised_name = revise_budget(...)

```python
revised_name = revise_budget(budget.name)
```

### Step 4: Assign revised_budget = frappe.get_doc(...)

```python
revised_budget = frappe.get_doc('Budget', revised_name)
```

### Step 5: Call self.assertGreater()

```python
self.assertGreater(len(revised_budget.budget_distribution), 0)
```

### Step 6: Assign total = sum(...)

```python
total = sum((row.amount for row in revised_budget.budget_distribution))
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(total, revised_budget.budget_amount)
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
set_total_expense_zero(nowdate(), 'cost_center', '_Test Cost Center - _TC')
budget = make_budget(budget_against='Cost Center', budget_amount=120000, do_not_save=False, submit_budget=True)
revised_name = revise_budget(budget.name)
revised_budget = frappe.get_doc('Budget', revised_name)
self.assertGreater(len(revised_budget.budget_distribution), 0)
total = sum((row.amount for row in revised_budget.budget_distribution))
self.assertEqual(total, revised_budget.budget_amount)
```

## Next Steps


---

*Source: test_budget.py:509 | Complexity: Intermediate | Last updated: 2026-02-03*