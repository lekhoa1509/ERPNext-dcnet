# How To: Over Transfer Qty Allowance

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test over transfer qty allowance

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

### Step 1: Assign mr = frappe.new_doc(...)

```python
mr = frappe.new_doc('Material Request')
```

### Step 2: Assign mr.company = '_Test Company'

```python
mr.company = '_Test Company'
```

### Step 3: Assign mr.scheduled_date = today(...)

```python
mr.scheduled_date = today()
```

### Step 4: Call mr.append()

```python
mr.append('items', {'item_code': '_Test FG Item', 'item_name': '_Test FG Item', 'qty': 10, 'schedule_date': today(), 'uom': '_Test UOM 1', 'warehouse': '_Test Warehouse - _TC'})
```

### Step 5: Assign mr.material_request_type = 'Material Transfer'

```python
mr.material_request_type = 'Material Transfer'
```

### Step 6: Call mr.insert()

```python
mr.insert()
```

### Step 7: Call mr.submit()

```python
mr.submit()
```

### Step 8: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Stock Settings', 'mr_qty_allowance', 20)
```

### Step 9: Assign se_doc = make_stock_entry(...)

```python
se_doc = make_stock_entry(mr.name)
```

### Step 10: Call se_doc.update()

```python
se_doc.update({'posting_date': today(), 'posting_time': '00:00'})
```

### Step 11: Call unknown.update()

```python
se_doc.get('items')[0].update({'qty': 13, 'transfer_qty': 12.0, 's_warehouse': '_Test Warehouse - _TC', 't_warehouse': '_Test Warehouse 1 - _TC', 'basic_rate': 1.0})
```

### Step 12: Assign sr = frappe.new_doc(...)

```python
sr = frappe.new_doc('Stock Reconciliation')
```

### Step 13: Assign sr.company = '_Test Company'

```python
sr.company = '_Test Company'
```

### Step 14: Assign sr.purpose = 'Opening Stock'

```python
sr.purpose = 'Opening Stock'
```

### Step 15: Call sr.append()

```python
sr.append('items', {'item_code': '_Test FG Item', 'warehouse': '_Test Warehouse - _TC', 'qty': 20, 'valuation_rate': 0.01})
```

### Step 16: Call sr.insert()

```python
sr.insert()
```

### Step 17: Call sr.submit()

```python
sr.submit()
```

### Step 18: Assign se = frappe.copy_doc(...)

```python
se = frappe.copy_doc(se_doc)
```

### Step 19: Call se.insert()

```python
se.insert()
```

### Step 20: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError)
```

### Step 21: Assign unknown.qty = 12

```python
se.items[0].qty = 12
```

### Step 22: Call se.submit()

```python
se.submit()
```


## Complete Example

```python
# Workflow
mr = frappe.new_doc('Material Request')
mr.company = '_Test Company'
mr.scheduled_date = today()
mr.append('items', {'item_code': '_Test FG Item', 'item_name': '_Test FG Item', 'qty': 10, 'schedule_date': today(), 'uom': '_Test UOM 1', 'warehouse': '_Test Warehouse - _TC'})
mr.material_request_type = 'Material Transfer'
mr.insert()
mr.submit()
frappe.db.set_single_value('Stock Settings', 'mr_qty_allowance', 20)
se_doc = make_stock_entry(mr.name)
se_doc.update({'posting_date': today(), 'posting_time': '00:00'})
se_doc.get('items')[0].update({'qty': 13, 'transfer_qty': 12.0, 's_warehouse': '_Test Warehouse - _TC', 't_warehouse': '_Test Warehouse 1 - _TC', 'basic_rate': 1.0})
sr = frappe.new_doc('Stock Reconciliation')
sr.company = '_Test Company'
sr.purpose = 'Opening Stock'
sr.append('items', {'item_code': '_Test FG Item', 'warehouse': '_Test Warehouse - _TC', 'qty': 20, 'valuation_rate': 0.01})
sr.insert()
sr.submit()
se = frappe.copy_doc(se_doc)
se.insert()
self.assertRaises(frappe.ValidationError)
se.items[0].qty = 12
se.submit()
```

## Next Steps


---

*Source: test_material_request.py:484 | Complexity: Advanced | Last updated: 2026-02-04*