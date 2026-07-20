# How To: Basic Report Output

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test basic report output

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.report.item_wise_purchase_register.item_wise_purchase_register`
- `erpnext.accounts.test.accounts_mixin`


## Step-by-Step Guide

### Step 1: Assign pi = self.create_purchase_invoice(...)

```python
pi = self.create_purchase_invoice()
```

### Step 2: Assign filters = frappe._dict(...)

```python
filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company})
```

### Step 3: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(len(report[1]), 1)
```

### Step 5: Assign expected_result = value

```python
expected_result = {'item_code': pi.items[0].item_code, 'invoice': pi.name, 'posting_date': getdate(), 'supplier': pi.supplier, 'credit_to': pi.credit_to, 'company': self.company, 'expense_account': pi.items[0].expense_account, 'stock_qty': 1.0, 'stock_uom': pi.items[0].stock_uom, 'rate': 100.0, 'amount': 100.0, 'total_tax': 0, 'total': 100.0, 'currency': 'INR'}
```

### Step 6: Assign report_output = value

```python
report_output = {k: v for k, v in report[1][0].items() if k in expected_result}
```

### Step 7: Call self.assertDictEqual()

```python
self.assertDictEqual(report_output, expected_result)
```


## Complete Example

```python
# Workflow
pi = self.create_purchase_invoice()
filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company})
report = execute(filters)
self.assertEqual(len(report[1]), 1)
expected_result = {'item_code': pi.items[0].item_code, 'invoice': pi.name, 'posting_date': getdate(), 'supplier': pi.supplier, 'credit_to': pi.credit_to, 'company': self.company, 'expense_account': pi.items[0].expense_account, 'stock_qty': 1.0, 'stock_uom': pi.items[0].stock_uom, 'rate': 100.0, 'amount': 100.0, 'total_tax': 0, 'total': 100.0, 'currency': 'INR'}
report_output = {k: v for k, v in report[1][0].items() if k in expected_result}
self.assertDictEqual(report_output, expected_result)
```

## Next Steps


---

*Source: test_item_wise_purchase_register.py:37 | Complexity: Intermediate | Last updated: 2026-02-03*