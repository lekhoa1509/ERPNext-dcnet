# How To: Payment Entry For Blocked Supplier Invoice

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test payment entry for blocked supplier invoice

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.setup.doctype.employee.test_employee`
- `erpnext.setup.doctype.currency_exchange.test_currency_exchange`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.accounts.utils`
- `erpnext.setup.doctype.currency_exchange.test_currency_exchange`
- `erpnext.accounts.party`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.doctype.opening_invoice_creation_tool.test_opening_invoice_creation_tool`


## Step-by-Step Guide

### Step 1: Assign supplier = frappe.get_doc(...)

```python
supplier = frappe.get_doc('Supplier', '_Test Supplier')
```

### Step 2: Assign supplier.on_hold = 1

```python
supplier.on_hold = 1
```

### Step 3: Assign supplier.hold_type = 'Invoices'

```python
supplier.hold_type = 'Invoices'
```

### Step 4: Call supplier.save()

```python
supplier.save()
```

### Step 5: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, make_purchase_invoice)
```

### Step 6: Assign supplier.on_hold = 0

```python
supplier.on_hold = 0
```

### Step 7: Call supplier.save()

```python
supplier.save()
```


## Complete Example

```python
# Workflow
supplier = frappe.get_doc('Supplier', '_Test Supplier')
supplier.on_hold = 1
supplier.hold_type = 'Invoices'
supplier.save()
self.assertRaises(frappe.ValidationError, make_purchase_invoice)
supplier.on_hold = 0
supplier.save()
```

## Next Steps


---

*Source: test_payment_entry.py:100 | Complexity: Intermediate | Last updated: 2026-02-03*