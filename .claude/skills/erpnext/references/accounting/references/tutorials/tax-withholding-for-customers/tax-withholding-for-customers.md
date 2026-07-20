# How To: Tax Withholding For Customers

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test tax withholding for customers

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.doctype.tax_withholding_category.test_tax_withholding_category`
- `erpnext.accounts.report.tax_withholding_details.tax_withholding_details`
- `erpnext.accounts.test.accounts_mixin`
- `erpnext.accounts.utils`


## Step-by-Step Guide

### Step 1: Call create_tax_category()

```python
create_tax_category(cumulative_threshold=300)
```

### Step 2: Call frappe.db.set_value()

```python
frappe.db.set_value('Customer', '_Test Customer', 'tax_withholding_category', 'TCS')
```

### Step 3: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(rate=1000)
```

### Step 4: Assign pe = create_tcs_payment_entry(...)

```python
pe = create_tcs_payment_entry()
```

### Step 5: Assign jv = create_tcs_journal_entry(...)

```python
jv = create_tcs_journal_entry()
```

### Step 6: Assign filters = frappe._dict(...)

```python
filters = frappe._dict(company='_Test Company', party_type='Customer', from_date=today(), to_date=today())
```

### Step 7: Assign result = value

```python
result = execute(filters)[1]
```

### Step 8: Assign expected_values = value

```python
expected_values = [[jv.name, 'TCS', 0.075, -10000.0, -7.5, -10000.0], [pe.name, 'TCS', 0.075, 2550, 0.53, 2550.53], [si.name, 'TCS', 0.075, 1000, 0.52, 1000.52]]
```

### Step 9: Call self.check_expected_values()

```python
self.check_expected_values(result, expected_values)
```


## Complete Example

```python
# Workflow
create_tax_category(cumulative_threshold=300)
frappe.db.set_value('Customer', '_Test Customer', 'tax_withholding_category', 'TCS')
si = create_sales_invoice(rate=1000)
pe = create_tcs_payment_entry()
jv = create_tcs_journal_entry()
filters = frappe._dict(company='_Test Company', party_type='Customer', from_date=today(), to_date=today())
result = execute(filters)[1]
expected_values = [[jv.name, 'TCS', 0.075, -10000.0, -7.5, -10000.0], [pe.name, 'TCS', 0.075, 2550, 0.53, 2550.53], [si.name, 'TCS', 0.075, 1000, 0.52, 1000.52]]
self.check_expected_values(result, expected_values)
```

## Next Steps


---

*Source: test_tax_withholding_details.py:25 | Complexity: Advanced | Last updated: 2026-02-03*