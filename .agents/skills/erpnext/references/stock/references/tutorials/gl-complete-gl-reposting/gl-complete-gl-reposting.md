# How To: Gl Complete Gl Reposting

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test gl complete gl reposting

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

### Step 1: Assign orig_chunk_size = value

```python
orig_chunk_size = utils.GL_REPOSTING_CHUNK
```

### Step 2: Assign utils.GL_REPOSTING_CHUNK = 2

```python
utils.GL_REPOSTING_CHUNK = 2
```

### Step 3: Call self.addCleanup()

```python
self.addCleanup(setattr, utils, 'GL_REPOSTING_CHUNK', orig_chunk_size)
```

### Step 4: Assign item = value

```python
item = self.make_item().name
```

### Step 5: Assign company = '_Test Company with perpetual inventory'

```python
company = '_Test Company with perpetual inventory'
```

### Step 6: Assign consumption = make_stock_entry(...)

```python
consumption = make_stock_entry(item=item, company=company, qty=1, source='Stores - TCP1')
```

### Step 7: Call self.assertGLEs()

```python
self.assertGLEs(consumption, [{'credit': 10, 'debit': 0}], gle_filters={'account': 'Stock In Hand - TCP1'})
```

### Step 8: Assign backdated_receipt = make_stock_entry(...)

```python
backdated_receipt = make_stock_entry(item=item, company=company, qty=1, rate=50, target='Stores - TCP1', posting_date=add_to_date(today(), days=-1))
```

### Step 9: Call self.assertGLEs()

```python
self.assertGLEs(backdated_receipt, [{'credit': 0, 'debit': 50}], gle_filters={'account': 'Stock In Hand - TCP1'})
```

### Step 10: Call self.assertGLEs()

```python
self.assertGLEs(consumption, [{'credit': 50, 'debit': 0}], gle_filters={'account': 'Stock In Hand - TCP1'})
```

### Step 11: Call make_stock_entry()

```python
make_stock_entry(item=item, company=company, qty=1, rate=10, target='Stores - TCP1')
```


## Complete Example

```python
# Workflow
from erpnext.accounts import utils
orig_chunk_size = utils.GL_REPOSTING_CHUNK
utils.GL_REPOSTING_CHUNK = 2
self.addCleanup(setattr, utils, 'GL_REPOSTING_CHUNK', orig_chunk_size)
item = self.make_item().name
company = '_Test Company with perpetual inventory'
for _ in range(10):
    make_stock_entry(item=item, company=company, qty=1, rate=10, target='Stores - TCP1')
consumption = make_stock_entry(item=item, company=company, qty=1, source='Stores - TCP1')
self.assertGLEs(consumption, [{'credit': 10, 'debit': 0}], gle_filters={'account': 'Stock In Hand - TCP1'})
backdated_receipt = make_stock_entry(item=item, company=company, qty=1, rate=50, target='Stores - TCP1', posting_date=add_to_date(today(), days=-1))
self.assertGLEs(backdated_receipt, [{'credit': 0, 'debit': 50}], gle_filters={'account': 'Stock In Hand - TCP1'})
self.assertGLEs(consumption, [{'credit': 50, 'debit': 0}], gle_filters={'account': 'Stock In Hand - TCP1'})
```

## Next Steps


---

*Source: test_repost_item_valuation.py:253 | Complexity: Advanced | Last updated: 2026-02-04*