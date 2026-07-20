# How To: Update Reserved Qty In Voucher

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test update reserved qty in voucher

## Prerequisites

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


## Step-by-Step Guide

### Step 1: Assign so = make_sales_order(...)

```python
so = make_sales_order(item_code=self.sr_item.name, warehouse=self.warehouse, qty=50, rate=100, do_not_submit=True)
```

### Step 2: Assign so.reserve_stock = 0

```python
so.reserve_stock = 0
```

### Step 3: Assign unknown.reserve_stock = 1

```python
so.items[0].reserve_stock = 1
```

### Step 4: Call so.save()

```python
so.save()
```

### Step 5: Call so.submit()

```python
so.submit()
```

### Step 6: Assign sre1 = make_stock_reservation_entry(...)

```python
sre1 = make_stock_reservation_entry(item_code=self.sr_item.name, warehouse=self.warehouse, voucher_type='Sales Order', voucher_no=so.name, voucher_detail_no=so.items[0].name, reserved_qty=30)
```

### Step 7: Call so.load_from_db()

```python
so.load_from_db()
```

### Step 8: Call sre1.load_from_db()

```python
sre1.load_from_db()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(sre1.status, 'Partially Reserved')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(so.items[0].stock_reserved_qty, sre1.reserved_qty)
```

### Step 11: Assign sre2 = make_stock_reservation_entry(...)

```python
sre2 = make_stock_reservation_entry(item_code=self.sr_item.name, warehouse=self.warehouse, voucher_type='Sales Order', voucher_no=so.name, voucher_detail_no=so.items[0].name, reserved_qty=20)
```

### Step 12: Call so.load_from_db()

```python
so.load_from_db()
```

### Step 13: Call sre2.load_from_db()

```python
sre2.load_from_db()
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(sre1.status, 'Partially Reserved')
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(so.items[0].stock_reserved_qty, sre1.reserved_qty + sre2.reserved_qty)
```

### Step 16: Call sre1.cancel()

```python
sre1.cancel()
```

### Step 17: Call so.load_from_db()

```python
so.load_from_db()
```

### Step 18: Call sre1.load_from_db()

```python
sre1.load_from_db()
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(sre1.status, 'Cancelled')
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(so.items[0].stock_reserved_qty, sre2.reserved_qty)
```

### Step 21: Call sre2.save()

```python
sre2.save()
```

### Step 22: Call so.load_from_db()

```python
so.load_from_db()
```

### Step 23: Call sre1.load_from_db()

```python
sre1.load_from_db()
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(sre2.status, 'Reserved')
```

### Step 25: Call self.assertEqual()

```python
self.assertEqual(so.items[0].stock_reserved_qty, sre2.reserved_qty)
```

### Step 26: Call sre2.cancel()

```python
sre2.cancel()
```

### Step 27: Call so.load_from_db()

```python
so.load_from_db()
```

### Step 28: Call sre2.load_from_db()

```python
sre2.load_from_db()
```

### Step 29: Call self.assertEqual()

```python
self.assertEqual(sre1.status, 'Cancelled')
```

### Step 30: Call self.assertEqual()

```python
self.assertEqual(so.items[0].stock_reserved_qty, 0)
```


## Complete Example

```python
# Workflow
so = make_sales_order(item_code=self.sr_item.name, warehouse=self.warehouse, qty=50, rate=100, do_not_submit=True)
so.reserve_stock = 0
so.items[0].reserve_stock = 1
so.save()
so.submit()
sre1 = make_stock_reservation_entry(item_code=self.sr_item.name, warehouse=self.warehouse, voucher_type='Sales Order', voucher_no=so.name, voucher_detail_no=so.items[0].name, reserved_qty=30)
so.load_from_db()
sre1.load_from_db()
self.assertEqual(sre1.status, 'Partially Reserved')
self.assertEqual(so.items[0].stock_reserved_qty, sre1.reserved_qty)
sre2 = make_stock_reservation_entry(item_code=self.sr_item.name, warehouse=self.warehouse, voucher_type='Sales Order', voucher_no=so.name, voucher_detail_no=so.items[0].name, reserved_qty=20)
so.load_from_db()
sre2.load_from_db()
self.assertEqual(sre1.status, 'Partially Reserved')
self.assertEqual(so.items[0].stock_reserved_qty, sre1.reserved_qty + sre2.reserved_qty)
sre1.cancel()
so.load_from_db()
sre1.load_from_db()
self.assertEqual(sre1.status, 'Cancelled')
self.assertEqual(so.items[0].stock_reserved_qty, sre2.reserved_qty)
sre2.reserved_qty += sre1.reserved_qty
sre2.save()
so.load_from_db()
sre1.load_from_db()
self.assertEqual(sre2.status, 'Reserved')
self.assertEqual(so.items[0].stock_reserved_qty, sre2.reserved_qty)
sre2.cancel()
so.load_from_db()
sre2.load_from_db()
self.assertEqual(sre1.status, 'Cancelled')
self.assertEqual(so.items[0].stock_reserved_qty, 0)
```

## Next Steps


---

*Source: test_stock_reservation_entry.py:126 | Complexity: Advanced | Last updated: 2026-02-04*