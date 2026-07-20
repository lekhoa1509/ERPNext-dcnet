# How To: Matching Loan Repayment

**Difficulty**: Advanced
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test matching loan repayment

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe`
- `frappe.model.docstatus`
- `frappe.tests`
- `erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool`
- `erpnext.accounts.doctype.mode_of_payment.test_mode_of_payment`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.pos_profile.test_pos_profile`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.tests.utils`
- `lending.loan_management.doctype.loan.test_loan`
- `lending.loan_management.doctype.process_loan_interest_accrual.process_loan_interest_accrual`
- `erpnext.setup.doctype.employee.test_employee`
- `lending.loan_management.doctype.loan.test_loan`


## Step-by-Step Guide

### Step 1: Call create_loan_accounts()

```python
create_loan_accounts()
```

### Step 2: Assign bank_account = frappe.get_doc.insert(...)

```python
bank_account = frappe.get_doc({'doctype': 'Bank Account', 'account_name': 'Payment Account', 'bank': 'Citi Bank', 'account': 'Payment Account - _TC'}).insert(ignore_if_duplicate=True)
```

### Step 3: Assign bank_transaction = frappe.get_doc.submit(...)

```python
bank_transaction = frappe.get_doc({'doctype': 'Bank Transaction', 'description': 'Loan Repayment - OPSKATTUZWXXX AT776000000098709837 Herr G', 'date': '2018-10-27', 'deposit': 500, 'currency': 'INR', 'bank_account': bank_account.name}).submit()
```

### Step 4: Assign repayment_entry = create_loan_and_repayment(...)

```python
repayment_entry = create_loan_and_repayment()
```

### Step 5: Assign linked_payments = get_linked_payments(...)

```python
linked_payments = get_linked_payments(bank_transaction.name, ['loan_repayment', 'exact_match'])
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(linked_payments[0]['name'], repayment_entry.name)
```


## Complete Example

```python
# Workflow
from lending.loan_management.doctype.loan.test_loan import create_loan_accounts
create_loan_accounts()
bank_account = frappe.get_doc({'doctype': 'Bank Account', 'account_name': 'Payment Account', 'bank': 'Citi Bank', 'account': 'Payment Account - _TC'}).insert(ignore_if_duplicate=True)
bank_transaction = frappe.get_doc({'doctype': 'Bank Transaction', 'description': 'Loan Repayment - OPSKATTUZWXXX AT776000000098709837 Herr G', 'date': '2018-10-27', 'deposit': 500, 'currency': 'INR', 'bank_account': bank_account.name}).submit()
repayment_entry = create_loan_and_repayment()
linked_payments = get_linked_payments(bank_transaction.name, ['loan_repayment', 'exact_match'])
self.assertEqual(linked_payments[0]['name'], repayment_entry.name)
```

## Next Steps


---

*Source: test_bank_transaction.py:190 | Complexity: Advanced | Last updated: 2026-02-03*