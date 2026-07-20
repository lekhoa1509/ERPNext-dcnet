# How To: Cumulative Threshold With Party Ledger Amount On Net Total

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test cumulative threshold with party ledger amount on net total

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

### Step 2: Call self.setup_party_with_category()

```python
self.setup_party_with_category('Supplier', 'Test TDS Supplier3', 'Advance TDS Category')
```

### Step 3: Assign pi1 = create_purchase_invoice(...)

```python
pi1 = create_purchase_invoice(supplier='Test TDS Supplier3', rate=6000)
```

### Step 4: Assign pi1.apply_tds = 1

```python
pi1.apply_tds = 1
```

### Step 5: Call pi1.save()

```python
pi1.save()
```

### Step 6: Call pi1.submit()

```python
pi1.submit()
```

### Step 7: Call invoices.append()

```python
invoices.append(pi1)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(pi1.taxes[0].tax_amount, 800)
```

### Step 9: Call self.cleanup_invoices()

```python
self.cleanup_invoices(invoices)
```

### Step 10: Assign pi = create_purchase_invoice(...)

```python
pi = create_purchase_invoice(supplier='Test TDS Supplier3', rate=1000, do_not_save=True)
```

### Step 11: Assign pi.apply_tds = 1

```python
pi.apply_tds = 1
```

### Step 12: Call pi.append()

```python
pi.append('taxes', {'category': 'Total', 'charge_type': 'Actual', 'account_head': '_Test Account VAT - _TC', 'cost_center': 'Main - _TC', 'tax_amount': 500, 'description': 'Test', 'add_deduct_tax': 'Add'})
```

### Step 13: Call pi.save()

```python
pi.save()
```

### Step 14: Call pi.submit()

```python
pi.submit()
```

### Step 15: Call invoices.append()

```python
invoices.append(pi)
```


## Complete Example

```python
# Workflow
invoices = []
self.setup_party_with_category('Supplier', 'Test TDS Supplier3', 'Advance TDS Category')
for _ in range(2):
    pi = create_purchase_invoice(supplier='Test TDS Supplier3', rate=1000, do_not_save=True)
    pi.apply_tds = 1
    pi.append('taxes', {'category': 'Total', 'charge_type': 'Actual', 'account_head': '_Test Account VAT - _TC', 'cost_center': 'Main - _TC', 'tax_amount': 500, 'description': 'Test', 'add_deduct_tax': 'Add'})
    pi.save()
    pi.submit()
    invoices.append(pi)
pi1 = create_purchase_invoice(supplier='Test TDS Supplier3', rate=6000)
pi1.apply_tds = 1
pi1.save()
pi1.submit()
invoices.append(pi1)
self.assertEqual(pi1.taxes[0].tax_amount, 800)
self.cleanup_invoices(invoices)
```

## Next Steps


---

*Source: test_tax_withholding_category.py:364 | Complexity: Advanced | Last updated: 2026-02-03*