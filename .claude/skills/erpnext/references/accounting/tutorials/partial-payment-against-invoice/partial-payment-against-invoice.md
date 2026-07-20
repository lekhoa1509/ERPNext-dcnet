# How To: Partial Payment Against Invoice

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test partial payment against invoice

## Prerequisites

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

### Step 4: Assign si2 = self.create_sales_invoice(...)

```python
si2 = self.create_sales_invoice(qty=1, rate=amount, posting_date=transaction_date)
```

### Step 5: Assign pe2 = get_payment_entry(...)

```python
pe2 = get_payment_entry(si2.doctype, si2.name)
```

### Step 6: Assign unknown.allocated_amount = 50

```python
pe2.get('references')[0].allocated_amount = 50
```

### Step 7: Assign unknown.outstanding_amount = 50

```python
pe2.get('references')[0].outstanding_amount = 50
```

### Step 8: Assign pe2 = pe2.save.submit(...)

```python
pe2 = pe2.save().submit()
```

### Step 9: Assign pl_entries = qb.from_.select.where.orderby.run(...)

```python
pl_entries = qb.from_(ple).select(ple.voucher_type, ple.voucher_no, ple.against_voucher_type, ple.against_voucher_no, ple.amount, ple.delinked).where((ple.against_voucher_type == si2.doctype) & (ple.against_voucher_no == si2.name)).orderby(ple.creation).run(as_dict=True)
```

### Step 10: Assign expected_values = value

```python
expected_values = [{'voucher_type': si2.doctype, 'voucher_no': si2.name, 'against_voucher_type': si2.doctype, 'against_voucher_no': si2.name, 'amount': amount, 'delinked': 0}, {'voucher_type': pe2.doctype, 'voucher_no': pe2.name, 'against_voucher_type': si2.doctype, 'against_voucher_no': si2.name, 'amount': -50, 'delinked': 0}]
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(pl_entries[0], expected_values[0])
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(pl_entries[1], expected_values[1])
```


## Complete Example

```python
# Workflow
ple = self.ple
transaction_date = nowdate()
amount = 100
si2 = self.create_sales_invoice(qty=1, rate=amount, posting_date=transaction_date)
pe2 = get_payment_entry(si2.doctype, si2.name)
pe2.get('references')[0].allocated_amount = 50
pe2.get('references')[0].outstanding_amount = 50
pe2 = pe2.save().submit()
pl_entries = qb.from_(ple).select(ple.voucher_type, ple.voucher_no, ple.against_voucher_type, ple.against_voucher_no, ple.amount, ple.delinked).where((ple.against_voucher_type == si2.doctype) & (ple.against_voucher_no == si2.name)).orderby(ple.creation).run(as_dict=True)
expected_values = [{'voucher_type': si2.doctype, 'voucher_no': si2.name, 'against_voucher_type': si2.doctype, 'against_voucher_no': si2.name, 'amount': amount, 'delinked': 0}, {'voucher_type': pe2.doctype, 'voucher_no': pe2.name, 'against_voucher_type': si2.doctype, 'against_voucher_no': si2.name, 'amount': -50, 'delinked': 0}]
self.assertEqual(pl_entries[0], expected_values[0])
self.assertEqual(pl_entries[1], expected_values[1])
```

## Next Steps


---

*Source: test_payment_ledger_entry.py:239 | Complexity: Advanced | Last updated: 2026-02-03*