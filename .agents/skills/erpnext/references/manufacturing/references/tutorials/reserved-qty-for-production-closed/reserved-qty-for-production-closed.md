# How To: Reserved Qty For Production Closed

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test reserved qty for production closed

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `collections`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.manufacturing.doctype.job_card.job_card`
- `erpnext.manufacturing.doctype.job_card.job_card`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.serial_no.serial_no`
- `erpnext.stock.doctype.stock_entry`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.utils`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.manufacturing.doctype.operation.test_operation`
- `erpnext.manufacturing.doctype.workstation.test_workstation`
- `erpnext.manufacturing.doctype.workstation_type.test_workstation_type`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.manufacturing.doctype.routing.test_routing`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`

**Setup Required:**
```python
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()
```

## Step-by-Step Guide

### Step 1: Assign wo1 = make_wo_order_test_record(...)

```python
wo1 = make_wo_order_test_record(item='_Test FG Item', qty=2, source_warehouse=self.warehouse)
```

### Step 2: Assign item = value

```python
item = wo1.required_items[0].item_code
```

### Step 3: Assign bin_before = get_bin(...)

```python
bin_before = get_bin(item, self.warehouse)
```

### Step 4: Call bin_before.update_reserved_qty_for_production()

```python
bin_before.update_reserved_qty_for_production()
```

### Step 5: Call make_wo_order_test_record()

```python
make_wo_order_test_record(item='_Test FG Item', qty=2, source_warehouse=self.warehouse)
```

### Step 6: Call close_work_order()

```python
close_work_order(wo1.name, 'Closed')
```

### Step 7: Assign bin_after = get_bin(...)

```python
bin_after = get_bin(item, self.warehouse)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(bin_before.reserved_qty_for_production, bin_after.reserved_qty_for_production)
```


## Complete Example

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

# Workflow
wo1 = make_wo_order_test_record(item='_Test FG Item', qty=2, source_warehouse=self.warehouse)
item = wo1.required_items[0].item_code
bin_before = get_bin(item, self.warehouse)
bin_before.update_reserved_qty_for_production()
make_wo_order_test_record(item='_Test FG Item', qty=2, source_warehouse=self.warehouse)
close_work_order(wo1.name, 'Closed')
bin_after = get_bin(item, self.warehouse)
self.assertEqual(bin_before.reserved_qty_for_production, bin_after.reserved_qty_for_production)
```

## Next Steps


---

*Source: test_work_order.py:237 | Complexity: Advanced | Last updated: 2026-02-04*