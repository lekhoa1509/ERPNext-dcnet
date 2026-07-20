# How To: Work Order Material Transferred Qty With Process Loss

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test work order material transferred qty with process loss

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

### Step 1: Assign stock_entries = value

```python
stock_entries = []
```

### Step 2: Assign bom = frappe.get_doc(...)

```python
bom = frappe.get_doc('BOM', {'docstatus': 1, 'with_operations': 1, 'company': '_Test Company'})
```

### Step 3: Assign work_order = make_wo_order_test_record(...)

```python
work_order = make_wo_order_test_record(item=bom.item, qty=2, bom_no=bom.name, source_warehouse='_Test Warehouse - _TC', transfer_material_against='Job Card')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(work_order.qty, 2)
```

### Step 5: Assign job_cards = frappe.get_all(...)

```python
job_cards = frappe.get_all('Job Card', filters={'work_order': work_order.name}, order_by='creation asc')
```

### Step 6: Call work_order.reload()

```python
work_order.reload()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(work_order.material_transferred_for_manufacturing, 2)
```

### Step 8: Assign stock_entry_doc = test_stock_entry.make_stock_entry(...)

```python
stock_entry_doc = test_stock_entry.make_stock_entry(item_code=row.item_code, target='_Test Warehouse - _TC', qty=row.required_qty, basic_rate=100)
```

### Step 9: Call stock_entries.append()

```python
stock_entries.append(stock_entry_doc)
```

### Step 10: Assign transfer_entry_1 = make_stock_entry_from_jc(...)

```python
transfer_entry_1 = make_stock_entry_from_jc(row.name)
```

### Step 11: Call transfer_entry_1.submit()

```python
transfer_entry_1.submit()
```

### Step 12: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc('Job Card', row.name)
```

### Step 13: Call doc.save()

```python
doc.save()
```

### Step 14: Call doc.submit()

```python
doc.submit()
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(doc.total_completed_qty, 1)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(doc.process_loss_qty, 1)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(row.completed_qty, 1)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(row.process_loss_qty, 1)
```

### Step 19: Call doc.append()

```python
doc.append('time_logs', {'from_time': row.from_time, 'to_time': row.to_time, 'time_in_mins': row.time_in_mins, 'completed_qty': 1})
```


## Complete Example

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

# Workflow
stock_entries = []
bom = frappe.get_doc('BOM', {'docstatus': 1, 'with_operations': 1, 'company': '_Test Company'})
work_order = make_wo_order_test_record(item=bom.item, qty=2, bom_no=bom.name, source_warehouse='_Test Warehouse - _TC', transfer_material_against='Job Card')
self.assertEqual(work_order.qty, 2)
for row in work_order.required_items:
    stock_entry_doc = test_stock_entry.make_stock_entry(item_code=row.item_code, target='_Test Warehouse - _TC', qty=row.required_qty, basic_rate=100)
    stock_entries.append(stock_entry_doc)
job_cards = frappe.get_all('Job Card', filters={'work_order': work_order.name}, order_by='creation asc')
for row in job_cards:
    transfer_entry_1 = make_stock_entry_from_jc(row.name)
    transfer_entry_1.submit()
    doc = frappe.get_doc('Job Card', row.name)
    for row in doc.scheduled_time_logs:
        doc.append('time_logs', {'from_time': row.from_time, 'to_time': row.to_time, 'time_in_mins': row.time_in_mins, 'completed_qty': 1})
    doc.save()
    doc.submit()
    self.assertEqual(doc.total_completed_qty, 1)
    self.assertEqual(doc.process_loss_qty, 1)
work_order.reload()
self.assertEqual(work_order.material_transferred_for_manufacturing, 2)
for row in work_order.operations:
    self.assertEqual(row.completed_qty, 1)
    self.assertEqual(row.process_loss_qty, 1)
```

## Next Steps


---

*Source: test_work_order.py:513 | Complexity: Advanced | Last updated: 2026-02-04*