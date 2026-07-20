# How To: Resolve Basic Processing Order

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test resolve basic processing order

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.utils`
- `erpnext.accounts.doctype.financial_report_template.financial_report_engine`
- `erpnext.accounts.doctype.financial_report_template.test_financial_report_template`
- `erpnext.accounts.utils`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`


## Step-by-Step Guide

### Step 1: Assign resolver = DependencyResolver(...)

```python
resolver = DependencyResolver(self.test_template)
```

### Step 2: Assign order = resolver.get_processing_order(...)

```python
order = resolver.get_processing_order()
```

### Step 3: Assign account_indices = value

```python
account_indices = [i for i, row in enumerate(order) if row.data_source == 'Account Data']
```

### Step 4: Assign formula_indices = value

```python
formula_indices = [i for i, row in enumerate(order) if row.data_source == 'Calculated Amount']
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(all((ai < fi for ai in account_indices for fi in formula_indices)))
```


## Complete Example

```python
# Workflow
resolver = DependencyResolver(self.test_template)
order = resolver.get_processing_order()
account_indices = [i for i, row in enumerate(order) if row.data_source == 'Account Data']
formula_indices = [i for i, row in enumerate(order) if row.data_source == 'Calculated Amount']
self.assertTrue(all((ai < fi for ai in account_indices for fi in formula_indices)))
```

## Next Steps


---

*Source: test_financial_report_engine.py:28 | Complexity: Intermediate | Last updated: 2026-02-03*