# How To: Requested Qty Multi Uom

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test requested qty multi uom

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

### Step 1: Assign existing_requested_qty = self._get_requested_qty(...)

```python
existing_requested_qty = self._get_requested_qty('_Test FG Item', '_Test Warehouse - _TC')
```

### Step 2: Assign mr = make_material_request(...)

```python
mr = make_material_request(item_code='_Test FG Item', material_request_type='Manufacture', uom='_Test UOM 1', conversion_factor=12)
```

### Step 3: Assign requested_qty = self._get_requested_qty(...)

```python
requested_qty = self._get_requested_qty('_Test FG Item', '_Test Warehouse - _TC')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(requested_qty, existing_requested_qty + 120)
```

### Step 5: Assign work_order = raise_work_orders(...)

```python
work_order = raise_work_orders(mr.name, mr.company)
```

### Step 6: Assign wo = frappe.get_doc(...)

```python
wo = frappe.get_doc('Work Order', work_order[0])
```

### Step 7: Assign wo.qty = 50

```python
wo.qty = 50
```

### Step 8: Assign wo.wip_warehouse = '_Test Warehouse 1 - _TC'

```python
wo.wip_warehouse = '_Test Warehouse 1 - _TC'
```

### Step 9: Call wo.submit()

```python
wo.submit()
```

### Step 10: Assign requested_qty = self._get_requested_qty(...)

```python
requested_qty = self._get_requested_qty('_Test FG Item', '_Test Warehouse - _TC')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(requested_qty, existing_requested_qty + 70)
```

### Step 12: Call wo.cancel()

```python
wo.cancel()
```

### Step 13: Assign requested_qty = self._get_requested_qty(...)

```python
requested_qty = self._get_requested_qty('_Test FG Item', '_Test Warehouse - _TC')
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(requested_qty, existing_requested_qty + 120)
```

### Step 15: Call mr.reload()

```python
mr.reload()
```

### Step 16: Call mr.cancel()

```python
mr.cancel()
```

### Step 17: Assign requested_qty = self._get_requested_qty(...)

```python
requested_qty = self._get_requested_qty('_Test FG Item', '_Test Warehouse - _TC')
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(requested_qty, existing_requested_qty)
```


## Complete Example

```python
# Workflow
existing_requested_qty = self._get_requested_qty('_Test FG Item', '_Test Warehouse - _TC')
mr = make_material_request(item_code='_Test FG Item', material_request_type='Manufacture', uom='_Test UOM 1', conversion_factor=12)
requested_qty = self._get_requested_qty('_Test FG Item', '_Test Warehouse - _TC')
self.assertEqual(requested_qty, existing_requested_qty + 120)
work_order = raise_work_orders(mr.name, mr.company)
wo = frappe.get_doc('Work Order', work_order[0])
wo.qty = 50
wo.wip_warehouse = '_Test Warehouse 1 - _TC'
wo.submit()
requested_qty = self._get_requested_qty('_Test FG Item', '_Test Warehouse - _TC')
self.assertEqual(requested_qty, existing_requested_qty + 70)
wo.cancel()
requested_qty = self._get_requested_qty('_Test FG Item', '_Test Warehouse - _TC')
self.assertEqual(requested_qty, existing_requested_qty + 120)
mr.reload()
mr.cancel()
requested_qty = self._get_requested_qty('_Test FG Item', '_Test Warehouse - _TC')
self.assertEqual(requested_qty, existing_requested_qty)
```

## Next Steps


---

*Source: test_material_request.py:778 | Complexity: Advanced | Last updated: 2026-02-04*