# How To: Payment Entry Against Si Usd To Usd

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test payment entry against si usd to usd

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

### Step 1: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(customer='_Test Customer USD', debit_to='_Test Receivable USD - _TC', currency='USD', conversion_rate=50)
```

### Step 2: Assign pe = get_payment_entry(...)

```python
pe = get_payment_entry('Sales Invoice', si.name, bank_account='_Test Bank USD - _TC')
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
expected_gle = dict(((d[0], d) for d in [['_Test Receivable USD - _TC', 0, 5000, si.name], ['_Test Bank USD - _TC', 5000.0, 0, None]]))
```

### Step 9: Call self.validate_gl_entries()

```python
self.validate_gl_entries(pe.name, expected_gle)
```

### Step 10: Assign outstanding_amount = flt(...)

```python
outstanding_amount = flt(frappe.db.get_value('Sales Invoice', si.name, 'outstanding_amount'))
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(outstanding_amount, 0)
```

### Step 12: Call pe.cancel()

```python
pe.cancel()
```

### Step 13: Assign outstanding_amount = flt(...)

```python
outstanding_amount = flt(frappe.db.get_value('Sales Invoice', si.name, 'outstanding_amount'))
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(outstanding_amount, 100)
```


## Complete Example

```python
# Workflow
si = create_sales_invoice(customer='_Test Customer USD', debit_to='_Test Receivable USD - _TC', currency='USD', conversion_rate=50)
pe = get_payment_entry('Sales Invoice', si.name, bank_account='_Test Bank USD - _TC')
pe.reference_no = '1'
pe.reference_date = '2016-01-01'
pe.source_exchange_rate = 50
pe.insert()
pe.submit()
expected_gle = dict(((d[0], d) for d in [['_Test Receivable USD - _TC', 0, 5000, si.name], ['_Test Bank USD - _TC', 5000.0, 0, None]]))
self.validate_gl_entries(pe.name, expected_gle)
outstanding_amount = flt(frappe.db.get_value('Sales Invoice', si.name, 'outstanding_amount'))
self.assertEqual(outstanding_amount, 0)
pe.cancel()
outstanding_amount = flt(frappe.db.get_value('Sales Invoice', si.name, 'outstanding_amount'))
self.assertEqual(outstanding_amount, 100)
```

## Next Steps


---

*Source: test_payment_entry.py:171 | Complexity: Advanced | Last updated: 2026-02-03*