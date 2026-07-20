# How To: Update Status

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test update status

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

### Step 1: Assign sre = make_stock_reservation_entry(...)

```python
sre = make_stock_reservation_entry(item_code=self.sr_item.name, warehouse=self.warehouse, reserved_qty=30, ignore_validate=True, do_not_submit=True)
```

### Step 2: Call sre.load_from_db()

```python
sre.load_from_db()
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(sre.status, 'Draft')
```

### Step 4: Call sre.submit()

```python
sre.submit()
```

### Step 5: Call sre.load_from_db()

```python
sre.load_from_db()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(sre.status, 'Partially Reserved')
```

### Step 7: Assign sre.reserved_qty = value

```python
sre.reserved_qty = sre.voucher_qty
```

### Step 8: Call sre.db_update()

```python
sre.db_update()
```

### Step 9: Call sre.update_status()

```python
sre.update_status()
```

### Step 10: Call sre.load_from_db()

```python
sre.load_from_db()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(sre.status, 'Reserved')
```

### Step 12: Assign sre.delivered_qty = 10

```python
sre.delivered_qty = 10
```

### Step 13: Call sre.db_update()

```python
sre.db_update()
```

### Step 14: Call sre.update_status()

```python
sre.update_status()
```

### Step 15: Call sre.load_from_db()

```python
sre.load_from_db()
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(sre.status, 'Partially Delivered')
```

### Step 17: Assign sre.delivered_qty = value

```python
sre.delivered_qty = sre.voucher_qty
```

### Step 18: Call sre.db_update()

```python
sre.db_update()
```

### Step 19: Call sre.update_status()

```python
sre.update_status()
```

### Step 20: Call sre.load_from_db()

```python
sre.load_from_db()
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(sre.status, 'Delivered')
```

### Step 22: Call sre.cancel()

```python
sre.cancel()
```

### Step 23: Call sre.load_from_db()

```python
sre.load_from_db()
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(sre.status, 'Cancelled')
```


## Complete Example

```python
# Workflow
sre = make_stock_reservation_entry(item_code=self.sr_item.name, warehouse=self.warehouse, reserved_qty=30, ignore_validate=True, do_not_submit=True)
sre.load_from_db()
self.assertEqual(sre.status, 'Draft')
sre.submit()
sre.load_from_db()
self.assertEqual(sre.status, 'Partially Reserved')
sre.reserved_qty = sre.voucher_qty
sre.db_update()
sre.update_status()
sre.load_from_db()
self.assertEqual(sre.status, 'Reserved')
sre.delivered_qty = 10
sre.db_update()
sre.update_status()
sre.load_from_db()
self.assertEqual(sre.status, 'Partially Delivered')
sre.delivered_qty = sre.voucher_qty
sre.db_update()
sre.update_status()
sre.load_from_db()
self.assertEqual(sre.status, 'Delivered')
sre.cancel()
sre.load_from_db()
self.assertEqual(sre.status, 'Cancelled')
```

## Next Steps


---

*Source: test_stock_reservation_entry.py:79 | Complexity: Advanced | Last updated: 2026-02-04*