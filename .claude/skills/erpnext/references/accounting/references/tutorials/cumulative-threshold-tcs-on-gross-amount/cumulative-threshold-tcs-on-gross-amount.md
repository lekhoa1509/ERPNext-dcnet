# How To: Cumulative Threshold Tcs On Gross Amount

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test cumulative threshold tcs on gross amount

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

### Step 2: Assign invoices = value

```python
invoices = []
```

### Step 3: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(customer='Test TCS Customer', rate=12000)
```

### Step 4: Call si.append()

```python
si.append('taxes', {'category': 'Total', 'charge_type': 'Actual', 'account_head': 'TCS - _TC', 'cost_center': 'Main - _TC', 'tax_amount': 400, 'description': 'Test Gross Tax'})
```

### Step 5: Call si.save()

```python
si.save()
```

### Step 6: Call si.reload()

```python
si.reload()
```

### Step 7: Call si.submit()

```python
si.submit()
```

### Step 8: Call invoices.append()

```python
invoices.append(si)
```

### Step 9: Assign expected_entries = value

```python
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=9600.0, withholding_amount=0.0, status='Settled', taxable_doctype='Sales Invoice', taxable_name=si.name, withholding_doctype='Sales Invoice', withholding_name=si.name, under_withheld_reason='Threshold Exemption'), self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=2800.0, withholding_amount=280.0, status='Settled', taxable_doctype='Sales Invoice', taxable_name=si.name, withholding_doctype='Sales Invoice', withholding_name=si.name, under_withheld_reason=None)]
```

### Step 10: Call self.validate_tax_withholding_entries()

```python
self.validate_tax_withholding_entries('Sales Invoice', si.name, expected_entries)
```

### Step 11: Call self.validate_tax_deduction()

```python
self.validate_tax_deduction(si, 280)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(si.grand_total, 12680)
```

### Step 13: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(customer='Test TCS Customer', rate=5000)
```

### Step 14: Call si.append()

```python
si.append('taxes', {'category': 'Total', 'charge_type': 'Actual', 'account_head': '_Test Account VAT - _TC', 'cost_center': 'Main - _TC', 'tax_amount': 500, 'description': 'VAT added to test TDS calculation on gross amount'})
```

### Step 15: Call si.save()

```python
si.save()
```

### Step 16: Call si.submit()

```python
si.submit()
```

### Step 17: Call invoices.append()

```python
invoices.append(si)
```

### Step 18: Assign expected_entries = value

```python
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=5500.0, withholding_amount=550.0, status='Settled', taxable_doctype='Sales Invoice', taxable_name=si.name, withholding_doctype='Sales Invoice', withholding_name=si.name, under_withheld_reason=None)]
```

### Step 19: Call self.validate_tax_withholding_entries()

```python
self.validate_tax_withholding_entries('Sales Invoice', si.name, expected_entries)
```

### Step 20: Call self.validate_tax_deduction()

```python
self.validate_tax_deduction(si, 550)
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(si.grand_total, 6050)
```

### Step 22: Call self.cleanup_invoices()

```python
self.cleanup_invoices(invoices)
```

### Step 23: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(customer='Test TCS Customer')
```

### Step 24: Call si.append()

```python
si.append('taxes', {'category': 'Total', 'charge_type': 'Actual', 'account_head': 'TCS - _TC', 'cost_center': 'Main - _TC', 'tax_amount': 200, 'description': 'Test Gross Tax'})
```

### Step 25: Call si.save()

```python
si.save()
```

### Step 26: Call si.submit()

```python
si.submit()
```

### Step 27: Call invoices.append()

```python
invoices.append(si)
```

### Step 28: Assign expected_entries = value

```python
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=10200.0, withholding_amount=0.0, status='Settled', taxable_doctype='Sales Invoice', taxable_name=si.name, withholding_doctype='Sales Invoice', withholding_name=si.name, under_withheld_reason='Threshold Exemption')]
```

### Step 29: Call self.validate_tax_withholding_entries()

```python
self.validate_tax_withholding_entries('Sales Invoice', si.name, expected_entries)
```


## Complete Example

```python
# Workflow
self.setup_party_with_category('Customer', 'Test TCS Customer', 'Cumulative Threshold TCS')
invoices = []
for _ in range(2):
    si = create_sales_invoice(customer='Test TCS Customer')
    si.append('taxes', {'category': 'Total', 'charge_type': 'Actual', 'account_head': 'TCS - _TC', 'cost_center': 'Main - _TC', 'tax_amount': 200, 'description': 'Test Gross Tax'})
    si.save()
    si.submit()
    invoices.append(si)
    expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=10200.0, withholding_amount=0.0, status='Settled', taxable_doctype='Sales Invoice', taxable_name=si.name, withholding_doctype='Sales Invoice', withholding_name=si.name, under_withheld_reason='Threshold Exemption')]
    self.validate_tax_withholding_entries('Sales Invoice', si.name, expected_entries)
si = create_sales_invoice(customer='Test TCS Customer', rate=12000)
si.append('taxes', {'category': 'Total', 'charge_type': 'Actual', 'account_head': 'TCS - _TC', 'cost_center': 'Main - _TC', 'tax_amount': 400, 'description': 'Test Gross Tax'})
si.save()
si.reload()
si.submit()
invoices.append(si)
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=9600.0, withholding_amount=0.0, status='Settled', taxable_doctype='Sales Invoice', taxable_name=si.name, withholding_doctype='Sales Invoice', withholding_name=si.name, under_withheld_reason='Threshold Exemption'), self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=2800.0, withholding_amount=280.0, status='Settled', taxable_doctype='Sales Invoice', taxable_name=si.name, withholding_doctype='Sales Invoice', withholding_name=si.name, under_withheld_reason=None)]
self.validate_tax_withholding_entries('Sales Invoice', si.name, expected_entries)
self.validate_tax_deduction(si, 280)
self.assertEqual(si.grand_total, 12680)
si = create_sales_invoice(customer='Test TCS Customer', rate=5000)
si.append('taxes', {'category': 'Total', 'charge_type': 'Actual', 'account_head': '_Test Account VAT - _TC', 'cost_center': 'Main - _TC', 'tax_amount': 500, 'description': 'VAT added to test TDS calculation on gross amount'})
si.save()
si.submit()
invoices.append(si)
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=5500.0, withholding_amount=550.0, status='Settled', taxable_doctype='Sales Invoice', taxable_name=si.name, withholding_doctype='Sales Invoice', withholding_name=si.name, under_withheld_reason=None)]
self.validate_tax_withholding_entries('Sales Invoice', si.name, expected_entries)
self.validate_tax_deduction(si, 550)
self.assertEqual(si.grand_total, 6050)
self.cleanup_invoices(invoices)
```

## Next Steps


---

*Source: test_tax_withholding_category.py:492 | Complexity: Advanced | Last updated: 2026-02-03*