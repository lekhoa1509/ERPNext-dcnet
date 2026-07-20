# How To: Inter Company Jv

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test inter company jv

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.doctype.journal_entry.journal_entry`
- `erpnext.exceptions`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.accounts.utils`
- `erpnext.accounts.doctype.journal_entry.journal_entry`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.projects.doctype.project.test_project`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.accounts.utils`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.accounts.general_ledger`
- `erpnext.accounts.general_ledger`


## Step-by-Step Guide

### Step 1: Assign jv = make_journal_entry(...)

```python
jv = make_journal_entry('Sales Expenses - _TC', 'Buildings - _TC', 100, posting_date=nowdate(), cost_center='Main - _TC', save=False)
```

### Step 2: Assign jv.voucher_type = 'Inter Company Journal Entry'

```python
jv.voucher_type = 'Inter Company Journal Entry'
```

### Step 3: Assign jv.multi_currency = 0

```python
jv.multi_currency = 0
```

### Step 4: Call jv.insert()

```python
jv.insert()
```

### Step 5: Call jv.submit()

```python
jv.submit()
```

### Step 6: Assign jv1 = make_journal_entry(...)

```python
jv1 = make_journal_entry('Sales Expenses - _TC1', 'Buildings - _TC1', 100, posting_date=nowdate(), cost_center='Main - _TC1', save=False)
```

### Step 7: Assign jv1.inter_company_journal_entry_reference = value

```python
jv1.inter_company_journal_entry_reference = jv.name
```

### Step 8: Assign jv1.company = '_Test Company 1'

```python
jv1.company = '_Test Company 1'
```

### Step 9: Assign jv1.voucher_type = 'Inter Company Journal Entry'

```python
jv1.voucher_type = 'Inter Company Journal Entry'
```

### Step 10: Assign jv1.multi_currency = 0

```python
jv1.multi_currency = 0
```

### Step 11: Call jv1.insert()

```python
jv1.insert()
```

### Step 12: Call jv1.submit()

```python
jv1.submit()
```

### Step 13: Call jv.reload()

```python
jv.reload()
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(jv.inter_company_journal_entry_reference, jv1.name)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(jv1.inter_company_journal_entry_reference, jv.name)
```

### Step 16: Call jv.cancel()

```python
jv.cancel()
```

### Step 17: Call jv1.reload()

```python
jv1.reload()
```

### Step 18: Call jv.reload()

```python
jv.reload()
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(jv.inter_company_journal_entry_reference, '')
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(jv1.inter_company_journal_entry_reference, '')
```


## Complete Example

```python
# Workflow
jv = make_journal_entry('Sales Expenses - _TC', 'Buildings - _TC', 100, posting_date=nowdate(), cost_center='Main - _TC', save=False)
jv.voucher_type = 'Inter Company Journal Entry'
jv.multi_currency = 0
jv.insert()
jv.submit()
jv1 = make_journal_entry('Sales Expenses - _TC1', 'Buildings - _TC1', 100, posting_date=nowdate(), cost_center='Main - _TC1', save=False)
jv1.inter_company_journal_entry_reference = jv.name
jv1.company = '_Test Company 1'
jv1.voucher_type = 'Inter Company Journal Entry'
jv1.multi_currency = 0
jv1.insert()
jv1.submit()
jv.reload()
self.assertEqual(jv.inter_company_journal_entry_reference, jv1.name)
self.assertEqual(jv1.inter_company_journal_entry_reference, jv.name)
jv.cancel()
jv1.reload()
jv.reload()
self.assertEqual(jv.inter_company_journal_entry_reference, '')
self.assertEqual(jv1.inter_company_journal_entry_reference, '')
```

## Next Steps


---

*Source: test_journal_entry.py:273 | Complexity: Advanced | Last updated: 2026-02-03*