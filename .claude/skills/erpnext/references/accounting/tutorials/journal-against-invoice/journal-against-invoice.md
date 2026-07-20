# How To: Journal Against Invoice

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test journal against invoice

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

### Step 2: Assign amount = 100

```python
amount = 100
```

### Step 3: Assign si = self.create_sales_invoice(...)

```python
si = self.create_sales_invoice(qty=1, rate=amount, posting_date=transaction_date)
```

### Step 4: Assign je = self.create_journal_entry(...)

```python
je = self.create_journal_entry(self.bank, self.debit_to, amount, transaction_date)
```

### Step 5: Assign unknown.party_type = 'Customer'

```python
je.accounts[1].party_type = 'Customer'
```

### Step 6: Assign unknown.party = value

```python
je.accounts[1].party = self.customer
```

### Step 7: Call je.save()

```python
je.save()
```

### Step 8: Call je.submit()

```python
je.submit()
```

### Step 9: Assign pr = self.create_payment_reconciliation(...)

```python
pr = self.create_payment_reconciliation()
```

### Step 10: Call pr.get_unreconciled_entries()

```python
pr.get_unreconciled_entries()
```

### Step 11: Assign invoices = value

```python
invoices = [x.as_dict() for x in pr.get('invoices')]
```

### Step 12: Assign payments = value

```python
payments = [x.as_dict() for x in pr.get('payments')]
```

### Step 13: Call pr.allocate_entries()

```python
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
```

### Step 14: Call pr.reconcile()

```python
pr.reconcile()
```

### Step 15: Call si.reload()

```python
si.reload()
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(si.status, 'Paid')
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(si.outstanding_amount, 0)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(len(pr.get('invoices')), 0)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(len(pr.get('payments')), 0)
```

### Step 20: Call self.assertEqual()

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
amount = 100
si = self.create_sales_invoice(qty=1, rate=amount, posting_date=transaction_date)
je = self.create_journal_entry(self.bank, self.debit_to, amount, transaction_date)
je.accounts[1].party_type = 'Customer'
je.accounts[1].party = self.customer
je.save()
je.submit()
pr = self.create_payment_reconciliation()
pr.get_unreconciled_entries()
invoices = [x.as_dict() for x in pr.get('invoices')]
payments = [x.as_dict() for x in pr.get('payments')]
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
for row in pr.allocation:
    self.assertEqual(flt(row.get('difference_amount')), 0.0)
pr.reconcile()
si.reload()
self.assertEqual(si.status, 'Paid')
self.assertEqual(si.outstanding_amount, 0)
self.assertEqual(len(pr.get('invoices')), 0)
self.assertEqual(len(pr.get('payments')), 0)
```

## Next Steps


---

*Source: test_payment_reconciliation.py:602 | Complexity: Advanced | Last updated: 2026-02-03*