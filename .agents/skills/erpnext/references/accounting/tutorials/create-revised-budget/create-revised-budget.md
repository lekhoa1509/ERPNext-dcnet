# How To: Create Revised Budget

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test create revised budget

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
budget = make_budget(budget_against='Cost Center', budget_amount=120000, do_not_save=False, submit_budget=True)
```

### Step 2: Assign revised_name = revise_budget(...)

```python
revised_name = revise_budget(budget.name)
```

### Step 3: Assign revised_budget = frappe.get_doc(...)

```python
revised_budget = frappe.get_doc('Budget', revised_name)
```

### Step 4: Call self.assertNotEqual()

```python
self.assertNotEqual(budget.name, revised_budget.name)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(revised_budget.budget_against, budget.budget_against)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(revised_budget.budget_amount, budget.budget_amount)
```

### Step 7: Assign old_budget = frappe.get_doc(...)

```python
old_budget = frappe.get_doc('Budget', budget.name)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(old_budget.docstatus, 2)
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
budget = make_budget(budget_against='Cost Center', budget_amount=120000, do_not_save=False, submit_budget=True)
revised_name = revise_budget(budget.name)
revised_budget = frappe.get_doc('Budget', revised_name)
self.assertNotEqual(budget.name, revised_budget.name)
self.assertEqual(revised_budget.budget_against, budget.budget_against)
self.assertEqual(revised_budget.budget_amount, budget.budget_amount)
old_budget = frappe.get_doc('Budget', budget.name)
self.assertEqual(old_budget.docstatus, 2)
```

## Next Steps


---

*Source: test_budget.py:494 | Complexity: Advanced | Last updated: 2026-02-03*