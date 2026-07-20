# How To: Bank Clearance

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bank clearance

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

### Step 1: Assign bank_clearance = frappe.get_doc(...)

```python
bank_clearance = frappe.get_doc('Bank Clearance')
```

### Step 2: Assign bank_clearance.account = '_Test Bank Clearance - _TC'

```python
bank_clearance.account = '_Test Bank Clearance - _TC'
```

### Step 3: Assign bank_clearance.from_date = add_months(...)

```python
bank_clearance.from_date = add_months(getdate(), -1)
```

### Step 4: Assign bank_clearance.to_date = getdate(...)

```python
bank_clearance.to_date = getdate()
```

### Step 5: Call bank_clearance.get_payment_entries()

```python
bank_clearance.get_payment_entries()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(bank_clearance.payment_entries), 1)
```


## Complete Example

```python
# Workflow
bank_clearance = frappe.get_doc('Bank Clearance')
bank_clearance.account = '_Test Bank Clearance - _TC'
bank_clearance.from_date = add_months(getdate(), -1)
bank_clearance.to_date = getdate()
bank_clearance.get_payment_entries()
self.assertEqual(len(bank_clearance.payment_entries), 1)
```

## Next Steps


---

*Source: test_bank_clearance.py:38 | Complexity: Intermediate | Last updated: 2026-02-03*