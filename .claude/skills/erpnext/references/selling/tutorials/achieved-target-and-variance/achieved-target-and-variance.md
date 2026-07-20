# How To: Achieved Target And Variance

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test achieved target and variance

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.utils`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.selling.report.sales_person_target_variance_based_on_item_group.sales_person_target_variance_based_on_item_group`


## Step-by-Step Guide

### Step 1: Assign distribution = create_target_distribution(...)

```python
distribution = create_target_distribution(self.fiscal_year)
```

### Step 2: Assign person_1 = create_sales_target_doc(...)

```python
person_1 = create_sales_target_doc('Sales Person', 'sales_person_name', 'Sales Person 1', self.fiscal_year, distribution.name)
```

### Step 3: Assign person_2 = create_sales_target_doc(...)

```python
person_2 = create_sales_target_doc('Sales Person', 'sales_person_name', 'Sales Person 2', self.fiscal_year, distribution.name)
```

### Step 4: Assign so = make_sales_order(...)

```python
so = make_sales_order(rate=1000, qty=20, do_not_submit=True)
```

### Step 5: Call so.set()

```python
so.set('sales_team', [{'sales_person': person_1.name, 'allocated_percentage': 50, 'allocated_amount': 10000}, {'sales_person': person_2.name, 'allocated_percentage': 50, 'allocated_amount': 10000}])
```

### Step 6: Call so.submit()

```python
so.submit()
```

### Step 7: Assign result = value

```python
result = execute(frappe._dict({'fiscal_year': self.fiscal_year, 'doctype': 'Sales Order', 'period': 'Yearly', 'target_on': 'Quantity'}))[1]
```

### Step 8: Assign row = frappe._dict(...)

```python
row = frappe._dict(result[0])
```

### Step 9: Call self.assertSequenceEqual()

```python
self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 10, -40])
```


## Complete Example

```python
# Workflow
distribution = create_target_distribution(self.fiscal_year)
person_1 = create_sales_target_doc('Sales Person', 'sales_person_name', 'Sales Person 1', self.fiscal_year, distribution.name)
person_2 = create_sales_target_doc('Sales Person', 'sales_person_name', 'Sales Person 2', self.fiscal_year, distribution.name)
so = make_sales_order(rate=1000, qty=20, do_not_submit=True)
so.set('sales_team', [{'sales_person': person_1.name, 'allocated_percentage': 50, 'allocated_amount': 10000}, {'sales_person': person_2.name, 'allocated_percentage': 50, 'allocated_amount': 10000}])
so.submit()
result = execute(frappe._dict({'fiscal_year': self.fiscal_year, 'doctype': 'Sales Order', 'period': 'Yearly', 'target_on': 'Quantity'}))[1]
row = frappe._dict(result[0])
self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 10, -40])
```

## Next Steps


---

*Source: test_sales_person_target_variance_based_on_item_group.py:19 | Complexity: Advanced | Last updated: 2026-02-04*