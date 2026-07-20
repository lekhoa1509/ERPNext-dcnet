# How To: Update Clearance Date On Si

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test update clearance date on si

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

### Step 1: Assign sales_invoice = make_pos_sales_invoice(...)

```python
sales_invoice = make_pos_sales_invoice()
```

### Step 2: Assign date = getdate(...)

```python
date = getdate()
```

### Step 3: Assign bank_clearance = frappe.get_doc(...)

```python
bank_clearance = frappe.get_doc('Bank Clearance')
```

### Step 4: Assign bank_clearance.account = '_Test Bank Clearance - _TC'

```python
bank_clearance.account = '_Test Bank Clearance - _TC'
```

### Step 5: Assign bank_clearance.from_date = add_months(...)

```python
bank_clearance.from_date = add_months(date, -1)
```

### Step 6: Assign bank_clearance.to_date = date

```python
bank_clearance.to_date = date
```

### Step 7: Assign bank_clearance.include_pos_transactions = 1

```python
bank_clearance.include_pos_transactions = 1
```

### Step 8: Call bank_clearance.get_payment_entries()

```python
bank_clearance.get_payment_entries()
```

### Step 9: Call self.assertNotEqual()

```python
self.assertNotEqual(len(bank_clearance.payment_entries), 0)
```

### Step 10: Call bank_clearance.update_clearance_date()

```python
bank_clearance.update_clearance_date()
```

### Step 11: Assign si_clearance_date = frappe.db.get_value(...)

```python
si_clearance_date = frappe.db.get_value('Sales Invoice Payment', {'parent': sales_invoice.name, 'account': bank_clearance.account}, 'clearance_date')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(si_clearance_date, date)
```

### Step 13: Assign payment.clearance_date = date

```python
payment.clearance_date = date
```


## Complete Example

```python
# Workflow
sales_invoice = make_pos_sales_invoice()
date = getdate()
bank_clearance = frappe.get_doc('Bank Clearance')
bank_clearance.account = '_Test Bank Clearance - _TC'
bank_clearance.from_date = add_months(date, -1)
bank_clearance.to_date = date
bank_clearance.include_pos_transactions = 1
bank_clearance.get_payment_entries()
self.assertNotEqual(len(bank_clearance.payment_entries), 0)
for payment in bank_clearance.payment_entries:
    if payment.payment_entry == sales_invoice.name:
        payment.clearance_date = date
bank_clearance.update_clearance_date()
si_clearance_date = frappe.db.get_value('Sales Invoice Payment', {'parent': sales_invoice.name, 'account': bank_clearance.account}, 'clearance_date')
self.assertEqual(si_clearance_date, date)
```

## Next Steps


---

*Source: test_bank_clearance.py:99 | Complexity: Advanced | Last updated: 2026-02-03*