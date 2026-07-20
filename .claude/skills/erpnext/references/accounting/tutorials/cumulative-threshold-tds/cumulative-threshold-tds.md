# How To: Cumulative Threshold Tds

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Tax withholding entries for cumulative threshold TDS with Tax on excess without single threshold

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

### Step 1: 'Tax withholding entries for cumulative threshold TDS with Tax on excess without single threshold'

```python
'Tax withholding entries for cumulative threshold TDS with Tax on excess without single threshold'
```

### Step 2: Call self.setup_party_with_category()

```python
self.setup_party_with_category('Supplier', 'Test TDS Supplier', 'Cumulative Threshold TDS')
```

### Step 3: Assign invoices = value

```python
invoices = []
```

### Step 4: Assign pi1 = create_purchase_invoice(...)

```python
pi1 = create_purchase_invoice(supplier='Test TDS Supplier')
```

### Step 5: Call pi1.submit()

```python
pi1.submit()
```

### Step 6: Assign expected_entries = value

```python
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', taxable_doctype='Purchase Invoice', taxable_name=pi1.name, tax_rate=10.0, taxable_amount=10000.0, withholding_amount=0.0, status='Under Withheld', withholding_doctype=None, withholding_name=None, under_withheld_reason=None)]
```

### Step 7: Call self.validate_tax_withholding_entries()

```python
self.validate_tax_withholding_entries('Purchase Invoice', pi1.name, expected_entries)
```

### Step 8: Assign pi2 = create_purchase_invoice(...)

```python
pi2 = create_purchase_invoice(supplier='Test TDS Supplier')
```

### Step 9: Call pi2.submit()

```python
pi2.submit()
```

### Step 10: Assign expected_entries = value

```python
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', taxable_doctype='Purchase Invoice', taxable_name=pi2.name, tax_rate=10.0, taxable_amount=10000.0, withholding_amount=0.0, status='Under Withheld', withholding_doctype=None, withholding_name=None, under_withheld_reason=None)]
```

### Step 11: Call self.validate_tax_withholding_entries()

```python
self.validate_tax_withholding_entries('Purchase Invoice', pi2.name, expected_entries)
```

### Step 12: Assign pi3 = create_purchase_invoice(...)

```python
pi3 = create_purchase_invoice(supplier='Test TDS Supplier')
```

### Step 13: Call pi3.submit()

```python
pi3.submit()
```

### Step 14: Assign expected_entries = value

```python
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', taxable_doctype='Purchase Invoice', taxable_name=pi1.name, withholding_amount=1000.0, tax_rate=10.0, taxable_amount=10000.0, status='Settled', withholding_doctype='Purchase Invoice', withholding_name=pi3.name, under_withheld_reason=None), self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', taxable_doctype='Purchase Invoice', taxable_name=pi2.name, withholding_amount=1000.0, tax_rate=10.0, taxable_amount=10000.0, status='Settled', withholding_doctype='Purchase Invoice', withholding_name=pi3.name, under_withheld_reason=None), self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', taxable_doctype='Purchase Invoice', taxable_name=pi3.name, tax_rate=10.0, taxable_amount=10000.0, withholding_amount=1000.0, status='Settled', withholding_doctype='Purchase Invoice', withholding_name=pi3.name, under_withheld_reason=None)]
```

### Step 15: Call self.validate_tax_deduction()

```python
self.validate_tax_deduction(pi3, 3000)
```

### Step 16: Call self.validate_tax_withholding_entries()

```python
self.validate_tax_withholding_entries('Purchase Invoice', pi3.name, expected_entries)
```

### Step 17: Call invoices.append()

```python
invoices.append(pi3)
```

### Step 18: Assign pi4 = create_purchase_invoice(...)

```python
pi4 = create_purchase_invoice(supplier='Test TDS Supplier', rate=5000)
```

### Step 19: Call pi4.submit()

```python
pi4.submit()
```

### Step 20: Assign expected_entries = value

```python
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', taxable_doctype='Purchase Invoice', taxable_name=pi4.name, tax_rate=10.0, taxable_amount=5000.0, withholding_amount=500.0, status='Settled', withholding_doctype='Purchase Invoice', withholding_name=pi4.name, under_withheld_reason=None)]
```

### Step 21: Call self.validate_tax_deduction()

```python
self.validate_tax_deduction(pi4, 500)
```

### Step 22: Call self.validate_tax_withholding_entries()

```python
self.validate_tax_withholding_entries('Purchase Invoice', pi4.name, expected_entries)
```

### Step 23: Call invoices.append()

```python
invoices.append(pi4)
```


## Complete Example

```python
# Workflow
'Tax withholding entries for cumulative threshold TDS with Tax on excess without single threshold'
self.setup_party_with_category('Supplier', 'Test TDS Supplier', 'Cumulative Threshold TDS')
invoices = []
pi1 = create_purchase_invoice(supplier='Test TDS Supplier')
pi1.submit()
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', taxable_doctype='Purchase Invoice', taxable_name=pi1.name, tax_rate=10.0, taxable_amount=10000.0, withholding_amount=0.0, status='Under Withheld', withholding_doctype=None, withholding_name=None, under_withheld_reason=None)]
self.validate_tax_withholding_entries('Purchase Invoice', pi1.name, expected_entries)
pi2 = create_purchase_invoice(supplier='Test TDS Supplier')
pi2.submit()
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', taxable_doctype='Purchase Invoice', taxable_name=pi2.name, tax_rate=10.0, taxable_amount=10000.0, withholding_amount=0.0, status='Under Withheld', withholding_doctype=None, withholding_name=None, under_withheld_reason=None)]
self.validate_tax_withholding_entries('Purchase Invoice', pi2.name, expected_entries)
pi3 = create_purchase_invoice(supplier='Test TDS Supplier')
pi3.submit()
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', taxable_doctype='Purchase Invoice', taxable_name=pi1.name, withholding_amount=1000.0, tax_rate=10.0, taxable_amount=10000.0, status='Settled', withholding_doctype='Purchase Invoice', withholding_name=pi3.name, under_withheld_reason=None), self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', taxable_doctype='Purchase Invoice', taxable_name=pi2.name, withholding_amount=1000.0, tax_rate=10.0, taxable_amount=10000.0, status='Settled', withholding_doctype='Purchase Invoice', withholding_name=pi3.name, under_withheld_reason=None), self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', taxable_doctype='Purchase Invoice', taxable_name=pi3.name, tax_rate=10.0, taxable_amount=10000.0, withholding_amount=1000.0, status='Settled', withholding_doctype='Purchase Invoice', withholding_name=pi3.name, under_withheld_reason=None)]
self.validate_tax_deduction(pi3, 3000)
self.validate_tax_withholding_entries('Purchase Invoice', pi3.name, expected_entries)
invoices.append(pi3)
pi4 = create_purchase_invoice(supplier='Test TDS Supplier', rate=5000)
pi4.submit()
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', taxable_doctype='Purchase Invoice', taxable_name=pi4.name, tax_rate=10.0, taxable_amount=5000.0, withholding_amount=500.0, status='Settled', withholding_doctype='Purchase Invoice', withholding_name=pi4.name, under_withheld_reason=None)]
self.validate_tax_deduction(pi4, 500)
self.validate_tax_withholding_entries('Purchase Invoice', pi4.name, expected_entries)
invoices.append(pi4)
```

## Next Steps


---

*Source: test_tax_withholding_category.py:132 | Complexity: Advanced | Last updated: 2026-02-03*