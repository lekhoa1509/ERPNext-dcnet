# How To: Filter Invoice Limit

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test filter invoice limit

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.data`
- `erpnext`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.party`
- `erpnext.accounts.utils`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.accounts.doctype.account.test_account`

**Setup Required:**
```python
self.create_company()
self.create_item()
self.create_customer()
self.create_account()
self.create_cost_center()
self.clear_old_entries()
```

## Step-by-Step Guide

### Step 1: Assign transaction_date = nowdate(...)

```python
transaction_date = nowdate()
```

### Step 2: Assign rate = 100

```python
rate = 100
```

### Step 3: Assign invoices = value

```python
invoices = []
```

### Step 4: Assign payments = value

```python
payments = []
```

### Step 5: Assign pr = self.create_payment_reconciliation(...)

```python
pr = self.create_payment_reconciliation()
```

### Step 6: Assign pr.from_invoice_date, pr.to_invoice_date = transaction_date

```python
pr.from_invoice_date = pr.to_invoice_date = transaction_date
```

### Step 7: Assign pr.from_payment_date, pr.to_payment_date = transaction_date

```python
pr.from_payment_date = pr.to_payment_date = transaction_date
```

### Step 8: Assign pr.invoice_limit = 2

```python
pr.invoice_limit = 2
```

### Step 9: Assign pr.payment_limit = 3

```python
pr.payment_limit = 3
```

### Step 10: Call pr.get_unreconciled_entries()

```python
pr.get_unreconciled_entries()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(len(pr.get('invoices')), 2)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(len(pr.get('payments')), 3)
```

### Step 13: Call invoices.append()

```python
invoices.append(self.create_sales_invoice(qty=1, rate=rate, posting_date=transaction_date))
```

### Step 14: Assign pe = self.create_payment_entry.save.submit(...)

```python
pe = self.create_payment_entry(amount=rate, posting_date=transaction_date).save().submit()
```

### Step 15: Call payments.append()

```python
payments.append(pe)
```


## Complete Example

```python
# Setup
self.create_company()
self.create_item()
self.create_customer()
self.create_account()
self.create_cost_center()
self.clear_old_entries()

# Workflow
transaction_date = nowdate()
rate = 100
invoices = []
payments = []
for _i in range(5):
    invoices.append(self.create_sales_invoice(qty=1, rate=rate, posting_date=transaction_date))
    pe = self.create_payment_entry(amount=rate, posting_date=transaction_date).save().submit()
    payments.append(pe)
pr = self.create_payment_reconciliation()
pr.from_invoice_date = pr.to_invoice_date = transaction_date
pr.from_payment_date = pr.to_payment_date = transaction_date
pr.invoice_limit = 2
pr.payment_limit = 3
pr.get_unreconciled_entries()
self.assertEqual(len(pr.get('invoices')), 2)
self.assertEqual(len(pr.get('payments')), 3)
```

## Next Steps


---

*Source: test_payment_reconciliation.py:426 | Complexity: Advanced | Last updated: 2026-02-03*