# How To: Already Reconciled

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test already reconciled

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

### Step 1: Assign bank_transaction = frappe.get_doc(...)

```python
bank_transaction = frappe.get_doc('Bank Transaction', dict(description='1512567 BG/000002918 OPSKATTUZWXXX AT776000000098709837 Herr G'))
```

### Step 2: Assign payment = frappe.get_doc(...)

```python
payment = frappe.get_doc('Payment Entry', dict(party='Mr G', paid_amount=1200))
```

### Step 3: Assign vouchers = json.dumps(...)

```python
vouchers = json.dumps([{'payment_doctype': 'Payment Entry', 'payment_name': payment.name, 'amount': bank_transaction.unallocated_amount}])
```

### Step 4: Call reconcile_vouchers()

```python
reconcile_vouchers(bank_transaction.name, vouchers)
```

### Step 5: Assign bank_transaction = frappe.get_doc(...)

```python
bank_transaction = frappe.get_doc('Bank Transaction', dict(description='1512567 BG/000002918 OPSKATTUZWXXX AT776000000098709837 Herr G'))
```

### Step 6: Assign payment = frappe.get_doc(...)

```python
payment = frappe.get_doc('Payment Entry', dict(party='Mr G', paid_amount=1200))
```

### Step 7: Assign vouchers = json.dumps(...)

```python
vouchers = json.dumps([{'payment_doctype': 'Payment Entry', 'payment_name': payment.name, 'amount': bank_transaction.unallocated_amount}])
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, reconcile_vouchers, bank_transaction_name=bank_transaction.name, vouchers=vouchers)
```


## Complete Example

```python
# Workflow
bank_transaction = frappe.get_doc('Bank Transaction', dict(description='1512567 BG/000002918 OPSKATTUZWXXX AT776000000098709837 Herr G'))
payment = frappe.get_doc('Payment Entry', dict(party='Mr G', paid_amount=1200))
vouchers = json.dumps([{'payment_doctype': 'Payment Entry', 'payment_name': payment.name, 'amount': bank_transaction.unallocated_amount}])
reconcile_vouchers(bank_transaction.name, vouchers)
bank_transaction = frappe.get_doc('Bank Transaction', dict(description='1512567 BG/000002918 OPSKATTUZWXXX AT776000000098709837 Herr G'))
payment = frappe.get_doc('Payment Entry', dict(party='Mr G', paid_amount=1200))
vouchers = json.dumps([{'payment_doctype': 'Payment Entry', 'payment_name': payment.name, 'amount': bank_transaction.unallocated_amount}])
self.assertRaises(frappe.ValidationError, reconcile_vouchers, bank_transaction_name=bank_transaction.name, vouchers=vouchers)
```

## Next Steps


---

*Source: test_bank_transaction.py:125 | Complexity: Advanced | Last updated: 2026-02-03*