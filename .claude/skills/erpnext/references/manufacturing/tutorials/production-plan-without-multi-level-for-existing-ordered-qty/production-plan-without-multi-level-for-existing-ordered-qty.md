# How To: Production Plan Without Multi Level For Existing Ordered Qty

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: - Disable 'ignore_existing_ordered_qty'.
- Test if MR Planning table avoids pulling Raw Material Qty as it is in stock for
non exploded BOM.

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

### Step 1: "\n\t\t- Disable 'ignore_existing_ordered_qty'.\n\t\t- Test if MR Planning table avoids pulling Raw Material Qty as it is in stock for\n\t\tnon exploded BOM.\n\t\t"

```python
"\n\t\t- Disable 'ignore_existing_ordered_qty'.\n\t\t- Test if MR Planning table avoids pulling Raw Material Qty as it is in stock for\n\t\tnon exploded BOM.\n\t\t"
```

### Step 2: Assign sr1 = create_stock_reconciliation(...)

```python
sr1 = create_stock_reconciliation(item_code='Raw Material Item 1', target='_Test Warehouse - _TC', qty=1, rate=130)
```

### Step 3: Assign sr2 = create_stock_reconciliation(...)

```python
sr2 = create_stock_reconciliation(item_code='Subassembly Item 1', target='_Test Warehouse - _TC', qty=1, rate=140)
```

### Step 4: Assign pln = create_production_plan(...)

```python
pln = create_production_plan(item_code='Test Production Item 1', use_multi_level_bom=0, ignore_existing_ordered_qty=1)
```

### Step 5: Assign items = value

```python
items = []
```

### Step 6: Call self.assertFalse()

```python
self.assertFalse(len(items))
```

### Step 7: Call pln.cancel()

```python
pln.cancel()
```

### Step 8: Call sr1.cancel()

```python
sr1.cancel()
```

### Step 9: Call sr2.cancel()

```python
sr2.cancel()
```

### Step 10: Call items.append()

```python
items.append(row.item_code)
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
"\n\t\t- Disable 'ignore_existing_ordered_qty'.\n\t\t- Test if MR Planning table avoids pulling Raw Material Qty as it is in stock for\n\t\tnon exploded BOM.\n\t\t"
sr1 = create_stock_reconciliation(item_code='Raw Material Item 1', target='_Test Warehouse - _TC', qty=1, rate=130)
sr2 = create_stock_reconciliation(item_code='Subassembly Item 1', target='_Test Warehouse - _TC', qty=1, rate=140)
pln = create_production_plan(item_code='Test Production Item 1', use_multi_level_bom=0, ignore_existing_ordered_qty=1)
items = []
for row in pln.mr_items:
    if row.quantity > 0:
        items.append(row.item_code)
self.assertFalse(len(items))
pln.cancel()
sr1.cancel()
sr2.cancel()
```

## Next Steps


---

*Source: test_production_plan.py:233 | Complexity: Advanced | Last updated: 2026-02-04*