# How To: Profit And Loss Output And Summary

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test profit and loss output and summary

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.desk.query_report`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.report.financial_statements`
- `erpnext.accounts.report.profit_and_loss_statement.profit_and_loss_statement`
- `erpnext.accounts.test.accounts_mixin`


## Step-by-Step Guide

### Step 1: Call self.create_sales_invoice()

```python
self.create_sales_invoice(qty=1, rate=150)
```

### Step 2: Assign filters = self.get_report_filters(...)

```python
filters = self.get_report_filters()
```

### Step 3: Assign period_list = get_period_list(...)

```python
period_list = get_period_list(filters.from_fiscal_year, filters.to_fiscal_year, filters.period_start_date, filters.period_end_date, filters.filter_based_on, filters.periodicity, company=filters.company)
```

### Step 4: Assign result = value

```python
result = execute(filters)[1]
```

### Step 5: Assign current_period = next(...)

```python
current_period = next((x for x in period_list if x.from_date <= getdate() and x.to_date >= getdate()))
```

### Step 6: Assign current_period_key = value

```python
current_period_key = current_period.key
```

### Step 7: Assign without_current_period = value

```python
without_current_period = [x for x in period_list if x.key != current_period.key]
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(acc[current_period_key], 150)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(acc['total'], 150)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(acc[period.key], 0)
```


## Complete Example

```python
# Workflow
self.create_sales_invoice(qty=1, rate=150)
filters = self.get_report_filters()
period_list = get_period_list(filters.from_fiscal_year, filters.to_fiscal_year, filters.period_start_date, filters.period_end_date, filters.filter_based_on, filters.periodicity, company=filters.company)
result = execute(filters)[1]
current_period = next((x for x in period_list if x.from_date <= getdate() and x.to_date >= getdate()))
current_period_key = current_period.key
without_current_period = [x for x in period_list if x.key != current_period.key]
for acc in result:
    if acc:
        with self.subTest(acc=acc):
            for period in without_current_period:
                self.assertEqual(acc[period.key], 0)
for acc in result:
    if acc:
        with self.subTest(current_period_key=current_period_key):
            self.assertEqual(acc[current_period_key], 150)
            self.assertEqual(acc['total'], 150)
```

## Next Steps


---

*Source: test_profit_and_loss_statement.py:64 | Complexity: Advanced | Last updated: 2026-02-03*