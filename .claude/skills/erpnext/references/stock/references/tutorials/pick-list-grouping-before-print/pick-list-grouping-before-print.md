# How To: Pick List Grouping Before Print

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test pick list grouping before print

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.packed_item.test_packed_item`
- `erpnext.stock.doctype.pick_list.pick_list`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.stock_reconciliation.stock_reconciliation`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.pick_list.pick_list`
- `json`
- `frappe.model.mapper`


## Step-by-Step Guide

### Step 1: Assign pl = frappe.get_doc(...)

```python
pl = frappe.get_doc(doctype='Pick List', group_same_items=True, locations=[_dict(item_code='A', warehouse='X', qty=1, picked_qty=2), _dict(item_code='B', warehouse='X', qty=1, picked_qty=2), _dict(item_code='A', warehouse='Y', qty=1, picked_qty=2), _dict(item_code='B', warehouse='Y', qty=1, picked_qty=2)])
```

### Step 2: Call pl.before_print()

```python
pl.before_print()
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(len(pl.locations), 4)
```

### Step 4: Assign pl = frappe.get_doc(...)

```python
pl = frappe.get_doc(doctype='Pick List', group_same_items=False, locations=[_dict(item_code='A', warehouse='X', qty=5, picked_qty=1), _dict(item_code='B', warehouse='Y', qty=4, picked_qty=2), _dict(item_code='A', warehouse='X', qty=3, picked_qty=2), _dict(item_code='B', warehouse='Y', qty=2, picked_qty=2)])
```

### Step 5: Call pl.before_print()

```python
pl.before_print()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(pl.locations), 4)
```

### Step 7: Assign pl.group_same_items = True

```python
pl.group_same_items = True
```

### Step 8: Call pl.before_print()

```python
pl.before_print()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(pl.locations), 2)
```

### Step 10: Assign expected_items = value

```python
expected_items = [_dict(item_code='A', warehouse='X', qty=8, picked_qty=3), _dict(item_code='B', warehouse='Y', qty=6, picked_qty=4)]
```

### Step 11: """compare dicts but ignore missing keys in `a`"""

```python
"""compare dicts but ignore missing keys in `a`"""
```

### Step 12: Call _compare_dicts()

```python
_compare_dicts(expected_item, created_item)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(b.get(key), value, msg=f"{key} doesn't match")
```


## Complete Example

```python
# Workflow
def _compare_dicts(a, b):
    """compare dicts but ignore missing keys in `a`"""
    for key, value in a.items():
        self.assertEqual(b.get(key), value, msg=f"{key} doesn't match")
pl = frappe.get_doc(doctype='Pick List', group_same_items=True, locations=[_dict(item_code='A', warehouse='X', qty=1, picked_qty=2), _dict(item_code='B', warehouse='X', qty=1, picked_qty=2), _dict(item_code='A', warehouse='Y', qty=1, picked_qty=2), _dict(item_code='B', warehouse='Y', qty=1, picked_qty=2)])
pl.before_print()
self.assertEqual(len(pl.locations), 4)
pl = frappe.get_doc(doctype='Pick List', group_same_items=False, locations=[_dict(item_code='A', warehouse='X', qty=5, picked_qty=1), _dict(item_code='B', warehouse='Y', qty=4, picked_qty=2), _dict(item_code='A', warehouse='X', qty=3, picked_qty=2), _dict(item_code='B', warehouse='Y', qty=2, picked_qty=2)])
pl.before_print()
self.assertEqual(len(pl.locations), 4)
pl.group_same_items = True
pl.before_print()
self.assertEqual(len(pl.locations), 2)
expected_items = [_dict(item_code='A', warehouse='X', qty=8, picked_qty=3), _dict(item_code='B', warehouse='Y', qty=6, picked_qty=4)]
for expected_item, created_item in zip(expected_items, pl.locations, strict=False):
    _compare_dicts(expected_item, created_item)
```

## Next Steps


---

*Source: test_pick_list.py:484 | Complexity: Advanced | Last updated: 2026-02-04*