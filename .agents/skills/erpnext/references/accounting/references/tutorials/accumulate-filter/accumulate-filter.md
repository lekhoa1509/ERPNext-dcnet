# How To: Accumulate Filter

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test accumulate filter

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.desk.query_report`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.report.financial_statements`
- `erpnext.accounts.report.profit_and_loss_statement.profit_and_loss_statement`
- `erpnext.accounts.test.accounts_mixin`


## Step-by-Step Guide

### Step 1: Assign cur_fy = self.get_fiscal_year(...)

```python
cur_fy = self.get_fiscal_year()
```

### Step 2: Assign find_for = add_days(...)

```python
find_for = add_days(cur_fy.year_start_date, -1)
```

### Step 3: Assign _x = value

```python
_x = frappe.db.get_all('Fiscal Year', filters={'disabled': 0, 'year_start_date': ('<=', find_for), 'year_end_date': ('>=', find_for)})[0]
```

### Step 4: Assign prev_fy = frappe.get_doc(...)

```python
prev_fy = frappe.get_doc('Fiscal Year', _x.name)
```

### Step 5: Call prev_fy.append()

```python
prev_fy.append('companies', {'company': self.company})
```

### Step 6: Call prev_fy.save()

```python
prev_fy.save()
```

### Step 7: Assign prev_fy_si = self.create_sales_invoice(...)

```python
prev_fy_si = self.create_sales_invoice(qty=1, rate=450, do_not_submit=True)
```

### Step 8: Assign prev_fy_si.posting_date = add_days(...)

```python
prev_fy_si.posting_date = add_days(prev_fy.year_end_date, -1)
```

### Step 9: Call prev_fy_si.save.submit()

```python
prev_fy_si.save().submit()
```

### Step 10: Assign income_acc = value

```python
income_acc = prev_fy_si.items[0].income_account
```

### Step 11: Call self.create_sales_invoice()

```python
self.create_sales_invoice(qty=1, rate=120)
```

### Step 12: Assign filters = frappe._dict(...)

```python
filters = frappe._dict(company=self.company, from_fiscal_year=prev_fy.name, to_fiscal_year=cur_fy.name, period_start_date=prev_fy.year_start_date, period_end_date=cur_fy.year_end_date, filter_based_on='Date Range', periodicity='Yearly', accumulated_values=False)
```

### Step 13: Assign result = execute(...)

```python
result = execute(filters)
```

### Step 14: Assign columns = value

```python
columns = [result[0][4], result[0][5]]
```

### Step 15: Assign expected = value

```python
expected = {'account': income_acc, columns[0].get('fieldname'): 450.0, columns[1].get('fieldname'): 120.0}
```

### Step 16: Assign actual = value

```python
actual = [x for x in result[1] if x.get('account') == income_acc]
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(len(actual), 1)
```

### Step 18: Assign actual = value

```python
actual = actual[0]
```

### Step 19: Call filters.update()

```python
filters.update({'accumulated_values': True})
```

### Step 20: Assign expected = value

```python
expected = {'account': income_acc, columns[0].get('fieldname'): 450.0, columns[1].get('fieldname'): 570.0}
```

### Step 21: Assign result = execute(...)

```python
result = execute(filters)
```

### Step 22: Assign columns = value

```python
columns = [result[0][4], result[0][5]]
```

### Step 23: Assign actual = value

```python
actual = [x for x in result[1] if x.get('account') == income_acc]
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(len(actual), 1)
```

### Step 25: Assign actual = value

```python
actual = actual[0]
```

### Step 26: Call self.assertEqual()

```python
self.assertEqual(expected.get(key), actual.get(key))
```

### Step 27: Call self.assertEqual()

```python
self.assertEqual(expected.get(key), actual.get(key))
```


## Complete Example

```python
# Workflow
cur_fy = self.get_fiscal_year()
find_for = add_days(cur_fy.year_start_date, -1)
_x = frappe.db.get_all('Fiscal Year', filters={'disabled': 0, 'year_start_date': ('<=', find_for), 'year_end_date': ('>=', find_for)})[0]
prev_fy = frappe.get_doc('Fiscal Year', _x.name)
prev_fy.append('companies', {'company': self.company})
prev_fy.save()
prev_fy_si = self.create_sales_invoice(qty=1, rate=450, do_not_submit=True)
prev_fy_si.posting_date = add_days(prev_fy.year_end_date, -1)
prev_fy_si.save().submit()
income_acc = prev_fy_si.items[0].income_account
self.create_sales_invoice(qty=1, rate=120)
filters = frappe._dict(company=self.company, from_fiscal_year=prev_fy.name, to_fiscal_year=cur_fy.name, period_start_date=prev_fy.year_start_date, period_end_date=cur_fy.year_end_date, filter_based_on='Date Range', periodicity='Yearly', accumulated_values=False)
result = execute(filters)
columns = [result[0][4], result[0][5]]
expected = {'account': income_acc, columns[0].get('fieldname'): 450.0, columns[1].get('fieldname'): 120.0}
actual = [x for x in result[1] if x.get('account') == income_acc]
self.assertEqual(len(actual), 1)
actual = actual[0]
for key in expected.keys():
    with self.subTest(key=key):
        self.assertEqual(expected.get(key), actual.get(key))
filters.update({'accumulated_values': True})
expected = {'account': income_acc, columns[0].get('fieldname'): 450.0, columns[1].get('fieldname'): 570.0}
result = execute(filters)
columns = [result[0][4], result[0][5]]
actual = [x for x in result[1] if x.get('account') == income_acc]
self.assertEqual(len(actual), 1)
actual = actual[0]
for key in expected.keys():
    with self.subTest(key=key):
        self.assertEqual(expected.get(key), actual.get(key))
```

## Next Steps


---

*Source: test_profit_and_loss_statement.py:113 | Complexity: Advanced | Last updated: 2026-02-03*