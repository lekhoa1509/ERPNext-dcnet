# How To: Single Account For Multiple Categories

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test single account for multiple categories

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
create_tax_category('TDS - 1', rate=10, account='TDS - _TC')
```

### Step 2: Assign inv_1 = make_purchase_invoice(...)

```python
inv_1 = make_purchase_invoice(rate=1000, do_not_submit=True)
```

### Step 3: Assign inv_1.tax_withholding_category = 'TDS - 1'

```python
inv_1.tax_withholding_category = 'TDS - 1'
```

### Step 4: Call inv_1.submit()

```python
inv_1.submit()
```

### Step 5: Call create_tax_category()

```python
create_tax_category('TDS - 2', rate=20, account='TDS - _TC')
```

### Step 6: Assign inv_2 = make_purchase_invoice(...)

```python
inv_2 = make_purchase_invoice(rate=1000, do_not_submit=True)
```

### Step 7: Assign inv_2.tax_withholding_category = 'TDS - 2'

```python
inv_2.tax_withholding_category = 'TDS - 2'
```

### Step 8: Call inv_2.submit()

```python
inv_2.submit()
```

### Step 9: Assign result = value

```python
result = execute(frappe._dict(company='_Test Company', party_type='Supplier', from_date=today(), to_date=today()))[1]
```

### Step 10: Assign expected_values = value

```python
expected_values = [[inv_1.name, 'TDS - 1', 10, 5000, 500, 5500], [inv_2.name, 'TDS - 2', 20, 5000, 1000, 6000]]
```

### Step 11: Call self.check_expected_values()

```python
self.check_expected_values(result, expected_values)
```


## Complete Example

```python
# Workflow
create_tax_category('TDS - 1', rate=10, account='TDS - _TC')
inv_1 = make_purchase_invoice(rate=1000, do_not_submit=True)
inv_1.tax_withholding_category = 'TDS - 1'
inv_1.submit()
create_tax_category('TDS - 2', rate=20, account='TDS - _TC')
inv_2 = make_purchase_invoice(rate=1000, do_not_submit=True)
inv_2.tax_withholding_category = 'TDS - 2'
inv_2.submit()
result = execute(frappe._dict(company='_Test Company', party_type='Supplier', from_date=today(), to_date=today()))[1]
expected_values = [[inv_1.name, 'TDS - 1', 10, 5000, 500, 5500], [inv_2.name, 'TDS - 2', 20, 5000, 1000, 6000]]
self.check_expected_values(result, expected_values)
```

## Next Steps


---

*Source: test_tax_withholding_details.py:44 | Complexity: Advanced | Last updated: 2026-02-03*