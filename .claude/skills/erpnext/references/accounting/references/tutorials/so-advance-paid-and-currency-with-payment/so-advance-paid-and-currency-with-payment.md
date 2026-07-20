# How To: So Advance Paid And Currency With Payment

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test so advance paid and currency with payment

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

### Step 5: Assign pe_exchange_rate = 85

```python
pe_exchange_rate = 85
```

### Step 6: Assign pe = get_payment_entry(...)

```python
pe = get_payment_entry(so.doctype, so.name, bank_account=self.cash)
```

### Step 7: Assign pe.reference_no = '1'

```python
pe.reference_no = '1'
```

### Step 8: Assign pe.reference_date = nowdate(...)

```python
pe.reference_date = nowdate()
```

### Step 9: Assign pe.paid_from = value

```python
pe.paid_from = self.debtors_usd
```

### Step 10: Assign pe.paid_from_account_currency = 'USD'

```python
pe.paid_from_account_currency = 'USD'
```

### Step 11: Assign pe.source_exchange_rate = pe_exchange_rate

```python
pe.source_exchange_rate = pe_exchange_rate
```

### Step 12: Assign pe.paid_amount = value

```python
pe.paid_amount = so.grand_total
```

### Step 13: Assign pe.received_amount = value

```python
pe.received_amount = pe_exchange_rate * pe.paid_amount
```

### Step 14: Assign unknown.outstanding_amount = 100

```python
pe.references[0].outstanding_amount = 100
```

### Step 15: Assign unknown.total_amount = 100

```python
pe.references[0].total_amount = 100
```

### Step 16: Assign unknown.allocated_amount = 100

```python
pe.references[0].allocated_amount = 100
```

### Step 17: Call pe.save.submit()

```python
pe.save().submit()
```

### Step 18: Call so.reload()

```python
so.reload()
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(so.advance_paid, 100)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(so.party_account_currency, 'USD')
```

### Step 21: Call pe.reload()

```python
pe.reload()
```

### Step 22: Call pe.cancel()

```python
pe.cancel()
```

### Step 23: Call so.reload()

```python
so.reload()
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(so.advance_paid, 0)
```

### Step 25: Call self.assertEqual()

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
pe_exchange_rate = 85
pe = get_payment_entry(so.doctype, so.name, bank_account=self.cash)
pe.reference_no = '1'
pe.reference_date = nowdate()
pe.paid_from = self.debtors_usd
pe.paid_from_account_currency = 'USD'
pe.source_exchange_rate = pe_exchange_rate
pe.paid_amount = so.grand_total
pe.received_amount = pe_exchange_rate * pe.paid_amount
pe.references[0].outstanding_amount = 100
pe.references[0].total_amount = 100
pe.references[0].allocated_amount = 100
pe.save().submit()
so.reload()
self.assertEqual(so.advance_paid, 100)
self.assertEqual(so.party_account_currency, 'USD')
pe.reload()
pe.cancel()
so.reload()
self.assertEqual(so.advance_paid, 0)
self.assertEqual(so.party_account_currency, 'USD')
```

## Next Steps


---

*Source: test_advance_payment_ledger_entry.py:68 | Complexity: Advanced | Last updated: 2026-02-03*