# How To: Make Subcontracted Purchase Order

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test make subcontracted purchase order

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.controllers.accounts_controller`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.material_request.material_request`
- `erpnext.stock.doctype.stock_entry.stock_entry`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.subcontracting.doctype.subcontracting_bom.test_subcontracting_bom`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.utils`
- `erpnext.stock.reorder_item`
- `erpnext.stock.doctype.material_request.material_request`
- `erpnext.controllers.status_updater`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `frappe.utils`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `json`
- `erpnext.stock.doctype.pick_list.pick_list`


## Step-by-Step Guide

### Step 1: Assign mr = frappe.copy_doc.insert(...)

```python
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][0]).insert()
```

### Step 2: Assign mr.material_request_type = 'Subcontracting'

```python
mr.material_request_type = 'Subcontracting'
```

### Step 3: Call mr.submit()

```python
mr.submit()
```

### Step 4: Call frappe.db.set_value()

```python
frappe.db.set_value('Item', mr.items[0].item_code, 'is_sub_contracted_item', 1)
```

### Step 5: Assign raw_materials = value

```python
raw_materials = ['Raw Material Item 1', 'Raw Material Item 2']
```

### Step 6: Call frappe.new_doc.update.save()

```python
frappe.new_doc('UOM').update({'uom_name': 'Test UOM'}).save()
```

### Step 7: Assign service_item = make_item(...)

```python
service_item = make_item(properties={'is_stock_item': 0}, uoms=[{'uom': 'Test UOM', 'conversion_factor': 3}])
```

### Step 8: Assign unknown.default_bom = make_bom(...)

```python
mr.items[0].default_bom = make_bom(item=mr.items[0].item_code, raw_materials=raw_materials)
```

### Step 9: Call mr.reload()

```python
mr.reload()
```

### Step 10: Call create_subcontracting_bom()

```python
create_subcontracting_bom(finished_good=mr.items[0].item_code, service_item=service_item.name, finished_good_qty=2, service_item_qty=1, service_item_uom='Test UOM')
```

### Step 11: Assign po = make_purchase_order(...)

```python
po = make_purchase_order(mr.name)
```

### Step 12: Assign po.supplier = '_Test Supplier'

```python
po.supplier = '_Test Supplier'
```

### Step 13: Assign unknown.schedule_date = today(...)

```python
po.items[0].schedule_date = today()
```

### Step 14: Call po.items.pop()

```python
po.items.pop(1)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(po.items[0].stock_qty, 81)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(po.items[0].qty, 27)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(po.items[0].fg_item_qty, 54)
```

### Step 18: Call po.submit()

```python
po.submit()
```

### Step 19: Call mr.reload()

```python
mr.reload()
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(mr.items[0].ordered_qty, 54)
```

### Step 21: Call create_item()

```python
create_item(item)
```


## Complete Example

```python
# Workflow
from erpnext.manufacturing.doctype.production_plan.test_production_plan import make_bom
from erpnext.stock.doctype.item.test_item import create_item, make_item
from erpnext.subcontracting.doctype.subcontracting_bom.test_subcontracting_bom import create_subcontracting_bom
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][0]).insert()
mr.material_request_type = 'Subcontracting'
mr.submit()
frappe.db.set_value('Item', mr.items[0].item_code, 'is_sub_contracted_item', 1)
raw_materials = ['Raw Material Item 1', 'Raw Material Item 2']
for item in raw_materials:
    create_item(item)
frappe.new_doc('UOM').update({'uom_name': 'Test UOM'}).save()
service_item = make_item(properties={'is_stock_item': 0}, uoms=[{'uom': 'Test UOM', 'conversion_factor': 3}])
mr.items[0].default_bom = make_bom(item=mr.items[0].item_code, raw_materials=raw_materials)
mr.reload()
create_subcontracting_bom(finished_good=mr.items[0].item_code, service_item=service_item.name, finished_good_qty=2, service_item_qty=1, service_item_uom='Test UOM')
po = make_purchase_order(mr.name)
po.supplier = '_Test Supplier'
po.items[0].schedule_date = today()
po.items.pop(1)
self.assertEqual(po.items[0].stock_qty, 81)
self.assertEqual(po.items[0].qty, 27)
self.assertEqual(po.items[0].fg_item_qty, 54)
po.submit()
mr.reload()
self.assertEqual(mr.items[0].ordered_qty, 54)
```

## Next Steps


---

*Source: test_material_request.py:50 | Complexity: Advanced | Last updated: 2026-02-04*