# How To: Picklist With Bundles

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test picklist with bundles

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

### Step 1: Assign warehouse = '_Test Warehouse - _TC'

```python
warehouse = '_Test Warehouse - _TC'
```

### Step 2: Assign quantities = value

```python
quantities = [5, 2]
```

### Step 3: Assign unknown = create_product_bundle(...)

```python
bundle, components = create_product_bundle(quantities, warehouse=warehouse)
```

### Step 4: Assign bundle_items = dict(...)

```python
bundle_items = dict(zip(components, quantities, strict=False))
```

### Step 5: Assign so = make_sales_order(...)

```python
so = make_sales_order(item_code=bundle, qty=3, rate=42)
```

### Step 6: Assign pl = create_pick_list(...)

```python
pl = create_pick_list(so.name)
```

### Step 7: Call pl.save()

```python
pl.save()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(len(pl.locations), 2)
```

### Step 9: Call pl.submit()

```python
pl.submit()
```

### Step 10: Call so.reload()

```python
so.reload()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(so.per_picked, 100)
```

### Step 12: Assign dn = create_delivery_note.submit(...)

```python
dn = create_delivery_note(pl.name).submit()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(dn.items[0].rate, 42)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(dn.packed_items[0].warehouse, warehouse)
```

### Step 15: Call so.reload()

```python
so.reload()
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(so.per_delivered, 100)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(item.stock_qty, bundle_items[item.item_code] * 3)
```


## Complete Example

```python
# Workflow
warehouse = '_Test Warehouse - _TC'
quantities = [5, 2]
bundle, components = create_product_bundle(quantities, warehouse=warehouse)
bundle_items = dict(zip(components, quantities, strict=False))
so = make_sales_order(item_code=bundle, qty=3, rate=42)
pl = create_pick_list(so.name)
pl.save()
self.assertEqual(len(pl.locations), 2)
for item in pl.locations:
    self.assertEqual(item.stock_qty, bundle_items[item.item_code] * 3)
pl.submit()
so.reload()
self.assertEqual(so.per_picked, 100)
dn = create_delivery_note(pl.name).submit()
self.assertEqual(dn.items[0].rate, 42)
self.assertEqual(dn.packed_items[0].warehouse, warehouse)
so.reload()
self.assertEqual(so.per_delivered, 100)
```

## Next Steps


---

*Source: test_pick_list.py:812 | Complexity: Advanced | Last updated: 2026-02-04*