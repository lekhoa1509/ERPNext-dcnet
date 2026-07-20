# How To: Duplicate Budget Validation

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test duplicate budget validation

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

### Step 1: Assign budget = make_budget(...)

```python
budget = make_budget(budget_against='Cost Center', distribute_equally=1, budget_amount=15000, do_not_save=False, submit_budget=True)
```

### Step 2: Assign new_budget = frappe.new_doc(...)

```python
new_budget = frappe.new_doc('Budget')
```

### Step 3: Assign new_budget.company = '_Test Company'

```python
new_budget.company = '_Test Company'
```

### Step 4: Assign new_budget.from_fiscal_year = value

```python
new_budget.from_fiscal_year = budget.from_fiscal_year
```

### Step 5: Assign new_budget.to_fiscal_year = value

```python
new_budget.to_fiscal_year = new_budget.from_fiscal_year
```

### Step 6: Assign new_budget.budget_against = 'Cost Center'

```python
new_budget.budget_against = 'Cost Center'
```

### Step 7: Assign new_budget.cost_center = '_Test Cost Center - _TC'

```python
new_budget.cost_center = '_Test Cost Center - _TC'
```

### Step 8: Assign new_budget.account = '_Test Account Cost for Goods Sold - _TC'

```python
new_budget.account = '_Test Account Cost for Goods Sold - _TC'
```

### Step 9: Assign new_budget.budget_amount = 10000

```python
new_budget.budget_amount = 10000
```

### Step 10: Call new_budget.insert()

```python
new_budget.insert()
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
budget = make_budget(budget_against='Cost Center', distribute_equally=1, budget_amount=15000, do_not_save=False, submit_budget=True)
new_budget = frappe.new_doc('Budget')
new_budget.company = '_Test Company'
new_budget.from_fiscal_year = budget.from_fiscal_year
new_budget.to_fiscal_year = new_budget.from_fiscal_year
new_budget.budget_against = 'Cost Center'
new_budget.cost_center = '_Test Cost Center - _TC'
new_budget.account = '_Test Account Cost for Goods Sold - _TC'
new_budget.budget_amount = 10000
with self.assertRaises(frappe.ValidationError):
    new_budget.insert()
```

## Next Steps


---

*Source: test_budget.py:585 | Complexity: Advanced | Last updated: 2026-02-03*