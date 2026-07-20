# How To: Repost Item Valuation For Closing Stock Balance

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test repost item valuation for closing stock balance

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

### Step 1: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc('Stock Closing Entry')
```

### Step 2: Assign doc.company = '_Test Company'

```python
doc.company = '_Test Company'
```

### Step 3: Assign doc.from_date = today(...)

```python
doc.from_date = today()
```

### Step 4: Assign doc.to_date = today(...)

```python
doc.to_date = today()
```

### Step 5: Call doc.submit()

```python
doc.submit()
```

### Step 6: Call prepare_closing_stock_balance()

```python
prepare_closing_stock_balance(doc.name)
```

### Step 7: Call doc.load_from_db()

```python
doc.load_from_db()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(doc.docstatus, 1)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(doc.status, 'Completed')
```

### Step 10: Assign riv = frappe.new_doc(...)

```python
riv = frappe.new_doc('Repost Item Valuation')
```

### Step 11: Call riv.update()

```python
riv.update({'item_code': '_Test Item', 'warehouse': '_Test Warehouse - _TC', 'based_on': 'Item and Warehouse', 'posting_date': today(), 'posting_time': '00:01:00'})
```

### Step 12: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, riv.save)
```

### Step 13: Call doc.cancel()

```python
doc.cancel()
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.stock_closing_entry.stock_closing_entry import prepare_closing_stock_balance
doc = frappe.new_doc('Stock Closing Entry')
doc.company = '_Test Company'
doc.from_date = today()
doc.to_date = today()
doc.submit()
prepare_closing_stock_balance(doc.name)
doc.load_from_db()
self.assertEqual(doc.docstatus, 1)
self.assertEqual(doc.status, 'Completed')
riv = frappe.new_doc('Repost Item Valuation')
riv.update({'item_code': '_Test Item', 'warehouse': '_Test Warehouse - _TC', 'based_on': 'Item and Warehouse', 'posting_date': today(), 'posting_time': '00:01:00'})
self.assertRaises(frappe.ValidationError, riv.save)
doc.cancel()
```

## Next Steps


---

*Source: test_repost_item_valuation.py:394 | Complexity: Advanced | Last updated: 2026-02-04*