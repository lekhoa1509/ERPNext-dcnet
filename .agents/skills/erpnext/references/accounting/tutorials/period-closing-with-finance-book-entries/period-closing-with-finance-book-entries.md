# How To: Period Closing With Finance Book Entries

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test period closing with finance book entries

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.finance_book.test_finance_book`
- `erpnext.accounts.doctype.journal_entry.test_journal_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.utils`


## Step-by-Step Guide

### Step 1: Call frappe.db.sql()

```python
frappe.db.sql("delete from `tabGL Entry` where company='Test PCV Company'")
```

### Step 2: Call frappe.db.sql()

```python
frappe.db.sql("delete from `tabPeriod Closing Voucher` where company='Test PCV Company'")
```

### Step 3: Assign company = create_company(...)

```python
company = create_company()
```

### Step 4: Assign surplus_account = create_account(...)

```python
surplus_account = create_account()
```

### Step 5: Assign cost_center = create_cost_center(...)

```python
cost_center = create_cost_center('Test Cost Center 1')
```

### Step 6: Call create_sales_invoice()

```python
create_sales_invoice(company=company, income_account='Sales - TPC', expense_account='Cost of Goods Sold - TPC', cost_center=cost_center, rate=400, debit_to='Debtors - TPC', currency='USD', customer='_Test Customer USD', posting_date='2021-03-15')
```

### Step 7: Assign jv = make_journal_entry(...)

```python
jv = make_journal_entry(account1='Cash - TPC', account2='Sales - TPC', amount=400, cost_center=cost_center, posting_date='2021-03-15', company=company)
```

### Step 8: Assign jv.company = company

```python
jv.company = company
```

### Step 9: Assign jv.finance_book = value

```python
jv.finance_book = create_finance_book().name
```

### Step 10: Call jv.save()

```python
jv.save()
```

### Step 11: Call jv.submit()

```python
jv.submit()
```

### Step 12: Assign pcv = self.make_period_closing_voucher(...)

```python
pcv = self.make_period_closing_voucher(posting_date='2021-03-31')
```

### Step 13: Assign surplus_account = value

```python
surplus_account = pcv.closing_account_head
```

### Step 14: Assign expected_gle = value

```python
expected_gle = ((surplus_account, 0.0, 400.0, None), (surplus_account, 0.0, 400.0, jv.finance_book), ('Sales - TPC', 400.0, 0.0, None), ('Sales - TPC', 400.0, 0.0, jv.finance_book))
```

### Step 15: Assign pcv_gle = frappe.db.sql(...)

```python
pcv_gle = frappe.db.sql('\n\t\t\tselect account, debit, credit, finance_book\n\t\t\tfrom `tabGL Entry` where voucher_no=%s\n\t\t\torder by account, finance_book\n\t\t', pcv.name)
```

### Step 16: Call self.assertSequenceEqual()

```python
self.assertSequenceEqual(pcv_gle, expected_gle)
```


## Complete Example

```python
# Workflow
frappe.db.sql("delete from `tabGL Entry` where company='Test PCV Company'")
frappe.db.sql("delete from `tabPeriod Closing Voucher` where company='Test PCV Company'")
company = create_company()
surplus_account = create_account()
cost_center = create_cost_center('Test Cost Center 1')
create_sales_invoice(company=company, income_account='Sales - TPC', expense_account='Cost of Goods Sold - TPC', cost_center=cost_center, rate=400, debit_to='Debtors - TPC', currency='USD', customer='_Test Customer USD', posting_date='2021-03-15')
jv = make_journal_entry(account1='Cash - TPC', account2='Sales - TPC', amount=400, cost_center=cost_center, posting_date='2021-03-15', company=company)
jv.company = company
jv.finance_book = create_finance_book().name
jv.save()
jv.submit()
pcv = self.make_period_closing_voucher(posting_date='2021-03-31')
surplus_account = pcv.closing_account_head
expected_gle = ((surplus_account, 0.0, 400.0, None), (surplus_account, 0.0, 400.0, jv.finance_book), ('Sales - TPC', 400.0, 0.0, None), ('Sales - TPC', 400.0, 0.0, jv.finance_book))
pcv_gle = frappe.db.sql('\n\t\t\tselect account, debit, credit, finance_book\n\t\t\tfrom `tabGL Entry` where voucher_no=%s\n\t\t\torder by account, finance_book\n\t\t', pcv.name)
self.assertSequenceEqual(pcv_gle, expected_gle)
```

## Next Steps


---

*Source: test_period_closing_voucher.py:137 | Complexity: Advanced | Last updated: 2026-02-03*