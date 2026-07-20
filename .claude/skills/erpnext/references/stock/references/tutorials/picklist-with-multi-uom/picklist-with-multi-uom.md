# How To: Picklist With Multi Uom

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test picklist with multi uom

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

### Step 2: Assign item = value

```python
item = make_item(properties={'uoms': [dict(uom='Box', conversion_factor=24)]}).name
```

### Step 3: Call make_stock_entry()

```python
make_stock_entry(item=item, to_warehouse=warehouse, qty=1000)
```

### Step 4: Assign so = make_sales_order(...)

```python
so = make_sales_order(item_code=item, qty=10, rate=42, uom='Box')
```

### Step 5: Assign pl = create_pick_list(...)

```python
pl = create_pick_list(so.name)
```

### Step 6: Call pl.save()

```python
pl.save()
```

### Step 7: Call pl.submit()

```python
pl.submit()
```

### Step 8: Call so.reload()

```python
so.reload()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(so.per_picked, 50)
```

### Step 10: Assign loc.picked_qty = value

```python
loc.picked_qty = loc.stock_qty / 2
```


## Complete Example

```python
# Workflow
warehouse = '_Test Warehouse - _TC'
item = make_item(properties={'uoms': [dict(uom='Box', conversion_factor=24)]}).name
make_stock_entry(item=item, to_warehouse=warehouse, qty=1000)
so = make_sales_order(item_code=item, qty=10, rate=42, uom='Box')
pl = create_pick_list(so.name)
for loc in pl.locations:
    loc.picked_qty = loc.stock_qty / 2
pl.save()
pl.submit()
so.reload()
self.assertEqual(so.per_picked, 50)
```

## Next Steps


---

*Source: test_pick_list.py:688 | Complexity: Advanced | Last updated: 2026-02-04*