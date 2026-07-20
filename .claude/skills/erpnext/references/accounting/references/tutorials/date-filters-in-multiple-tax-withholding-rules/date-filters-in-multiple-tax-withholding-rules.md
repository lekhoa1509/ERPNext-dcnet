# How To: Date Filters In Multiple Tax Withholding Rules

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test date filters in multiple tax withholding rules

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
create_tax_category('TDS - 3', rate=10, account='TDS - _TC', cumulative_threshold=1)
```

### Step 2: Assign fiscal_year = get_fiscal_year(...)

```python
fiscal_year = get_fiscal_year(today(), company='_Test Company')
```

### Step 3: Assign mid_year = add_to_date(...)

```python
mid_year = add_to_date(fiscal_year[1], months=6)
```

### Step 4: Assign tds_doc = frappe.get_doc(...)

```python
tds_doc = frappe.get_doc('Tax Withholding Category', 'TDS - 3')
```

### Step 5: Assign unknown.to_date = mid_year

```python
tds_doc.rates[0].to_date = mid_year
```

### Step 6: Assign from_date = add_to_date(...)

```python
from_date = add_to_date(mid_year, days=1)
```

### Step 7: Call tds_doc.append()

```python
tds_doc.append('rates', {'tax_withholding_rate': 20, 'from_date': from_date, 'to_date': fiscal_year[2], 'single_threshold': 1, 'cumulative_threshold': 1})
```

### Step 8: Call tds_doc.save()

```python
tds_doc.save()
```

### Step 9: Assign inv_1 = make_purchase_invoice(...)

```python
inv_1 = make_purchase_invoice(rate=1000, posting_date=add_to_date(fiscal_year[1], days=1), do_not_save=True, do_not_submit=True)
```

### Step 10: Assign inv_1.set_posting_time = 1

```python
inv_1.set_posting_time = 1
```

### Step 11: Assign inv_1.apply_tds = 1

```python
inv_1.apply_tds = 1
```

### Step 12: Assign inv_1.tax_withholding_category = value

```python
inv_1.tax_withholding_category = tds_doc.name
```

### Step 13: Call inv_1.save()

```python
inv_1.save()
```

### Step 14: Call inv_1.submit()

```python
inv_1.submit()
```

### Step 15: Assign inv_2 = make_purchase_invoice(...)

```python
inv_2 = make_purchase_invoice(rate=1000, posting_date=from_date, do_not_save=True, do_not_submit=True)
```

### Step 16: Assign inv_2.set_posting_time = 1

```python
inv_2.set_posting_time = 1
```

### Step 17: Assign inv_2.apply_tds = 1

```python
inv_2.apply_tds = 1
```

### Step 18: Assign inv_2.tax_withholding_category = value

```python
inv_2.tax_withholding_category = tds_doc.name
```

### Step 19: Call inv_2.save()

```python
inv_2.save()
```

### Step 20: Call inv_2.submit()

```python
inv_2.submit()
```

### Step 21: Assign result = value

```python
result = execute(frappe._dict(company='_Test Company', party_type='Supplier', from_date=fiscal_year[1], to_date=fiscal_year[2]))[1]
```

### Step 22: Assign expected_values = value

```python
expected_values = [[inv_1.name, 'TDS - 3', 10.0, 5000, 500, 4500], [inv_2.name, 'TDS - 3', 20.0, 5000, 1000, 4000]]
```

### Step 23: Call self.check_expected_values()

```python
self.check_expected_values(result, expected_values)
```


## Complete Example

```python
# Workflow
create_tax_category('TDS - 3', rate=10, account='TDS - _TC', cumulative_threshold=1)
fiscal_year = get_fiscal_year(today(), company='_Test Company')
mid_year = add_to_date(fiscal_year[1], months=6)
tds_doc = frappe.get_doc('Tax Withholding Category', 'TDS - 3')
tds_doc.rates[0].to_date = mid_year
from_date = add_to_date(mid_year, days=1)
tds_doc.append('rates', {'tax_withholding_rate': 20, 'from_date': from_date, 'to_date': fiscal_year[2], 'single_threshold': 1, 'cumulative_threshold': 1})
tds_doc.save()
inv_1 = make_purchase_invoice(rate=1000, posting_date=add_to_date(fiscal_year[1], days=1), do_not_save=True, do_not_submit=True)
inv_1.set_posting_time = 1
inv_1.apply_tds = 1
inv_1.tax_withholding_category = tds_doc.name
inv_1.save()
inv_1.submit()
inv_2 = make_purchase_invoice(rate=1000, posting_date=from_date, do_not_save=True, do_not_submit=True)
inv_2.set_posting_time = 1
inv_2.apply_tds = 1
inv_2.tax_withholding_category = tds_doc.name
inv_2.save()
inv_2.submit()
result = execute(frappe._dict(company='_Test Company', party_type='Supplier', from_date=fiscal_year[1], to_date=fiscal_year[2]))[1]
expected_values = [[inv_1.name, 'TDS - 3', 10.0, 5000, 500, 4500], [inv_2.name, 'TDS - 3', 20.0, 5000, 1000, 4000]]
self.check_expected_values(result, expected_values)
```

## Next Steps


---

*Source: test_tax_withholding_details.py:63 | Complexity: Advanced | Last updated: 2026-02-03*