# How To: Payment Against Sales Order Usd To Inr

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test payment against sales order usd to inr

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

### Step 1: Assign so = make_sales_order(...)

```python
so = make_sales_order(customer='_Test Customer USD', currency='USD', qty=1, rate=100, do_not_submit=True)
```

### Step 2: Assign so.conversion_rate = 50

```python
so.conversion_rate = 50
```

### Step 3: Call so.submit()

```python
so.submit()
```

### Step 4: Assign pe = get_payment_entry(...)

```python
pe = get_payment_entry('Sales Order', so.name)
```

### Step 5: Assign pe.source_exchange_rate = 55

```python
pe.source_exchange_rate = 55
```

### Step 6: Assign pe.received_amount = 5500

```python
pe.received_amount = 5500
```

### Step 7: Call pe.insert()

```python
pe.insert()
```

### Step 8: Call pe.submit()

```python
pe.submit()
```

### Step 9: Call pe.reload()

```python
pe.reload()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(pe.difference_amount, 0)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(pe.deductions, [])
```

### Step 12: Assign expected_gle = dict(...)

```python
expected_gle = dict(((d[0], d) for d in [['_Test Receivable USD - _TC', 0, 5500, pe.name], [pe.paid_to, 5500.0, 0, None]]))
```

### Step 13: Call self.validate_gl_entries()

```python
self.validate_gl_entries(pe.name, expected_gle)
```

### Step 14: Assign so_advance_paid = frappe.db.get_value(...)

```python
so_advance_paid = frappe.db.get_value('Sales Order', so.name, 'advance_paid')
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(so_advance_paid, 100)
```

### Step 16: Call pe.cancel()

```python
pe.cancel()
```

### Step 17: Assign so_advance_paid = frappe.db.get_value(...)

```python
so_advance_paid = frappe.db.get_value('Sales Order', so.name, 'advance_paid')
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(so_advance_paid, 0)
```


## Complete Example

```python
# Workflow
so = make_sales_order(customer='_Test Customer USD', currency='USD', qty=1, rate=100, do_not_submit=True)
so.conversion_rate = 50
so.submit()
pe = get_payment_entry('Sales Order', so.name)
pe.source_exchange_rate = 55
pe.received_amount = 5500
pe.insert()
pe.submit()
pe.reload()
self.assertEqual(pe.difference_amount, 0)
self.assertEqual(pe.deductions, [])
expected_gle = dict(((d[0], d) for d in [['_Test Receivable USD - _TC', 0, 5500, pe.name], [pe.paid_to, 5500.0, 0, None]]))
self.validate_gl_entries(pe.name, expected_gle)
so_advance_paid = frappe.db.get_value('Sales Order', so.name, 'advance_paid')
self.assertEqual(so_advance_paid, 100)
pe.cancel()
so_advance_paid = frappe.db.get_value('Sales Order', so.name, 'advance_paid')
self.assertEqual(so_advance_paid, 0)
```

## Next Steps


---

*Source: test_payment_entry.py:68 | Complexity: Advanced | Last updated: 2026-02-03*