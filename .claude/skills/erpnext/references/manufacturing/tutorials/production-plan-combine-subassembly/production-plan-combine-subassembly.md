# How To: Production Plan Combine Subassembly

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test combining Sub assembly items belonging to the same BOM in Prod Plan.
1) Red-Car -> Wheel (sub assembly) > BOM-WHEEL-001
2) Green-Car -> Wheel (sub assembly) > BOM-WHEEL-001

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.controllers.item_variant`
- `erpnext.manufacturing.doctype.production_plan.production_plan`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.doctype.stock_reservation_entry.stock_reservation_entry`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.controllers.status_updater`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.subcontracting.doctype.subcontracting_bom.test_subcontracting_bom`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.manufacturing.doctype.work_order.test_work_order`
- `erpnext.manufacturing.doctype.work_order.test_work_order`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.manufacturing.doctype.work_order.test_work_order`
- `erpnext.manufacturing.doctype.work_order.test_work_order`
- `erpnext.utilities.transaction_base`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.stock.utils`
- `erpnext.stock.utils`
- `erpnext.stock.utils`
- `erpnext.stock.utils`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.utils`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.utils`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.manufacturing.doctype.production_plan.production_plan`
- `collections`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.stock.doctype.material_request.material_request`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.stock.doctype.material_request.material_request`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.stock.doctype.material_request.material_request`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.manufacturing.doctype.bom.test_bom`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.controllers.subcontracting_controller`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.subcontracting.doctype.subcontracting_order.subcontracting_order`
- `erpnext.subcontracting.doctype.subcontracting_receipt.subcontracting_receipt`

**Setup Required:**
```python
for item in ['Test Production Item 1', 'Subassembly Item 1', 'Raw Material Item 1', 'Raw Material Item 2']:
    create_item(item, valuation_rate=100)
    sr = frappe.db.get_value('Stock Reconciliation Item', {'item_code': item, 'docstatus': 1}, 'parent')
    if sr:
        sr_doc = frappe.get_doc('Stock Reconciliation', sr)
        sr_doc.cancel()
create_item('Test Non Stock Raw Material', is_stock_item=0)
for item, raw_materials in {'Subassembly Item 1': ['Raw Material Item 1', 'Raw Material Item 2'], 'Test Production Item 1': ['Raw Material Item 1', 'Subassembly Item 1', 'Test Non Stock Raw Material']}.items():
    if not frappe.db.get_value('BOM', {'item': item}):
        make_bom(item=item, raw_materials=raw_materials)
```

## Step-by-Step Guide

### Step 1: '\n\t\tTest combining Sub assembly items belonging to the same BOM in Prod Plan.\n\t\t1) Red-Car -> Wheel (sub assembly) > BOM-WHEEL-001\n\t\t2) Green-Car -> Wheel (sub assembly) > BOM-WHEEL-001\n\t\t'

```python
'\n\t\tTest combining Sub assembly items belonging to the same BOM in Prod Plan.\n\t\t1) Red-Car -> Wheel (sub assembly) > BOM-WHEEL-001\n\t\t2) Green-Car -> Wheel (sub assembly) > BOM-WHEEL-001\n\t\t'
```

### Step 2: Assign bom_tree_1 = value

```python
bom_tree_1 = {'Red-Car': {'Wheel': {'Rubber': {}}}}
```

### Step 3: Assign bom_tree_2 = value

```python
bom_tree_2 = {'Green-Car': {'Wheel': {'Rubber': {}}}}
```

### Step 4: Assign parent_bom_1 = create_nested_bom(...)

```python
parent_bom_1 = create_nested_bom(bom_tree_1, prefix='')
```

### Step 5: Assign parent_bom_2 = create_nested_bom(...)

```python
parent_bom_2 = create_nested_bom(bom_tree_2, prefix='')
```

### Step 6: Assign subassembly_bom = value

```python
subassembly_bom = parent_bom_1.items[0].bom_no
```

### Step 7: Call frappe.db.set_value()

```python
frappe.db.set_value('BOM Item', parent_bom_2.items[0].name, 'bom_no', subassembly_bom)
```

### Step 8: Assign plan = create_production_plan(...)

```python
plan = create_production_plan(item_code='Red-Car', use_multi_level_bom=1, do_not_save=True)
```

### Step 9: Call plan.append()

```python
plan.append('po_items', {'use_multi_level_bom': 1, 'item_code': 'Green-Car', 'bom_no': frappe.db.get_value('Item', 'Green-Car', 'default_bom'), 'planned_qty': 1, 'planned_start_date': now_datetime()})
```

### Step 10: Call plan.get_sub_assembly_items()

```python
plan.get_sub_assembly_items()
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(len(plan.sub_assembly_items), 2)
```

### Step 12: Assign plan.combine_sub_items = 1

```python
plan.combine_sub_items = 1
```

### Step 13: Call plan.get_sub_assembly_items()

```python
plan.get_sub_assembly_items()
```

### Step 14: Call self.assertTrue()

```python
self.assertTrue(len(plan.sub_assembly_items), 1)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(plan.sub_assembly_items[0].qty, 2.0)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(plan.sub_assembly_items[0].stock_qty, 2.0)
```

### Step 17: Assign unknown.warehouse = 'Finished Goods - _TC'

```python
plan.po_items[0].warehouse = 'Finished Goods - _TC'
```

### Step 18: Call plan.get_sub_assembly_items()

```python
plan.get_sub_assembly_items()
```

### Step 19: Call self.assertTrue()

```python
self.assertTrue(len(plan.sub_assembly_items), 2)
```


## Complete Example

```python
# Setup
for item in ['Test Production Item 1', 'Subassembly Item 1', 'Raw Material Item 1', 'Raw Material Item 2']:
    create_item(item, valuation_rate=100)
    sr = frappe.db.get_value('Stock Reconciliation Item', {'item_code': item, 'docstatus': 1}, 'parent')
    if sr:
        sr_doc = frappe.get_doc('Stock Reconciliation', sr)
        sr_doc.cancel()
create_item('Test Non Stock Raw Material', is_stock_item=0)
for item, raw_materials in {'Subassembly Item 1': ['Raw Material Item 1', 'Raw Material Item 2'], 'Test Production Item 1': ['Raw Material Item 1', 'Subassembly Item 1', 'Test Non Stock Raw Material']}.items():
    if not frappe.db.get_value('BOM', {'item': item}):
        make_bom(item=item, raw_materials=raw_materials)

# Workflow
'\n\t\tTest combining Sub assembly items belonging to the same BOM in Prod Plan.\n\t\t1) Red-Car -> Wheel (sub assembly) > BOM-WHEEL-001\n\t\t2) Green-Car -> Wheel (sub assembly) > BOM-WHEEL-001\n\t\t'
from erpnext.manufacturing.doctype.bom.test_bom import create_nested_bom
bom_tree_1 = {'Red-Car': {'Wheel': {'Rubber': {}}}}
bom_tree_2 = {'Green-Car': {'Wheel': {'Rubber': {}}}}
parent_bom_1 = create_nested_bom(bom_tree_1, prefix='')
parent_bom_2 = create_nested_bom(bom_tree_2, prefix='')
subassembly_bom = parent_bom_1.items[0].bom_no
frappe.db.set_value('BOM Item', parent_bom_2.items[0].name, 'bom_no', subassembly_bom)
plan = create_production_plan(item_code='Red-Car', use_multi_level_bom=1, do_not_save=True)
plan.append('po_items', {'use_multi_level_bom': 1, 'item_code': 'Green-Car', 'bom_no': frappe.db.get_value('Item', 'Green-Car', 'default_bom'), 'planned_qty': 1, 'planned_start_date': now_datetime()})
plan.get_sub_assembly_items()
self.assertTrue(len(plan.sub_assembly_items), 2)
plan.combine_sub_items = 1
plan.get_sub_assembly_items()
self.assertTrue(len(plan.sub_assembly_items), 1)
self.assertEqual(plan.sub_assembly_items[0].qty, 2.0)
self.assertEqual(plan.sub_assembly_items[0].stock_qty, 2.0)
plan.po_items[0].warehouse = 'Finished Goods - _TC'
plan.get_sub_assembly_items()
self.assertTrue(len(plan.sub_assembly_items), 2)
```

## Next Steps


---

*Source: test_production_plan.py:700 | Complexity: Advanced | Last updated: 2026-02-04*