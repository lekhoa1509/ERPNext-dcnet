# How To: Payment Against Credit Note

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Payment against credit/debit note should be considered against the parent invoice

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.report.accounts_receivable.accounts_receivable`
- `erpnext.accounts.test.accounts_mixin`
- `erpnext.selling.doctype.sales_order.test_sales_order`

**Setup Required:**
```python
self.create_company()
self.create_customer()
self.create_item()
self.create_usd_receivable_account()
self.clear_old_entries()
```

## Step-by-Step Guide

### Step 1: '\n\t\tPayment against credit/debit note should be considered against the parent invoice\n\t\t'

```python
'\n\t\tPayment against credit/debit note should be considered against the parent invoice\n\t\t'
```

### Step 2: Assign si1 = self.create_sales_invoice(...)

```python
si1 = self.create_sales_invoice()
```

### Step 3: Assign pe = get_payment_entry(...)

```python
pe = get_payment_entry(si1.doctype, si1.name, bank_account=self.cash)
```

### Step 4: Assign pe.paid_from = value

```python
pe.paid_from = self.debit_to
```

### Step 5: Call pe.insert()

```python
pe.insert()
```

### Step 6: Call pe.submit()

```python
pe.submit()
```

### Step 7: Assign cr_note = self.create_credit_note(...)

```python
cr_note = self.create_credit_note(si1.name)
```

### Step 8: Assign si2 = self.create_sales_invoice(...)

```python
si2 = self.create_sales_invoice()
```

### Step 9: Assign je = frappe.new_doc(...)

```python
je = frappe.new_doc('Journal Entry')
```

### Step 10: Assign je.company = value

```python
je.company = self.company
```

### Step 11: Assign je.voucher_type = 'Credit Note'

```python
je.voucher_type = 'Credit Note'
```

### Step 12: Assign je.posting_date = today(...)

```python
je.posting_date = today()
```

### Step 13: Assign debit_entry = value

```python
debit_entry = {'account': self.debit_to, 'party_type': 'Customer', 'party': self.customer, 'debit': 100, 'debit_in_account_currency': 100, 'reference_type': cr_note.doctype, 'reference_name': cr_note.name, 'cost_center': self.cost_center}
```

### Step 14: Assign credit_entry = value

```python
credit_entry = {'account': self.debit_to, 'party_type': 'Customer', 'party': self.customer, 'credit': 100, 'credit_in_account_currency': 100, 'reference_type': si2.doctype, 'reference_name': si2.name, 'cost_center': self.cost_center}
```

### Step 15: Call je.append()

```python
je.append('accounts', debit_entry)
```

### Step 16: Call je.append()

```python
je.append('accounts', credit_entry)
```

### Step 17: Assign je = je.save.submit(...)

```python
je = je.save().submit()
```

### Step 18: Assign filters = value

```python
filters = {'company': self.company, 'report_date': today(), 'range': '30, 60, 90, 120'}
```

### Step 19: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(report[1], [])
```


## Complete Example

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_usd_receivable_account()
self.clear_old_entries()

# Workflow
'\n\t\tPayment against credit/debit note should be considered against the parent invoice\n\t\t'
si1 = self.create_sales_invoice()
pe = get_payment_entry(si1.doctype, si1.name, bank_account=self.cash)
pe.paid_from = self.debit_to
pe.insert()
pe.submit()
cr_note = self.create_credit_note(si1.name)
si2 = self.create_sales_invoice()
je = frappe.new_doc('Journal Entry')
je.company = self.company
je.voucher_type = 'Credit Note'
je.posting_date = today()
debit_entry = {'account': self.debit_to, 'party_type': 'Customer', 'party': self.customer, 'debit': 100, 'debit_in_account_currency': 100, 'reference_type': cr_note.doctype, 'reference_name': cr_note.name, 'cost_center': self.cost_center}
credit_entry = {'account': self.debit_to, 'party_type': 'Customer', 'party': self.customer, 'credit': 100, 'credit_in_account_currency': 100, 'reference_type': si2.doctype, 'reference_name': si2.name, 'cost_center': self.cost_center}
je.append('accounts', debit_entry)
je.append('accounts', credit_entry)
je = je.save().submit()
filters = {'company': self.company, 'report_date': today(), 'range': '30, 60, 90, 120'}
report = execute(filters)
self.assertEqual(report[1], [])
```

## Next Steps


---

*Source: test_accounts_receivable.py:508 | Complexity: Advanced | Last updated: 2026-02-03*