# How To: Journal Against Journal

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test journal against journal

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

### Step 2: Assign sales = 'Sales - _PR'

```python
sales = 'Sales - _PR'
```

### Step 3: Assign amount = 100

```python
amount = 100
```

### Step 4: Assign je1 = self.create_journal_entry(...)

```python
je1 = self.create_journal_entry(self.debit_to, sales, amount, transaction_date)
```

### Step 5: Assign unknown.party_type = 'Customer'

```python
je1.accounts[0].party_type = 'Customer'
```

### Step 6: Assign unknown.party = value

```python
je1.accounts[0].party = self.customer
```

### Step 7: Call je1.save()

```python
je1.save()
```

### Step 8: Call je1.submit()

```python
je1.submit()
```

### Step 9: Assign je2 = self.create_journal_entry(...)

```python
je2 = self.create_journal_entry(self.bank, self.debit_to, amount, transaction_date)
```

### Step 10: Assign unknown.party_type = 'Customer'

```python
je2.accounts[1].party_type = 'Customer'
```

### Step 11: Assign unknown.party = value

```python
je2.accounts[1].party = self.customer
```

### Step 12: Call je2.save()

```python
je2.save()
```

### Step 13: Call je2.submit()

```python
je2.submit()
```

### Step 14: Assign pr = self.create_payment_reconciliation(...)

```python
pr = self.create_payment_reconciliation()
```

### Step 15: Call pr.get_unreconciled_entries()

```python
pr.get_unreconciled_entries()
```

### Step 16: Assign invoices = value

```python
invoices = [x.as_dict() for x in pr.get('invoices')]
```

### Step 17: Assign payments = value

```python
payments = [x.as_dict() for x in pr.get('payments')]
```

### Step 18: Call pr.allocate_entries()

```python
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
```

### Step 19: Call pr.reconcile()

```python
pr.reconcile()
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(pr.get('invoices'), [])
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(pr.get('payments'), [])
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(flt(row.get('difference_amount')), 0.0)
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
sales = 'Sales - _PR'
amount = 100
je1 = self.create_journal_entry(self.debit_to, sales, amount, transaction_date)
je1.accounts[0].party_type = 'Customer'
je1.accounts[0].party = self.customer
je1.save()
je1.submit()
je2 = self.create_journal_entry(self.bank, self.debit_to, amount, transaction_date)
je2.accounts[1].party_type = 'Customer'
je2.accounts[1].party = self.customer
je2.save()
je2.submit()
pr = self.create_payment_reconciliation()
pr.get_unreconciled_entries()
invoices = [x.as_dict() for x in pr.get('invoices')]
payments = [x.as_dict() for x in pr.get('payments')]
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
for row in pr.allocation:
    self.assertEqual(flt(row.get('difference_amount')), 0.0)
pr.reconcile()
self.assertEqual(pr.get('invoices'), [])
self.assertEqual(pr.get('payments'), [])
```

## Next Steps


---

*Source: test_payment_reconciliation.py:672 | Complexity: Advanced | Last updated: 2026-02-03*