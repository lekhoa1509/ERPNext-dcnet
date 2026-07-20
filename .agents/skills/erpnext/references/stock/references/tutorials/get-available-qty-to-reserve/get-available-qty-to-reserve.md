# How To: Get Available Qty To Reserve

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get available qty to reserve

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

### Step 1: Assign available_qty_to_reserve = get_available_qty_to_reserve(...)

```python
available_qty_to_reserve = get_available_qty_to_reserve(self.sr_item.name, self.warehouse)
```

### Step 2: Assign expected_available_qty_to_reserve = get_stock_balance(...)

```python
expected_available_qty_to_reserve = get_stock_balance(self.sr_item.name, self.warehouse)
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(available_qty_to_reserve, expected_available_qty_to_reserve)
```

### Step 4: Assign sre = make_stock_reservation_entry(...)

```python
sre = make_stock_reservation_entry(item_code=self.sr_item.name, warehouse=self.warehouse, ignore_validate=True)
```

### Step 5: Assign available_qty_to_reserve = get_available_qty_to_reserve(...)

```python
available_qty_to_reserve = get_available_qty_to_reserve(self.sr_item.name, self.warehouse)
```

### Step 6: Assign expected_available_qty_to_reserve = value

```python
expected_available_qty_to_reserve = get_stock_balance(self.sr_item.name, self.warehouse) - sre.reserved_qty
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(available_qty_to_reserve, expected_available_qty_to_reserve)
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.stock_reservation_entry.stock_reservation_entry import get_available_qty_to_reserve
available_qty_to_reserve = get_available_qty_to_reserve(self.sr_item.name, self.warehouse)
expected_available_qty_to_reserve = get_stock_balance(self.sr_item.name, self.warehouse)
self.assertEqual(available_qty_to_reserve, expected_available_qty_to_reserve)
sre = make_stock_reservation_entry(item_code=self.sr_item.name, warehouse=self.warehouse, ignore_validate=True)
available_qty_to_reserve = get_available_qty_to_reserve(self.sr_item.name, self.warehouse)
expected_available_qty_to_reserve = get_stock_balance(self.sr_item.name, self.warehouse) - sre.reserved_qty
self.assertEqual(available_qty_to_reserve, expected_available_qty_to_reserve)
```

## Next Steps


---

*Source: test_stock_reservation_entry.py:55 | Complexity: Advanced | Last updated: 2026-02-04*