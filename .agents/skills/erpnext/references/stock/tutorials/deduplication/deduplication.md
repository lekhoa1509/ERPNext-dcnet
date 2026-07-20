# How To: Deduplication

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test deduplication

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

### Step 1: Assign riv_args = frappe._dict(...)

```python
riv_args = frappe._dict(doctype='Repost Item Valuation', item_code='_Test Item', warehouse='_Test Warehouse - _TC', based_on='Item and Warehouse', posting_date='2021-01-02', posting_time='00:01:00')
```

### Step 2: Assign riv1 = frappe.get_doc(...)

```python
riv1 = frappe.get_doc(riv_args)
```

### Step 3: Assign riv1.flags.dont_run_in_test = True

```python
riv1.flags.dont_run_in_test = True
```

### Step 4: Call riv1.submit()

```python
riv1.submit()
```

### Step 5: Call _assert_status()

```python
_assert_status(riv1, 'Queued')
```

### Step 6: Assign riv2 = frappe.get_doc(...)

```python
riv2 = frappe.get_doc(riv_args.update({'posting_date': '2021-01-03'}))
```

### Step 7: Assign riv2.flags.dont_run_in_test = True

```python
riv2.flags.dont_run_in_test = True
```

### Step 8: Call riv2.submit()

```python
riv2.submit()
```

### Step 9: Call riv1.deduplicate_similar_repost()

```python
riv1.deduplicate_similar_repost()
```

### Step 10: Call _assert_status()

```python
_assert_status(riv2, 'Skipped')
```

### Step 11: Assign riv3 = frappe.get_doc(...)

```python
riv3 = frappe.get_doc(riv_args.update({'posting_date': '2021-01-01'}))
```

### Step 12: Assign riv3.flags.dont_run_in_test = True

```python
riv3.flags.dont_run_in_test = True
```

### Step 13: Call riv3.submit()

```python
riv3.submit()
```

### Step 14: Call riv3.deduplicate_similar_repost()

```python
riv3.deduplicate_similar_repost()
```

### Step 15: Call _assert_status()

```python
_assert_status(riv3, 'Queued')
```

### Step 16: Call _assert_status()

```python
_assert_status(riv1, 'Skipped')
```

### Step 17: Assign riv4 = frappe.get_doc(...)

```python
riv4 = frappe.get_doc(riv_args.update({'warehouse': 'Stores - _TC'}))
```

### Step 18: Assign riv4.flags.dont_run_in_test = True

```python
riv4.flags.dont_run_in_test = True
```

### Step 19: Call riv4.submit()

```python
riv4.submit()
```

### Step 20: Call riv4.deduplicate_similar_repost()

```python
riv4.deduplicate_similar_repost()
```

### Step 21: Call _assert_status()

```python
_assert_status(riv4, 'Queued')
```

### Step 22: Call _assert_status()

```python
_assert_status(riv3, 'Queued')
```

### Step 23: Call riv4.set_status()

```python
riv4.set_status('Skipped')
```

### Step 24: Call riv3.set_status()

```python
riv3.set_status('Skipped')
```

### Step 25: Call doc.load_from_db()

```python
doc.load_from_db()
```

### Step 26: Call self.assertEqual()

```python
self.assertEqual(doc.status, status)
```


## Complete Example

```python
# Workflow
def _assert_status(doc, status):
    doc.load_from_db()
    self.assertEqual(doc.status, status)
riv_args = frappe._dict(doctype='Repost Item Valuation', item_code='_Test Item', warehouse='_Test Warehouse - _TC', based_on='Item and Warehouse', posting_date='2021-01-02', posting_time='00:01:00')
riv1 = frappe.get_doc(riv_args)
riv1.flags.dont_run_in_test = True
riv1.submit()
_assert_status(riv1, 'Queued')
riv2 = frappe.get_doc(riv_args.update({'posting_date': '2021-01-03'}))
riv2.flags.dont_run_in_test = True
riv2.submit()
riv1.deduplicate_similar_repost()
_assert_status(riv2, 'Skipped')
riv3 = frappe.get_doc(riv_args.update({'posting_date': '2021-01-01'}))
riv3.flags.dont_run_in_test = True
riv3.submit()
riv3.deduplicate_similar_repost()
_assert_status(riv3, 'Queued')
_assert_status(riv1, 'Skipped')
riv4 = frappe.get_doc(riv_args.update({'warehouse': 'Stores - _TC'}))
riv4.flags.dont_run_in_test = True
riv4.submit()
riv4.deduplicate_similar_repost()
_assert_status(riv4, 'Queued')
_assert_status(riv3, 'Queued')
riv4.set_status('Skipped')
riv3.set_status('Skipped')
```

## Next Steps


---

*Source: test_repost_item_valuation.py:130 | Complexity: Advanced | Last updated: 2026-02-04*