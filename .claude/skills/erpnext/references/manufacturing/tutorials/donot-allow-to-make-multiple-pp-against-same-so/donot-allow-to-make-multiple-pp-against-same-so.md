# How To: Donot Allow To Make Multiple Pp Against Same So

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test donot allow to make multiple pp against same so

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

### Step 5: Assign so = make_sales_order(...)

```python
so = make_sales_order(item_code=item, qty=4)
```

### Step 6: Assign pln = frappe.new_doc(...)

```python
pln = frappe.new_doc('Production Plan')
```

### Step 7: Assign pln.company = value

```python
pln.company = so.company
```

### Step 8: Assign pln.get_items_from = 'Sales Order'

```python
pln.get_items_from = 'Sales Order'
```

### Step 9: Call pln.append()

```python
pln.append('sales_orders', {'sales_order': so.name, 'sales_order_date': so.transaction_date, 'customer': so.customer, 'grand_total': so.grand_total})
```

### Step 10: Call pln.get_so_items()

```python
pln.get_so_items()
```

### Step 11: Call pln.submit()

```python
pln.submit()
```

### Step 12: Assign pln = frappe.new_doc(...)

```python
pln = frappe.new_doc('Production Plan')
```

### Step 13: Assign pln.company = value

```python
pln.company = so.company
```

### Step 14: Assign pln.get_items_from = 'Sales Order'

```python
pln.get_items_from = 'Sales Order'
```

### Step 15: Call pln.append()

```python
pln.append('sales_orders', {'sales_order': so.name, 'sales_order_date': so.transaction_date, 'customer': so.customer, 'grand_total': so.grand_total})
```

### Step 16: Call pln.get_so_items()

```python
pln.get_so_items()
```

### Step 17: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, pln.save)
```

### Step 18: Call make_bom()

```python
make_bom(item=item, raw_materials=[raw_material])
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
if not frappe.db.get_value('BOM', {'item': item}):
    make_bom(item=item, raw_materials=[raw_material])
so = make_sales_order(item_code=item, qty=4)
pln = frappe.new_doc('Production Plan')
pln.company = so.company
pln.get_items_from = 'Sales Order'
pln.append('sales_orders', {'sales_order': so.name, 'sales_order_date': so.transaction_date, 'customer': so.customer, 'grand_total': so.grand_total})
pln.get_so_items()
pln.submit()
pln = frappe.new_doc('Production Plan')
pln.company = so.company
pln.get_items_from = 'Sales Order'
pln.append('sales_orders', {'sales_order': so.name, 'sales_order_date': so.transaction_date, 'customer': so.customer, 'grand_total': so.grand_total})
pln.get_so_items()
self.assertRaises(frappe.ValidationError, pln.save)
```

## Next Steps


---

*Source: test_production_plan.py:314 | Complexity: Advanced | Last updated: 2026-02-04*