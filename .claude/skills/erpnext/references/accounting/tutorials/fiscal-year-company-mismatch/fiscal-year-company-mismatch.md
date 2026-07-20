# How To: Fiscal Year Company Mismatch

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test fiscal year company mismatch

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
budget = make_budget(budget_against='Cost Center', do_not_save=True, submit_budget=False)
```

### Step 2: Assign fy = frappe.get_doc.insert(...)

```python
fy = frappe.get_doc({'doctype': 'Fiscal Year', 'year': '2099', 'year_start_date': '2099-04-01', 'year_end_date': '2100-03-31', 'companies': [{'company': '_Test Company 2'}]}).insert(ignore_permissions=True)
```

### Step 3: Assign budget.from_fiscal_year = value

```python
budget.from_fiscal_year = fy.name
```

### Step 4: Assign budget.to_fiscal_year = value

```python
budget.to_fiscal_year = fy.name
```

### Step 5: Assign budget.company = '_Test Company'

```python
budget.company = '_Test Company'
```

### Step 6: Call budget.save()

```python
budget.save()
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
budget = make_budget(budget_against='Cost Center', do_not_save=True, submit_budget=False)
fy = frappe.get_doc({'doctype': 'Fiscal Year', 'year': '2099', 'year_start_date': '2099-04-01', 'year_end_date': '2100-03-31', 'companies': [{'company': '_Test Company 2'}]}).insert(ignore_permissions=True)
budget.from_fiscal_year = fy.name
budget.to_fiscal_year = fy.name
budget.company = '_Test Company'
with self.assertRaises(frappe.ValidationError):
    budget.save()
```

## Next Steps


---

*Source: test_budget.py:549 | Complexity: Intermediate | Last updated: 2026-02-03*