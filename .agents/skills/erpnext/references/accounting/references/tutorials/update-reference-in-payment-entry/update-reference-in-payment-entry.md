# How To: Update Reference In Payment Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test update reference in payment entry

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.test_runner`
- `frappe.tests`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.party`
- `erpnext.accounts.utils`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `frappe.custom.doctype.property_setter.property_setter`
- `frappe.utils`
- `erpnext.accounts.utils`
- `erpnext.buying.doctype.supplier.test_supplier`


## Step-by-Step Guide

### Step 1: Assign item = value

```python
item = make_item().name
```

### Step 2: Assign purchase_invoice = make_purchase_invoice(...)

```python
purchase_invoice = make_purchase_invoice(item=item, supplier='_Test Supplier USD', currency='USD', conversion_rate=82.32, do_not_submit=1)
```

### Step 3: Assign purchase_invoice.credit_to = '_Test Payable USD - _TC'

```python
purchase_invoice.credit_to = '_Test Payable USD - _TC'
```

### Step 4: Call purchase_invoice.submit()

```python
purchase_invoice.submit()
```

### Step 5: Assign payment_entry = get_payment_entry(...)

```python
payment_entry = get_payment_entry(purchase_invoice.doctype, purchase_invoice.name)
```

### Step 6: Assign payment_entry.paid_amount = 15725

```python
payment_entry.paid_amount = 15725
```

### Step 7: Assign payment_entry.deductions = value

```python
payment_entry.deductions = []
```

### Step 8: Call payment_entry.save()

```python
payment_entry.save()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(payment_entry.deductions[0].amount, -4855.0)
```

### Step 10: Assign payment_entry.target_exchange_rate = 62.9

```python
payment_entry.target_exchange_rate = 62.9
```

### Step 11: Call payment_entry.save()

```python
payment_entry.save()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(payment_entry.deductions, [])
```

### Step 13: Assign payment_entry.references = value

```python
payment_entry.references = []
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(payment_entry.difference_amount, 0.0)
```

### Step 15: Call payment_entry.submit()

```python
payment_entry.submit()
```

### Step 16: Assign payment_reconciliation = frappe.new_doc(...)

```python
payment_reconciliation = frappe.new_doc('Payment Reconciliation')
```

### Step 17: Assign payment_reconciliation.company = value

```python
payment_reconciliation.company = payment_entry.company
```

### Step 18: Assign payment_reconciliation.party_type = 'Supplier'

```python
payment_reconciliation.party_type = 'Supplier'
```

### Step 19: Assign payment_reconciliation.party = value

```python
payment_reconciliation.party = purchase_invoice.supplier
```

### Step 20: Assign payment_reconciliation.receivable_payable_account = value

```python
payment_reconciliation.receivable_payable_account = payment_entry.paid_to
```

### Step 21: Call payment_reconciliation.get_unreconciled_entries()

```python
payment_reconciliation.get_unreconciled_entries()
```

### Step 22: Call payment_reconciliation.allocate_entries()

```python
payment_reconciliation.allocate_entries({'payments': [d.__dict__ for d in payment_reconciliation.payments], 'invoices': [d.__dict__ for d in payment_reconciliation.invoices]})
```

### Step 23: Call payment_reconciliation.reconcile()

```python
payment_reconciliation.reconcile()
```

### Step 24: Call payment_entry.load_from_db()

```python
payment_entry.load_from_db()
```

### Step 25: Call self.assertEqual()

```python
self.assertEqual(len(payment_entry.references), 1)
```

### Step 26: Call self.assertEqual()

```python
self.assertEqual(payment_entry.difference_amount, 0)
```

### Step 27: Assign d.outstanding_amount = value

```python
d.outstanding_amount = d.amount
```

### Step 28: Assign d.difference_account = 'Exchange Gain/Loss - _TC'

```python
d.difference_account = 'Exchange Gain/Loss - _TC'
```


## Complete Example

```python
# Workflow
item = make_item().name
purchase_invoice = make_purchase_invoice(item=item, supplier='_Test Supplier USD', currency='USD', conversion_rate=82.32, do_not_submit=1)
purchase_invoice.credit_to = '_Test Payable USD - _TC'
purchase_invoice.submit()
payment_entry = get_payment_entry(purchase_invoice.doctype, purchase_invoice.name)
payment_entry.paid_amount = 15725
payment_entry.deductions = []
payment_entry.save()
self.assertEqual(payment_entry.deductions[0].amount, -4855.0)
payment_entry.target_exchange_rate = 62.9
payment_entry.save()
self.assertEqual(payment_entry.deductions, [])
payment_entry.references = []
self.assertEqual(payment_entry.difference_amount, 0.0)
payment_entry.submit()
payment_reconciliation = frappe.new_doc('Payment Reconciliation')
payment_reconciliation.company = payment_entry.company
payment_reconciliation.party_type = 'Supplier'
payment_reconciliation.party = purchase_invoice.supplier
payment_reconciliation.receivable_payable_account = payment_entry.paid_to
payment_reconciliation.get_unreconciled_entries()
payment_reconciliation.allocate_entries({'payments': [d.__dict__ for d in payment_reconciliation.payments], 'invoices': [d.__dict__ for d in payment_reconciliation.invoices]})
for d in payment_reconciliation.invoices:
    d.outstanding_amount = d.amount
for d in payment_reconciliation.allocation:
    d.difference_account = 'Exchange Gain/Loss - _TC'
payment_reconciliation.reconcile()
payment_entry.load_from_db()
self.assertEqual(len(payment_entry.references), 1)
self.assertEqual(payment_entry.difference_amount, 0)
```

## Next Steps


---

*Source: test_utils.py:81 | Complexity: Advanced | Last updated: 2026-02-03*