# How To: Cant Consume Reserved Stock

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test cant consume reserved stock

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

### Step 1: Assign so = make_sales_order(...)

```python
so = make_sales_order(item_code=self.sr_item.name, warehouse=self.warehouse, qty=50, rate=100, do_not_submit=True)
```

### Step 2: Assign so.reserve_stock = 1

```python
so.reserve_stock = 1
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

### Step 6: Assign actual_qty = get_stock_balance(...)

```python
actual_qty = get_stock_balance(self.sr_item.name, self.warehouse)
```

### Step 7: Assign se = make_stock_entry(...)

```python
se = make_stock_entry(item_code=self.sr_item.name, qty=actual_qty, from_warehouse=self.warehouse, rate=100, purpose='Material Issue', do_not_submit=True)
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(NegativeStockError, se.submit)
```

### Step 9: Call se.cancel()

```python
se.cancel()
```

### Step 10: Call cancel_stock_reservation_entries()

```python
cancel_stock_reservation_entries(so.doctype, so.name)
```

### Step 11: Assign se = make_stock_entry(...)

```python
se = make_stock_entry(item_code=self.sr_item.name, qty=actual_qty, from_warehouse=self.warehouse, rate=100, purpose='Material Issue', do_not_submit=True)
```

### Step 12: Call se.submit()

```python
se.submit()
```

### Step 13: Call se.cancel()

```python
se.cancel()
```


## Complete Example

```python
# Setup
self.warehouse = '_Test Warehouse - _TC'
self.sr_item = make_item(properties={'is_stock_item': 1, 'valuation_rate': 100})
create_material_receipt(items={self.sr_item.name: self.sr_item}, warehouse=self.warehouse, qty=100)

# Workflow
from erpnext.stock.doctype.stock_reservation_entry.stock_reservation_entry import cancel_stock_reservation_entries
from erpnext.stock.stock_ledger import NegativeStockError
so = make_sales_order(item_code=self.sr_item.name, warehouse=self.warehouse, qty=50, rate=100, do_not_submit=True)
so.reserve_stock = 1
so.items[0].reserve_stock = 1
so.save()
so.submit()
actual_qty = get_stock_balance(self.sr_item.name, self.warehouse)
se = make_stock_entry(item_code=self.sr_item.name, qty=actual_qty, from_warehouse=self.warehouse, rate=100, purpose='Material Issue', do_not_submit=True)
self.assertRaises(NegativeStockError, se.submit)
se.cancel()
cancel_stock_reservation_entries(so.doctype, so.name)
se = make_stock_entry(item_code=self.sr_item.name, qty=actual_qty, from_warehouse=self.warehouse, rate=100, purpose='Material Issue', do_not_submit=True)
se.submit()
se.cancel()
```

## Next Steps


---

*Source: test_stock_reservation_entry.py:195 | Complexity: Advanced | Last updated: 2026-02-04*