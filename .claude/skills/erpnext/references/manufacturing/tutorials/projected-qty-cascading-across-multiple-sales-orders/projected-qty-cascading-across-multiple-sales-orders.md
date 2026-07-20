# How To: Projected Qty Cascading Across Multiple Sales Orders

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test projected qty cascading across multiple sales orders

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

### Step 1: Assign rm_item = value

```python
rm_item = make_item('_Test RM For Cascading', {'is_stock_item': 1, 'valuation_rate': 100}).name
```

### Step 2: Assign fg_item_a = value

```python
fg_item_a = make_item('_Test FG A For Cascading', {'is_stock_item': 1, 'valuation_rate': 200}).name
```

### Step 3: Assign sr = create_stock_reconciliation(...)

```python
sr = create_stock_reconciliation(item_code=rm_item, target='_Test Warehouse - _TC', qty=1, rate=100)
```

### Step 4: Assign so1 = make_sales_order(...)

```python
so1 = make_sales_order(item_code=fg_item_a, qty=1)
```

### Step 5: Assign so2 = make_sales_order(...)

```python
so2 = make_sales_order(item_code=fg_item_a, qty=1)
```

### Step 6: Assign pln = frappe.get_doc(...)

```python
pln = frappe.get_doc({'doctype': 'Production Plan', 'company': '_Test Company', 'posting_date': nowdate(), 'get_items_from': 'Sales Order', 'ignore_existing_ordered_qty': 1})
```

### Step 7: Call pln.append()

```python
pln.append('sales_orders', {'sales_order': so1.name, 'sales_order_date': so1.transaction_date, 'customer': so1.customer, 'grand_total': so1.grand_total})
```

### Step 8: Call pln.append()

```python
pln.append('sales_orders', {'sales_order': so2.name, 'sales_order_date': so2.transaction_date, 'customer': so2.customer, 'grand_total': so2.grand_total})
```

### Step 9: Call pln.get_items()

```python
pln.get_items()
```

### Step 10: Call pln.insert()

```python
pln.insert()
```

### Step 11: Assign mr_items = get_items_for_material_requests(...)

```python
mr_items = get_items_for_material_requests(pln.as_dict())
```

### Step 12: Assign quantities = value

```python
quantities = [d['quantity'] for d in mr_items]
```

### Step 13: Assign rm_qty = sum(...)

```python
rm_qty = sum(quantities)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(len(mr_items), 2)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(rm_qty, 1, 'Cascading failed: total MR qty should be 1 (2 needed - 1 in stock)')
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(quantities, [0, 1], 'Cascading failed: first item should consume stock (qty=0), second should need procurement (qty=1)')
```

### Step 17: Call sr.cancel()

```python
sr.cancel()
```

### Step 18: Call make_bom()

```python
make_bom(item=fg_item_a, raw_materials=[rm_item], rm_qty=1)
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
rm_item = make_item('_Test RM For Cascading', {'is_stock_item': 1, 'valuation_rate': 100}).name
fg_item_a = make_item('_Test FG A For Cascading', {'is_stock_item': 1, 'valuation_rate': 200}).name
if not frappe.db.exists('BOM', {'item': fg_item_a, 'docstatus': 1}):
    make_bom(item=fg_item_a, raw_materials=[rm_item], rm_qty=1)
sr = create_stock_reconciliation(item_code=rm_item, target='_Test Warehouse - _TC', qty=1, rate=100)
so1 = make_sales_order(item_code=fg_item_a, qty=1)
so2 = make_sales_order(item_code=fg_item_a, qty=1)
pln = frappe.get_doc({'doctype': 'Production Plan', 'company': '_Test Company', 'posting_date': nowdate(), 'get_items_from': 'Sales Order', 'ignore_existing_ordered_qty': 1})
pln.append('sales_orders', {'sales_order': so1.name, 'sales_order_date': so1.transaction_date, 'customer': so1.customer, 'grand_total': so1.grand_total})
pln.append('sales_orders', {'sales_order': so2.name, 'sales_order_date': so2.transaction_date, 'customer': so2.customer, 'grand_total': so2.grand_total})
pln.get_items()
pln.insert()
mr_items = get_items_for_material_requests(pln.as_dict())
quantities = [d['quantity'] for d in mr_items]
rm_qty = sum(quantities)
self.assertEqual(len(mr_items), 2)
self.assertEqual(rm_qty, 1, 'Cascading failed: total MR qty should be 1 (2 needed - 1 in stock)')
self.assertEqual(quantities, [0, 1], 'Cascading failed: first item should consume stock (qty=0), second should need procurement (qty=1)')
sr.cancel()
```

## Next Steps


---

*Source: test_production_plan.py:154 | Complexity: Advanced | Last updated: 2026-02-04*