# How To: Creation Of Ledger Entry On Submit

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test creation of gl entries on submission of document

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.stock.doctype.item.test_item`


## Step-by-Step Guide

### Step 1: 'test creation of gl entries on submission of document'

```python
'test creation of gl entries on submission of document'
```

### Step 2: Call change_acc_settings()

```python
change_acc_settings(acc_frozen_till_date='2023-05-31', book_deferred_entries_based_on='Months')
```

### Step 3: Assign deferred_account = create_account(...)

```python
deferred_account = create_account(account_name='Deferred Revenue for Accounts Frozen', parent_account='Current Liabilities - _TC', company='_Test Company')
```

### Step 4: Assign item = create_item(...)

```python
item = create_item('_Test Item for Deferred Accounting')
```

### Step 5: Assign item.enable_deferred_revenue = 1

```python
item.enable_deferred_revenue = 1
```

### Step 6: Assign item.deferred_revenue_account = deferred_account

```python
item.deferred_revenue_account = deferred_account
```

### Step 7: Assign item.no_of_months = 12

```python
item.no_of_months = 12
```

### Step 8: Call item.save()

```python
item.save()
```

### Step 9: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(item=item.name, rate=3000, update_stock=0, posting_date='2023-07-01', do_not_submit=True)
```

### Step 10: Assign unknown.enable_deferred_revenue = 1

```python
si.items[0].enable_deferred_revenue = 1
```

### Step 11: Assign unknown.service_start_date = '2023-05-01'

```python
si.items[0].service_start_date = '2023-05-01'
```

### Step 12: Assign unknown.service_end_date = '2023-07-31'

```python
si.items[0].service_end_date = '2023-07-31'
```

### Step 13: Assign unknown.deferred_revenue_account = deferred_account

```python
si.items[0].deferred_revenue_account = deferred_account
```

### Step 14: Call si.save()

```python
si.save()
```

### Step 15: Call si.submit()

```python
si.submit()
```

### Step 16: Assign original_gle = value

```python
original_gle = [['Debtors - _TC', 3000.0, 0, '2023-07-01'], [deferred_account, 0.0, 3000, '2023-07-01']]
```

### Step 17: Call check_gl_entries()

```python
check_gl_entries(self, si.name, original_gle, '2023-07-01')
```

### Step 18: Assign process_deferred_accounting = frappe.get_doc(...)

```python
process_deferred_accounting = frappe.get_doc(doctype='Process Deferred Accounting', posting_date='2023-07-01', start_date='2023-05-01', end_date='2023-06-30', type='Income')
```

### Step 19: Call process_deferred_accounting.insert()

```python
process_deferred_accounting.insert()
```

### Step 20: Call process_deferred_accounting.submit()

```python
process_deferred_accounting.submit()
```

### Step 21: Assign expected_gle = value

```python
expected_gle = [['Debtors - _TC', 3000, 0.0, '2023-07-01'], [deferred_account, 0.0, 3000, '2023-07-01'], ['Sales - _TC', 0.0, 1000, '2023-06-30'], [deferred_account, 1000, 0.0, '2023-06-30'], ['Sales - _TC', 0.0, 1000, '2023-06-30'], [deferred_account, 1000, 0.0, '2023-06-30']]
```

### Step 22: Call check_gl_entries()

```python
check_gl_entries(self, si.name, expected_gle, '2023-07-01')
```

### Step 23: Call process_deferred_accounting.cancel()

```python
process_deferred_accounting.cancel()
```

### Step 24: Call check_gl_entries()

```python
check_gl_entries(self, si.name, original_gle, '2023-07-01')
```

### Step 25: Call change_acc_settings()

```python
change_acc_settings()
```


## Complete Example

```python
# Workflow
'test creation of gl entries on submission of document'
change_acc_settings(acc_frozen_till_date='2023-05-31', book_deferred_entries_based_on='Months')
deferred_account = create_account(account_name='Deferred Revenue for Accounts Frozen', parent_account='Current Liabilities - _TC', company='_Test Company')
item = create_item('_Test Item for Deferred Accounting')
item.enable_deferred_revenue = 1
item.deferred_revenue_account = deferred_account
item.no_of_months = 12
item.save()
si = create_sales_invoice(item=item.name, rate=3000, update_stock=0, posting_date='2023-07-01', do_not_submit=True)
si.items[0].enable_deferred_revenue = 1
si.items[0].service_start_date = '2023-05-01'
si.items[0].service_end_date = '2023-07-31'
si.items[0].deferred_revenue_account = deferred_account
si.save()
si.submit()
original_gle = [['Debtors - _TC', 3000.0, 0, '2023-07-01'], [deferred_account, 0.0, 3000, '2023-07-01']]
check_gl_entries(self, si.name, original_gle, '2023-07-01')
process_deferred_accounting = frappe.get_doc(doctype='Process Deferred Accounting', posting_date='2023-07-01', start_date='2023-05-01', end_date='2023-06-30', type='Income')
process_deferred_accounting.insert()
process_deferred_accounting.submit()
expected_gle = [['Debtors - _TC', 3000, 0.0, '2023-07-01'], [deferred_account, 0.0, 3000, '2023-07-01'], ['Sales - _TC', 0.0, 1000, '2023-06-30'], [deferred_account, 1000, 0.0, '2023-06-30'], ['Sales - _TC', 0.0, 1000, '2023-06-30'], [deferred_account, 1000, 0.0, '2023-06-30']]
check_gl_entries(self, si.name, expected_gle, '2023-07-01')
process_deferred_accounting.cancel()
check_gl_entries(self, si.name, original_gle, '2023-07-01')
change_acc_settings()
```

## Next Steps


---

*Source: test_process_deferred_accounting.py:16 | Complexity: Advanced | Last updated: 2026-02-03*