# How To: Customer Ledger Ignore Cr Dr Filter

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test customer ledger ignore cr dr filter

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.report.customer_ledger_summary.customer_ledger_summary`
- `erpnext.accounts.test.accounts_mixin`
- `erpnext.controllers.sales_and_purchase_return`


## Step-by-Step Guide

### Step 1: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice()
```

### Step 2: Assign cr_note = make_return_doc(...)

```python
cr_note = make_return_doc(si.doctype, si.name)
```

### Step 3: Call cr_note.submit()

```python
cr_note.submit()
```

### Step 4: Assign pr = frappe.get_doc(...)

```python
pr = frappe.get_doc('Payment Reconciliation')
```

### Step 5: Assign pr.company = value

```python
pr.company = si.company
```

### Step 6: Assign pr.party_type = 'Customer'

```python
pr.party_type = 'Customer'
```

### Step 7: Assign pr.party = value

```python
pr.party = si.customer
```

### Step 8: Assign pr.receivable_payable_account = value

```python
pr.receivable_payable_account = si.debit_to
```

### Step 9: Call pr.get_unreconciled_entries()

```python
pr.get_unreconciled_entries()
```

### Step 10: Assign invoices = value

```python
invoices = [invoice.as_dict() for invoice in pr.invoices if invoice.invoice_number == si.name]
```

### Step 11: Assign payments = value

```python
payments = [payment.as_dict() for payment in pr.payments if payment.reference_name == cr_note.name]
```

### Step 12: Call pr.allocate_entries()

```python
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
```

### Step 13: Call pr.reconcile()

```python
pr.reconcile()
```

### Step 14: Assign system_generated_journal = frappe.db.get_all(...)

```python
system_generated_journal = frappe.db.get_all('Journal Entry', filters={'docstatus': 1, 'reference_type': si.doctype, 'reference_name': si.name, 'voucher_type': 'Credit Note', 'is_system_generated': True}, fields=['name'])
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(len(system_generated_journal), 1)
```

### Step 16: Assign expected = value

```python
expected = {'party': '_Test Customer', 'customer_name': '_Test Customer', 'customer_group': '_Test Customer Group', 'territory': '_Test Territory', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 100.0, 'paid_amount': 0.0, 'return_amount': 100.0, 'closing_balance': 0.0, 'currency': 'INR', 'dr_or_cr': ''}
```

### Step 17: Assign unknown = execute(...)

```python
columns, data = execute(frappe._dict({'company': si.company, 'from_date': si.posting_date, 'to_date': si.posting_date, 'ignore_cr_dr_notes': False}))
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(len(data), 1)
```

### Step 19: Call self.assertDictEqual()

```python
self.assertDictEqual(expected, data[0])
```

### Step 20: Assign expected = value

```python
expected = {'party': '_Test Customer', 'customer_name': '_Test Customer', 'customer_group': '_Test Customer Group', 'territory': '_Test Territory', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 100.0, 'paid_amount': 0.0, 'return_amount': 100.0, 'closing_balance': 0.0, 'currency': 'INR', 'dr_or_cr': ''}
```

### Step 21: Assign unknown = execute(...)

```python
columns, data = execute(frappe._dict({'company': si.company, 'from_date': si.posting_date, 'to_date': si.posting_date, 'ignore_cr_dr_notes': True}))
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(len(data), 1)
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(expected, data[0])
```


## Complete Example

```python
# Workflow
si = create_sales_invoice()
cr_note = make_return_doc(si.doctype, si.name)
cr_note.submit()
pr = frappe.get_doc('Payment Reconciliation')
pr.company = si.company
pr.party_type = 'Customer'
pr.party = si.customer
pr.receivable_payable_account = si.debit_to
pr.get_unreconciled_entries()
invoices = [invoice.as_dict() for invoice in pr.invoices if invoice.invoice_number == si.name]
payments = [payment.as_dict() for payment in pr.payments if payment.reference_name == cr_note.name]
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
pr.reconcile()
system_generated_journal = frappe.db.get_all('Journal Entry', filters={'docstatus': 1, 'reference_type': si.doctype, 'reference_name': si.name, 'voucher_type': 'Credit Note', 'is_system_generated': True}, fields=['name'])
self.assertEqual(len(system_generated_journal), 1)
expected = {'party': '_Test Customer', 'customer_name': '_Test Customer', 'customer_group': '_Test Customer Group', 'territory': '_Test Territory', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 100.0, 'paid_amount': 0.0, 'return_amount': 100.0, 'closing_balance': 0.0, 'currency': 'INR', 'dr_or_cr': ''}
columns, data = execute(frappe._dict({'company': si.company, 'from_date': si.posting_date, 'to_date': si.posting_date, 'ignore_cr_dr_notes': False}))
self.assertEqual(len(data), 1)
self.assertDictEqual(expected, data[0])
expected = {'party': '_Test Customer', 'customer_name': '_Test Customer', 'customer_group': '_Test Customer Group', 'territory': '_Test Territory', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 100.0, 'paid_amount': 0.0, 'return_amount': 100.0, 'closing_balance': 0.0, 'currency': 'INR', 'dr_or_cr': ''}
columns, data = execute(frappe._dict({'company': si.company, 'from_date': si.posting_date, 'to_date': si.posting_date, 'ignore_cr_dr_notes': True}))
self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
```

## Next Steps


---

*Source: test_customer_ledger_summary.py:154 | Complexity: Advanced | Last updated: 2026-02-03*