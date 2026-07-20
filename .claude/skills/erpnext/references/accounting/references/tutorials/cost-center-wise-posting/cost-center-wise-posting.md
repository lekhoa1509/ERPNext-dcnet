# How To: Cost Center Wise Posting

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test cost center wise posting

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

### Step 5: Assign cost_center1 = create_cost_center(...)

```python
cost_center1 = create_cost_center('Main')
```

### Step 6: Assign cost_center2 = create_cost_center(...)

```python
cost_center2 = create_cost_center('Western Branch')
```

### Step 7: Call create_sales_invoice()

```python
create_sales_invoice(company=company, cost_center=cost_center1, income_account='Sales - TPC', expense_account='Cost of Goods Sold - TPC', rate=400, debit_to='Debtors - TPC', currency='USD', customer='_Test Customer USD', posting_date='2021-03-15')
```

### Step 8: Call create_sales_invoice()

```python
create_sales_invoice(company=company, cost_center=cost_center2, income_account='Sales - TPC', expense_account='Cost of Goods Sold - TPC', rate=200, debit_to='Debtors - TPC', currency='USD', customer='_Test Customer USD', posting_date='2021-03-15')
```

### Step 9: Assign pcv = self.make_period_closing_voucher(...)

```python
pcv = self.make_period_closing_voucher(posting_date='2021-03-31', submit=False)
```

### Step 10: Call pcv.save()

```python
pcv.save()
```

### Step 11: Call pcv.submit()

```python
pcv.submit()
```

### Step 12: Assign surplus_account = value

```python
surplus_account = pcv.closing_account_head
```

### Step 13: Assign expected_gle = value

```python
expected_gle = ((surplus_account, 0.0, 400.0, cost_center1), (surplus_account, 0.0, 200.0, cost_center2), ('Sales - TPC', 400.0, 0.0, cost_center1), ('Sales - TPC', 200.0, 0.0, cost_center2))
```

### Step 14: Assign pcv_gle = frappe.db.sql(...)

```python
pcv_gle = frappe.db.sql('\n\t\t\tselect account, debit, credit, cost_center\n\t\t\tfrom `tabGL Entry` where voucher_no=%s\n\t\t\torder by account, cost_center\n\t\t', pcv.name)
```

### Step 15: Call self.assertSequenceEqual()

```python
self.assertSequenceEqual(pcv_gle, expected_gle)
```

### Step 16: Call pcv.reload()

```python
pcv.reload()
```

### Step 17: Call pcv.cancel()

```python
pcv.cancel()
```

### Step 18: Call self.assertFalse()

```python
self.assertFalse(frappe.db.get_value('GL Entry', {'voucher_type': 'Period Closing Voucher', 'voucher_no': pcv.name, 'is_cancelled': 0}))
```


## Complete Example

```python
# Workflow
frappe.db.sql("delete from `tabGL Entry` where company='Test PCV Company'")
frappe.db.sql("delete from `tabPeriod Closing Voucher` where company='Test PCV Company'")
company = create_company()
surplus_account = create_account()
cost_center1 = create_cost_center('Main')
cost_center2 = create_cost_center('Western Branch')
create_sales_invoice(company=company, cost_center=cost_center1, income_account='Sales - TPC', expense_account='Cost of Goods Sold - TPC', rate=400, debit_to='Debtors - TPC', currency='USD', customer='_Test Customer USD', posting_date='2021-03-15')
create_sales_invoice(company=company, cost_center=cost_center2, income_account='Sales - TPC', expense_account='Cost of Goods Sold - TPC', rate=200, debit_to='Debtors - TPC', currency='USD', customer='_Test Customer USD', posting_date='2021-03-15')
pcv = self.make_period_closing_voucher(posting_date='2021-03-31', submit=False)
pcv.save()
pcv.submit()
surplus_account = pcv.closing_account_head
expected_gle = ((surplus_account, 0.0, 400.0, cost_center1), (surplus_account, 0.0, 200.0, cost_center2), ('Sales - TPC', 400.0, 0.0, cost_center1), ('Sales - TPC', 200.0, 0.0, cost_center2))
pcv_gle = frappe.db.sql('\n\t\t\tselect account, debit, credit, cost_center\n\t\t\tfrom `tabGL Entry` where voucher_no=%s\n\t\t\torder by account, cost_center\n\t\t', pcv.name)
self.assertSequenceEqual(pcv_gle, expected_gle)
pcv.reload()
pcv.cancel()
self.assertFalse(frappe.db.get_value('GL Entry', {'voucher_type': 'Period Closing Voucher', 'voucher_no': pcv.name, 'is_cancelled': 0}))
```

## Next Steps


---

*Source: test_period_closing_voucher.py:71 | Complexity: Advanced | Last updated: 2026-02-03*