# How To: Gl Entries In Base Currency

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test gl entries in base currency

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
inv = create_sales_invoice(rate=200)
```

### Step 2: Assign inv_disc = create_invoice_discounting(...)

```python
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account)
```

### Step 3: Assign gle = get_gl_entries(...)

```python
gle = get_gl_entries('Invoice Discounting', inv_disc.name)
```

### Step 4: Assign expected_gle = value

```python
expected_gle = {inv.debit_to: [0.0, 200], self.ar_credit: [200, 0.0]}
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual([gle_value.debit, gle_value.credit], expected_gle.get(gle_value.account))
```


## Complete Example

```python
# Workflow
inv = create_sales_invoice(rate=200)
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account)
gle = get_gl_entries('Invoice Discounting', inv_disc.name)
expected_gle = {inv.debit_to: [0.0, 200], self.ar_credit: [200, 0.0]}
for _i, gle_value in enumerate(gle):
    self.assertEqual([gle_value.debit, gle_value.credit], expected_gle.get(gle_value.account))
```

## Next Steps


---

*Source: test_invoice_discounting.py:62 | Complexity: Intermediate | Last updated: 2026-02-03*