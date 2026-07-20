# How To: Stock Freeze Validation

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test stock freeze validation

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
riv = frappe.get_doc(doctype='Repost Item Valuation', item_code='_Test Item', warehouse='_Test Warehouse - _TC', based_on='Item and Warehouse', posting_date=today, posting_time='00:01:00')
```

### Step 3: Assign riv.flags.dont_run_in_test = True

```python
riv.flags.dont_run_in_test = True
```

### Step 4: Call riv.submit()

```python
riv.submit()
```

### Step 5: Assign stock_settings = frappe.get_doc(...)

```python
stock_settings = frappe.get_doc('Stock Settings')
```

### Step 6: Assign stock_settings.stock_frozen_upto = today

```python
stock_settings.stock_frozen_upto = today
```

### Step 7: Call self.assertRaises()

```python
self.assertRaises(PendingRepostingError, stock_settings.save)
```

### Step 8: Call riv.set_status()

```python
riv.set_status('Skipped')
```


## Complete Example

```python
# Workflow
today = nowdate()
riv = frappe.get_doc(doctype='Repost Item Valuation', item_code='_Test Item', warehouse='_Test Warehouse - _TC', based_on='Item and Warehouse', posting_date=today, posting_time='00:01:00')
riv.flags.dont_run_in_test = True
riv.submit()
stock_settings = frappe.get_doc('Stock Settings')
stock_settings.stock_frozen_upto = today
self.assertRaises(PendingRepostingError, stock_settings.save)
riv.set_status('Skipped')
```

## Next Steps


---

*Source: test_repost_item_valuation.py:177 | Complexity: Advanced | Last updated: 2026-02-04*