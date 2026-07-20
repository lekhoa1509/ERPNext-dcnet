# How To: On Close After Loan Period After Inv Payment

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test on close after loan period after inv payment

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
inv = create_sales_invoice(rate=600)
```

### Step 2: Assign inv_disc = create_invoice_discounting(...)

```python
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account, start=nowdate(), period=60)
```

### Step 3: Assign je1 = inv_disc.create_disbursement_entry(...)

```python
je1 = inv_disc.create_disbursement_entry()
```

### Step 4: Assign je1.posting_date = nowdate(...)

```python
je1.posting_date = nowdate()
```

### Step 5: Call je1.submit()

```python
je1.submit()
```

### Step 6: Assign je_on_payment = frappe.get_doc(...)

```python
je_on_payment = frappe.get_doc(get_payment_entry_against_invoice('Sales Invoice', inv.name))
```

### Step 7: Assign je_on_payment.posting_date = nowdate(...)

```python
je_on_payment.posting_date = nowdate()
```

### Step 8: Assign je_on_payment.cheque_no = '126981'

```python
je_on_payment.cheque_no = '126981'
```

### Step 9: Assign je_on_payment.cheque_date = nowdate(...)

```python
je_on_payment.cheque_date = nowdate()
```

### Step 10: Call je_on_payment.save()

```python
je_on_payment.save()
```

### Step 11: Call je_on_payment.submit()

```python
je_on_payment.submit()
```

### Step 12: Assign je2 = inv_disc.close_loan(...)

```python
je2 = inv_disc.close_loan()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(je2.accounts[0].account, self.short_term_loan)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(je2.accounts[0].debit_in_account_currency, flt(inv_disc.total_amount))
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(je2.accounts[1].account, self.bank_account)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(je2.accounts[1].credit_in_account_currency, flt(inv_disc.total_amount))
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
inv = create_sales_invoice(rate=600)
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account, start=nowdate(), period=60)
je1 = inv_disc.create_disbursement_entry()
je1.posting_date = nowdate()
je1.submit()
je_on_payment = frappe.get_doc(get_payment_entry_against_invoice('Sales Invoice', inv.name))
je_on_payment.posting_date = nowdate()
je_on_payment.cheque_no = '126981'
je_on_payment.cheque_date = nowdate()
je_on_payment.save()
je_on_payment.submit()
je2 = inv_disc.close_loan()
self.assertEqual(je2.accounts[0].account, self.short_term_loan)
self.assertEqual(je2.accounts[0].debit_in_account_currency, flt(inv_disc.total_amount))
self.assertEqual(je2.accounts[1].account, self.bank_account)
self.assertEqual(je2.accounts[1].credit_in_account_currency, flt(inv_disc.total_amount))
```

## Next Steps


---

*Source: test_invoice_discounting.py:176 | Complexity: Advanced | Last updated: 2026-02-03*