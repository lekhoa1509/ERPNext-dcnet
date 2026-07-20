# How To: Payment Entry Against Payment Terms With Discount

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test payment entry against payment terms with discount

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
si = create_sales_invoice(do_not_save=1, qty=1, rate=200)
```

### Step 2: Call create_payment_terms_template_with_discount()

```python
create_payment_terms_template_with_discount()
```

### Step 3: Assign si.payment_terms_template = 'Test Discount Template'

```python
si.payment_terms_template = 'Test Discount Template'
```

### Step 4: Call frappe.db.set_value()

```python
frappe.db.set_value('Company', si.company, 'default_discount_account', 'Write Off - _TC')
```

### Step 5: Call si.append()

```python
si.append('taxes', {'charge_type': 'On Net Total', 'account_head': '_Test Account Service Tax - _TC', 'cost_center': '_Test Cost Center - _TC', 'description': 'Service Tax', 'rate': 18})
```

### Step 6: Call si.save()

```python
si.save()
```

### Step 7: Call si.submit()

```python
si.submit()
```

### Step 8: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Accounts Settings', 'book_tax_discount_loss', 1)
```

### Step 9: Assign pe_with_tax_loss = get_payment_entry(...)

```python
pe_with_tax_loss = get_payment_entry('Sales Invoice', si.name, bank_account='_Test Cash - _TC')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(pe_with_tax_loss.references[0].payment_term, '30 Credit Days with 10% Discount')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(pe_with_tax_loss.references[0].allocated_amount, 236.0)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(pe_with_tax_loss.paid_amount, 212.4)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(pe_with_tax_loss.deductions[0].amount, 20.0)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(pe_with_tax_loss.deductions[1].amount, 3.6)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(pe_with_tax_loss.deductions[1].account, '_Test Account Service Tax - _TC')
```

### Step 16: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Accounts Settings', 'book_tax_discount_loss', 0)
```

### Step 17: Assign pe = get_payment_entry(...)

```python
pe = get_payment_entry('Sales Invoice', si.name, bank_account='_Test Cash - _TC')
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(pe.references[0].allocated_amount, 236.0)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(pe.paid_amount, 212.4)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(pe.deductions[0].amount, 23.6)
```

### Step 21: Call pe.submit()

```python
pe.submit()
```

### Step 22: Call si.load_from_db()

```python
si.load_from_db()
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(pe.references[0].payment_term, '30 Credit Days with 10% Discount')
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(si.payment_schedule[0].payment_amount, 236.0)
```

### Step 25: Call self.assertEqual()

```python
self.assertEqual(si.payment_schedule[0].paid_amount, 212.4)
```

### Step 26: Call self.assertEqual()

```python
self.assertEqual(si.payment_schedule[0].outstanding, 0)
```

### Step 27: Call self.assertEqual()

```python
self.assertEqual(si.payment_schedule[0].discounted_amount, 23.6)
```


## Complete Example

```python
# Workflow
si = create_sales_invoice(do_not_save=1, qty=1, rate=200)
create_payment_terms_template_with_discount()
si.payment_terms_template = 'Test Discount Template'
frappe.db.set_value('Company', si.company, 'default_discount_account', 'Write Off - _TC')
si.append('taxes', {'charge_type': 'On Net Total', 'account_head': '_Test Account Service Tax - _TC', 'cost_center': '_Test Cost Center - _TC', 'description': 'Service Tax', 'rate': 18})
si.save()
si.submit()
frappe.db.set_single_value('Accounts Settings', 'book_tax_discount_loss', 1)
pe_with_tax_loss = get_payment_entry('Sales Invoice', si.name, bank_account='_Test Cash - _TC')
self.assertEqual(pe_with_tax_loss.references[0].payment_term, '30 Credit Days with 10% Discount')
self.assertEqual(pe_with_tax_loss.references[0].allocated_amount, 236.0)
self.assertEqual(pe_with_tax_loss.paid_amount, 212.4)
self.assertEqual(pe_with_tax_loss.deductions[0].amount, 20.0)
self.assertEqual(pe_with_tax_loss.deductions[1].amount, 3.6)
self.assertEqual(pe_with_tax_loss.deductions[1].account, '_Test Account Service Tax - _TC')
frappe.db.set_single_value('Accounts Settings', 'book_tax_discount_loss', 0)
pe = get_payment_entry('Sales Invoice', si.name, bank_account='_Test Cash - _TC')
self.assertEqual(pe.references[0].allocated_amount, 236.0)
self.assertEqual(pe.paid_amount, 212.4)
self.assertEqual(pe.deductions[0].amount, 23.6)
pe.submit()
si.load_from_db()
self.assertEqual(pe.references[0].payment_term, '30 Credit Days with 10% Discount')
self.assertEqual(si.payment_schedule[0].payment_amount, 236.0)
self.assertEqual(si.payment_schedule[0].paid_amount, 212.4)
self.assertEqual(si.payment_schedule[0].outstanding, 0)
self.assertEqual(si.payment_schedule[0].discounted_amount, 23.6)
```

## Next Steps


---

*Source: test_payment_entry.py:329 | Complexity: Advanced | Last updated: 2026-02-03*