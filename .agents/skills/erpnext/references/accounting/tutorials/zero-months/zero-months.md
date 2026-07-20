# How To: Zero Months

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test zero months

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.report.deferred_revenue_and_expense.deferred_revenue_and_expense`
- `erpnext.accounts.test.accounts_mixin`
- `erpnext.accounts.utils`


## Step-by-Step Guide

### Step 1: Call self.create_item()

```python
self.create_item('_Test Internet Subscription', 0, self.warehouse, self.company)
```

### Step 2: Assign item = frappe.get_doc(...)

```python
item = frappe.get_doc('Item', self.item)
```

### Step 3: Assign item.enable_deferred_revenue = 1

```python
item.enable_deferred_revenue = 1
```

### Step 4: Assign item.deferred_revenue_account = value

```python
item.deferred_revenue_account = self.deferred_revenue_account
```

### Step 5: Assign item.no_of_months = 0

```python
item.no_of_months = 0
```

### Step 6: Call item.save()

```python
item.save()
```

### Step 7: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(item=item.name, company=self.company, customer=self.customer, debit_to=self.debit_to, posting_date='2021-05-01', parent_cost_center=self.cost_center, cost_center=self.cost_center, do_not_save=True, rate=300, price_list_rate=300)
```

### Step 8: Assign unknown.enable_deferred_revenue = 1

```python
si.items[0].enable_deferred_revenue = 1
```

### Step 9: Assign unknown.income_account = value

```python
si.items[0].income_account = self.income_account
```

### Step 10: Assign unknown.deferred_revenue_account = value

```python
si.items[0].deferred_revenue_account = self.deferred_revenue_account
```

### Step 11: Call si.save()

```python
si.save()
```

### Step 12: Call si.submit()

```python
si.submit()
```

### Step 13: Assign pda = frappe.get_doc(...)

```python
pda = frappe.get_doc(doctype='Process Deferred Accounting', posting_date=nowdate(), start_date='2021-05-01', end_date='2021-08-01', type='Income', company=self.company)
```

### Step 14: Call pda.insert()

```python
pda.insert()
```

### Step 15: Call pda.submit()

```python
pda.submit()
```

### Step 16: Assign fiscal_year = frappe.get_doc(...)

```python
fiscal_year = frappe.get_doc('Fiscal Year', get_fiscal_year(date='2021-05-01')[0])
```

### Step 17: Assign self.filters = frappe._dict(...)

```python
self.filters = frappe._dict({'company': self.company, 'filter_based_on': 'Date Range', 'period_start_date': '2021-05-01', 'period_end_date': '2021-08-01', 'from_fiscal_year': fiscal_year.year, 'to_fiscal_year': fiscal_year.year, 'periodicity': 'Monthly', 'type': 'Revenue', 'with_upcoming_postings': False})
```

### Step 18: Assign report = Deferred_Revenue_and_Expense_Report(...)

```python
report = Deferred_Revenue_and_Expense_Report(filters=self.filters)
```

### Step 19: Call report.run()

```python
report.run()
```

### Step 20: Assign expected = value

```python
expected = [{'key': 'may_2021', 'total': 300.0, 'actual': 300.0}, {'key': 'jun_2021', 'total': 0, 'actual': 0}, {'key': 'jul_2021', 'total': 0, 'actual': 0}, {'key': 'aug_2021', 'total': 0, 'actual': 0}]
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(report.period_total, expected)
```


## Complete Example

```python
# Workflow
self.create_item('_Test Internet Subscription', 0, self.warehouse, self.company)
item = frappe.get_doc('Item', self.item)
item.enable_deferred_revenue = 1
item.deferred_revenue_account = self.deferred_revenue_account
item.no_of_months = 0
item.save()
si = create_sales_invoice(item=item.name, company=self.company, customer=self.customer, debit_to=self.debit_to, posting_date='2021-05-01', parent_cost_center=self.cost_center, cost_center=self.cost_center, do_not_save=True, rate=300, price_list_rate=300)
si.items[0].enable_deferred_revenue = 1
si.items[0].income_account = self.income_account
si.items[0].deferred_revenue_account = self.deferred_revenue_account
si.save()
si.submit()
pda = frappe.get_doc(doctype='Process Deferred Accounting', posting_date=nowdate(), start_date='2021-05-01', end_date='2021-08-01', type='Income', company=self.company)
pda.insert()
pda.submit()
fiscal_year = frappe.get_doc('Fiscal Year', get_fiscal_year(date='2021-05-01')[0])
self.filters = frappe._dict({'company': self.company, 'filter_based_on': 'Date Range', 'period_start_date': '2021-05-01', 'period_end_date': '2021-08-01', 'from_fiscal_year': fiscal_year.year, 'to_fiscal_year': fiscal_year.year, 'periodicity': 'Monthly', 'type': 'Revenue', 'with_upcoming_postings': False})
report = Deferred_Revenue_and_Expense_Report(filters=self.filters)
report.run()
expected = [{'key': 'may_2021', 'total': 300.0, 'actual': 300.0}, {'key': 'jun_2021', 'total': 0, 'actual': 0}, {'key': 'jul_2021', 'total': 0, 'actual': 0}, {'key': 'aug_2021', 'total': 0, 'actual': 0}]
self.assertEqual(report.period_total, expected)
```

## Next Steps


---

*Source: test_deferred_revenue_and_expense.py:211 | Complexity: Advanced | Last updated: 2026-02-03*