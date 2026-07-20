# How To: Gl Entries Restrictions

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test gl entries restrictions

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

### Step 4: Assign cost_center = create_cost_center(...)

```python
cost_center = create_cost_center('Test Cost Center 1')
```

### Step 5: Call self.make_period_closing_voucher()

```python
self.make_period_closing_voucher(posting_date='2021-03-31')
```

### Step 6: Assign jv1 = make_journal_entry(...)

```python
jv1 = make_journal_entry(posting_date='2021-03-15', amount=400, account1='Cash - TPC', account2='Sales - TPC', cost_center=cost_center, company=company, save=False)
```

### Step 7: Assign jv1.company = company

```python
jv1.company = company
```

### Step 8: Call jv1.save()

```python
jv1.save()
```

### Step 9: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, jv1.submit)
```


## Complete Example

```python
# Workflow
frappe.db.sql("delete from `tabGL Entry` where company='Test PCV Company'")
frappe.db.sql("delete from `tabPeriod Closing Voucher` where company='Test PCV Company'")
company = create_company()
cost_center = create_cost_center('Test Cost Center 1')
self.make_period_closing_voucher(posting_date='2021-03-31')
jv1 = make_journal_entry(posting_date='2021-03-15', amount=400, account1='Cash - TPC', account2='Sales - TPC', cost_center=cost_center, company=company, save=False)
jv1.company = company
jv1.save()
self.assertRaises(frappe.ValidationError, jv1.submit)
```

## Next Steps


---

*Source: test_period_closing_voucher.py:191 | Complexity: Advanced | Last updated: 2026-02-03*