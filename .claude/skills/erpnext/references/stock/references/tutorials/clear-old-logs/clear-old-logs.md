# How To: Clear Old Logs

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test clear old logs

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

### Step 1: Assign logs = frappe.get_all(...)

```python
logs = frappe.get_all('Repost Item Valuation', filters={'status': 'Skipped'})
```

### Step 2: Call self.assertTrue()

```python
self.assertTrue(len(logs) > 10)
```

### Step 3: Call RepostItemValuation.clear_old_logs()

```python
RepostItemValuation.clear_old_logs(days=1)
```

### Step 4: Assign logs = frappe.get_all(...)

```python
logs = frappe.get_all('Repost Item Valuation', filters={'status': 'Skipped'})
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(len(logs) == 0)
```

### Step 6: Assign repost_doc = frappe.get_doc.insert(...)

```python
repost_doc = frappe.get_doc(doctype='Repost Item Valuation', item_code='_Test Item', warehouse='_Test Warehouse - _TC', based_on='Item and Warehouse', posting_date=nowdate(), status='Skipped', posting_time='00:01:00').insert(ignore_permissions=True)
```

### Step 7: Call repost_doc.load_from_db()

```python
repost_doc.load_from_db()
```

### Step 8: Assign repost_doc.creation = add_days(...)

```python
repost_doc.creation = add_days(now(), days=-i * 10)
```

### Step 9: Call repost_doc.db_update_all()

```python
repost_doc.db_update_all()
```


## Complete Example

```python
# Workflow
for i in range(1, 20):
    repost_doc = frappe.get_doc(doctype='Repost Item Valuation', item_code='_Test Item', warehouse='_Test Warehouse - _TC', based_on='Item and Warehouse', posting_date=nowdate(), status='Skipped', posting_time='00:01:00').insert(ignore_permissions=True)
    repost_doc.load_from_db()
    repost_doc.creation = add_days(now(), days=-i * 10)
    repost_doc.db_update_all()
logs = frappe.get_all('Repost Item Valuation', filters={'status': 'Skipped'})
self.assertTrue(len(logs) > 10)
from erpnext.stock.doctype.repost_item_valuation.repost_item_valuation import RepostItemValuation
RepostItemValuation.clear_old_logs(days=1)
logs = frappe.get_all('Repost Item Valuation', filters={'status': 'Skipped'})
self.assertTrue(len(logs) == 0)
```

## Next Steps


---

*Source: test_repost_item_valuation.py:88 | Complexity: Advanced | Last updated: 2026-02-04*