# How To: Production Plan Mr Creation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test if MRs are created for unavailable raw materials.

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

### Step 1: 'Test if MRs are created for unavailable raw materials.'

```python
'Test if MRs are created for unavailable raw materials.'
```

### Step 2: Assign pln = create_production_plan(...)

```python
pln = create_production_plan(item_code='Test Production Item 1')
```

### Step 3: Call self.assertTrue()

```python
self.assertTrue(len(pln.mr_items), 2)
```

### Step 4: Call pln.make_material_request()

```python
pln.make_material_request()
```

### Step 5: Call pln.reload()

```python
pln.reload()
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(pln.status, 'Material Requested')
```

### Step 7: Assign material_requests = frappe.get_all(...)

```python
material_requests = frappe.get_all('Material Request Item', fields=['parent'], filters={'production_plan': pln.name}, as_list=1, distinct=True)
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(len(material_requests), 2)
```

### Step 9: Call pln.make_work_order()

```python
pln.make_work_order()
```

### Step 10: Assign work_orders = frappe.get_all(...)

```python
work_orders = frappe.get_all('Work Order', fields=['name'], filters={'production_plan': pln.name}, as_list=1)
```

### Step 11: Call pln.make_work_order()

```python
pln.make_work_order()
```

### Step 12: Assign nwork_orders = frappe.get_all(...)

```python
nwork_orders = frappe.get_all('Work Order', fields=['name'], filters={'production_plan': pln.name}, as_list=1)
```

### Step 13: Call self.assertTrue()

```python
self.assertTrue(len(work_orders), len(nwork_orders))
```

### Step 14: Call self.assertTrue()

```python
self.assertTrue(len(work_orders), len(pln.po_items))
```

### Step 15: Assign pln = frappe.get_doc(...)

```python
pln = frappe.get_doc('Production Plan', pln.name)
```

### Step 16: Call pln.cancel()

```python
pln.cancel()
```

### Step 17: Assign row.schedule_date = add_to_date(...)

```python
row.schedule_date = add_to_date(nowdate(), days=10)
```

### Step 18: Assign mr_schedule_date = getdate(...)

```python
mr_schedule_date = getdate(frappe.db.get_value('Material Request', row[0], 'schedule_date'))
```

### Step 19: Assign expected_date = getdate(...)

```python
expected_date = getdate(add_to_date(nowdate(), days=10))
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(mr_schedule_date, expected_date)
```

### Step 21: Assign mr = frappe.get_doc(...)

```python
mr = frappe.get_doc('Material Request', name[0])
```

### Step 22: Assign mr = frappe.delete_doc(...)

```python
mr = frappe.delete_doc('Work Order', name[0])
```

### Step 23: Call mr.cancel()

```python
mr.cancel()
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
'Test if MRs are created for unavailable raw materials.'
pln = create_production_plan(item_code='Test Production Item 1')
self.assertTrue(len(pln.mr_items), 2)
for row in pln.mr_items:
    row.schedule_date = add_to_date(nowdate(), days=10)
pln.make_material_request()
pln.reload()
self.assertTrue(pln.status, 'Material Requested')
material_requests = frappe.get_all('Material Request Item', fields=['parent'], filters={'production_plan': pln.name}, as_list=1, distinct=True)
self.assertTrue(len(material_requests), 2)
for row in material_requests:
    mr_schedule_date = getdate(frappe.db.get_value('Material Request', row[0], 'schedule_date'))
    expected_date = getdate(add_to_date(nowdate(), days=10))
    self.assertEqual(mr_schedule_date, expected_date)
pln.make_work_order()
work_orders = frappe.get_all('Work Order', fields=['name'], filters={'production_plan': pln.name}, as_list=1)
pln.make_work_order()
nwork_orders = frappe.get_all('Work Order', fields=['name'], filters={'production_plan': pln.name}, as_list=1)
self.assertTrue(len(work_orders), len(nwork_orders))
self.assertTrue(len(work_orders), len(pln.po_items))
for name in material_requests:
    mr = frappe.get_doc('Material Request', name[0])
    if mr.docstatus != 0:
        mr.cancel()
for name in work_orders:
    mr = frappe.delete_doc('Work Order', name[0])
pln = frappe.get_doc('Production Plan', pln.name)
pln.cancel()
```

## Next Steps


---

*Source: test_production_plan.py:62 | Complexity: Advanced | Last updated: 2026-02-04*