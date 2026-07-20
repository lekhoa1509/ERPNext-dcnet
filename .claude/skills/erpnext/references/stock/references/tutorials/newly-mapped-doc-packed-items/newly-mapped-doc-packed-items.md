# How To: Newly Mapped Doc Packed Items

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test impact on packed items in newly mapped DN from SO.

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`


## Step-by-Step Guide

### Step 1: 'Test impact on packed items in newly mapped DN from SO.'

```python
'Test impact on packed items in newly mapped DN from SO.'
```

### Step 2: Assign so_items = value

```python
so_items = []
```

### Step 3: Assign so = make_sales_order(...)

```python
so = make_sales_order(item_list=so_items)
```

### Step 4: Assign dn = make_delivery_note(...)

```python
dn = make_delivery_note(so.name)
```

### Step 5: Assign unknown.qty = 3

```python
dn.items[1].qty = 3
```

### Step 6: Call dn.save()

```python
dn.save()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(dn.packed_items), 4)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(dn.packed_items[2].qty, 6)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(dn.packed_items[3].qty, 6)
```

### Step 10: Call so_items.append()

```python
so_items.append({'item_code': self.bundle, 'qty': qty, 'rate': 400, 'warehouse': '_Test Warehouse - _TC'})
```


## Complete Example

```python
# Workflow
'Test impact on packed items in newly mapped DN from SO.'
so_items = []
for qty in [2, 4]:
    so_items.append({'item_code': self.bundle, 'qty': qty, 'rate': 400, 'warehouse': '_Test Warehouse - _TC'})
so = make_sales_order(item_list=so_items)
dn = make_delivery_note(so.name)
dn.items[1].qty = 3
dn.save()
self.assertEqual(len(dn.packed_items), 4)
self.assertEqual(dn.packed_items[2].qty, 6)
self.assertEqual(dn.packed_items[3].qty, 6)
```

## Next Steps


---

*Source: test_packed_item.py:131 | Complexity: Advanced | Last updated: 2026-02-04*