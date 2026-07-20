# How To: Cumulative Threshold Tds With Account Change

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Cumulative threshold TDS without tax_on_excess, with account change in the middle of the year

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

### Step 1: 'Cumulative threshold TDS without tax_on_excess, with account change in the middle of the year'

```python
'Cumulative threshold TDS without tax_on_excess, with account change in the middle of the year'
```

### Step 2: Call self.setup_party_with_category()

```python
self.setup_party_with_category('Supplier', 'Test TDS Supplier', 'Multi Account TDS Category')
```

### Step 3: Assign invoices = value

```python
invoices = []
```

### Step 4: Assign pi = create_purchase_invoice(...)

```python
pi = create_purchase_invoice(supplier='Test TDS Supplier')
```

### Step 5: Call pi.submit()

```python
pi.submit()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(pi.taxes_and_charges_deducted, 3000)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(pi.grand_total, 7000)
```

### Step 8: Call invoices.append()

```python
invoices.append(pi)
```

### Step 9: Call frappe.db.set_value()

```python
frappe.db.set_value('Tax Withholding Account', {'parent': 'Multi Account TDS Category'}, 'account', '_Test Account VAT - _TC')
```

### Step 10: Assign pi = create_purchase_invoice(...)

```python
pi = create_purchase_invoice(supplier='Test TDS Supplier', rate=5000)
```

### Step 11: Call pi.submit()

```python
pi.submit()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(pi.taxes_and_charges_deducted, 500)
```

### Step 13: Call invoices.append()

```python
invoices.append(pi)
```

### Step 14: Call self.cleanup_invoices()

```python
self.cleanup_invoices(invoices)
```

### Step 15: Assign pi = create_purchase_invoice(...)

```python
pi = create_purchase_invoice(supplier='Test TDS Supplier')
```

### Step 16: Call pi.submit()

```python
pi.submit()
```

### Step 17: Call invoices.append()

```python
invoices.append(pi)
```


## Complete Example

```python
# Workflow
'Cumulative threshold TDS without tax_on_excess, with account change in the middle of the year'
self.setup_party_with_category('Supplier', 'Test TDS Supplier', 'Multi Account TDS Category')
invoices = []
for _ in range(2):
    pi = create_purchase_invoice(supplier='Test TDS Supplier')
    pi.submit()
    invoices.append(pi)
pi = create_purchase_invoice(supplier='Test TDS Supplier')
pi.submit()
self.assertEqual(pi.taxes_and_charges_deducted, 3000)
self.assertEqual(pi.grand_total, 7000)
invoices.append(pi)
frappe.db.set_value('Tax Withholding Account', {'parent': 'Multi Account TDS Category'}, 'account', '_Test Account VAT - _TC')
pi = create_purchase_invoice(supplier='Test TDS Supplier', rate=5000)
pi.submit()
self.assertEqual(pi.taxes_and_charges_deducted, 500)
invoices.append(pi)
self.cleanup_invoices(invoices)
```

## Next Steps


---

*Source: test_tax_withholding_category.py:261 | Complexity: Advanced | Last updated: 2026-02-03*