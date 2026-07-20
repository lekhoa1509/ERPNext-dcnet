# How To: Purchase Register Ledger View

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test purchase register ledger view

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.report.purchase_register.purchase_register`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`


## Step-by-Step Guide

### Step 1: Call frappe.db.sql()

```python
frappe.db.sql("delete from `tabPurchase Invoice` where company='_Test Company 6'")
```

### Step 2: Call frappe.db.sql()

```python
frappe.db.sql("delete from `tabGL Entry` where company='_Test Company 6'")
```

### Step 3: Assign filters = frappe._dict(...)

```python
filters = frappe._dict(company='_Test Company 6', from_date=add_months(today(), -1), to_date=today(), include_payments=True, supplier='_Test Supplier')
```

### Step 4: Call make_purchase_invoice()

```python
make_purchase_invoice()
```

### Step 5: Assign pe = make_payment_entry(...)

```python
pe = make_payment_entry()
```

### Step 6: Assign report_results = execute(...)

```python
report_results = execute(filters)
```

### Step 7: Assign first_row = frappe._dict(...)

```python
first_row = frappe._dict(report_results[1][2])
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(first_row.voucher_type, 'Payment Entry')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(first_row.voucher_no, pe.name)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(first_row.payable_account, 'Creditors - _TC6')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(first_row.debit, 0)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(first_row.credit, 600)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(first_row.balance, 500)
```


## Complete Example

```python
# Workflow
frappe.db.sql("delete from `tabPurchase Invoice` where company='_Test Company 6'")
frappe.db.sql("delete from `tabGL Entry` where company='_Test Company 6'")
filters = frappe._dict(company='_Test Company 6', from_date=add_months(today(), -1), to_date=today(), include_payments=True, supplier='_Test Supplier')
make_purchase_invoice()
pe = make_payment_entry()
report_results = execute(filters)
first_row = frappe._dict(report_results[1][2])
self.assertEqual(first_row.voucher_type, 'Payment Entry')
self.assertEqual(first_row.voucher_no, pe.name)
self.assertEqual(first_row.payable_account, 'Creditors - _TC6')
self.assertEqual(first_row.debit, 0)
self.assertEqual(first_row.credit, 600)
self.assertEqual(first_row.balance, 500)
```

## Next Steps


---

*Source: test_purchase_register.py:29 | Complexity: Advanced | Last updated: 2026-02-03*