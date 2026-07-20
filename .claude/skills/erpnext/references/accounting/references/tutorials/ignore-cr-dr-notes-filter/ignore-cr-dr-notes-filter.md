# How To: Ignore Cr Dr Notes Filter

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test ignore cr dr notes filter

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.report.general_ledger.general_ledger`
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

### Step 16: Assign expected = set(...)

```python
expected = set([si.name, cr_note.name, system_generated_journal[0].name])
```

### Step 17: Assign unknown = execute(...)

```python
columns, data = execute(frappe._dict({'company': si.company, 'from_date': si.posting_date, 'to_date': si.posting_date, 'account': [si.debit_to], 'categorize_by': 'Categorize by Voucher (Consolidated)', 'ignore_cr_dr_notes': False}))
```

### Step 18: Assign actual = set(...)

```python
actual = set([x.voucher_no for x in data if x.voucher_no])
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(expected, actual)
```

### Step 20: Assign expected = set(...)

```python
expected = set([si.name, cr_note.name])
```

### Step 21: Assign unknown = execute(...)

```python
columns, data = execute(frappe._dict({'company': si.company, 'from_date': si.posting_date, 'to_date': si.posting_date, 'account': [si.debit_to], 'categorize_by': 'Categorize by Voucher (Consolidated)', 'ignore_cr_dr_notes': True}))
```

### Step 22: Assign actual = set(...)

```python
actual = set([x.voucher_no for x in data if x.voucher_no])
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(expected, actual)
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
expected = set([si.name, cr_note.name, system_generated_journal[0].name])
columns, data = execute(frappe._dict({'company': si.company, 'from_date': si.posting_date, 'to_date': si.posting_date, 'account': [si.debit_to], 'categorize_by': 'Categorize by Voucher (Consolidated)', 'ignore_cr_dr_notes': False}))
actual = set([x.voucher_no for x in data if x.voucher_no])
self.assertEqual(expected, actual)
expected = set([si.name, cr_note.name])
columns, data = execute(frappe._dict({'company': si.company, 'from_date': si.posting_date, 'to_date': si.posting_date, 'account': [si.debit_to], 'categorize_by': 'Categorize by Voucher (Consolidated)', 'ignore_cr_dr_notes': True}))
actual = set([x.voucher_no for x in data if x.voucher_no])
self.assertEqual(expected, actual)
```

## Next Steps


---

*Source: test_general_ledger.py:271 | Complexity: Advanced | Last updated: 2026-02-03*