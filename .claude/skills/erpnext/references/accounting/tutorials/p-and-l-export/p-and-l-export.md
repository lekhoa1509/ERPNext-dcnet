# How To: P And L Export

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test p and l export

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

### Step 1: Call self.create_sales_invoice()

```python
self.create_sales_invoice(qty=1, rate=150)
```

### Step 2: Assign filters = self.get_report_filters(...)

```python
filters = self.get_report_filters()
```

### Step 3: Assign frappe.local.form_dict = frappe._dict(...)

```python
frappe.local.form_dict = frappe._dict({'report_name': 'Profit and Loss Statement', 'file_format_type': 'CSV', 'filters': filters, 'visible_idx': [0, 1, 2, 3, 4, 5, 6]})
```

### Step 4: Call export_query()

```python
export_query()
```

### Step 5: Assign contents = unknown.decode(...)

```python
contents = frappe.response['filecontent'].decode()
```

### Step 6: Assign sales_account = frappe.db.get_value(...)

```python
sales_account = frappe.db.get_value('Company', self.company, 'default_income_account')
```

### Step 7: Call self.assertIn()

```python
self.assertIn(sales_account, contents)
```


## Complete Example

```python
# Workflow
self.create_sales_invoice(qty=1, rate=150)
filters = self.get_report_filters()
frappe.local.form_dict = frappe._dict({'report_name': 'Profit and Loss Statement', 'file_format_type': 'CSV', 'filters': filters, 'visible_idx': [0, 1, 2, 3, 4, 5, 6]})
export_query()
contents = frappe.response['filecontent'].decode()
sales_account = frappe.db.get_value('Company', self.company, 'default_income_account')
self.assertIn(sales_account, contents)
```

## Next Steps


---

*Source: test_profit_and_loss_statement.py:95 | Complexity: Intermediate | Last updated: 2026-02-03*