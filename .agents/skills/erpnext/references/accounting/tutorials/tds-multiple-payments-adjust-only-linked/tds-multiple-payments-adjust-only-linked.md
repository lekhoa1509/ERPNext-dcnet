# How To: Tds Multiple Payments Adjust Only Linked

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that when multiple advance payment entries exist for the same supplier,
only the payment entry that is linked/allocated to the invoice is adjusted.

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

### Step 1: '\n\t\tTest that when multiple advance payment entries exist for the same supplier,\n\t\tonly the payment entry that is linked/allocated to the invoice is adjusted.\n\t\t'

```python
'\n\t\tTest that when multiple advance payment entries exist for the same supplier,\n\t\tonly the payment entry that is linked/allocated to the invoice is adjusted.\n\t\t'
```

### Step 2: Call self.setup_party_with_category()

```python
self.setup_party_with_category('Supplier', 'Test TDS Supplier', 'Cumulative Threshold TDS')
```

### Step 3: Assign vouchers = value

```python
vouchers = []
```

### Step 4: Assign pe1 = create_payment_entry(...)

```python
pe1 = create_payment_entry(payment_type='Pay', party_type='Supplier', party='Test TDS Supplier', paid_amount=5000)
```

### Step 5: Assign pe1.apply_tds = 1

```python
pe1.apply_tds = 1
```

### Step 6: Assign pe1.tax_withholding_category = 'Cumulative Threshold TDS'

```python
pe1.tax_withholding_category = 'Cumulative Threshold TDS'
```

### Step 7: Call pe1.save()

```python
pe1.save()
```

### Step 8: Call pe1.submit()

```python
pe1.submit()
```

### Step 9: Call vouchers.append()

```python
vouchers.append(pe1)
```

### Step 10: Assign pe1_expected_entries = value

```python
pe1_expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', tax_rate=10.0, taxable_amount=5000.0, withholding_amount=500.0, status='Over Withheld', taxable_doctype='', taxable_name='', withholding_doctype='Payment Entry', withholding_name=pe1.name)]
```

### Step 11: Call self.validate_tax_withholding_entries()

```python
self.validate_tax_withholding_entries('Payment Entry', pe1.name, pe1_expected_entries)
```

### Step 12: Assign pe2 = create_payment_entry(...)

```python
pe2 = create_payment_entry(payment_type='Pay', party_type='Supplier', party='Test TDS Supplier', paid_amount=3000)
```

### Step 13: Assign pe2.apply_tds = 1

```python
pe2.apply_tds = 1
```

### Step 14: Assign pe2.tax_withholding_category = 'Cumulative Threshold TDS'

```python
pe2.tax_withholding_category = 'Cumulative Threshold TDS'
```

### Step 15: Call pe2.save()

```python
pe2.save()
```

### Step 16: Call pe2.submit()

```python
pe2.submit()
```

### Step 17: Call vouchers.append()

```python
vouchers.append(pe2)
```

### Step 18: Assign pe2_expected_entries = value

```python
pe2_expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', tax_rate=10.0, taxable_amount=3000.0, withholding_amount=300.0, status='Over Withheld', taxable_doctype='', taxable_name='', withholding_doctype='Payment Entry', withholding_name=pe2.name)]
```

### Step 19: Call self.validate_tax_withholding_entries()

```python
self.validate_tax_withholding_entries('Payment Entry', pe2.name, pe2_expected_entries)
```

### Step 20: Assign pi = create_purchase_invoice(...)

```python
pi = create_purchase_invoice(supplier='Test TDS Supplier', rate=40000)
```

### Step 21: Call pi.append()

```python
pi.append('advances', {'reference_type': pe1.doctype, 'reference_name': pe1.name, 'advance_amount': 5000, 'allocated_amount': 5000})
```

### Step 22: Call pi.submit()

```python
pi.submit()
```

### Step 23: Call vouchers.append()

```python
vouchers.append(pi)
```

### Step 24: Assign invoice_expected_entries = value

```python
invoice_expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', tax_rate=10.0, taxable_amount=35000.0, withholding_amount=3500.0, status='Settled', taxable_doctype='Purchase Invoice', taxable_name=pi.name, withholding_doctype='Purchase Invoice', withholding_name=pi.name), self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', tax_rate=10.0, taxable_amount=5000.0, withholding_amount=500.0, status='Settled', taxable_doctype='Purchase Invoice', taxable_name=pi.name, withholding_doctype='Payment Entry', withholding_name=pe1.name)]
```

### Step 25: Call self.validate_tax_withholding_entries()

```python
self.validate_tax_withholding_entries('Purchase Invoice', pi.name, invoice_expected_entries)
```

### Step 26: Call self.cleanup_invoices()

```python
self.cleanup_invoices(vouchers)
```


## Complete Example

```python
# Workflow
'\n\t\tTest that when multiple advance payment entries exist for the same supplier,\n\t\tonly the payment entry that is linked/allocated to the invoice is adjusted.\n\t\t'
self.setup_party_with_category('Supplier', 'Test TDS Supplier', 'Cumulative Threshold TDS')
vouchers = []
pe1 = create_payment_entry(payment_type='Pay', party_type='Supplier', party='Test TDS Supplier', paid_amount=5000)
pe1.apply_tds = 1
pe1.tax_withholding_category = 'Cumulative Threshold TDS'
pe1.save()
pe1.submit()
vouchers.append(pe1)
pe1_expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', tax_rate=10.0, taxable_amount=5000.0, withholding_amount=500.0, status='Over Withheld', taxable_doctype='', taxable_name='', withholding_doctype='Payment Entry', withholding_name=pe1.name)]
self.validate_tax_withholding_entries('Payment Entry', pe1.name, pe1_expected_entries)
pe2 = create_payment_entry(payment_type='Pay', party_type='Supplier', party='Test TDS Supplier', paid_amount=3000)
pe2.apply_tds = 1
pe2.tax_withholding_category = 'Cumulative Threshold TDS'
pe2.save()
pe2.submit()
vouchers.append(pe2)
pe2_expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', tax_rate=10.0, taxable_amount=3000.0, withholding_amount=300.0, status='Over Withheld', taxable_doctype='', taxable_name='', withholding_doctype='Payment Entry', withholding_name=pe2.name)]
self.validate_tax_withholding_entries('Payment Entry', pe2.name, pe2_expected_entries)
pi = create_purchase_invoice(supplier='Test TDS Supplier', rate=40000)
pi.append('advances', {'reference_type': pe1.doctype, 'reference_name': pe1.name, 'advance_amount': 5000, 'allocated_amount': 5000})
pi.submit()
vouchers.append(pi)
invoice_expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', tax_rate=10.0, taxable_amount=35000.0, withholding_amount=3500.0, status='Settled', taxable_doctype='Purchase Invoice', taxable_name=pi.name, withholding_doctype='Purchase Invoice', withholding_name=pi.name), self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', tax_rate=10.0, taxable_amount=5000.0, withholding_amount=500.0, status='Settled', taxable_doctype='Purchase Invoice', taxable_name=pi.name, withholding_doctype='Payment Entry', withholding_name=pe1.name)]
self.validate_tax_withholding_entries('Purchase Invoice', pi.name, invoice_expected_entries)
self.cleanup_invoices(vouchers)
```

## Next Steps


---

*Source: test_tax_withholding_category.py:714 | Complexity: Advanced | Last updated: 2026-02-03*