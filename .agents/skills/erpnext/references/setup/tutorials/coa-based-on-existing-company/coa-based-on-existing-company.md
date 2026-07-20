# How To: Coa Based On Existing Company

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test coa based on existing company

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts`
- `erpnext.setup.doctype.company.company`
- `erpnext.setup.demo`


## Step-by-Step Guide

### Step 1: Assign company = frappe.new_doc(...)

```python
company = frappe.new_doc('Company')
```

### Step 2: Assign company.company_name = 'COA from Existing Company'

```python
company.company_name = 'COA from Existing Company'
```

### Step 3: Assign company.abbr = 'CFEC'

```python
company.abbr = 'CFEC'
```

### Step 4: Assign company.default_currency = 'INR'

```python
company.default_currency = 'INR'
```

### Step 5: Assign company.create_chart_of_accounts_based_on = 'Existing Company'

```python
company.create_chart_of_accounts_based_on = 'Existing Company'
```

### Step 6: Assign company.existing_company = '_Test Company'

```python
company.existing_company = '_Test Company'
```

### Step 7: Call company.save()

```python
company.save()
```

### Step 8: Assign expected_results = value

```python
expected_results = {'Debtors - CFEC': {'account_type': 'Receivable', 'is_group': 0, 'root_type': 'Asset', 'parent_account': 'Accounts Receivable - CFEC'}, 'Cash - CFEC': {'account_type': 'Cash', 'is_group': 0, 'root_type': 'Asset', 'parent_account': 'Cash In Hand - CFEC'}}
```

### Step 9: Call self.delete_mode_of_payment()

```python
self.delete_mode_of_payment('COA from Existing Company')
```

### Step 10: Call frappe.delete_doc()

```python
frappe.delete_doc('Company', 'COA from Existing Company')
```

### Step 11: Assign acc = frappe.get_doc(...)

```python
acc = frappe.get_doc('Account', account)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(acc.get(prop), val)
```


## Complete Example

```python
# Workflow
company = frappe.new_doc('Company')
company.company_name = 'COA from Existing Company'
company.abbr = 'CFEC'
company.default_currency = 'INR'
company.create_chart_of_accounts_based_on = 'Existing Company'
company.existing_company = '_Test Company'
company.save()
expected_results = {'Debtors - CFEC': {'account_type': 'Receivable', 'is_group': 0, 'root_type': 'Asset', 'parent_account': 'Accounts Receivable - CFEC'}, 'Cash - CFEC': {'account_type': 'Cash', 'is_group': 0, 'root_type': 'Asset', 'parent_account': 'Cash In Hand - CFEC'}}
for account, acc_property in expected_results.items():
    acc = frappe.get_doc('Account', account)
    for prop, val in acc_property.items():
        self.assertEqual(acc.get(prop), val)
self.delete_mode_of_payment('COA from Existing Company')
frappe.delete_doc('Company', 'COA from Existing Company')
```

## Next Steps


---

*Source: test_company.py:26 | Complexity: Advanced | Last updated: 2026-02-04*