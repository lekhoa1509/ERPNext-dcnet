# How To: Partial Make Stock Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test partial make stock entry

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

### Step 2: Assign source_wh = create_warehouse(...)

```python
source_wh = create_warehouse(warehouse_name='_Test Source Warehouse', properties={'parent_warehouse': 'All Warehouses - _TC'}, company='_Test Company')
```

### Step 3: Assign mr = frappe.get_doc(...)

```python
mr = frappe.get_doc('Material Request', mr.name)
```

### Step 4: Assign mr.material_request_type = 'Material Transfer'

```python
mr.material_request_type = 'Material Transfer'
```

### Step 5: Call mr.save()

```python
mr.save()
```

### Step 6: Call mr.submit()

```python
mr.submit()
```

### Step 7: Assign se = make_stock_entry(...)

```python
se = make_stock_entry(mr.name)
```

### Step 8: Assign unknown.qty = 5

```python
se.get('items')[0].qty = 5
```

### Step 9: Call se.insert()

```python
se.insert()
```

### Step 10: Call se.submit()

```python
se.submit()
```

### Step 11: Call mr.reload()

```python
mr.reload()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(mr.status, 'Partially Received')
```

### Step 13: Call _make_stock_entry()

```python
_make_stock_entry(item_code=row.item_code, qty=10, to_warehouse=source_wh, company='_Test Company', rate=100)
```

### Step 14: Assign row.from_warehouse = source_wh

```python
row.from_warehouse = source_wh
```

### Step 15: Assign row.qty = 10

```python
row.qty = 10
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry as _make_stock_entry
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][0]).insert()
source_wh = create_warehouse(warehouse_name='_Test Source Warehouse', properties={'parent_warehouse': 'All Warehouses - _TC'}, company='_Test Company')
mr = frappe.get_doc('Material Request', mr.name)
mr.material_request_type = 'Material Transfer'
for row in mr.items:
    _make_stock_entry(item_code=row.item_code, qty=10, to_warehouse=source_wh, company='_Test Company', rate=100)
    row.from_warehouse = source_wh
    row.qty = 10
mr.save()
mr.submit()
se = make_stock_entry(mr.name)
se.get('items')[0].qty = 5
se.insert()
se.submit()
mr.reload()
self.assertEqual(mr.status, 'Partially Received')
```

## Next Steps


---

*Source: test_material_request.py:126 | Complexity: Advanced | Last updated: 2026-02-04*