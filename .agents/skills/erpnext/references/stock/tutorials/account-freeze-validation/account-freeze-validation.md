# How To: Account Freeze Validation

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test account freeze validation

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.utils`
- `erpnext.controllers.stock_controller`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.repost_item_valuation.repost_item_valuation`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.tests.test_utils`
- `erpnext.stock.utils`
- `erpnext.stock.doctype.repost_item_valuation.repost_item_valuation`
- `erpnext.accounts`
- `erpnext.accounts`
- `erpnext.accounts`
- `erpnext.stock.doctype.stock_closing_entry.stock_closing_entry`


## Step-by-Step Guide

### Step 1: Assign today = nowdate(...)

```python
today = nowdate()
```

### Step 2: Assign riv = frappe.get_doc(...)

```python
riv = frappe.get_doc(doctype='Repost Item Valuation', item_code='_Test Item', company='_Test Company', warehouse='_Test Warehouse - _TC', based_on='Item and Warehouse', posting_date=today, posting_time='00:01:00')
```

### Step 3: Assign riv.flags.dont_run_in_test = True

```python
riv.flags.dont_run_in_test = True
```

### Step 4: Assign company = frappe.get_doc(...)

```python
company = frappe.get_doc('Company', '_Test Company')
```

### Step 5: Assign company.accounts_frozen_till_date = today

```python
company.accounts_frozen_till_date = today
```

### Step 6: Assign company.role_allowed_for_frozen_entries = ''

```python
company.role_allowed_for_frozen_entries = ''
```

### Step 7: Call company.save()

```python
company.save()
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, riv.save)
```

### Step 9: Assign company.accounts_frozen_till_date = ''

```python
company.accounts_frozen_till_date = ''
```

### Step 10: Call company.save()

```python
company.save()
```


## Complete Example

```python
# Workflow
today = nowdate()
riv = frappe.get_doc(doctype='Repost Item Valuation', item_code='_Test Item', company='_Test Company', warehouse='_Test Warehouse - _TC', based_on='Item and Warehouse', posting_date=today, posting_time='00:01:00')
riv.flags.dont_run_in_test = True
company = frappe.get_doc('Company', '_Test Company')
company.accounts_frozen_till_date = today
company.role_allowed_for_frozen_entries = ''
company.save()
self.assertRaises(frappe.ValidationError, riv.save)
company.accounts_frozen_till_date = ''
company.save()
```

## Next Steps


---

*Source: test_repost_item_valuation.py:353 | Complexity: Advanced | Last updated: 2026-02-04*