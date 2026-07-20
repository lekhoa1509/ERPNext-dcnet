# How To: Work Order With Non Transfer Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test work order with non transfer item

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
frappe.db.set_single_value('Manufacturing Settings', 'backflush_raw_materials_based_on', 'BOM')
```

### Step 2: Assign items = value

```python
items = {'Finished Good Transfer Item': 1, '_Test FG Item': 1, '_Test FG Item 1': 0}
```

### Step 3: Assign fg_item = 'Finished Good Transfer Item'

```python
fg_item = 'Finished Good Transfer Item'
```

### Step 4: Call test_stock_entry.make_stock_entry()

```python
test_stock_entry.make_stock_entry(item_code='_Test FG Item', target='_Test Warehouse - _TC', qty=1, basic_rate=100)
```

### Step 5: Call test_stock_entry.make_stock_entry()

```python
test_stock_entry.make_stock_entry(item_code='_Test FG Item 1', target='_Test Warehouse - _TC', qty=1, basic_rate=100)
```

### Step 6: Assign wo = make_wo_order_test_record(...)

```python
wo = make_wo_order_test_record(production_item=fg_item)
```

### Step 7: Assign ste = frappe.get_doc(...)

```python
ste = frappe.get_doc(make_stock_entry(wo.name, 'Material Transfer for Manufacture', 1))
```

### Step 8: Call ste.insert()

```python
ste.insert()
```

### Step 9: Call ste.submit()

```python
ste.submit()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(len(ste.items), 1)
```

### Step 11: Assign ste1 = frappe.get_doc(...)

```python
ste1 = frappe.get_doc(make_stock_entry(wo.name, 'Manufacture', 1))
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(len(ste1.items), 3)
```

### Step 13: Call make_item()

```python
make_item(item, {'include_item_in_manufacturing': allow_transfer})
```

### Step 14: Call make_bom()

```python
make_bom(item=fg_item, raw_materials=['_Test FG Item', '_Test FG Item 1'])
```


## Complete Example

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

# Workflow
frappe.db.set_single_value('Manufacturing Settings', 'backflush_raw_materials_based_on', 'BOM')
items = {'Finished Good Transfer Item': 1, '_Test FG Item': 1, '_Test FG Item 1': 0}
for item, allow_transfer in items.items():
    make_item(item, {'include_item_in_manufacturing': allow_transfer})
fg_item = 'Finished Good Transfer Item'
test_stock_entry.make_stock_entry(item_code='_Test FG Item', target='_Test Warehouse - _TC', qty=1, basic_rate=100)
test_stock_entry.make_stock_entry(item_code='_Test FG Item 1', target='_Test Warehouse - _TC', qty=1, basic_rate=100)
if not frappe.db.get_value('BOM', {'item': fg_item}):
    make_bom(item=fg_item, raw_materials=['_Test FG Item', '_Test FG Item 1'])
wo = make_wo_order_test_record(production_item=fg_item)
ste = frappe.get_doc(make_stock_entry(wo.name, 'Material Transfer for Manufacture', 1))
ste.insert()
ste.submit()
self.assertEqual(len(ste.items), 1)
ste1 = frappe.get_doc(make_stock_entry(wo.name, 'Manufacture', 1))
self.assertEqual(len(ste1.items), 3)
```

## Next Steps


---

*Source: test_work_order.py:601 | Complexity: Advanced | Last updated: 2026-02-04*