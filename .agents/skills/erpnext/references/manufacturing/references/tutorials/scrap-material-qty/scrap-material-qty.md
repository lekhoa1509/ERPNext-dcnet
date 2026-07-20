# How To: Scrap Material Qty

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test scrap material qty

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

### Step 1: Assign wo_order = make_wo_order_test_record(...)

```python
wo_order = make_wo_order_test_record(planned_start_date=now(), qty=2)
```

### Step 2: Call test_stock_entry.make_stock_entry()

```python
test_stock_entry.make_stock_entry(item_code='_Test Item', target='Stores - _TC', qty=10, basic_rate=5000.0)
```

### Step 3: Call test_stock_entry.make_stock_entry()

```python
test_stock_entry.make_stock_entry(item_code='_Test Item Home Desktop 100', target='Stores - _TC', qty=10, basic_rate=1000.0)
```

### Step 4: Assign s = frappe.get_doc(...)

```python
s = frappe.get_doc(make_stock_entry(wo_order.name, 'Material Transfer for Manufacture', 2))
```

### Step 5: Call s.insert()

```python
s.insert()
```

### Step 6: Call s.submit()

```python
s.submit()
```

### Step 7: Assign s = frappe.get_doc(...)

```python
s = frappe.get_doc(make_stock_entry(wo_order.name, 'Manufacture', 2))
```

### Step 8: Call s.insert()

```python
s.insert()
```

### Step 9: Call s.submit()

```python
s.submit()
```

### Step 10: Assign wo_order_details = frappe.db.get_value(...)

```python
wo_order_details = frappe.db.get_value('Work Order', wo_order.name, ['scrap_warehouse', 'qty', 'produced_qty', 'bom_no'], as_dict=1)
```

### Step 11: Assign scrap_item_details = get_scrap_item_details(...)

```python
scrap_item_details = get_scrap_item_details(wo_order_details.bom_no)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(wo_order_details.produced_qty, 2)
```

### Step 13: Assign d.s_warehouse = 'Stores - _TC'

```python
d.s_warehouse = 'Stores - _TC'
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(wo_order_details.scrap_warehouse, item.t_warehouse)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(flt(wo_order_details.qty) * flt(scrap_item_details[item.item_code]), item.qty)
```


## Complete Example

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

# Workflow
wo_order = make_wo_order_test_record(planned_start_date=now(), qty=2)
test_stock_entry.make_stock_entry(item_code='_Test Item', target='Stores - _TC', qty=10, basic_rate=5000.0)
test_stock_entry.make_stock_entry(item_code='_Test Item Home Desktop 100', target='Stores - _TC', qty=10, basic_rate=1000.0)
s = frappe.get_doc(make_stock_entry(wo_order.name, 'Material Transfer for Manufacture', 2))
for d in s.get('items'):
    d.s_warehouse = 'Stores - _TC'
s.insert()
s.submit()
s = frappe.get_doc(make_stock_entry(wo_order.name, 'Manufacture', 2))
s.insert()
s.submit()
wo_order_details = frappe.db.get_value('Work Order', wo_order.name, ['scrap_warehouse', 'qty', 'produced_qty', 'bom_no'], as_dict=1)
scrap_item_details = get_scrap_item_details(wo_order_details.bom_no)
self.assertEqual(wo_order_details.produced_qty, 2)
for item in s.items:
    if item.bom_no and item.item_code in scrap_item_details:
        self.assertEqual(wo_order_details.scrap_warehouse, item.t_warehouse)
        self.assertEqual(flt(wo_order_details.qty) * flt(scrap_item_details[item.item_code]), item.qty)
```

## Next Steps


---

*Source: test_work_order.py:337 | Complexity: Advanced | Last updated: 2026-02-04*