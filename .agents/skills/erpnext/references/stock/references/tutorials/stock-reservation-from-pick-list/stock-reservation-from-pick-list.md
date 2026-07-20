# How To: Stock Reservation From Pick List

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test stock reservation from pick list

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `random`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_entry.stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_reservation_entry.stock_reservation_entry`
- `erpnext.stock.utils`
- `erpnext.stock.doctype.stock_reservation_entry.stock_reservation_entry`
- `erpnext.stock.doctype.stock_reservation_entry.stock_reservation_entry`
- `erpnext.stock.doctype.stock_reservation_entry.stock_reservation_entry`
- `erpnext.stock.stock_ledger`
- `erpnext.stock.doctype.serial_no.serial_no`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.stock.doctype.material_request.material_request`

**Setup Required:**
```python
self.warehouse = '_Test Warehouse - _TC'
self.sr_item = make_item(properties={'is_stock_item': 1, 'valuation_rate': 100})
create_material_receipt(items={self.sr_item.name: self.sr_item}, warehouse=self.warehouse, qty=100)
```

## Step-by-Step Guide

### Step 1: Assign items_details = create_items(...)

```python
items_details = create_items()
```

### Step 2: Call create_material_receipt()

```python
create_material_receipt(items_details, self.warehouse, qty=100)
```

### Step 3: Assign item_list = value

```python
item_list = []
```

### Step 4: Assign so = make_sales_order(...)

```python
so = make_sales_order(item_list=item_list, warehouse=self.warehouse)
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

### Step 8: Call pl.create_stock_reservation_entries()

```python
pl.create_stock_reservation_entries()
```

### Step 9: Call pl.load_from_db()

```python
pl.load_from_db()
```

### Step 10: Call so.load_from_db()

```python
so.load_from_db()
```

### Step 11: Assign sre = frappe.qb.DocType(...)

```python
sre = frappe.qb.DocType('Stock Reservation Entry')
```

### Step 12: Assign sb_entry = frappe.qb.DocType(...)

```python
sb_entry = frappe.qb.DocType('Serial and Batch Entry')
```

### Step 13: Call item_list.append()

```python
item_list.append({'item_code': item_code, 'warehouse': self.warehouse, 'qty': randint(11, 100), 'uom': properties.stock_uom, 'rate': randint(10, 400)})
```

### Step 14: Assign sre_details = value

```python
sre_details = get_stock_reservation_entries_for_voucher('Sales Order', so.name, item.name, fields=['reserved_qty'])[0]
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(item.stock_reserved_qty, sre_details.reserved_qty)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(location.stock_reserved_qty, location.qty)
```

### Step 17: Assign picked_sb_entries = frappe.db.get_all(...)

```python
picked_sb_entries = frappe.db.get_all('Serial and Batch Entry', filters={'parent': location.serial_and_batch_bundle}, fields=['serial_no', 'batch_no', 'qty'], as_list=True)
```

### Step 18: Assign reserved_sb_entries = frappe.qb.from_.inner_join.on.select.where.run(...)

```python
reserved_sb_entries = frappe.qb.from_(sre).inner_join(sb_entry).on(sre.name == sb_entry.parent).select(sb_entry.serial_no, sb_entry.batch_no, sb_entry.qty).where((sre.voucher_type == 'Sales Order') & (sre.voucher_no == location.sales_order) & (sre.voucher_detail_no == location.sales_order_item) & (sre.from_voucher_type == 'Pick List') & (sre.from_voucher_no == pl.name) & (sre.from_voucher_detail_no == location.name)).run(as_dict=True)
```

### Step 19: Call self.assertSetEqual()

```python
self.assertSetEqual(picked_sb_details, reserved_sb_details)
```


## Complete Example

```python
# Setup
self.warehouse = '_Test Warehouse - _TC'
self.sr_item = make_item(properties={'is_stock_item': 1, 'valuation_rate': 100})
create_material_receipt(items={self.sr_item.name: self.sr_item}, warehouse=self.warehouse, qty=100)

# Workflow
items_details = create_items()
create_material_receipt(items_details, self.warehouse, qty=100)
item_list = []
for item_code, properties in items_details.items():
    item_list.append({'item_code': item_code, 'warehouse': self.warehouse, 'qty': randint(11, 100), 'uom': properties.stock_uom, 'rate': randint(10, 400)})
so = make_sales_order(item_list=item_list, warehouse=self.warehouse)
pl = create_pick_list(so.name)
pl.save()
pl.submit()
pl.create_stock_reservation_entries()
pl.load_from_db()
so.load_from_db()
for item in so.items:
    sre_details = get_stock_reservation_entries_for_voucher('Sales Order', so.name, item.name, fields=['reserved_qty'])[0]
    self.assertEqual(item.stock_reserved_qty, sre_details.reserved_qty)
sre = frappe.qb.DocType('Stock Reservation Entry')
sb_entry = frappe.qb.DocType('Serial and Batch Entry')
for location in pl.locations:
    self.assertEqual(location.stock_reserved_qty, location.qty)
    if location.serial_and_batch_bundle:
        picked_sb_entries = frappe.db.get_all('Serial and Batch Entry', filters={'parent': location.serial_and_batch_bundle}, fields=['serial_no', 'batch_no', 'qty'], as_list=True)
        picked_sb_details: set[tuple] = set(picked_sb_entries)
        reserved_sb_entries = frappe.qb.from_(sre).inner_join(sb_entry).on(sre.name == sb_entry.parent).select(sb_entry.serial_no, sb_entry.batch_no, sb_entry.qty).where((sre.voucher_type == 'Sales Order') & (sre.voucher_no == location.sales_order) & (sre.voucher_detail_no == location.sales_order_item) & (sre.from_voucher_type == 'Pick List') & (sre.from_voucher_no == pl.name) & (sre.from_voucher_detail_no == location.name)).run(as_dict=True)
        reserved_sb_details: set[tuple] = {(sb_details.serial_no, sb_details.batch_no, -1 * sb_details.qty) for sb_details in reserved_sb_entries}
        self.assertSetEqual(picked_sb_details, reserved_sb_details)
```

## Next Steps


---

*Source: test_stock_reservation_entry.py:514 | Complexity: Advanced | Last updated: 2026-02-04*