# How To: Unpaid Invoice Outstanding

**Difficulty**: Advanced
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test unpaid invoice outstanding

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.report.payment_ledger.payment_ledger`


## Step-by-Step Guide

### Step 1: Assign sinv = create_sales_invoice(...)

```python
sinv = create_sales_invoice(company=self.company, debit_to=self.debit_to, expense_account=self.expense_account, cost_center=self.cost_center, income_account=self.income_account, warehouse=self.warehouse)
```

### Step 2: Call get_payment_entry.save.submit()

```python
get_payment_entry(sinv.doctype, sinv.name).save().submit()
```

### Step 3: Assign filters = frappe._dict(...)

```python
filters = frappe._dict({'company': self.company})
```

### Step 4: Assign unknown = execute(...)

```python
columns, data = execute(filters=filters)
```

### Step 5: Assign outstanding = value

```python
outstanding = [x for x in data if x.get('against_voucher_no') == 'Outstanding:']
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(outstanding[0].get('amount'), 0)
```


## Complete Example

```python
# Workflow
sinv = create_sales_invoice(company=self.company, debit_to=self.debit_to, expense_account=self.expense_account, cost_center=self.cost_center, income_account=self.income_account, warehouse=self.warehouse)
get_payment_entry(sinv.doctype, sinv.name).save().submit()
filters = frappe._dict({'company': self.company})
columns, data = execute(filters=filters)
outstanding = [x for x in data if x.get('against_voucher_no') == 'Outstanding:']
self.assertEqual(outstanding[0].get('amount'), 0)
```

## Next Steps


---

*Source: test_payment_ledger.py:49 | Complexity: Advanced | Last updated: 2026-02-03*