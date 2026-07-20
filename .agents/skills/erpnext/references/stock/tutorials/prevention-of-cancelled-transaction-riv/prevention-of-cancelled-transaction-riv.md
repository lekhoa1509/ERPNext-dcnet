# How To: Prevention Of Cancelled Transaction Riv

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test prevention of cancelled transaction riv

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

### Step 1: Assign frappe.flags.dont_execute_stock_reposts = True

```python
frappe.flags.dont_execute_stock_reposts = True
```

### Step 2: Assign item = make_item(...)

```python
item = make_item()
```

### Step 3: Assign warehouse = '_Test Warehouse - _TC'

```python
warehouse = '_Test Warehouse - _TC'
```

### Step 4: Assign old = make_stock_entry(...)

```python
old = make_stock_entry(item_code=item.name, to_warehouse=warehouse, qty=2, rate=5)
```

### Step 5: Assign _new = make_stock_entry(...)

```python
_new = make_stock_entry(item_code=item.name, to_warehouse=warehouse, qty=5, rate=10)
```

### Step 6: Call old.cancel()

```python
old.cancel()
```

### Step 7: Assign riv = frappe.get_last_doc(...)

```python
riv = frappe.get_last_doc('Repost Item Valuation', {'voucher_type': old.doctype, 'voucher_no': old.name})
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, riv.cancel)
```

### Step 9: Call riv.db_set()

```python
riv.db_set('status', 'Skipped')
```

### Step 10: Call riv.reload()

```python
riv.reload()
```

### Step 11: Call riv.cancel()

```python
riv.cancel()
```


## Complete Example

```python
# Workflow
frappe.flags.dont_execute_stock_reposts = True
item = make_item()
warehouse = '_Test Warehouse - _TC'
old = make_stock_entry(item_code=item.name, to_warehouse=warehouse, qty=2, rate=5)
_new = make_stock_entry(item_code=item.name, to_warehouse=warehouse, qty=5, rate=10)
old.cancel()
riv = frappe.get_last_doc('Repost Item Valuation', {'voucher_type': old.doctype, 'voucher_no': old.name})
self.assertRaises(frappe.ValidationError, riv.cancel)
riv.db_set('status', 'Skipped')
riv.reload()
riv.cancel()
```

## Next Steps


---

*Source: test_repost_item_valuation.py:199 | Complexity: Advanced | Last updated: 2026-02-04*