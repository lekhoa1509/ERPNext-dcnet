# How To: On Close After Loan Period

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test on close after loan period

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.doctype.journal_entry.journal_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`


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

### Step 6: Assign je2 = inv_disc.close_loan(...)

```python
je2 = inv_disc.close_loan()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(je2.accounts[0].account, self.short_term_loan)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(je2.accounts[0].debit_in_account_currency, flt(inv_disc.total_amount))
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(je2.accounts[1].account, self.bank_account)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(je2.accounts[1].credit_in_account_currency, flt(inv_disc.total_amount))
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(je2.accounts[2].account, self.ar_discounted)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(je2.accounts[2].credit_in_account_currency, flt(inv.outstanding_amount))
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(je2.accounts[3].account, self.ar_unpaid)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(je2.accounts[3].debit_in_account_currency, flt(inv.outstanding_amount))
```

### Step 15: Assign je2.posting_date = nowdate(...)

```python
je2.posting_date = nowdate()
```

### Step 16: Call je2.submit()

```python
je2.submit()
```

### Step 17: Call inv_disc.reload()

```python
inv_disc.reload()
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(inv_disc.status, 'Settled')
```


## Complete Example

```python
# Workflow
inv = create_sales_invoice(rate=600)
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account, start=nowdate(), period=60)
je1 = inv_disc.create_disbursement_entry()
je1.posting_date = nowdate()
je1.submit()
je2 = inv_disc.close_loan()
self.assertEqual(je2.accounts[0].account, self.short_term_loan)
self.assertEqual(je2.accounts[0].debit_in_account_currency, flt(inv_disc.total_amount))
self.assertEqual(je2.accounts[1].account, self.bank_account)
self.assertEqual(je2.accounts[1].credit_in_account_currency, flt(inv_disc.total_amount))
self.assertEqual(je2.accounts[2].account, self.ar_discounted)
self.assertEqual(je2.accounts[2].credit_in_account_currency, flt(inv.outstanding_amount))
self.assertEqual(je2.accounts[3].account, self.ar_unpaid)
self.assertEqual(je2.accounts[3].debit_in_account_currency, flt(inv.outstanding_amount))
je2.posting_date = nowdate()
je2.submit()
inv_disc.reload()
self.assertEqual(inv_disc.status, 'Settled')
```

## Next Steps


---

*Source: test_invoice_discounting.py:138 | Complexity: Advanced | Last updated: 2026-02-03*