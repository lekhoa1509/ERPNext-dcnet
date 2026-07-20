# How To: Payment Against Sales Invoice To Check Status

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test payment against sales invoice to check status

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

### Step 8: Assign unknown = frappe.db.get_value(...)

```python
outstanding_amount, status = frappe.db.get_value('Sales Invoice', si.name, ['outstanding_amount', 'status'])
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(flt(outstanding_amount), 0)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(status, 'Paid')
```

### Step 11: Call pe.cancel()

```python
pe.cancel()
```

### Step 12: Assign unknown = frappe.db.get_value(...)

```python
outstanding_amount, status = frappe.db.get_value('Sales Invoice', si.name, ['outstanding_amount', 'status'])
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(flt(outstanding_amount), 100)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(status, 'Unpaid')
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
outstanding_amount, status = frappe.db.get_value('Sales Invoice', si.name, ['outstanding_amount', 'status'])
self.assertEqual(flt(outstanding_amount), 0)
self.assertEqual(status, 'Paid')
pe.cancel()
outstanding_amount, status = frappe.db.get_value('Sales Invoice', si.name, ['outstanding_amount', 'status'])
self.assertEqual(flt(outstanding_amount), 100)
self.assertEqual(status, 'Unpaid')
```

## Next Steps


---

*Source: test_payment_entry.py:230 | Complexity: Advanced | Last updated: 2026-02-03*