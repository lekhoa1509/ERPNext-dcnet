# How To: In Transit Make Stock Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test in transit make stock entry

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

### Step 2: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, make_stock_entry, mr.name)
```

### Step 3: Assign mr = frappe.get_doc(...)

```python
mr = frappe.get_doc('Material Request', mr.name)
```

### Step 4: Assign mr.material_request_type = 'Material Transfer'

```python
mr.material_request_type = 'Material Transfer'
```

### Step 5: Call mr.submit()

```python
mr.submit()
```

### Step 6: Assign in_transit_warehouse = get_in_transit_warehouse(...)

```python
in_transit_warehouse = get_in_transit_warehouse(mr.company)
```

### Step 7: Assign se = make_in_transit_stock_entry(...)

```python
se = make_in_transit_stock_entry(mr.name, in_transit_warehouse)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(se.stock_entry_type, 'Material Transfer')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(se.purpose, 'Material Transfer')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(se.doctype, 'Stock Entry')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(row.t_warehouse, in_transit_warehouse)
```


## Complete Example

```python
# Workflow
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][0]).insert()
self.assertRaises(frappe.ValidationError, make_stock_entry, mr.name)
mr = frappe.get_doc('Material Request', mr.name)
mr.material_request_type = 'Material Transfer'
mr.submit()
in_transit_warehouse = get_in_transit_warehouse(mr.company)
se = make_in_transit_stock_entry(mr.name, in_transit_warehouse)
self.assertEqual(se.stock_entry_type, 'Material Transfer')
self.assertEqual(se.purpose, 'Material Transfer')
self.assertEqual(se.doctype, 'Stock Entry')
for row in se.get('items'):
    self.assertEqual(row.t_warehouse, in_transit_warehouse)
```

## Next Steps


---

*Source: test_material_request.py:163 | Complexity: Advanced | Last updated: 2026-02-04*