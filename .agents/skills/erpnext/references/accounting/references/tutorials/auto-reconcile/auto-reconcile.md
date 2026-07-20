# How To: Auto Reconcile

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test auto reconcile

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.test.accounts_mixin`


## Step-by-Step Guide

### Step 1: Assign from_date = add_days(...)

```python
from_date = add_days(today(), -1)
```

### Step 2: Assign to_date = today(...)

```python
to_date = today()
```

### Step 3: Assign payment = create_payment_entry.save(...)

```python
payment = create_payment_entry(company=self.company, posting_date=from_date, payment_type='Receive', party_type='Customer', party=self.customer, paid_from=self.debit_to, paid_to=self.bank, paid_amount=100).save()
```

### Step 4: Assign payment.reference_no = '123'

```python
payment.reference_no = '123'
```

### Step 5: Assign payment = payment.save.submit(...)

```python
payment = payment.save().submit()
```

### Step 6: Assign bank_transaction = frappe.get_doc.save.submit(...)

```python
bank_transaction = frappe.get_doc({'doctype': 'Bank Transaction', 'date': to_date, 'deposit': 100, 'bank_account': self.bank_account, 'reference_number': '123', 'currency': 'INR'}).save().submit()
```

### Step 7: Assign transactions = get_bank_transactions(...)

```python
transactions = get_bank_transactions(self.bank_account, from_date, to_date)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(len(transactions), 1)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(transactions[0].name, bank_transaction.name)
```

### Step 10: Call auto_reconcile_vouchers()

```python
auto_reconcile_vouchers(bank_account=self.bank_account, from_date=from_date, to_date=to_date, filter_by_reference_date=False)
```

### Step 11: Assign transactions = get_bank_transactions(...)

```python
transactions = get_bank_transactions(self.bank_account, from_date, to_date)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(len(transactions), 0)
```


## Complete Example

```python
# Workflow
from_date = add_days(today(), -1)
to_date = today()
payment = create_payment_entry(company=self.company, posting_date=from_date, payment_type='Receive', party_type='Customer', party=self.customer, paid_from=self.debit_to, paid_to=self.bank, paid_amount=100).save()
payment.reference_no = '123'
payment = payment.save().submit()
bank_transaction = frappe.get_doc({'doctype': 'Bank Transaction', 'date': to_date, 'deposit': 100, 'bank_account': self.bank_account, 'reference_number': '123', 'currency': 'INR'}).save().submit()
transactions = get_bank_transactions(self.bank_account, from_date, to_date)
self.assertEqual(len(transactions), 1)
self.assertEqual(transactions[0].name, bank_transaction.name)
auto_reconcile_vouchers(bank_account=self.bank_account, from_date=from_date, to_date=to_date, filter_by_reference_date=False)
transactions = get_bank_transactions(self.bank_account, from_date, to_date)
self.assertEqual(len(transactions), 0)
```

## Next Steps


---

*Source: test_bank_reconciliation_tool.py:52 | Complexity: Advanced | Last updated: 2026-02-03*