# How To: Journal With Cost Center Filter

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test journal with cost center filter

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.report.sales_register.sales_register`
- `erpnext.accounts.test.accounts_mixin`


## Step-by-Step Guide

### Step 1: Assign je1 = frappe.get_doc(...)

```python
je1 = frappe.get_doc({'doctype': 'Journal Entry', 'voucher_type': 'Journal Entry', 'company': self.company, 'posting_date': getdate(), 'accounts': [{'account': self.debit_to, 'party_type': 'Customer', 'party': self.customer, 'credit_in_account_currency': 77, 'credit': 77, 'is_advance': 'Yes', 'cost_center': self.cost_center}, {'account': self.cash, 'debit_in_account_currency': 77, 'debit': 77}]})
```

### Step 2: Call je1.submit()

```python
je1.submit()
```

### Step 3: Assign je2 = frappe.get_doc(...)

```python
je2 = frappe.get_doc({'doctype': 'Journal Entry', 'voucher_type': 'Journal Entry', 'company': self.company, 'posting_date': getdate(), 'accounts': [{'account': self.debit_to, 'party_type': 'Customer', 'party': self.customer, 'credit_in_account_currency': 98, 'credit': 98, 'is_advance': 'Yes', 'cost_center': self.south_cc}, {'account': self.cash, 'debit_in_account_currency': 98, 'debit': 98}]})
```

### Step 4: Call je2.submit()

```python
je2.submit()
```

### Step 5: Assign filters = frappe._dict(...)

```python
filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company, 'include_payments': True, 'customer': self.customer, 'cost_center': self.cost_center})
```

### Step 6: Assign report_output = value

```python
report_output = execute(filters)[1]
```

### Step 7: Assign filtered_output = value

```python
filtered_output = [x for x in report_output if x.get('voucher_no') == je1.name]
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(len(filtered_output), 1)
```

### Step 9: Assign expected_result = value

```python
expected_result = {'voucher_type': je1.doctype, 'voucher_no': je1.name, 'posting_date': je1.posting_date, 'customer': self.customer, 'receivable_account': self.debit_to, 'net_total': 77.0, 'credit': 77.0}
```

### Step 10: Assign result_fields = value

```python
result_fields = {k: v for k, v in filtered_output[0].items() if k in expected_result}
```

### Step 11: Call self.assertDictEqual()

```python
self.assertDictEqual(result_fields, expected_result)
```

### Step 12: Assign filters = frappe._dict(...)

```python
filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company, 'include_payments': True, 'customer': self.customer, 'cost_center': self.south_cc})
```

### Step 13: Assign report_output = value

```python
report_output = execute(filters)[1]
```

### Step 14: Assign filtered_output = value

```python
filtered_output = [x for x in report_output if x.get('voucher_no') == je2.name]
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(len(filtered_output), 1)
```

### Step 16: Assign expected_result = value

```python
expected_result = {'voucher_type': je2.doctype, 'voucher_no': je2.name, 'posting_date': je2.posting_date, 'customer': self.customer, 'receivable_account': self.debit_to, 'net_total': 98.0, 'credit': 98.0}
```

### Step 17: Assign result_output = value

```python
result_output = {k: v for k, v in filtered_output[0].items() if k in expected_result}
```

### Step 18: Call self.assertDictEqual()

```python
self.assertDictEqual(result_output, expected_result)
```


## Complete Example

```python
# Workflow
je1 = frappe.get_doc({'doctype': 'Journal Entry', 'voucher_type': 'Journal Entry', 'company': self.company, 'posting_date': getdate(), 'accounts': [{'account': self.debit_to, 'party_type': 'Customer', 'party': self.customer, 'credit_in_account_currency': 77, 'credit': 77, 'is_advance': 'Yes', 'cost_center': self.cost_center}, {'account': self.cash, 'debit_in_account_currency': 77, 'debit': 77}]})
je1.submit()
je2 = frappe.get_doc({'doctype': 'Journal Entry', 'voucher_type': 'Journal Entry', 'company': self.company, 'posting_date': getdate(), 'accounts': [{'account': self.debit_to, 'party_type': 'Customer', 'party': self.customer, 'credit_in_account_currency': 98, 'credit': 98, 'is_advance': 'Yes', 'cost_center': self.south_cc}, {'account': self.cash, 'debit_in_account_currency': 98, 'debit': 98}]})
je2.submit()
filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company, 'include_payments': True, 'customer': self.customer, 'cost_center': self.cost_center})
report_output = execute(filters)[1]
filtered_output = [x for x in report_output if x.get('voucher_no') == je1.name]
self.assertEqual(len(filtered_output), 1)
expected_result = {'voucher_type': je1.doctype, 'voucher_no': je1.name, 'posting_date': je1.posting_date, 'customer': self.customer, 'receivable_account': self.debit_to, 'net_total': 77.0, 'credit': 77.0}
result_fields = {k: v for k, v in filtered_output[0].items() if k in expected_result}
self.assertDictEqual(result_fields, expected_result)
filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company, 'include_payments': True, 'customer': self.customer, 'cost_center': self.south_cc})
report_output = execute(filters)[1]
filtered_output = [x for x in report_output if x.get('voucher_no') == je2.name]
self.assertEqual(len(filtered_output), 1)
expected_result = {'voucher_type': je2.doctype, 'voucher_no': je2.name, 'posting_date': je2.posting_date, 'customer': self.customer, 'receivable_account': self.debit_to, 'net_total': 98.0, 'credit': 98.0}
result_output = {k: v for k, v in filtered_output[0].items() if k in expected_result}
self.assertDictEqual(result_output, expected_result)
```

## Next Steps


---

*Source: test_sales_register.py:78 | Complexity: Advanced | Last updated: 2026-02-03*