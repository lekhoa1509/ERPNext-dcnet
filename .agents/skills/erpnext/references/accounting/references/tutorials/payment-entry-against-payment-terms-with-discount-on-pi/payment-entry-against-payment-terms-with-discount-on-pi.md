# How To: Payment Entry Against Payment Terms With Discount On Pi

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test payment entry against payment terms with discount on pi

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
pi = make_purchase_invoice(do_not_save=1)
```

### Step 2: Call create_payment_terms_template_with_discount()

```python
create_payment_terms_template_with_discount()
```

### Step 3: Assign pi.payment_terms_template = 'Test Discount Template'

```python
pi.payment_terms_template = 'Test Discount Template'
```

### Step 4: Call frappe.db.set_value()

```python
frappe.db.set_value('Company', pi.company, 'default_discount_account', 'Write Off - _TC')
```

### Step 5: Call pi.append()

```python
pi.append('taxes', {'charge_type': 'On Net Total', 'account_head': '_Test Account Service Tax - _TC', 'cost_center': '_Test Cost Center - _TC', 'description': 'Service Tax', 'rate': 18})
```

### Step 6: Call pi.save()

```python
pi.save()
```

### Step 7: Call pi.submit()

```python
pi.submit()
```

### Step 8: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Accounts Settings', 'book_tax_discount_loss', 1)
```

### Step 9: Assign pe_with_tax_loss = get_payment_entry(...)

```python
pe_with_tax_loss = get_payment_entry('Purchase Invoice', pi.name, bank_account='_Test Cash - _TC')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(pe_with_tax_loss.references[0].payment_term, '30 Credit Days with 10% Discount')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(pe_with_tax_loss.payment_type, 'Pay')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(pe_with_tax_loss.references[0].allocated_amount, 295.0)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(pe_with_tax_loss.paid_amount, 265.5)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(pe_with_tax_loss.difference_amount, 0)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(pe_with_tax_loss.deductions[0].amount, -25.0)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(pe_with_tax_loss.deductions[1].amount, -4.5)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(pe_with_tax_loss.deductions[1].account, '_Test Account Service Tax - _TC')
```

### Step 18: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Accounts Settings', 'book_tax_discount_loss', 0)
```

### Step 19: Assign pe = get_payment_entry(...)

```python
pe = get_payment_entry('Purchase Invoice', pi.name, bank_account='_Test Cash - _TC')
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(pe.references[0].payment_term, '30 Credit Days with 10% Discount')
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(pe.payment_type, 'Pay')
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(pe.references[0].allocated_amount, 295.0)
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(pe.paid_amount, 265.5)
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(pe.deductions[0].amount, -29.5)
```

### Step 25: Call self.assertEqual()

```python
self.assertEqual(pe.difference_amount, 0)
```


## Complete Example

```python
# Workflow
pi = make_purchase_invoice(do_not_save=1)
create_payment_terms_template_with_discount()
pi.payment_terms_template = 'Test Discount Template'
frappe.db.set_value('Company', pi.company, 'default_discount_account', 'Write Off - _TC')
pi.append('taxes', {'charge_type': 'On Net Total', 'account_head': '_Test Account Service Tax - _TC', 'cost_center': '_Test Cost Center - _TC', 'description': 'Service Tax', 'rate': 18})
pi.save()
pi.submit()
frappe.db.set_single_value('Accounts Settings', 'book_tax_discount_loss', 1)
pe_with_tax_loss = get_payment_entry('Purchase Invoice', pi.name, bank_account='_Test Cash - _TC')
self.assertEqual(pe_with_tax_loss.references[0].payment_term, '30 Credit Days with 10% Discount')
self.assertEqual(pe_with_tax_loss.payment_type, 'Pay')
self.assertEqual(pe_with_tax_loss.references[0].allocated_amount, 295.0)
self.assertEqual(pe_with_tax_loss.paid_amount, 265.5)
self.assertEqual(pe_with_tax_loss.difference_amount, 0)
self.assertEqual(pe_with_tax_loss.deductions[0].amount, -25.0)
self.assertEqual(pe_with_tax_loss.deductions[1].amount, -4.5)
self.assertEqual(pe_with_tax_loss.deductions[1].account, '_Test Account Service Tax - _TC')
frappe.db.set_single_value('Accounts Settings', 'book_tax_discount_loss', 0)
pe = get_payment_entry('Purchase Invoice', pi.name, bank_account='_Test Cash - _TC')
self.assertEqual(pe.references[0].payment_term, '30 Credit Days with 10% Discount')
self.assertEqual(pe.payment_type, 'Pay')
self.assertEqual(pe.references[0].allocated_amount, 295.0)
self.assertEqual(pe.paid_amount, 265.5)
self.assertEqual(pe.deductions[0].amount, -29.5)
self.assertEqual(pe.difference_amount, 0)
```

## Next Steps


---

*Source: test_payment_entry.py:287 | Complexity: Advanced | Last updated: 2026-02-03*