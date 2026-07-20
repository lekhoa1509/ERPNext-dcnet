# How To: Capcity Planning

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test capcity planning

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

### Step 1: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Manufacturing Settings', {'disable_capacity_planning': 0, 'capacity_planning_for_days': 1})
```

### Step 2: Assign data = frappe.get_cached_value(...)

```python
data = frappe.get_cached_value('BOM', {'docstatus': 1, 'item': '_Test FG Item 2', 'with_operations': 1, 'company': '_Test Company'}, ['name', 'item'])
```

### Step 3: Assign unknown = data

```python
bom, bom_item = data
```

### Step 4: Assign planned_start_date = add_months(...)

```python
planned_start_date = add_months(today(), months=-1)
```

### Step 5: Assign work_order = make_wo_order_test_record(...)

```python
work_order = make_wo_order_test_record(item=bom_item, qty=10, bom_no=bom, planned_start_date=planned_start_date)
```

### Step 6: Assign work_order1 = make_wo_order_test_record(...)

```python
work_order1 = make_wo_order_test_record(item=bom_item, qty=30, bom_no=bom, planned_start_date=planned_start_date, do_not_submit=1)
```

### Step 7: Call self.assertRaises()

```python
self.assertRaises(CapacityError, work_order1.submit)
```

### Step 8: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Manufacturing Settings', {'capacity_planning_for_days': 30})
```

### Step 9: Call work_order1.reload()

```python
work_order1.reload()
```

### Step 10: Call work_order1.submit()

```python
work_order1.submit()
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(work_order1.docstatus, 1)
```

### Step 12: Call work_order1.cancel()

```python
work_order1.cancel()
```

### Step 13: Call work_order.cancel()

```python
work_order.cancel()
```


## Complete Example

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

# Workflow
frappe.db.set_single_value('Manufacturing Settings', {'disable_capacity_planning': 0, 'capacity_planning_for_days': 1})
data = frappe.get_cached_value('BOM', {'docstatus': 1, 'item': '_Test FG Item 2', 'with_operations': 1, 'company': '_Test Company'}, ['name', 'item'])
if data:
    bom, bom_item = data
    planned_start_date = add_months(today(), months=-1)
    work_order = make_wo_order_test_record(item=bom_item, qty=10, bom_no=bom, planned_start_date=planned_start_date)
    work_order1 = make_wo_order_test_record(item=bom_item, qty=30, bom_no=bom, planned_start_date=planned_start_date, do_not_submit=1)
    self.assertRaises(CapacityError, work_order1.submit)
    frappe.db.set_single_value('Manufacturing Settings', {'capacity_planning_for_days': 30})
    work_order1.reload()
    work_order1.submit()
    self.assertTrue(work_order1.docstatus, 1)
    work_order1.cancel()
    work_order.cancel()
```

## Next Steps


---

*Source: test_work_order.py:567 | Complexity: Advanced | Last updated: 2026-02-04*