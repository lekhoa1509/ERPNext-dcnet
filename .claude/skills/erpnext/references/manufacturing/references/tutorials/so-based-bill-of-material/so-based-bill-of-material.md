# How To: So Based Bill Of Material

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test so based bill of material

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

### Step 1: Assign item = 'Test SO Production Item 1'

```python
item = 'Test SO Production Item 1'
```

### Step 2: Call create_item()

```python
create_item(item)
```

### Step 3: Assign raw_material = 'Test SO RM Production Item 1'

```python
raw_material = 'Test SO RM Production Item 1'
```

### Step 4: Call create_item()

```python
create_item(raw_material)
```

### Step 5: Assign bom1 = make_bom(...)

```python
bom1 = make_bom(item=item, raw_materials=[raw_material])
```

### Step 6: Assign so = make_sales_order(...)

```python
so = make_sales_order(item_code=item, qty=4)
```

### Step 7: Assign bom2 = make_bom(...)

```python
bom2 = make_bom(item=item, raw_materials=[raw_material])
```

### Step 8: Assign so2 = make_sales_order(...)

```python
so2 = make_sales_order(item_code=item, qty=4)
```

### Step 9: Assign pln1 = frappe.new_doc(...)

```python
pln1 = frappe.new_doc('Production Plan')
```

### Step 10: Assign pln1.company = value

```python
pln1.company = so.company
```

### Step 11: Assign pln1.get_items_from = 'Sales Order'

```python
pln1.get_items_from = 'Sales Order'
```

### Step 12: Call pln1.append()

```python
pln1.append('sales_orders', {'sales_order': so.name, 'sales_order_date': so.transaction_date, 'customer': so.customer, 'grand_total': so.grand_total})
```

### Step 13: Call pln1.get_so_items()

```python
pln1.get_so_items()
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(pln1.po_items[0].bom_no, bom1.name)
```

### Step 15: Assign pln2 = frappe.new_doc(...)

```python
pln2 = frappe.new_doc('Production Plan')
```

### Step 16: Assign pln2.company = value

```python
pln2.company = so2.company
```

### Step 17: Assign pln2.get_items_from = 'Sales Order'

```python
pln2.get_items_from = 'Sales Order'
```

### Step 18: Call pln2.append()

```python
pln2.append('sales_orders', {'sales_order': so2.name, 'sales_order_date': so2.transaction_date, 'customer': so2.customer, 'grand_total': so2.grand_total})
```

### Step 19: Call pln2.get_so_items()

```python
pln2.get_so_items()
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(pln2.po_items[0].bom_no, bom2.name)
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
item = 'Test SO Production Item 1'
create_item(item)
raw_material = 'Test SO RM Production Item 1'
create_item(raw_material)
bom1 = make_bom(item=item, raw_materials=[raw_material])
so = make_sales_order(item_code=item, qty=4)
bom2 = make_bom(item=item, raw_materials=[raw_material])
so2 = make_sales_order(item_code=item, qty=4)
pln1 = frappe.new_doc('Production Plan')
pln1.company = so.company
pln1.get_items_from = 'Sales Order'
pln1.append('sales_orders', {'sales_order': so.name, 'sales_order_date': so.transaction_date, 'customer': so.customer, 'grand_total': so.grand_total})
pln1.get_so_items()
self.assertEqual(pln1.po_items[0].bom_no, bom1.name)
pln2 = frappe.new_doc('Production Plan')
pln2.company = so2.company
pln2.get_items_from = 'Sales Order'
pln2.append('sales_orders', {'sales_order': so2.name, 'sales_order_date': so2.transaction_date, 'customer': so2.customer, 'grand_total': so2.grand_total})
pln2.get_so_items()
self.assertEqual(pln2.po_items[0].bom_no, bom2.name)
```

## Next Steps


---

*Source: test_production_plan.py:359 | Complexity: Advanced | Last updated: 2026-02-04*