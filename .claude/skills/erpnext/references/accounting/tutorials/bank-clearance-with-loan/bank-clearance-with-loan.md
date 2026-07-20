# How To: Bank Clearance With Loan

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bank clearance with loan

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.accounts.doctype.mode_of_payment.test_mode_of_payment`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.tests.utils`
- `erpnext.buying.doctype.supplier.test_supplier`
- `erpnext.accounts.doctype.opening_invoice_creation_tool.test_opening_invoice_creation_tool`
- `lending.loan_management.doctype.loan.test_loan`


## Step-by-Step Guide

### Step 1: Call create_loan_accounts()

```python
create_loan_accounts()
```

### Step 2: Call create_loan_masters()

```python
create_loan_masters()
```

### Step 3: Call make_loan()

```python
make_loan()
```

### Step 4: Assign bank_clearance = frappe.get_doc(...)

```python
bank_clearance = frappe.get_doc('Bank Clearance')
```

### Step 5: Assign bank_clearance.account = '_Test Bank Clearance - _TC'

```python
bank_clearance.account = '_Test Bank Clearance - _TC'
```

### Step 6: Assign bank_clearance.from_date = add_months(...)

```python
bank_clearance.from_date = add_months(getdate(), -1)
```

### Step 7: Assign bank_clearance.to_date = getdate(...)

```python
bank_clearance.to_date = getdate()
```

### Step 8: Call bank_clearance.get_payment_entries()

```python
bank_clearance.get_payment_entries()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(bank_clearance.payment_entries), 3)
```

### Step 10: Call create_loan_product()

```python
create_loan_product('Clearance Loan', 'Clearance Loan', 2000000, 13.5, 25, 0, 5, 'Cash', '_Test Bank Clearance - _TC', '_Test Bank Clearance - _TC', 'Loan Account - _TC', 'Interest Income Account - _TC', 'Penalty Income Account - _TC')
```

### Step 11: Assign loan = create_loan(...)

```python
loan = create_loan('_Test Customer', 'Clearance Loan', 280000, 'Repay Over Number of Periods', 20, applicant_type='Customer')
```

### Step 12: Call loan.submit()

```python
loan.submit()
```

### Step 13: Call make_loan_disbursement_entry()

```python
make_loan_disbursement_entry(loan.name, loan.loan_amount, disbursement_date=getdate())
```

### Step 14: Assign repayment_entry = create_repayment_entry(...)

```python
repayment_entry = create_repayment_entry(loan.name, '_Test Customer', getdate(), loan.loan_amount)
```

### Step 15: Call repayment_entry.save()

```python
repayment_entry.save()
```

### Step 16: Call repayment_entry.submit()

```python
repayment_entry.submit()
```


## Complete Example

```python
# Workflow
from lending.loan_management.doctype.loan.test_loan import create_loan, create_loan_accounts, create_loan_product, create_repayment_entry, make_loan_disbursement_entry

def create_loan_masters():
    create_loan_product('Clearance Loan', 'Clearance Loan', 2000000, 13.5, 25, 0, 5, 'Cash', '_Test Bank Clearance - _TC', '_Test Bank Clearance - _TC', 'Loan Account - _TC', 'Interest Income Account - _TC', 'Penalty Income Account - _TC')

def make_loan():
    loan = create_loan('_Test Customer', 'Clearance Loan', 280000, 'Repay Over Number of Periods', 20, applicant_type='Customer')
    loan.submit()
    make_loan_disbursement_entry(loan.name, loan.loan_amount, disbursement_date=getdate())
    repayment_entry = create_repayment_entry(loan.name, '_Test Customer', getdate(), loan.loan_amount)
    repayment_entry.save()
    repayment_entry.submit()
create_loan_accounts()
create_loan_masters()
make_loan()
bank_clearance = frappe.get_doc('Bank Clearance')
bank_clearance.account = '_Test Bank Clearance - _TC'
bank_clearance.from_date = add_months(getdate(), -1)
bank_clearance.to_date = getdate()
bank_clearance.get_payment_entries()
self.assertEqual(len(bank_clearance.payment_entries), 3)
```

## Next Steps


---

*Source: test_bank_clearance.py:47 | Complexity: Advanced | Last updated: 2026-02-03*