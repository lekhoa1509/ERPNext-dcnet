# How To: Consider Reserved Stock While Cancelling An Inward Transaction

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test consider reserved stock while cancelling an inward transaction

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

### Step 2: Assign se = create_material_receipt(...)

```python
se = create_material_receipt(items_details, self.warehouse, qty=100)
```

### Step 3: Assign item_list = value

```python
item_list = []
```

### Step 4: Assign so = make_sales_order(...)

```python
so = make_sales_order(item_list=item_list, warehouse=self.warehouse)
```

### Step 5: Call so.create_stock_reservation_entries()

```python
so.create_stock_reservation_entries()
```

### Step 6: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, se.cancel)
```

### Step 7: Call item_list.append()

```python
item_list.append({'item_code': item_code, 'warehouse': self.warehouse, 'qty': randint(11, 100), 'uom': properties.stock_uom, 'rate': randint(10, 400)})
```


## Complete Example

```python
# Setup
self.warehouse = '_Test Warehouse - _TC'
self.sr_item = make_item(properties={'is_stock_item': 1, 'valuation_rate': 100})
create_material_receipt(items={self.sr_item.name: self.sr_item}, warehouse=self.warehouse, qty=100)

# Workflow
items_details = create_items()
se = create_material_receipt(items_details, self.warehouse, qty=100)
item_list = []
for item_code, properties in items_details.items():
    item_list.append({'item_code': item_code, 'warehouse': self.warehouse, 'qty': randint(11, 100), 'uom': properties.stock_uom, 'rate': randint(10, 400)})
so = make_sales_order(item_list=item_list, warehouse=self.warehouse)
so.create_stock_reservation_entries()
self.assertRaises(frappe.ValidationError, se.cancel)
```

## Next Steps


---

*Source: test_stock_reservation_entry.py:675 | Complexity: Intermediate | Last updated: 2026-02-04*