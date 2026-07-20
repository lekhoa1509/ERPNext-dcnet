# How To: Completed Qty For Issue

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test completed qty for issue

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

### Step 1: Assign existing_requested_qty = _get_requested_qty(...)

```python
existing_requested_qty = _get_requested_qty()
```

### Step 2: Assign mr = frappe.copy_doc(...)

```python
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][0])
```

### Step 3: Assign mr.material_request_type = 'Material Issue'

```python
mr.material_request_type = 'Material Issue'
```

### Step 4: Call mr.submit()

```python
mr.submit()
```

### Step 5: Call frappe.db.value_cache.clear()

```python
frappe.db.value_cache.clear()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(_get_requested_qty(), existing_requested_qty - 54.0)
```

### Step 7: Call self._insert_stock_entry()

```python
self._insert_stock_entry(60, 6, '_Test Warehouse - _TC')
```

### Step 8: Assign se_doc = make_stock_entry(...)

```python
se_doc = make_stock_entry(mr.name)
```

### Step 9: Assign se_doc.fiscal_year = '_Test Fiscal Year 2014'

```python
se_doc.fiscal_year = '_Test Fiscal Year 2014'
```

### Step 10: Assign unknown.qty = 54.0

```python
se_doc.get('items')[0].qty = 54.0
```

### Step 11: Call se_doc.insert()

```python
se_doc.insert()
```

### Step 12: Call se_doc.submit()

```python
se_doc.submit()
```

### Step 13: Call mr.load_from_db()

```python
mr.load_from_db()
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(mr.get('items')[0].ordered_qty, 54.0)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(mr.get('items')[1].ordered_qty, 3.0)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(_get_requested_qty(), existing_requested_qty)
```


## Complete Example

```python
# Workflow
def _get_requested_qty():
    return flt(frappe.db.get_value('Bin', {'item_code': '_Test Item Home Desktop 100', 'warehouse': '_Test Warehouse - _TC'}, 'indented_qty'))
existing_requested_qty = _get_requested_qty()
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][0])
mr.material_request_type = 'Material Issue'
mr.submit()
frappe.db.value_cache.clear()
self.assertEqual(_get_requested_qty(), existing_requested_qty - 54.0)
self._insert_stock_entry(60, 6, '_Test Warehouse - _TC')
se_doc = make_stock_entry(mr.name)
se_doc.fiscal_year = '_Test Fiscal Year 2014'
se_doc.get('items')[0].qty = 54.0
se_doc.insert()
se_doc.submit()
mr.load_from_db()
self.assertEqual(mr.get('items')[0].ordered_qty, 54.0)
self.assertEqual(mr.get('items')[1].ordered_qty, 3.0)
self.assertEqual(_get_requested_qty(), existing_requested_qty)
```

## Next Steps


---

*Source: test_material_request.py:700 | Complexity: Advanced | Last updated: 2026-02-04*