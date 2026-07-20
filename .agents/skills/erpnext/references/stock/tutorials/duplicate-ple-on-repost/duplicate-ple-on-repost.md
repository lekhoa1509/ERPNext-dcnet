# How To: Duplicate Ple On Repost

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test duplicate ple on repost

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

### Step 4: Assign rate = 100

```python
rate = 100
```

### Step 5: Assign item = self.make_item(...)

```python
item = self.make_item()
```

### Step 6: Assign item.valuation_rate = 90

```python
item.valuation_rate = 90
```

### Step 7: Assign item.allow_negative_stock = 1

```python
item.allow_negative_stock = 1
```

### Step 8: Call item.save()

```python
item.save()
```

### Step 9: Assign company = '_Test Company with perpetual inventory'

```python
company = '_Test Company with perpetual inventory'
```

### Step 10: Assign sinv = create_sales_invoice(...)

```python
sinv = create_sales_invoice(company=company, posting_date=today(), debit_to='Debtors - TCP1', income_account='Sales - TCP1', expense_account='Cost of Goods Sold - TCP1', warehouse='Stores - TCP1', update_stock=1, currency='INR', item_code=item.name, cost_center='Main - TCP1', qty=1, rate=rate)
```

### Step 11: Call make_stock_entry()

```python
make_stock_entry(item=item.name, company=company, qty=5, rate=rate, target='Stores - TCP1', posting_date=add_to_date(today(), days=-1))
```

### Step 12: Assign ple_entries = frappe.db.get_list(...)

```python
ple_entries = frappe.db.get_list('Payment Ledger Entry', filters={'voucher_type': sinv.doctype, 'voucher_no': sinv.name, 'delinked': 0})
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(len(ple_entries), 1)
```

### Step 14: Call sinv.reload()

```python
sinv.reload()
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(sinv.outstanding_amount, 100)
```


## Complete Example

```python
# Workflow
from erpnext.accounts import utils
orig_chunk_size = utils.GL_REPOSTING_CHUNK
utils.GL_REPOSTING_CHUNK = 2
self.addCleanup(setattr, utils, 'GL_REPOSTING_CHUNK', orig_chunk_size)
rate = 100
item = self.make_item()
item.valuation_rate = 90
item.allow_negative_stock = 1
item.save()
company = '_Test Company with perpetual inventory'
sinv = create_sales_invoice(company=company, posting_date=today(), debit_to='Debtors - TCP1', income_account='Sales - TCP1', expense_account='Cost of Goods Sold - TCP1', warehouse='Stores - TCP1', update_stock=1, currency='INR', item_code=item.name, cost_center='Main - TCP1', qty=1, rate=rate)
make_stock_entry(item=item.name, company=company, qty=5, rate=rate, target='Stores - TCP1', posting_date=add_to_date(today(), days=-1))
ple_entries = frappe.db.get_list('Payment Ledger Entry', filters={'voucher_type': sinv.doctype, 'voucher_no': sinv.name, 'delinked': 0})
self.assertEqual(len(ple_entries), 1)
sinv.reload()
self.assertEqual(sinv.outstanding_amount, 100)
```

## Next Steps


---

*Source: test_repost_item_valuation.py:299 | Complexity: Advanced | Last updated: 2026-02-04*