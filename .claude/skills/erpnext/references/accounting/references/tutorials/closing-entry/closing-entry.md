# How To: Closing Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test closing entry

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

### Step 5: Assign jv1 = make_journal_entry(...)

```python
jv1 = make_journal_entry(posting_date='2021-03-15', amount=400, account1='Cash - TPC', account2='Sales - TPC', cost_center=cost_center, company=company, save=False)
```

### Step 6: Assign jv1.company = company

```python
jv1.company = company
```

### Step 7: Call jv1.save()

```python
jv1.save()
```

### Step 8: Call jv1.submit()

```python
jv1.submit()
```

### Step 9: Assign jv2 = make_journal_entry(...)

```python
jv2 = make_journal_entry(posting_date='2021-03-15', amount=600, account1='Cost of Goods Sold - TPC', account2='Cash - TPC', cost_center=cost_center, company=company, save=False)
```

### Step 10: Assign jv2.company = company

```python
jv2.company = company
```

### Step 11: Call jv2.save()

```python
jv2.save()
```

### Step 12: Call jv2.submit()

```python
jv2.submit()
```

### Step 13: Assign pcv = self.make_period_closing_voucher(...)

```python
pcv = self.make_period_closing_voucher(posting_date='2021-03-31')
```

### Step 14: Assign surplus_account = value

```python
surplus_account = pcv.closing_account_head
```

### Step 15: Assign expected_gle = value

```python
expected_gle = (('Cost of Goods Sold - TPC', 0.0, 600.0), (surplus_account, 200.0, 0.0), ('Sales - TPC', 400.0, 0.0))
```

### Step 16: Assign pcv_gle = frappe.db.sql(...)

```python
pcv_gle = frappe.db.sql('\n\t\t\tselect account, debit, credit from `tabGL Entry` where voucher_no=%s order by account\n\t\t', pcv.name)
```

### Step 17: Call pcv.reload()

```python
pcv.reload()
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(pcv.gle_processing_status, 'Completed')
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(pcv_gle, expected_gle)
```


## Complete Example

```python
# Workflow
frappe.db.sql("delete from `tabGL Entry` where company='Test PCV Company'")
frappe.db.sql("delete from `tabPeriod Closing Voucher` where company='Test PCV Company'")
company = create_company()
cost_center = create_cost_center('Test Cost Center 1')
jv1 = make_journal_entry(posting_date='2021-03-15', amount=400, account1='Cash - TPC', account2='Sales - TPC', cost_center=cost_center, company=company, save=False)
jv1.company = company
jv1.save()
jv1.submit()
jv2 = make_journal_entry(posting_date='2021-03-15', amount=600, account1='Cost of Goods Sold - TPC', account2='Cash - TPC', cost_center=cost_center, company=company, save=False)
jv2.company = company
jv2.save()
jv2.submit()
pcv = self.make_period_closing_voucher(posting_date='2021-03-31')
surplus_account = pcv.closing_account_head
expected_gle = (('Cost of Goods Sold - TPC', 0.0, 600.0), (surplus_account, 200.0, 0.0), ('Sales - TPC', 400.0, 0.0))
pcv_gle = frappe.db.sql('\n\t\t\tselect account, debit, credit from `tabGL Entry` where voucher_no=%s order by account\n\t\t', pcv.name)
pcv.reload()
self.assertEqual(pcv.gle_processing_status, 'Completed')
self.assertEqual(pcv_gle, expected_gle)
```

## Next Steps


---

*Source: test_period_closing_voucher.py:19 | Complexity: Advanced | Last updated: 2026-02-03*