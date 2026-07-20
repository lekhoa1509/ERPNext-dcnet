# How To: Multi Je Unlink On Invoice Cancellation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test multi je unlink on invoice cancellation

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.item.test_item`

**Setup Required:**
```python
self.ple = qb.DocType('Payment Ledger Entry')
self.create_company()
self.create_item()
self.create_customer()
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

### Step 4: Call si.reload()

```python
si.reload()
```

### Step 5: Call si.cancel()

```python
si.cancel()
```

### Step 6: Assign entries = frappe.db.get_list(...)

```python
entries = frappe.db.get_list('Payment Ledger Entry', filters={'against_voucher_type': si.doctype, 'against_voucher_no': si.name, 'delinked': 0})
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(entries, [])
```

### Step 8: Call si.delete()

```python
si.delete()
```

### Step 9: Call self.assertRaises()

```python
self.assertRaises(frappe.DoesNotExistError, frappe.get_doc, si.doctype, si.name)
```

### Step 10: Assign je1 = self.create_journal_entry(...)

```python
je1 = self.create_journal_entry(self.income_account, self.debit_to, amt, posting_date=transaction_date)
```

### Step 11: Assign unknown.party_type = 'Customer'

```python
je1.get('accounts')[1].party_type = 'Customer'
```

### Step 12: Assign unknown.party = value

```python
je1.get('accounts')[1].party = self.customer
```

### Step 13: Assign unknown.reference_type = value

```python
je1.get('accounts')[1].reference_type = si.doctype
```

### Step 14: Assign unknown.reference_name = value

```python
je1.get('accounts')[1].reference_name = si.name
```

### Step 15: Assign je1 = je1.save.submit(...)

```python
je1 = je1.save().submit()
```


## Complete Example

```python
# Setup
self.ple = qb.DocType('Payment Ledger Entry')
self.create_company()
self.create_item()
self.create_customer()
self.clear_old_entries()

# Workflow
transaction_date = nowdate()
amount = 100
si = self.create_sales_invoice(qty=1, rate=amount, posting_date=transaction_date)
for amt in [40, 40, 20]:
    je1 = self.create_journal_entry(self.income_account, self.debit_to, amt, posting_date=transaction_date)
    je1.get('accounts')[1].party_type = 'Customer'
    je1.get('accounts')[1].party = self.customer
    je1.get('accounts')[1].reference_type = si.doctype
    je1.get('accounts')[1].reference_name = si.name
    je1 = je1.save().submit()
si.reload()
si.cancel()
entries = frappe.db.get_list('Payment Ledger Entry', filters={'against_voucher_type': si.doctype, 'against_voucher_no': si.name, 'delinked': 0})
self.assertEqual(entries, [])
si.delete()
self.assertRaises(frappe.DoesNotExistError, frappe.get_doc, si.doctype, si.name)
```

## Next Steps


---

*Source: test_payment_ledger_entry.py:481 | Complexity: Advanced | Last updated: 2026-02-03*