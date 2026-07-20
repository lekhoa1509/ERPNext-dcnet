# How To: Make Payment Before After Period

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test make payment before after period

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.doctype.journal_entry.journal_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`

**Setup Required:**
```python
self.ar_credit = create_account(account_name='_Test Accounts Receivable Credit', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.ar_discounted = create_account(account_name='_Test Accounts Receivable Discounted', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.ar_unpaid = create_account(account_name='_Test Accounts Receivable Unpaid', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.short_term_loan = create_account(account_name='_Test Short Term Loan', parent_account='Source of Funds (Liabilities) - _TC', company='_Test Company')
self.bank_account = create_account(account_name='_Test Bank 2', parent_account='Bank Accounts - _TC', company='_Test Company')
self.bank_charges_account = create_account(account_name='_Test Bank Charges Account', parent_account='Expenses - _TC', company='_Test Company')
frappe.db.set_value('Company', '_Test Company', 'default_bank_account', self.bank_account)
```

## Step-by-Step Guide

### Step 1: Assign inv = create_sales_invoice(...)

```python
inv = create_sales_invoice(rate=700)
```

### Step 2: Assign inv_disc = create_invoice_discounting(...)

```python
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account, loan_start_date=add_days(nowdate(), -10), period=5)
```

### Step 3: Assign je = inv_disc.create_disbursement_entry(...)

```python
je = inv_disc.create_disbursement_entry()
```

### Step 4: Call inv_disc.reload()

```python
inv_disc.reload()
```

### Step 5: Assign je.posting_date = nowdate(...)

```python
je.posting_date = nowdate()
```

### Step 6: Call je.submit()

```python
je.submit()
```

### Step 7: Assign je = inv_disc.close_loan(...)

```python
je = inv_disc.close_loan()
```

### Step 8: Call inv_disc.reload()

```python
inv_disc.reload()
```

### Step 9: Assign je.posting_date = nowdate(...)

```python
je.posting_date = nowdate()
```

### Step 10: Call je.submit()

```python
je.submit()
```

### Step 11: Assign je_on_payment = frappe.get_doc(...)

```python
je_on_payment = frappe.get_doc(get_payment_entry_against_invoice('Sales Invoice', inv.name))
```

### Step 12: Assign je_on_payment.posting_date = nowdate(...)

```python
je_on_payment.posting_date = nowdate()
```

### Step 13: Assign je_on_payment.cheque_no = '126981'

```python
je_on_payment.cheque_no = '126981'
```

### Step 14: Assign je_on_payment.cheque_date = nowdate(...)

```python
je_on_payment.cheque_date = nowdate()
```

### Step 15: Call je_on_payment.submit()

```python
je_on_payment.submit()
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(je_on_payment.accounts[0].account, self.ar_unpaid)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(je_on_payment.accounts[0].credit_in_account_currency, flt(inv.outstanding_amount))
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(je_on_payment.accounts[1].account, self.bank_account)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(je_on_payment.accounts[1].debit_in_account_currency, flt(inv.outstanding_amount))
```

### Step 20: Call inv.reload()

```python
inv.reload()
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(inv.outstanding_amount, 0)
```


## Complete Example

```python
# Setup
self.ar_credit = create_account(account_name='_Test Accounts Receivable Credit', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.ar_discounted = create_account(account_name='_Test Accounts Receivable Discounted', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.ar_unpaid = create_account(account_name='_Test Accounts Receivable Unpaid', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.short_term_loan = create_account(account_name='_Test Short Term Loan', parent_account='Source of Funds (Liabilities) - _TC', company='_Test Company')
self.bank_account = create_account(account_name='_Test Bank 2', parent_account='Bank Accounts - _TC', company='_Test Company')
self.bank_charges_account = create_account(account_name='_Test Bank Charges Account', parent_account='Expenses - _TC', company='_Test Company')
frappe.db.set_value('Company', '_Test Company', 'default_bank_account', self.bank_account)

# Workflow
inv = create_sales_invoice(rate=700)
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account, loan_start_date=add_days(nowdate(), -10), period=5)
je = inv_disc.create_disbursement_entry()
inv_disc.reload()
je.posting_date = nowdate()
je.submit()
je = inv_disc.close_loan()
inv_disc.reload()
je.posting_date = nowdate()
je.submit()
je_on_payment = frappe.get_doc(get_payment_entry_against_invoice('Sales Invoice', inv.name))
je_on_payment.posting_date = nowdate()
je_on_payment.cheque_no = '126981'
je_on_payment.cheque_date = nowdate()
je_on_payment.submit()
self.assertEqual(je_on_payment.accounts[0].account, self.ar_unpaid)
self.assertEqual(je_on_payment.accounts[0].credit_in_account_currency, flt(inv.outstanding_amount))
self.assertEqual(je_on_payment.accounts[1].account, self.bank_account)
self.assertEqual(je_on_payment.accounts[1].debit_in_account_currency, flt(inv.outstanding_amount))
inv.reload()
self.assertEqual(inv.outstanding_amount, 0)
```

## Next Steps


---

*Source: test_invoice_discounting.py:269 | Complexity: Advanced | Last updated: 2026-02-03*