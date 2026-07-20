# How To: On Close Before Loan Period

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test on close before loan period

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
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account, start=add_days(nowdate(), -80), period=60)
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

### Step 6: Assign je2 = inv_disc.close_loan(...)

```python
je2 = inv_disc.close_loan()
```

### Step 7: Assign je2.posting_date = nowdate(...)

```python
je2.posting_date = nowdate()
```

### Step 8: Call je2.submit()

```python
je2.submit()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(je2.accounts[0].account, self.short_term_loan)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(je2.accounts[0].debit_in_account_currency, flt(inv_disc.total_amount))
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(je2.accounts[1].account, self.bank_account)
```

### Step 12: Call self.assertEqual()

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
inv = create_sales_invoice(rate=700)
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account, start=add_days(nowdate(), -80), period=60)
je1 = inv_disc.create_disbursement_entry()
je1.posting_date = nowdate()
je1.submit()
je2 = inv_disc.close_loan()
je2.posting_date = nowdate()
je2.submit()
self.assertEqual(je2.accounts[0].account, self.short_term_loan)
self.assertEqual(je2.accounts[0].debit_in_account_currency, flt(inv_disc.total_amount))
self.assertEqual(je2.accounts[1].account, self.bank_account)
self.assertEqual(je2.accounts[1].credit_in_account_currency, flt(inv_disc.total_amount))
```

## Next Steps


---

*Source: test_invoice_discounting.py:209 | Complexity: Advanced | Last updated: 2026-02-03*