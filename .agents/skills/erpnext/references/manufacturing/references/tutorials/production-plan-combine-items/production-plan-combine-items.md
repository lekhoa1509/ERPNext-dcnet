# How To: Production Plan Combine Items

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test combining FG items in Production Plan.

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

### Step 1: 'Test combining FG items in Production Plan.'

```python
'Test combining FG items in Production Plan.'
```

### Step 2: Assign item = 'Test Production Item 1'

```python
item = 'Test Production Item 1'
```

### Step 3: Assign so1 = make_sales_order(...)

```python
so1 = make_sales_order(item_code=item, qty=1)
```

### Step 4: Assign pln = frappe.new_doc(...)

```python
pln = frappe.new_doc('Production Plan')
```

### Step 5: Assign pln.company = value

```python
pln.company = so1.company
```

### Step 6: Assign pln.get_items_from = 'Sales Order'

```python
pln.get_items_from = 'Sales Order'
```

### Step 7: Call pln.append()

```python
pln.append('sales_orders', {'sales_order': so1.name, 'sales_order_date': so1.transaction_date, 'customer': so1.customer, 'grand_total': so1.grand_total})
```

### Step 8: Assign so2 = make_sales_order(...)

```python
so2 = make_sales_order(item_code=item, qty=2)
```

### Step 9: Call pln.append()

```python
pln.append('sales_orders', {'sales_order': so2.name, 'sales_order_date': so2.transaction_date, 'customer': so2.customer, 'grand_total': so2.grand_total})
```

### Step 10: Assign pln.combine_items = 1

```python
pln.combine_items = 1
```

### Step 11: Call pln.get_items()

```python
pln.get_items()
```

### Step 12: Call pln.submit()

```python
pln.submit()
```

### Step 13: Call self.assertTrue()

```python
self.assertTrue(pln.po_items[0].planned_qty, 3)
```

### Step 14: Call pln.make_work_order()

```python
pln.make_work_order()
```

### Step 15: Assign work_order = frappe.db.get_value(...)

```python
work_order = frappe.db.get_value('Work Order', {'production_plan_item': pln.po_items[0].name, 'production_plan': pln.name}, 'name')
```

### Step 16: Assign wo_doc = frappe.get_doc(...)

```python
wo_doc = frappe.get_doc('Work Order', work_order)
```

### Step 17: Call wo_doc.update()

```python
wo_doc.update({'wip_warehouse': 'Work In Progress - _TC'})
```

### Step 18: Call wo_doc.submit()

```python
wo_doc.submit()
```

### Step 19: Assign so_items = value

```python
so_items = []
```

### Step 20: Call wo_doc.cancel()

```python
wo_doc.cancel()
```

### Step 21: Call pln.reload()

```python
pln.reload()
```

### Step 22: Call pln.cancel()

```python
pln.cancel()
```

### Step 23: Call so_items.append()

```python
so_items.append(plan_reference.sales_order_item)
```

### Step 24: Assign so_wo_qty = frappe.db.get_value(...)

```python
so_wo_qty = frappe.db.get_value('Sales Order Item', plan_reference.sales_order_item, 'work_order_qty')
```

### Step 25: Call self.assertEqual()

```python
self.assertEqual(so_wo_qty, plan_reference.qty)
```

### Step 26: Assign so_wo_qty = frappe.db.get_value(...)

```python
so_wo_qty = frappe.db.get_value('Sales Order Item', so_item, 'work_order_qty')
```

### Step 27: Call self.assertEqual()

```python
self.assertEqual(so_wo_qty, 0.0)
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
'Test combining FG items in Production Plan.'
item = 'Test Production Item 1'
so1 = make_sales_order(item_code=item, qty=1)
pln = frappe.new_doc('Production Plan')
pln.company = so1.company
pln.get_items_from = 'Sales Order'
pln.append('sales_orders', {'sales_order': so1.name, 'sales_order_date': so1.transaction_date, 'customer': so1.customer, 'grand_total': so1.grand_total})
so2 = make_sales_order(item_code=item, qty=2)
pln.append('sales_orders', {'sales_order': so2.name, 'sales_order_date': so2.transaction_date, 'customer': so2.customer, 'grand_total': so2.grand_total})
pln.combine_items = 1
pln.get_items()
pln.submit()
self.assertTrue(pln.po_items[0].planned_qty, 3)
pln.make_work_order()
work_order = frappe.db.get_value('Work Order', {'production_plan_item': pln.po_items[0].name, 'production_plan': pln.name}, 'name')
wo_doc = frappe.get_doc('Work Order', work_order)
wo_doc.update({'wip_warehouse': 'Work In Progress - _TC'})
wo_doc.submit()
so_items = []
for plan_reference in pln.prod_plan_references:
    so_items.append(plan_reference.sales_order_item)
    so_wo_qty = frappe.db.get_value('Sales Order Item', plan_reference.sales_order_item, 'work_order_qty')
    self.assertEqual(so_wo_qty, plan_reference.qty)
wo_doc.cancel()
for so_item in so_items:
    so_wo_qty = frappe.db.get_value('Sales Order Item', so_item, 'work_order_qty')
    self.assertEqual(so_wo_qty, 0.0)
pln.reload()
pln.cancel()
```

## Next Steps


---

*Source: test_production_plan.py:432 | Complexity: Advanced | Last updated: 2026-02-04*