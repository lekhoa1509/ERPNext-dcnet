# How To: Make Stock Entry

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test make stock entry

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

### Step 6: Assign se = make_stock_entry(...)

```python
se = make_stock_entry(mr.name)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(se.stock_entry_type, 'Material Transfer')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(se.purpose, 'Material Transfer')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(se.doctype, 'Stock Entry')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(len(se.get('items')), len(mr.get('items')))
```


## Complete Example

```python
# Workflow
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][0]).insert()
self.assertRaises(frappe.ValidationError, make_stock_entry, mr.name)
mr = frappe.get_doc('Material Request', mr.name)
mr.material_request_type = 'Material Transfer'
mr.submit()
se = make_stock_entry(mr.name)
self.assertEqual(se.stock_entry_type, 'Material Transfer')
self.assertEqual(se.purpose, 'Material Transfer')
self.assertEqual(se.doctype, 'Stock Entry')
self.assertEqual(len(se.get('items')), len(mr.get('items')))
```

## Next Steps


---

*Source: test_material_request.py:111 | Complexity: Advanced | Last updated: 2026-02-04*