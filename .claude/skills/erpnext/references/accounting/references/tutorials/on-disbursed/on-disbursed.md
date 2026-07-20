# How To: On Disbursed

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test on disbursed

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
inv = create_sales_invoice(rate=500)
```

### Step 2: Assign inv_disc = create_invoice_discounting(...)

```python
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account, bank_charges=100)
```

### Step 3: Assign je = inv_disc.create_disbursement_entry(...)

```python
je = inv_disc.create_disbursement_entry()
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(je.accounts[0].account, self.bank_account)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(je.accounts[0].debit_in_account_currency, flt(inv_disc.total_amount) - flt(inv_disc.bank_charges))
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(je.accounts[1].account, self.bank_charges_account)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(je.accounts[1].debit_in_account_currency, flt(inv_disc.bank_charges))
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(je.accounts[2].account, self.short_term_loan)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(je.accounts[2].credit_in_account_currency, flt(inv_disc.total_amount))
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(je.accounts[3].account, self.ar_discounted)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(je.accounts[3].debit_in_account_currency, flt(inv.outstanding_amount))
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(je.accounts[4].account, self.ar_credit)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(je.accounts[4].credit_in_account_currency, flt(inv.outstanding_amount))
```

### Step 14: Assign je.posting_date = nowdate(...)

```python
je.posting_date = nowdate()
```

### Step 15: Call je.submit()

```python
je.submit()
```

### Step 16: Call inv_disc.reload()

```python
inv_disc.reload()
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(inv_disc.status, 'Disbursed')
```

### Step 18: Call inv.reload()

```python
inv.reload()
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(inv.outstanding_amount, 500)
```


## Complete Example

```python
# Workflow
inv = create_sales_invoice(rate=500)
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account, bank_charges=100)
je = inv_disc.create_disbursement_entry()
self.assertEqual(je.accounts[0].account, self.bank_account)
self.assertEqual(je.accounts[0].debit_in_account_currency, flt(inv_disc.total_amount) - flt(inv_disc.bank_charges))
self.assertEqual(je.accounts[1].account, self.bank_charges_account)
self.assertEqual(je.accounts[1].debit_in_account_currency, flt(inv_disc.bank_charges))
self.assertEqual(je.accounts[2].account, self.short_term_loan)
self.assertEqual(je.accounts[2].credit_in_account_currency, flt(inv_disc.total_amount))
self.assertEqual(je.accounts[3].account, self.ar_discounted)
self.assertEqual(je.accounts[3].debit_in_account_currency, flt(inv.outstanding_amount))
self.assertEqual(je.accounts[4].account, self.ar_credit)
self.assertEqual(je.accounts[4].credit_in_account_currency, flt(inv.outstanding_amount))
je.posting_date = nowdate()
je.submit()
inv_disc.reload()
self.assertEqual(inv_disc.status, 'Disbursed')
inv.reload()
self.assertEqual(inv.outstanding_amount, 500)
```

## Next Steps


---

*Source: test_invoice_discounting.py:96 | Complexity: Advanced | Last updated: 2026-02-03*