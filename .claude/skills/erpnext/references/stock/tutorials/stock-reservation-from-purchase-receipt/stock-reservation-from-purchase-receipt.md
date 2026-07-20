# How To: Stock Reservation From Purchase Receipt

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test stock reservation from purchase receipt

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
create_material_receipt(items_details, self.warehouse, qty=10)
```

### Step 3: Assign item_list = value

```python
item_list = []
```

### Step 4: Assign so = make_sales_order(...)

```python
so = make_sales_order(item_list=item_list, warehouse=self.warehouse)
```

### Step 5: Assign mr = make_material_request(...)

```python
mr = make_material_request(so.name)
```

### Step 6: Assign mr.schedule_date = today(...)

```python
mr.schedule_date = today()
```

### Step 7: Call mr.save.submit()

```python
mr.save().submit()
```

### Step 8: Assign po = make_purchase_order(...)

```python
po = make_purchase_order(mr.name)
```

### Step 9: Assign po.supplier = '_Test Supplier'

```python
po.supplier = '_Test Supplier'
```

### Step 10: Call po.save.submit()

```python
po.save().submit()
```

### Step 11: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(po.name)
```

### Step 12: Call pr.save.submit()

```python
pr.save().submit()
```

### Step 13: Call item_list.append()

```python
item_list.append({'item_code': item_code, 'warehouse': self.warehouse, 'qty': randint(11, 100), 'uom': properties.stock_uom, 'rate': randint(10, 400)})
```

### Step 14: Assign unknown = frappe.db.get_value(...)

```python
sre, status, reserved_qty = frappe.db.get_value('Stock Reservation Entry', {'from_voucher_type': 'Purchase Receipt', 'from_voucher_no': pr.name, 'from_voucher_detail_no': item.name}, ['name', 'status', 'reserved_qty'])
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(status, 'Reserved')
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(reserved_qty, item.qty)
```

### Step 17: Assign sb_details = frappe.db.get_all(...)

```python
sb_details = frappe.db.get_all('Serial and Batch Entry', filters={'parent': item.serial_and_batch_bundle}, fields=['serial_no', 'batch_no', 'qty'], as_list=True)
```

### Step 18: Assign reserved_sb_details = frappe.db.get_all(...)

```python
reserved_sb_details = frappe.db.get_all('Serial and Batch Entry', filters={'parent': sre}, fields=['serial_no', 'batch_no', 'qty'], as_list=True)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(set(sb_details), set(reserved_sb_details))
```


## Complete Example

```python
# Setup
self.warehouse = '_Test Warehouse - _TC'
self.sr_item = make_item(properties={'is_stock_item': 1, 'valuation_rate': 100})
create_material_receipt(items={self.sr_item.name: self.sr_item}, warehouse=self.warehouse, qty=100)

# Workflow
from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_receipt
from erpnext.selling.doctype.sales_order.sales_order import make_material_request
from erpnext.stock.doctype.material_request.material_request import make_purchase_order
items_details = create_items()
create_material_receipt(items_details, self.warehouse, qty=10)
item_list = []
for item_code, properties in items_details.items():
    item_list.append({'item_code': item_code, 'warehouse': self.warehouse, 'qty': randint(11, 100), 'uom': properties.stock_uom, 'rate': randint(10, 400)})
so = make_sales_order(item_list=item_list, warehouse=self.warehouse)
mr = make_material_request(so.name)
mr.schedule_date = today()
mr.save().submit()
po = make_purchase_order(mr.name)
po.supplier = '_Test Supplier'
po.save().submit()
pr = make_purchase_receipt(po.name)
pr.save().submit()
for item in pr.items:
    sre, status, reserved_qty = frappe.db.get_value('Stock Reservation Entry', {'from_voucher_type': 'Purchase Receipt', 'from_voucher_no': pr.name, 'from_voucher_detail_no': item.name}, ['name', 'status', 'reserved_qty'])
    self.assertEqual(status, 'Reserved')
    self.assertEqual(reserved_qty, item.qty)
    if item.serial_and_batch_bundle:
        sb_details = frappe.db.get_all('Serial and Batch Entry', filters={'parent': item.serial_and_batch_bundle}, fields=['serial_no', 'batch_no', 'qty'], as_list=True)
        reserved_sb_details = frappe.db.get_all('Serial and Batch Entry', filters={'parent': sre}, fields=['serial_no', 'batch_no', 'qty'], as_list=True)
        self.assertEqual(set(sb_details), set(reserved_sb_details))
```

## Next Steps


---

*Source: test_stock_reservation_entry.py:596 | Complexity: Advanced | Last updated: 2026-02-04*