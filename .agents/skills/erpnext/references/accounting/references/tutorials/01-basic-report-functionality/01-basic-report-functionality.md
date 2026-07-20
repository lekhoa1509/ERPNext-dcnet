# How To: 01 Basic Report Functionality

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test 01 basic report functionality

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.report.general_and_payment_ledger_comparison.general_and_payment_ledger_comparison`
- `erpnext.accounts.test.accounts_mixin`


## Step-by-Step Guide

### Step 1: Assign sinv = create_sales_invoice(...)

```python
sinv = create_sales_invoice(company=self.company, debit_to=self.debit_to, expense_account=self.expense_account, cost_center=self.cost_center, income_account=self.income_account, warehouse=self.warehouse)
```

### Step 2: Assign ple = value

```python
ple = frappe.db.get_all('Payment Ledger Entry', filters={'voucher_no': sinv.name, 'delinked': 0})[0]
```

### Step 3: Call frappe.db.set_value()

```python
frappe.db.set_value('Payment Ledger Entry', ple.name, 'amount', sinv.grand_total - 1)
```

### Step 4: Assign filters = frappe._dict(...)

```python
filters = frappe._dict({'company': self.company})
```

### Step 5: Assign unknown = execute(...)

```python
columns, data = execute(filters=filters)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(data), 1)
```

### Step 7: Assign expected = value

```python
expected = {'company': sinv.company, 'account': sinv.debit_to, 'voucher_type': sinv.doctype, 'voucher_no': sinv.name, 'party_type': 'Customer', 'party': sinv.customer, 'gl_balance': sinv.grand_total, 'pl_balance': sinv.grand_total - 1}
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(expected, data[0])
```

### Step 9: Assign filters = frappe._dict(...)

```python
filters = frappe._dict({'company': self.company, 'account': self.debit_to})
```

### Step 10: Assign unknown = execute(...)

```python
columns, data = execute(filters=filters)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(len(data), 1)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(expected, data[0])
```

### Step 13: Assign filters = frappe._dict(...)

```python
filters = frappe._dict({'company': self.company, 'account': self.creditors})
```

### Step 14: Assign unknown = execute(...)

```python
columns, data = execute(filters=filters)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual([], data)
```

### Step 16: Assign filters = frappe._dict(...)

```python
filters = frappe._dict({'company': self.company, 'voucher_no': sinv.name})
```

### Step 17: Assign unknown = execute(...)

```python
columns, data = execute(filters=filters)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(len(data), 1)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(expected, data[0])
```

### Step 20: Assign filters = frappe._dict(...)

```python
filters = frappe._dict({'company': self.company, 'voucher_no': sinv.name + '-1'})
```

### Step 21: Assign unknown = execute(...)

```python
columns, data = execute(filters=filters)
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual([], data)
```

### Step 23: Assign filters = frappe._dict(...)

```python
filters = frappe._dict({'company': self.company, 'period_start_date': sinv.posting_date, 'period_end_date': sinv.posting_date})
```

### Step 24: Assign unknown = execute(...)

```python
columns, data = execute(filters=filters)
```

### Step 25: Call self.assertEqual()

```python
self.assertEqual(len(data), 1)
```

### Step 26: Call self.assertEqual()

```python
self.assertEqual(expected, data[0])
```

### Step 27: Assign filters = frappe._dict(...)

```python
filters = frappe._dict({'company': self.company, 'period_start_date': add_days(sinv.posting_date, -1), 'period_end_date': add_days(sinv.posting_date, -1)})
```

### Step 28: Assign unknown = execute(...)

```python
columns, data = execute(filters=filters)
```

### Step 29: Call self.assertEqual()

```python
self.assertEqual([], data)
```


## Complete Example

```python
# Workflow
sinv = create_sales_invoice(company=self.company, debit_to=self.debit_to, expense_account=self.expense_account, cost_center=self.cost_center, income_account=self.income_account, warehouse=self.warehouse)
ple = frappe.db.get_all('Payment Ledger Entry', filters={'voucher_no': sinv.name, 'delinked': 0})[0]
frappe.db.set_value('Payment Ledger Entry', ple.name, 'amount', sinv.grand_total - 1)
filters = frappe._dict({'company': self.company})
columns, data = execute(filters=filters)
self.assertEqual(len(data), 1)
expected = {'company': sinv.company, 'account': sinv.debit_to, 'voucher_type': sinv.doctype, 'voucher_no': sinv.name, 'party_type': 'Customer', 'party': sinv.customer, 'gl_balance': sinv.grand_total, 'pl_balance': sinv.grand_total - 1}
self.assertEqual(expected, data[0])
filters = frappe._dict({'company': self.company, 'account': self.debit_to})
columns, data = execute(filters=filters)
self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
filters = frappe._dict({'company': self.company, 'account': self.creditors})
columns, data = execute(filters=filters)
self.assertEqual([], data)
filters = frappe._dict({'company': self.company, 'voucher_no': sinv.name})
columns, data = execute(filters=filters)
self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
filters = frappe._dict({'company': self.company, 'voucher_no': sinv.name + '-1'})
columns, data = execute(filters=filters)
self.assertEqual([], data)
filters = frappe._dict({'company': self.company, 'period_start_date': sinv.posting_date, 'period_end_date': sinv.posting_date})
columns, data = execute(filters=filters)
self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
filters = frappe._dict({'company': self.company, 'period_start_date': add_days(sinv.posting_date, -1), 'period_end_date': add_days(sinv.posting_date, -1)})
columns, data = execute(filters=filters)
self.assertEqual([], data)
```

## Next Steps


---

*Source: test_general_and_payment_ledger_comparison.py:30 | Complexity: Advanced | Last updated: 2026-02-03*