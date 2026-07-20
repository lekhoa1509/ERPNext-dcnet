# How To: Je Against Inv And Note

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test je against inv and note

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

### Step 1: Assign ple = value

```python
ple = self.ple
```

### Step 2: Assign transaction_date = nowdate(...)

```python
transaction_date = nowdate()
```

### Step 3: Assign amount = 100

```python
amount = 100
```

### Step 4: Assign si4 = self.create_sales_invoice(...)

```python
si4 = self.create_sales_invoice(qty=1, rate=amount, posting_date=transaction_date)
```

### Step 5: Assign cr_note2 = self.create_sales_invoice(...)

```python
cr_note2 = self.create_sales_invoice(qty=-1, rate=amount, posting_date=transaction_date, do_not_save=True, do_not_submit=True)
```

### Step 6: Assign cr_note2.is_return = 1

```python
cr_note2.is_return = 1
```

### Step 7: Assign cr_note2 = cr_note2.save.submit(...)

```python
cr_note2 = cr_note2.save().submit()
```

### Step 8: Assign je1 = self.create_journal_entry(...)

```python
je1 = self.create_journal_entry(self.debit_to, self.debit_to, amount, posting_date=transaction_date)
```

### Step 9: Assign unknown.party_type, unknown.party_type = 'Customer'

```python
je1.get('accounts')[0].party_type = je1.get('accounts')[1].party_type = 'Customer'
```

### Step 10: Assign unknown.party, unknown.party = value

```python
je1.get('accounts')[0].party = je1.get('accounts')[1].party = self.customer
```

### Step 11: Assign unknown.reference_type = value

```python
je1.get('accounts')[0].reference_type = cr_note2.doctype
```

### Step 12: Assign unknown.reference_name = value

```python
je1.get('accounts')[0].reference_name = cr_note2.name
```

### Step 13: Assign unknown.reference_type = value

```python
je1.get('accounts')[1].reference_type = si4.doctype
```

### Step 14: Assign unknown.reference_name = value

```python
je1.get('accounts')[1].reference_name = si4.name
```

### Step 15: Assign je1 = je1.save.submit(...)

```python
je1 = je1.save().submit()
```

### Step 16: Assign pl_entries_for_invoice = qb.from_.select.where.orderby.run(...)

```python
pl_entries_for_invoice = qb.from_(ple).select(ple.voucher_type, ple.voucher_no, ple.against_voucher_type, ple.against_voucher_no, ple.amount, ple.delinked).where((ple.against_voucher_type == si4.doctype) & (ple.against_voucher_no == si4.name)).orderby(ple.creation).run(as_dict=True)
```

### Step 17: Assign expected_values = value

```python
expected_values = [{'voucher_type': si4.doctype, 'voucher_no': si4.name, 'against_voucher_type': si4.doctype, 'against_voucher_no': si4.name, 'amount': amount, 'delinked': 0}, {'voucher_type': je1.doctype, 'voucher_no': je1.name, 'against_voucher_type': si4.doctype, 'against_voucher_no': si4.name, 'amount': -amount, 'delinked': 0}]
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(pl_entries_for_invoice[0], expected_values[0])
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(pl_entries_for_invoice[1], expected_values[1])
```

### Step 20: Assign pl_entries_for_crnote = qb.from_.select.where.orderby.run(...)

```python
pl_entries_for_crnote = qb.from_(ple).select(ple.voucher_type, ple.voucher_no, ple.against_voucher_type, ple.against_voucher_no, ple.amount, ple.delinked).where((ple.against_voucher_type == cr_note2.doctype) & (ple.against_voucher_no == cr_note2.name)).orderby(ple.creation).run(as_dict=True)
```

### Step 21: Assign expected_values = value

```python
expected_values = [{'voucher_type': cr_note2.doctype, 'voucher_no': cr_note2.name, 'against_voucher_type': cr_note2.doctype, 'against_voucher_no': cr_note2.name, 'amount': -amount, 'delinked': 0}, {'voucher_type': je1.doctype, 'voucher_no': je1.name, 'against_voucher_type': cr_note2.doctype, 'against_voucher_no': cr_note2.name, 'amount': amount, 'delinked': 0}]
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(pl_entries_for_crnote[0], expected_values[0])
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(pl_entries_for_crnote[1], expected_values[1])
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
ple = self.ple
transaction_date = nowdate()
amount = 100
si4 = self.create_sales_invoice(qty=1, rate=amount, posting_date=transaction_date)
cr_note2 = self.create_sales_invoice(qty=-1, rate=amount, posting_date=transaction_date, do_not_save=True, do_not_submit=True)
cr_note2.is_return = 1
cr_note2 = cr_note2.save().submit()
je1 = self.create_journal_entry(self.debit_to, self.debit_to, amount, posting_date=transaction_date)
je1.get('accounts')[0].party_type = je1.get('accounts')[1].party_type = 'Customer'
je1.get('accounts')[0].party = je1.get('accounts')[1].party = self.customer
je1.get('accounts')[0].reference_type = cr_note2.doctype
je1.get('accounts')[0].reference_name = cr_note2.name
je1.get('accounts')[1].reference_type = si4.doctype
je1.get('accounts')[1].reference_name = si4.name
je1 = je1.save().submit()
pl_entries_for_invoice = qb.from_(ple).select(ple.voucher_type, ple.voucher_no, ple.against_voucher_type, ple.against_voucher_no, ple.amount, ple.delinked).where((ple.against_voucher_type == si4.doctype) & (ple.against_voucher_no == si4.name)).orderby(ple.creation).run(as_dict=True)
expected_values = [{'voucher_type': si4.doctype, 'voucher_no': si4.name, 'against_voucher_type': si4.doctype, 'against_voucher_no': si4.name, 'amount': amount, 'delinked': 0}, {'voucher_type': je1.doctype, 'voucher_no': je1.name, 'against_voucher_type': si4.doctype, 'against_voucher_no': si4.name, 'amount': -amount, 'delinked': 0}]
self.assertEqual(pl_entries_for_invoice[0], expected_values[0])
self.assertEqual(pl_entries_for_invoice[1], expected_values[1])
pl_entries_for_crnote = qb.from_(ple).select(ple.voucher_type, ple.voucher_no, ple.against_voucher_type, ple.against_voucher_no, ple.amount, ple.delinked).where((ple.against_voucher_type == cr_note2.doctype) & (ple.against_voucher_no == cr_note2.name)).orderby(ple.creation).run(as_dict=True)
expected_values = [{'voucher_type': cr_note2.doctype, 'voucher_no': cr_note2.name, 'against_voucher_type': cr_note2.doctype, 'against_voucher_no': cr_note2.name, 'amount': -amount, 'delinked': 0}, {'voucher_type': je1.doctype, 'voucher_no': je1.name, 'against_voucher_type': cr_note2.doctype, 'against_voucher_no': cr_note2.name, 'amount': amount, 'delinked': 0}]
self.assertEqual(pl_entries_for_crnote[0], expected_values[0])
self.assertEqual(pl_entries_for_crnote[1], expected_values[1])
```

## Next Steps


---

*Source: test_payment_ledger_entry.py:355 | Complexity: Advanced | Last updated: 2026-02-03*