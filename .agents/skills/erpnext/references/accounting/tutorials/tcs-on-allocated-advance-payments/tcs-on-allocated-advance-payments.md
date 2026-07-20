# How To: Tcs On Allocated Advance Payments

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test tcs on allocated advance payments

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

### Step 1: Call self.setup_party_with_category()

```python
self.setup_party_with_category('Customer', 'Test TCS Customer', 'Cumulative Threshold TCS')
```

### Step 2: Assign vouchers = value

```python
vouchers = []
```

### Step 3: Assign pe = create_payment_entry(...)

```python
pe = create_payment_entry(payment_type='Receive', party_type='Customer', party='Test TCS Customer', paid_amount=30000)
```

### Step 4: Assign pe.paid_from = 'Debtors - _TC'

```python
pe.paid_from = 'Debtors - _TC'
```

### Step 5: Assign pe.paid_to = 'Cash - _TC'

```python
pe.paid_to = 'Cash - _TC'
```

### Step 6: Assign pe.apply_tds = 1

```python
pe.apply_tds = 1
```

### Step 7: Assign pe.tax_withholding_category = 'Cumulative Threshold TCS'

```python
pe.tax_withholding_category = 'Cumulative Threshold TCS'
```

### Step 8: Call pe.submit()

```python
pe.submit()
```

### Step 9: Call vouchers.append()

```python
vouchers.append(pe)
```

### Step 10: Assign payment_expected_entries = value

```python
payment_expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=30000.0, withholding_amount=3000.0, status='Over Withheld', taxable_doctype='', taxable_name='', withholding_doctype='Payment Entry', withholding_name=pe.name)]
```

### Step 11: Call self.validate_tax_withholding_entries()

```python
self.validate_tax_withholding_entries('Payment Entry', pe.name, payment_expected_entries)
```

### Step 12: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(customer='Test TCS Customer', rate=50000)
```

### Step 13: Assign advances = si.get_advance_entries(...)

```python
advances = si.get_advance_entries()
```

### Step 14: Call si.append()

```python
si.append('advances', {'reference_type': advances[0].reference_type, 'reference_name': advances[0].reference_name, 'advance_amount': advances[0].amount, 'allocated_amount': 30000})
```

### Step 15: Call si.submit()

```python
si.submit()
```

### Step 16: Call vouchers.append()

```python
vouchers.append(si)
```

### Step 17: Assign tcs_charged = sum(...)

```python
tcs_charged = sum([d.base_tax_amount for d in si.taxes if d.account_head == 'TCS - _TC'])
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(tcs_charged, 0)
```

### Step 19: Assign invoice_expected_entries = value

```python
invoice_expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=30000, withholding_amount=0, status='Settled', taxable_doctype='Sales Invoice', taxable_name=si.name, withholding_doctype='Sales Invoice', withholding_name=si.name, under_withheld_reason='Threshold Exemption'), self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=20000.0, withholding_amount=2000.0, status='Settled', taxable_doctype='Sales Invoice', taxable_name=si.name, withholding_doctype='Payment Entry', withholding_name=pe.name)]
```

### Step 20: Call self.validate_tax_withholding_entries()

```python
self.validate_tax_withholding_entries('Sales Invoice', si.name, invoice_expected_entries)
```

### Step 21: Call self.cleanup_invoices()

```python
self.cleanup_invoices(vouchers)
```


## Complete Example

```python
# Workflow
self.setup_party_with_category('Customer', 'Test TCS Customer', 'Cumulative Threshold TCS')
vouchers = []
pe = create_payment_entry(payment_type='Receive', party_type='Customer', party='Test TCS Customer', paid_amount=30000)
pe.paid_from = 'Debtors - _TC'
pe.paid_to = 'Cash - _TC'
pe.apply_tds = 1
pe.tax_withholding_category = 'Cumulative Threshold TCS'
pe.submit()
vouchers.append(pe)
payment_expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=30000.0, withholding_amount=3000.0, status='Over Withheld', taxable_doctype='', taxable_name='', withholding_doctype='Payment Entry', withholding_name=pe.name)]
self.validate_tax_withholding_entries('Payment Entry', pe.name, payment_expected_entries)
si = create_sales_invoice(customer='Test TCS Customer', rate=50000)
advances = si.get_advance_entries()
si.append('advances', {'reference_type': advances[0].reference_type, 'reference_name': advances[0].reference_name, 'advance_amount': advances[0].amount, 'allocated_amount': 30000})
si.submit()
vouchers.append(si)
tcs_charged = sum([d.base_tax_amount for d in si.taxes if d.account_head == 'TCS - _TC'])
self.assertEqual(tcs_charged, 0)
invoice_expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=30000, withholding_amount=0, status='Settled', taxable_doctype='Sales Invoice', taxable_name=si.name, withholding_doctype='Sales Invoice', withholding_name=si.name, under_withheld_reason='Threshold Exemption'), self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=20000.0, withholding_amount=2000.0, status='Settled', taxable_doctype='Sales Invoice', taxable_name=si.name, withholding_doctype='Payment Entry', withholding_name=pe.name)]
self.validate_tax_withholding_entries('Sales Invoice', si.name, invoice_expected_entries)
self.cleanup_invoices(vouchers)
```

## Next Steps


---

*Source: test_tax_withholding_category.py:623 | Complexity: Advanced | Last updated: 2026-02-03*