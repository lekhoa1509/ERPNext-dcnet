# How To: Reserved Qty For Partial Completion

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test reserved qty for partial completion

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

### Step 1: Assign item = '_Test Item'

```python
item = '_Test Item'
```

### Step 2: Assign warehouse = '_Test Warehouse - _TC'

```python
warehouse = '_Test Warehouse - _TC'
```

### Step 3: Assign bin1_at_start = get_bin(...)

```python
bin1_at_start = get_bin(item, warehouse)
```

### Step 4: Call bin1_at_start.update_reserved_qty_for_production()

```python
bin1_at_start.update_reserved_qty_for_production()
```

### Step 5: Assign wo_order = make_wo_order_test_record(...)

```python
wo_order = make_wo_order_test_record(item='_Test FG Item', qty=2, source_warehouse=warehouse, skip_transfer=1)
```

### Step 6: Assign reserved_qty_on_submission = cint(...)

```python
reserved_qty_on_submission = cint(get_bin(item, warehouse).reserved_qty_for_production)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(cint(bin1_at_start.reserved_qty_for_production) + 2, reserved_qty_on_submission)
```

### Step 8: Call test_stock_entry.make_stock_entry()

```python
test_stock_entry.make_stock_entry(item_code='_Test Item', target=warehouse, qty=100, basic_rate=100)
```

### Step 9: Call test_stock_entry.make_stock_entry()

```python
test_stock_entry.make_stock_entry(item_code='_Test Item Home Desktop 100', target=warehouse, qty=100, basic_rate=100)
```

### Step 10: Assign s = frappe.get_doc(...)

```python
s = frappe.get_doc(make_stock_entry(wo_order.name, 'Manufacture', 1))
```

### Step 11: Call s.submit()

```python
s.submit()
```

### Step 12: Assign bin1_at_completion = get_bin(...)

```python
bin1_at_completion = get_bin(item, warehouse)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(cint(bin1_at_completion.reserved_qty_for_production), reserved_qty_on_submission - 1)
```


## Complete Example

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

# Workflow
item = '_Test Item'
warehouse = '_Test Warehouse - _TC'
bin1_at_start = get_bin(item, warehouse)
bin1_at_start.update_reserved_qty_for_production()
wo_order = make_wo_order_test_record(item='_Test FG Item', qty=2, source_warehouse=warehouse, skip_transfer=1)
reserved_qty_on_submission = cint(get_bin(item, warehouse).reserved_qty_for_production)
self.assertEqual(cint(bin1_at_start.reserved_qty_for_production) + 2, reserved_qty_on_submission)
test_stock_entry.make_stock_entry(item_code='_Test Item', target=warehouse, qty=100, basic_rate=100)
test_stock_entry.make_stock_entry(item_code='_Test Item Home Desktop 100', target=warehouse, qty=100, basic_rate=100)
s = frappe.get_doc(make_stock_entry(wo_order.name, 'Manufacture', 1))
s.submit()
bin1_at_completion = get_bin(item, warehouse)
self.assertEqual(cint(bin1_at_completion.reserved_qty_for_production), reserved_qty_on_submission - 1)
```

## Next Steps


---

*Source: test_work_order.py:121 | Complexity: Advanced | Last updated: 2026-02-04*