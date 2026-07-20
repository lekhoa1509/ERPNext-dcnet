# How To: Payment Entry Against Pi

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test payment entry against pi

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

### Step 1: Assign pi = make_purchase_invoice(...)

```python
pi = make_purchase_invoice(supplier='_Test Supplier USD', debit_to='_Test Payable USD - _TC', currency='USD', conversion_rate=50)
```

### Step 2: Assign pe = get_payment_entry(...)

```python
pe = get_payment_entry('Purchase Invoice', pi.name, bank_account='_Test Bank USD - _TC')
```

### Step 3: Assign pe.reference_no = '1'

```python
pe.reference_no = '1'
```

### Step 4: Assign pe.reference_date = '2016-01-01'

```python
pe.reference_date = '2016-01-01'
```

### Step 5: Assign pe.source_exchange_rate = 50

```python
pe.source_exchange_rate = 50
```

### Step 6: Call pe.insert()

```python
pe.insert()
```

### Step 7: Call pe.submit()

```python
pe.submit()
```

### Step 8: Assign expected_gle = dict(...)

```python
expected_gle = dict(((d[0], d) for d in [['_Test Payable USD - _TC', 12500, 0, pi.name], ['_Test Bank USD - _TC', 0, 12500, None]]))
```

### Step 9: Call self.validate_gl_entries()

```python
self.validate_gl_entries(pe.name, expected_gle)
```

### Step 10: Assign outstanding_amount = flt(...)

```python
outstanding_amount = flt(frappe.db.get_value('Sales Invoice', pi.name, 'outstanding_amount'))
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(outstanding_amount, 0)
```


## Complete Example

```python
# Workflow
pi = make_purchase_invoice(supplier='_Test Supplier USD', debit_to='_Test Payable USD - _TC', currency='USD', conversion_rate=50)
pe = get_payment_entry('Purchase Invoice', pi.name, bank_account='_Test Bank USD - _TC')
pe.reference_no = '1'
pe.reference_date = '2016-01-01'
pe.source_exchange_rate = 50
pe.insert()
pe.submit()
expected_gle = dict(((d[0], d) for d in [['_Test Payable USD - _TC', 12500, 0, pi.name], ['_Test Bank USD - _TC', 0, 12500, None]]))
self.validate_gl_entries(pe.name, expected_gle)
outstanding_amount = flt(frappe.db.get_value('Sales Invoice', pi.name, 'outstanding_amount'))
self.assertEqual(outstanding_amount, 0)
```

## Next Steps


---

*Source: test_payment_entry.py:203 | Complexity: Advanced | Last updated: 2026-02-03*