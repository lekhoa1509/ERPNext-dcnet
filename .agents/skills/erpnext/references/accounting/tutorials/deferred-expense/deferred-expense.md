# How To: Deferred Expense

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test deferred expense

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
self.create_item('_Test Office Desk', 0, self.warehouse, self.company)
```

### Step 2: Assign item = frappe.get_doc(...)

```python
item = frappe.get_doc('Item', self.item)
```

### Step 3: Assign item.enable_deferred_expense = 1

```python
item.enable_deferred_expense = 1
```

### Step 4: Assign unknown.deferred_expense_account = value

```python
item.item_defaults[0].deferred_expense_account = self.deferred_expense_account
```

### Step 5: Assign item.no_of_months_exp = 3

```python
item.no_of_months_exp = 3
```

### Step 6: Call item.save()

```python
item.save()
```

### Step 7: Assign pi = make_purchase_invoice(...)

```python
pi = make_purchase_invoice(item=self.item, company=self.company, supplier=self.supplier, is_return=False, update_stock=False, posting_date=frappe.utils.datetime.date(2021, 5, 1), parent_cost_center=self.cost_center, cost_center=self.cost_center, do_not_save=True, rate=300, price_list_rate=300, warehouse=self.warehouse, qty=1)
```

### Step 8: Assign pi.set_posting_time = True

```python
pi.set_posting_time = True
```

### Step 9: Assign unknown.enable_deferred_expense = 1

```python
pi.items[0].enable_deferred_expense = 1
```

### Step 10: Assign unknown.service_start_date = '2021-05-01'

```python
pi.items[0].service_start_date = '2021-05-01'
```

### Step 11: Assign unknown.service_end_date = '2021-08-01'

```python
pi.items[0].service_end_date = '2021-08-01'
```

### Step 12: Assign unknown.deferred_expense_account = value

```python
pi.items[0].deferred_expense_account = self.deferred_expense_account
```

### Step 13: Assign unknown.expense_account = value

```python
pi.items[0].expense_account = self.expense_account
```

### Step 14: Call pi.save()

```python
pi.save()
```

### Step 15: Call pi.submit()

```python
pi.submit()
```

### Step 16: Assign pda = frappe.get_doc(...)

```python
pda = frappe.get_doc(doctype='Process Deferred Accounting', posting_date=nowdate(), start_date='2021-05-01', end_date='2021-08-01', type='Expense', company=self.company)
```

### Step 17: Call pda.insert()

```python
pda.insert()
```

### Step 18: Call pda.submit()

```python
pda.submit()
```

### Step 19: Assign fiscal_year = frappe.get_doc(...)

```python
fiscal_year = frappe.get_doc('Fiscal Year', get_fiscal_year(date='2021-05-01')[0])
```

### Step 20: Assign self.filters = frappe._dict(...)

```python
self.filters = frappe._dict({'company': self.company, 'filter_based_on': 'Date Range', 'period_start_date': '2021-05-01', 'period_end_date': '2021-08-01', 'from_fiscal_year': fiscal_year.year, 'to_fiscal_year': fiscal_year.year, 'periodicity': 'Monthly', 'type': 'Expense', 'with_upcoming_postings': False})
```

### Step 21: Assign report = Deferred_Revenue_and_Expense_Report(...)

```python
report = Deferred_Revenue_and_Expense_Report(filters=self.filters)
```

### Step 22: Call report.run()

```python
report.run()
```

### Step 23: Assign expected = value

```python
expected = [{'key': 'may_2021', 'total': -100.0, 'actual': -100.0}, {'key': 'jun_2021', 'total': -100.0, 'actual': -100.0}, {'key': 'jul_2021', 'total': -100.0, 'actual': -100.0}, {'key': 'aug_2021', 'total': 0, 'actual': 0}]
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(report.period_total, expected)
```


## Complete Example

```python
# Workflow
self.create_item('_Test Office Desk', 0, self.warehouse, self.company)
item = frappe.get_doc('Item', self.item)
item.enable_deferred_expense = 1
item.item_defaults[0].deferred_expense_account = self.deferred_expense_account
item.no_of_months_exp = 3
item.save()
pi = make_purchase_invoice(item=self.item, company=self.company, supplier=self.supplier, is_return=False, update_stock=False, posting_date=frappe.utils.datetime.date(2021, 5, 1), parent_cost_center=self.cost_center, cost_center=self.cost_center, do_not_save=True, rate=300, price_list_rate=300, warehouse=self.warehouse, qty=1)
pi.set_posting_time = True
pi.items[0].enable_deferred_expense = 1
pi.items[0].service_start_date = '2021-05-01'
pi.items[0].service_end_date = '2021-08-01'
pi.items[0].deferred_expense_account = self.deferred_expense_account
pi.items[0].expense_account = self.expense_account
pi.save()
pi.submit()
pda = frappe.get_doc(doctype='Process Deferred Accounting', posting_date=nowdate(), start_date='2021-05-01', end_date='2021-08-01', type='Expense', company=self.company)
pda.insert()
pda.submit()
fiscal_year = frappe.get_doc('Fiscal Year', get_fiscal_year(date='2021-05-01')[0])
self.filters = frappe._dict({'company': self.company, 'filter_based_on': 'Date Range', 'period_start_date': '2021-05-01', 'period_end_date': '2021-08-01', 'from_fiscal_year': fiscal_year.year, 'to_fiscal_year': fiscal_year.year, 'periodicity': 'Monthly', 'type': 'Expense', 'with_upcoming_postings': False})
report = Deferred_Revenue_and_Expense_Report(filters=self.filters)
report.run()
expected = [{'key': 'may_2021', 'total': -100.0, 'actual': -100.0}, {'key': 'jun_2021', 'total': -100.0, 'actual': -100.0}, {'key': 'jul_2021', 'total': -100.0, 'actual': -100.0}, {'key': 'aug_2021', 'total': 0, 'actual': 0}]
self.assertEqual(report.period_total, expected)
```

## Next Steps


---

*Source: test_deferred_revenue_and_expense.py:141 | Complexity: Advanced | Last updated: 2026-02-03*