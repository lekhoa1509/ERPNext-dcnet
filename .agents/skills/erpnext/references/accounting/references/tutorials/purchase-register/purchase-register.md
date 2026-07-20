# How To: Purchase Register

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test purchase register

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
filters = frappe._dict(company='_Test Company 6', from_date=add_months(today(), -1), to_date=today())
```

### Step 4: Assign pi = make_purchase_invoice(...)

```python
pi = make_purchase_invoice()
```

### Step 5: Assign report_results = execute(...)

```python
report_results = execute(filters)
```

### Step 6: Assign first_row = frappe._dict(...)

```python
first_row = frappe._dict(report_results[1][0])
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(first_row.voucher_type, 'Purchase Invoice')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(first_row.voucher_no, pi.name)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(first_row.payable_account, 'Creditors - _TC6')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(first_row.net_total, 1000)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(first_row.total_tax, 100)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(first_row.grand_total, 1100)
```


## Complete Example

```python
# Workflow
frappe.db.sql("delete from `tabPurchase Invoice` where company='_Test Company 6'")
frappe.db.sql("delete from `tabGL Entry` where company='_Test Company 6'")
filters = frappe._dict(company='_Test Company 6', from_date=add_months(today(), -1), to_date=today())
pi = make_purchase_invoice()
report_results = execute(filters)
first_row = frappe._dict(report_results[1][0])
self.assertEqual(first_row.voucher_type, 'Purchase Invoice')
self.assertEqual(first_row.voucher_no, pi.name)
self.assertEqual(first_row.payable_account, 'Creditors - _TC6')
self.assertEqual(first_row.net_total, 1000)
self.assertEqual(first_row.total_tax, 100)
self.assertEqual(first_row.grand_total, 1100)
```

## Next Steps


---

*Source: test_purchase_register.py:12 | Complexity: Advanced | Last updated: 2026-02-03*