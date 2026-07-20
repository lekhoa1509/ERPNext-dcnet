# How To: Reconcile

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test reconcile

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
bank_transaction = frappe.get_doc('Bank Transaction', dict(description='1512567 BG/000003025 OPSKATTUZWXXX AT776000000098709849 Herr G'))
```

### Step 2: Assign payment = frappe.get_doc(...)

```python
payment = frappe.get_doc('Payment Entry', dict(party='Mr G', paid_amount=1700))
```

### Step 3: Assign vouchers = json.dumps(...)

```python
vouchers = json.dumps([{'payment_doctype': 'Payment Entry', 'payment_name': payment.name, 'amount': bank_transaction.unallocated_amount}])
```

### Step 4: Call reconcile_vouchers()

```python
reconcile_vouchers(bank_transaction.name, vouchers)
```

### Step 5: Assign unallocated_amount = frappe.db.get_value(...)

```python
unallocated_amount = frappe.db.get_value('Bank Transaction', bank_transaction.name, 'unallocated_amount')
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(unallocated_amount == 0)
```

### Step 7: Assign clearance_date = frappe.db.get_value(...)

```python
clearance_date = frappe.db.get_value('Payment Entry', payment.name, 'clearance_date')
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(clearance_date is not None)
```

### Step 9: Call bank_transaction.reload()

```python
bank_transaction.reload()
```

### Step 10: Call bank_transaction.cancel()

```python
bank_transaction.cancel()
```

### Step 11: Assign clearance_date = frappe.db.get_value(...)

```python
clearance_date = frappe.db.get_value('Payment Entry', payment.name, 'clearance_date')
```

### Step 12: Call self.assertFalse()

```python
self.assertFalse(clearance_date)
```


## Complete Example

```python
# Workflow
bank_transaction = frappe.get_doc('Bank Transaction', dict(description='1512567 BG/000003025 OPSKATTUZWXXX AT776000000098709849 Herr G'))
payment = frappe.get_doc('Payment Entry', dict(party='Mr G', paid_amount=1700))
vouchers = json.dumps([{'payment_doctype': 'Payment Entry', 'payment_name': payment.name, 'amount': bank_transaction.unallocated_amount}])
reconcile_vouchers(bank_transaction.name, vouchers)
unallocated_amount = frappe.db.get_value('Bank Transaction', bank_transaction.name, 'unallocated_amount')
self.assertTrue(unallocated_amount == 0)
clearance_date = frappe.db.get_value('Payment Entry', payment.name, 'clearance_date')
self.assertTrue(clearance_date is not None)
bank_transaction.reload()
bank_transaction.cancel()
clearance_date = frappe.db.get_value('Payment Entry', payment.name, 'clearance_date')
self.assertFalse(clearance_date)
```

## Next Steps


---

*Source: test_bank_transaction.py:56 | Complexity: Advanced | Last updated: 2026-02-03*