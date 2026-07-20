# How To: Po Advance Paid And Currency With Journal

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test po advance paid and currency with journal

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

### Step 1: Call self.create_supplier()

```python
self.create_supplier('_Test USD Supplier', 'USD')
```

### Step 2: Assign po = self.create_purchase_order(...)

```python
po = self.create_purchase_order(currency='USD', do_not_submit=True)
```

### Step 3: Assign po.conversion_rate = 80

```python
po.conversion_rate = 80
```

### Step 4: Call po.submit()

```python
po.submit()
```

### Step 5: Assign je_exchange_rate = 85

```python
je_exchange_rate = 85
```

### Step 6: Assign je = frappe.get_doc(...)

```python
je = frappe.get_doc({'doctype': 'Journal Entry', 'company': self.company, 'voucher_type': 'Journal Entry', 'posting_date': po.transaction_date, 'multi_currency': True, 'accounts': [{'account': self.creditors_usd, 'party_type': 'Supplier', 'party': po.supplier, 'debit': 8500, 'debit_in_account_currency': 100, 'is_advance': 'Yes', 'reference_type': po.doctype, 'reference_name': po.name, 'exchange_rate': je_exchange_rate}, {'account': self.cash, 'credit': 8500, 'credit_in_account_currency': 8500}]})
```

### Step 7: Call je.save.submit()

```python
je.save().submit()
```

### Step 8: Call po.reload()

```python
po.reload()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(po.advance_paid, 100)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(po.party_account_currency, 'USD')
```

### Step 11: Call je.reload()

```python
je.reload()
```

### Step 12: Call je.cancel()

```python
je.cancel()
```

### Step 13: Call po.reload()

```python
po.reload()
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(po.advance_paid, 0)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(po.party_account_currency, 'USD')
```


## Complete Example

```python
# Workflow
self.create_supplier('_Test USD Supplier', 'USD')
po = self.create_purchase_order(currency='USD', do_not_submit=True)
po.conversion_rate = 80
po.submit()
je_exchange_rate = 85
je = frappe.get_doc({'doctype': 'Journal Entry', 'company': self.company, 'voucher_type': 'Journal Entry', 'posting_date': po.transaction_date, 'multi_currency': True, 'accounts': [{'account': self.creditors_usd, 'party_type': 'Supplier', 'party': po.supplier, 'debit': 8500, 'debit_in_account_currency': 100, 'is_advance': 'Yes', 'reference_type': po.doctype, 'reference_name': po.name, 'exchange_rate': je_exchange_rate}, {'account': self.cash, 'credit': 8500, 'credit_in_account_currency': 8500}]})
je.save().submit()
po.reload()
self.assertEqual(po.advance_paid, 100)
self.assertEqual(po.party_account_currency, 'USD')
je.reload()
je.cancel()
po.reload()
self.assertEqual(po.advance_paid, 0)
self.assertEqual(po.party_account_currency, 'USD')
```

## Next Steps


---

*Source: test_advance_payment_ledger_entry.py:182 | Complexity: Advanced | Last updated: 2026-02-03*