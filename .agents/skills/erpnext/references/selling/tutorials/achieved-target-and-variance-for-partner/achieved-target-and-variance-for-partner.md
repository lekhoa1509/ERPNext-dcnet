# How To: Achieved Target And Variance For Partner

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test achieved target and variance for partner

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.utils`
- `erpnext.selling.report.sales_partner_target_variance_based_on_item_group.sales_partner_target_variance_based_on_item_group`
- `erpnext.selling.report.sales_person_target_variance_based_on_item_group.test_sales_person_target_variance_based_on_item_group`


## Step-by-Step Guide

### Step 1: Assign distribution = create_target_distribution(...)

```python
distribution = create_target_distribution(self.fiscal_year)
```

### Step 2: Assign sales_partner = create_sales_target_doc(...)

```python
sales_partner = create_sales_target_doc('Sales Partner', 'partner_name', 'Sales Partner 1', self.fiscal_year, distribution.name)
```

### Step 3: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(rate=1000, qty=20, do_not_submit=True)
```

### Step 4: Assign si.sales_partner = value

```python
si.sales_partner = sales_partner.name
```

### Step 5: Assign si.commission_rate = 5

```python
si.commission_rate = 5
```

### Step 6: Call si.submit()

```python
si.submit()
```

### Step 7: Assign result = value

```python
result = execute(frappe._dict({'fiscal_year': self.fiscal_year, 'doctype': 'Sales Invoice', 'period': 'Yearly', 'target_on': 'Quantity'}))[1]
```

### Step 8: Assign row = frappe._dict(...)

```python
row = frappe._dict(result[0])
```

### Step 9: Call self.assertSequenceEqual()

```python
self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 20, -30])
```


## Complete Example

```python
# Workflow
distribution = create_target_distribution(self.fiscal_year)
sales_partner = create_sales_target_doc('Sales Partner', 'partner_name', 'Sales Partner 1', self.fiscal_year, distribution.name)
si = create_sales_invoice(rate=1000, qty=20, do_not_submit=True)
si.sales_partner = sales_partner.name
si.commission_rate = 5
si.submit()
result = execute(frappe._dict({'fiscal_year': self.fiscal_year, 'doctype': 'Sales Invoice', 'period': 'Yearly', 'target_on': 'Quantity'}))[1]
row = frappe._dict(result[0])
self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 20, -30])
```

## Next Steps


---

*Source: test_sales_partner_target_variance_based_on_item_group.py:23 | Complexity: Advanced | Last updated: 2026-02-04*