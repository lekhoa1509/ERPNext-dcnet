# How To: Incorrect Mapping Of Stock Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test incorrect mapping of stock entry

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

### Step 1: Assign mr = frappe.copy_doc(...)

```python
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][0])
```

### Step 2: Assign mr.material_request_type = 'Material Transfer'

```python
mr.material_request_type = 'Material Transfer'
```

### Step 3: Call mr.insert()

```python
mr.insert()
```

### Step 4: Call mr.submit()

```python
mr.submit()
```

### Step 5: Assign se_doc = make_stock_entry(...)

```python
se_doc = make_stock_entry(mr.name)
```

### Step 6: Call se_doc.update()

```python
se_doc.update({'posting_date': '2013-03-01', 'posting_time': '00:00', 'fiscal_year': '_Test Fiscal Year 2013'})
```

### Step 7: Call unknown.update()

```python
se_doc.get('items')[0].update({'qty': 60.0, 'transfer_qty': 60.0, 's_warehouse': '_Test Warehouse - _TC', 't_warehouse': '_Test Warehouse 1 - _TC', 'basic_rate': 1.0})
```

### Step 8: Call unknown.update()

```python
se_doc.get('items')[1].update({'item_code': '_Test Item Home Desktop 100', 'qty': 3.0, 'transfer_qty': 3.0, 's_warehouse': '_Test Warehouse 1 - _TC', 'basic_rate': 1.0})
```

### Step 9: Assign se = frappe.copy_doc(...)

```python
se = frappe.copy_doc(se_doc)
```

### Step 10: Call self.assertRaises()

```python
self.assertRaises(frappe.MappingMismatchError, se.insert)
```

### Step 11: Assign mr = frappe.copy_doc(...)

```python
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][0])
```

### Step 12: Assign mr.material_request_type = 'Material Issue'

```python
mr.material_request_type = 'Material Issue'
```

### Step 13: Call mr.insert()

```python
mr.insert()
```

### Step 14: Call mr.submit()

```python
mr.submit()
```

### Step 15: Assign se_doc = make_stock_entry(...)

```python
se_doc = make_stock_entry(mr.name)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(se_doc.get('items')[0].s_warehouse, '_Test Warehouse - _TC')
```


## Complete Example

```python
# Workflow
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][0])
mr.material_request_type = 'Material Transfer'
mr.insert()
mr.submit()
se_doc = make_stock_entry(mr.name)
se_doc.update({'posting_date': '2013-03-01', 'posting_time': '00:00', 'fiscal_year': '_Test Fiscal Year 2013'})
se_doc.get('items')[0].update({'qty': 60.0, 'transfer_qty': 60.0, 's_warehouse': '_Test Warehouse - _TC', 't_warehouse': '_Test Warehouse 1 - _TC', 'basic_rate': 1.0})
se_doc.get('items')[1].update({'item_code': '_Test Item Home Desktop 100', 'qty': 3.0, 'transfer_qty': 3.0, 's_warehouse': '_Test Warehouse 1 - _TC', 'basic_rate': 1.0})
se = frappe.copy_doc(se_doc)
self.assertRaises(frappe.MappingMismatchError, se.insert)
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][0])
mr.material_request_type = 'Material Issue'
mr.insert()
mr.submit()
se_doc = make_stock_entry(mr.name)
self.assertEqual(se_doc.get('items')[0].s_warehouse, '_Test Warehouse - _TC')
```

## Next Steps


---

*Source: test_material_request.py:628 | Complexity: Advanced | Last updated: 2026-02-04*