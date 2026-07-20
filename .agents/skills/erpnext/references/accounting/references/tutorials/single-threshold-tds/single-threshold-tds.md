# How To: Single Threshold Tds

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test single threshold tds

## Prerequisites

**Required Modules:**
- `datetime`
- `frappe`
- `frappe.custom.doctype.custom_field.custom_field`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.utils`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.accounts.doctype.tax_withholding_entry.tax_withholding_entry`


## Step-by-Step Guide

### Step 1: Assign invoices = value

```python
invoices = []
```

### Step 2: Call frappe.db.set_value()

```python
frappe.db.set_value('Supplier', 'Test TDS Supplier1', 'tax_withholding_category', 'Single Threshold TDS')
```

### Step 3: Assign pi = create_purchase_invoice(...)

```python
pi = create_purchase_invoice(supplier='Test TDS Supplier1', rate=20000)
```

### Step 4: Call pi.submit()

```python
pi.submit()
```

### Step 5: Call invoices.append()

```python
invoices.append(pi)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(pi.taxes_and_charges_deducted, 2000)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(pi.grand_total, 18000)
```

### Step 8: Assign gl_entries = frappe.db.get_all(...)

```python
gl_entries = frappe.db.get_all('GL Entry', filters={'voucher_no': pi.name}, fields=['account', {'SUM': 'debit', 'as': 'debit'}, {'SUM': 'credit', 'as': 'credit'}], group_by='account')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(gl_entries), 3)
```

### Step 10: Assign pi = create_purchase_invoice(...)

```python
pi = create_purchase_invoice(supplier='Test TDS Supplier1')
```

### Step 11: Call pi.submit()

```python
pi.submit()
```

### Step 12: Call invoices.append()

```python
invoices.append(pi)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(pi.taxes_and_charges_deducted, 1000)
```

### Step 14: Call self.cleanup_invoices()

```python
self.cleanup_invoices(invoices)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(d.credit, 20000)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(d.debit, 2000)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(d.debit, 20000)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(d.credit, 2000)
```


## Complete Example

```python
# Workflow
invoices = []
frappe.db.set_value('Supplier', 'Test TDS Supplier1', 'tax_withholding_category', 'Single Threshold TDS')
pi = create_purchase_invoice(supplier='Test TDS Supplier1', rate=20000)
pi.submit()
invoices.append(pi)
self.assertEqual(pi.taxes_and_charges_deducted, 2000)
self.assertEqual(pi.grand_total, 18000)
gl_entries = frappe.db.get_all('GL Entry', filters={'voucher_no': pi.name}, fields=['account', {'SUM': 'debit', 'as': 'debit'}, {'SUM': 'credit', 'as': 'credit'}], group_by='account')
self.assertEqual(len(gl_entries), 3)
for d in gl_entries:
    if d.account == pi.credit_to:
        self.assertEqual(d.credit, 20000)
        self.assertEqual(d.debit, 2000)
    elif d.account == pi.items[0].get('expense_account'):
        self.assertEqual(d.debit, 20000)
    elif d.account == pi.taxes[0].get('account_head'):
        self.assertEqual(d.credit, 2000)
    else:
        raise ValueError('Account head does not match.')
pi = create_purchase_invoice(supplier='Test TDS Supplier1')
pi.submit()
invoices.append(pi)
self.assertEqual(pi.taxes_and_charges_deducted, 1000)
self.cleanup_invoices(invoices)
```

## Next Steps


---

*Source: test_tax_withholding_category.py:301 | Complexity: Advanced | Last updated: 2026-02-03*