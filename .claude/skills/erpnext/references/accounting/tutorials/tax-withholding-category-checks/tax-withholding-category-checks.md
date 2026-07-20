# How To: Tax Withholding Category Checks

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test tax withholding category checks

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
self.setup_party_with_category('Supplier', 'Test TDS Supplier3', 'New TDS Category')
```

### Step 3: Assign pi = create_purchase_invoice(...)

```python
pi = create_purchase_invoice(supplier='Test TDS Supplier3', rate=20000, do_not_save=True)
```

### Step 4: Assign pi.apply_tds = 0

```python
pi.apply_tds = 0
```

### Step 5: Call pi.save()

```python
pi.save()
```

### Step 6: Call pi.submit()

```python
pi.submit()
```

### Step 7: Call invoices.append()

```python
invoices.append(pi)
```

### Step 8: Assign pi1 = create_purchase_invoice(...)

```python
pi1 = create_purchase_invoice(supplier='Test TDS Supplier3', rate=20000)
```

### Step 9: Call pi1.submit()

```python
pi1.submit()
```

### Step 10: Call invoices.append()

```python
invoices.append(pi1)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(pi1.taxes, [])
```

### Step 12: Call self.cleanup_invoices()

```python
self.cleanup_invoices(invoices)
```


## Complete Example

```python
# Workflow
invoices = []
self.setup_party_with_category('Supplier', 'Test TDS Supplier3', 'New TDS Category')
pi = create_purchase_invoice(supplier='Test TDS Supplier3', rate=20000, do_not_save=True)
pi.apply_tds = 0
pi.save()
pi.submit()
invoices.append(pi)
pi1 = create_purchase_invoice(supplier='Test TDS Supplier3', rate=20000)
pi1.submit()
invoices.append(pi1)
self.assertEqual(pi1.taxes, [])
self.cleanup_invoices(invoices)
```

## Next Steps


---

*Source: test_tax_withholding_category.py:341 | Complexity: Advanced | Last updated: 2026-02-03*