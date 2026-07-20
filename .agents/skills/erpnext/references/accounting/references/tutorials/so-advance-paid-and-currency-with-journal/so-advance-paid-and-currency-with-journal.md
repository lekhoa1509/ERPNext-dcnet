# How To: So Advance Paid And Currency With Journal

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test so advance paid and currency with journal

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.test.accounts_mixin`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`


## Step-by-Step Guide

### Step 1: Call self.create_customer()

```python
self.create_customer('_Test USD Customer', 'USD')
```

### Step 2: Assign so = self.create_sales_order(...)

```python
so = self.create_sales_order(currency='USD', do_not_submit=True)
```

### Step 3: Assign so.conversion_rate = 80

```python
so.conversion_rate = 80
```

### Step 4: Call so.submit()

```python
so.submit()
```

### Step 5: Assign je_exchange_rate = 85

```python
je_exchange_rate = 85
```

### Step 6: Assign je = frappe.get_doc(...)

```python
je = frappe.get_doc({'doctype': 'Journal Entry', 'company': self.company, 'voucher_type': 'Journal Entry', 'posting_date': so.transaction_date, 'multi_currency': True, 'accounts': [{'account': self.debtors_usd, 'party_type': 'Customer', 'party': so.customer, 'credit': 8500, 'credit_in_account_currency': 100, 'is_advance': 'Yes', 'reference_type': so.doctype, 'reference_name': so.name, 'exchange_rate': je_exchange_rate}, {'account': self.cash, 'debit': 8500, 'debit_in_account_currency': 8500}]})
```

### Step 7: Call je.save.submit()

```python
je.save().submit()
```

### Step 8: Call so.reload()

```python
so.reload()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(so.advance_paid, 100)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(so.party_account_currency, 'USD')
```

### Step 11: Call je.reload()

```python
je.reload()
```

### Step 12: Call je.cancel()

```python
je.cancel()
```

### Step 13: Call so.reload()

```python
so.reload()
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(so.advance_paid, 0)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(so.party_account_currency, 'USD')
```


## Complete Example

```python
# Workflow
self.create_customer('_Test USD Customer', 'USD')
so = self.create_sales_order(currency='USD', do_not_submit=True)
so.conversion_rate = 80
so.submit()
je_exchange_rate = 85
je = frappe.get_doc({'doctype': 'Journal Entry', 'company': self.company, 'voucher_type': 'Journal Entry', 'posting_date': so.transaction_date, 'multi_currency': True, 'accounts': [{'account': self.debtors_usd, 'party_type': 'Customer', 'party': so.customer, 'credit': 8500, 'credit_in_account_currency': 100, 'is_advance': 'Yes', 'reference_type': so.doctype, 'reference_name': so.name, 'exchange_rate': je_exchange_rate}, {'account': self.cash, 'debit': 8500, 'debit_in_account_currency': 8500}]})
je.save().submit()
so.reload()
self.assertEqual(so.advance_paid, 100)
self.assertEqual(so.party_account_currency, 'USD')
je.reload()
je.cancel()
so.reload()
self.assertEqual(so.advance_paid, 0)
self.assertEqual(so.party_account_currency, 'USD')
```

## Next Steps


---

*Source: test_advance_payment_ledger_entry.py:101 | Complexity: Advanced | Last updated: 2026-02-03*