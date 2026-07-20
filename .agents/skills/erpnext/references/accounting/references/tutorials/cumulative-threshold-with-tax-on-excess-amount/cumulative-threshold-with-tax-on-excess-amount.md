# How To: Cumulative Threshold With Tax On Excess Amount

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test cumulative threshold with tax on excess amount

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

### Step 3: Assign pi1 = create_purchase_invoice(...)

```python
pi1 = create_purchase_invoice(supplier='Test TDS Supplier3', rate=20000)
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

### Step 8: Assign expected_entries = value

```python
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='New TDS Category', party_type='Supplier', party='Test TDS Supplier3', tax_rate=10.0, taxable_amount=10000.0, withholding_amount=0.0, status='Settled', taxable_doctype='Purchase Invoice', taxable_name=pi1.name, withholding_doctype='Purchase Invoice', withholding_name=pi1.name, under_withheld_reason='Threshold Exemption'), self.get_tax_withholding_entry(tax_withholding_category='New TDS Category', party_type='Supplier', party='Test TDS Supplier3', tax_rate=10.0, taxable_amount=10000.0, withholding_amount=1000.0, status='Settled', taxable_doctype='Purchase Invoice', taxable_name=pi1.name, withholding_doctype='Purchase Invoice', withholding_name=pi1.name, under_withheld_reason=None)]
```

### Step 9: Call self.validate_tax_withholding_entries()

```python
self.validate_tax_withholding_entries('Purchase Invoice', pi1.name, expected_entries)
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(len(pi1.taxes) > 0)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(pi1.taxes[0].tax_amount, 1000)
```

### Step 12: Call self.cleanup_invoices()

```python
self.cleanup_invoices(invoices)
```

### Step 13: Assign pi = create_purchase_invoice(...)

```python
pi = create_purchase_invoice(supplier='Test TDS Supplier3', rate=10000, do_not_save=True)
```

### Step 14: Assign pi.apply_tds = 1

```python
pi.apply_tds = 1
```

### Step 15: Call pi.append()

```python
pi.append('taxes', {'category': 'Total', 'charge_type': 'Actual', 'account_head': '_Test Account VAT - _TC', 'cost_center': 'Main - _TC', 'tax_amount': 500, 'description': 'Test'})
```

### Step 16: Call pi.save()

```python
pi.save()
```

### Step 17: Call pi.submit()

```python
pi.submit()
```

### Step 18: Call invoices.append()

```python
invoices.append(pi)
```

### Step 19: Assign expected_entries = value

```python
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='New TDS Category', party_type='Supplier', party='Test TDS Supplier3', tax_rate=10.0, taxable_amount=10000.0, withholding_amount=0.0, status='Settled', taxable_doctype='Purchase Invoice', taxable_name=pi.name, withholding_doctype='Purchase Invoice', withholding_name=pi.name, under_withheld_reason='Threshold Exemption')]
```

### Step 20: Call self.validate_tax_withholding_entries()

```python
self.validate_tax_withholding_entries('Purchase Invoice', pi.name, expected_entries)
```


## Complete Example

```python
# Workflow
invoices = []
self.setup_party_with_category('Supplier', 'Test TDS Supplier3', 'New TDS Category')
for _ in range(2):
    pi = create_purchase_invoice(supplier='Test TDS Supplier3', rate=10000, do_not_save=True)
    pi.apply_tds = 1
    pi.append('taxes', {'category': 'Total', 'charge_type': 'Actual', 'account_head': '_Test Account VAT - _TC', 'cost_center': 'Main - _TC', 'tax_amount': 500, 'description': 'Test'})
    pi.save()
    pi.submit()
    invoices.append(pi)
    expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='New TDS Category', party_type='Supplier', party='Test TDS Supplier3', tax_rate=10.0, taxable_amount=10000.0, withholding_amount=0.0, status='Settled', taxable_doctype='Purchase Invoice', taxable_name=pi.name, withholding_doctype='Purchase Invoice', withholding_name=pi.name, under_withheld_reason='Threshold Exemption')]
    self.validate_tax_withholding_entries('Purchase Invoice', pi.name, expected_entries)
pi1 = create_purchase_invoice(supplier='Test TDS Supplier3', rate=20000)
pi1.apply_tds = 1
pi1.save()
pi1.submit()
invoices.append(pi1)
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='New TDS Category', party_type='Supplier', party='Test TDS Supplier3', tax_rate=10.0, taxable_amount=10000.0, withholding_amount=0.0, status='Settled', taxable_doctype='Purchase Invoice', taxable_name=pi1.name, withholding_doctype='Purchase Invoice', withholding_name=pi1.name, under_withheld_reason='Threshold Exemption'), self.get_tax_withholding_entry(tax_withholding_category='New TDS Category', party_type='Supplier', party='Test TDS Supplier3', tax_rate=10.0, taxable_amount=10000.0, withholding_amount=1000.0, status='Settled', taxable_doctype='Purchase Invoice', taxable_name=pi1.name, withholding_doctype='Purchase Invoice', withholding_name=pi1.name, under_withheld_reason=None)]
self.validate_tax_withholding_entries('Purchase Invoice', pi1.name, expected_entries)
self.assertTrue(len(pi1.taxes) > 0)
self.assertEqual(pi1.taxes[0].tax_amount, 1000)
self.cleanup_invoices(invoices)
```

## Next Steps


---

*Source: test_tax_withholding_category.py:401 | Complexity: Advanced | Last updated: 2026-02-03*