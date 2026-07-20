# How To: Material Request Type Manufacture

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test material request type manufacture

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
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][1]).insert()
```

### Step 2: Assign mr = frappe.get_doc(...)

```python
mr = frappe.get_doc('Material Request', mr.name)
```

### Step 3: Call mr.submit()

```python
mr.submit()
```

### Step 4: Assign completed_qty = value

```python
completed_qty = mr.items[0].ordered_qty
```

### Step 5: Assign requested_qty = value

```python
requested_qty = frappe.db.sql('select indented_qty from `tabBin` where \t\t\titem_code= %s and warehouse= %s ', (mr.items[0].item_code, mr.items[0].warehouse))[0][0]
```

### Step 6: Assign prod_order = raise_work_orders(...)

```python
prod_order = raise_work_orders(mr.name, mr.company)
```

### Step 7: Assign po = frappe.get_doc(...)

```python
po = frappe.get_doc('Work Order', prod_order[0])
```

### Step 8: Assign po.wip_warehouse = '_Test Warehouse 1 - _TC'

```python
po.wip_warehouse = '_Test Warehouse 1 - _TC'
```

### Step 9: Call po.submit()

```python
po.submit()
```

### Step 10: Assign mr = frappe.get_doc(...)

```python
mr = frappe.get_doc('Material Request', mr.name)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(completed_qty + po.qty, mr.items[0].ordered_qty)
```

### Step 12: Assign new_requested_qty = value

```python
new_requested_qty = frappe.db.sql('select indented_qty from `tabBin` where \t\t\titem_code= %s and warehouse= %s ', (mr.items[0].item_code, mr.items[0].warehouse))[0][0]
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(requested_qty - po.qty, new_requested_qty)
```

### Step 14: Call po.cancel()

```python
po.cancel()
```

### Step 15: Assign mr = frappe.get_doc(...)

```python
mr = frappe.get_doc('Material Request', mr.name)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(completed_qty, mr.items[0].ordered_qty)
```

### Step 17: Assign new_requested_qty = value

```python
new_requested_qty = frappe.db.sql('select indented_qty from `tabBin` where \t\t\titem_code= %s and warehouse= %s ', (mr.items[0].item_code, mr.items[0].warehouse))[0][0]
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(requested_qty, new_requested_qty)
```


## Complete Example

```python
# Workflow
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][1]).insert()
mr = frappe.get_doc('Material Request', mr.name)
mr.submit()
completed_qty = mr.items[0].ordered_qty
requested_qty = frappe.db.sql('select indented_qty from `tabBin` where \t\t\titem_code= %s and warehouse= %s ', (mr.items[0].item_code, mr.items[0].warehouse))[0][0]
prod_order = raise_work_orders(mr.name, mr.company)
po = frappe.get_doc('Work Order', prod_order[0])
po.wip_warehouse = '_Test Warehouse 1 - _TC'
po.submit()
mr = frappe.get_doc('Material Request', mr.name)
self.assertEqual(completed_qty + po.qty, mr.items[0].ordered_qty)
new_requested_qty = frappe.db.sql('select indented_qty from `tabBin` where \t\t\titem_code= %s and warehouse= %s ', (mr.items[0].item_code, mr.items[0].warehouse))[0][0]
self.assertEqual(requested_qty - po.qty, new_requested_qty)
po.cancel()
mr = frappe.get_doc('Material Request', mr.name)
self.assertEqual(completed_qty, mr.items[0].ordered_qty)
new_requested_qty = frappe.db.sql('select indented_qty from `tabBin` where \t\t\titem_code= %s and warehouse= %s ', (mr.items[0].item_code, mr.items[0].warehouse))[0][0]
self.assertEqual(requested_qty, new_requested_qty)
```

## Next Steps


---

*Source: test_material_request.py:739 | Complexity: Advanced | Last updated: 2026-02-04*