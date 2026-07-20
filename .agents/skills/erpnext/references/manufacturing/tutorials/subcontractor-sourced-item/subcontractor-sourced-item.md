# How To: Subcontractor Sourced Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test subcontractor sourced item

## Prerequisites

**Required Modules:**
- `collections`
- `functools`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.controllers.tests.test_subcontracting_controller`
- `erpnext.manufacturing.doctype.bom.bom`
- `erpnext.manufacturing.doctype.bom_update_log.test_bom_update_log`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.manufacturing.doctype.bom.bom`
- `erpnext.manufacturing.doctype.bom.bom`
- `erpnext.manufacturing.doctype.bom.bom`
- `erpnext.controllers.tests.test_subcontracting_controller`
- `erpnext.controllers.item_variant`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.doctype.bom.bom`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`


## Step-by-Step Guide

### Step 1: Assign item_code = '_Test Subcontracted FG Item 1'

```python
item_code = '_Test Subcontracted FG Item 1'
```

### Step 2: Call set_backflush_based_on()

```python
set_backflush_based_on('Material Transferred for Subcontract')
```

### Step 3: Assign bom = frappe.get_doc(...)

```python
bom = frappe.get_doc({'doctype': 'BOM', 'is_default': 1, 'item': item_code, 'currency': 'USD', 'quantity': 1, 'company': '_Test Company'})
```

### Step 4: Call bom.append()

```python
bom.append('items', {'item_code': 'Test Extra Item 3', 'qty': 1, 'uom': item_doc.stock_uom, 'stock_uom': item_doc.stock_uom, 'rate': 0, 'sourced_by_supplier': 1})
```

### Step 5: Call bom.insert()

```python
bom.insert(ignore_permissions=True)
```

### Step 6: Call bom.update_cost()

```python
bom.update_cost()
```

### Step 7: Call bom.submit()

```python
bom.submit()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(bom.items[2].rate, 0)
```

### Step 9: Call make_service_item()

```python
make_service_item('Subcontracted Service Item 1')
```

### Step 10: Assign service_items = value

```python
service_items = [{'warehouse': '_Test Warehouse - _TC', 'item_code': 'Subcontracted Service Item 1', 'qty': 1, 'rate': 100, 'fg_item': item_code, 'fg_item_qty': 1}]
```

### Step 11: Assign sco = get_subcontracting_order(...)

```python
sco = get_subcontracting_order(service_items=service_items, supplier_warehouse='_Test Warehouse 1 - _TC')
```

### Step 12: Assign bom_items = sorted(...)

```python
bom_items = sorted([d.item_code for d in bom.items if d.sourced_by_supplier != 1])
```

### Step 13: Assign supplied_items = sorted(...)

```python
supplied_items = sorted([d.rm_item_code for d in sco.supplied_items])
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(bom_items, supplied_items)
```

### Step 15: Call make_item()

```python
make_item(item_code, {'is_stock_item': 1, 'is_sub_contracted_item': 1, 'stock_uom': 'Nos'})
```

### Step 16: Call make_item()

```python
make_item('Test Extra Item 1', {'is_stock_item': 1, 'stock_uom': 'Nos'})
```

### Step 17: Call make_item()

```python
make_item('Test Extra Item 2', {'is_stock_item': 1, 'stock_uom': 'Nos'})
```

### Step 18: Call make_item()

```python
make_item('Test Extra Item 3', {'is_stock_item': 1, 'stock_uom': 'Nos'})
```

### Step 19: Assign item_doc = frappe.get_doc(...)

```python
item_doc = frappe.get_doc('Item', item)
```

### Step 20: Call bom.append()

```python
bom.append('items', {'item_code': item, 'qty': 1, 'uom': item_doc.stock_uom, 'stock_uom': item_doc.stock_uom, 'rate': item_doc.valuation_rate})
```


## Complete Example

```python
# Workflow
item_code = '_Test Subcontracted FG Item 1'
set_backflush_based_on('Material Transferred for Subcontract')
if not frappe.db.exists('Item', item_code):
    make_item(item_code, {'is_stock_item': 1, 'is_sub_contracted_item': 1, 'stock_uom': 'Nos'})
if not frappe.db.exists('Item', 'Test Extra Item 1'):
    make_item('Test Extra Item 1', {'is_stock_item': 1, 'stock_uom': 'Nos'})
if not frappe.db.exists('Item', 'Test Extra Item 2'):
    make_item('Test Extra Item 2', {'is_stock_item': 1, 'stock_uom': 'Nos'})
if not frappe.db.exists('Item', 'Test Extra Item 3'):
    make_item('Test Extra Item 3', {'is_stock_item': 1, 'stock_uom': 'Nos'})
bom = frappe.get_doc({'doctype': 'BOM', 'is_default': 1, 'item': item_code, 'currency': 'USD', 'quantity': 1, 'company': '_Test Company'})
for item in ['Test Extra Item 1', 'Test Extra Item 2']:
    item_doc = frappe.get_doc('Item', item)
    bom.append('items', {'item_code': item, 'qty': 1, 'uom': item_doc.stock_uom, 'stock_uom': item_doc.stock_uom, 'rate': item_doc.valuation_rate})
bom.append('items', {'item_code': 'Test Extra Item 3', 'qty': 1, 'uom': item_doc.stock_uom, 'stock_uom': item_doc.stock_uom, 'rate': 0, 'sourced_by_supplier': 1})
bom.insert(ignore_permissions=True)
bom.update_cost()
bom.submit()
self.assertEqual(bom.items[2].rate, 0)
from erpnext.controllers.tests.test_subcontracting_controller import get_subcontracting_order, make_service_item
make_service_item('Subcontracted Service Item 1')
service_items = [{'warehouse': '_Test Warehouse - _TC', 'item_code': 'Subcontracted Service Item 1', 'qty': 1, 'rate': 100, 'fg_item': item_code, 'fg_item_qty': 1}]
sco = get_subcontracting_order(service_items=service_items, supplier_warehouse='_Test Warehouse 1 - _TC')
bom_items = sorted([d.item_code for d in bom.items if d.sourced_by_supplier != 1])
supplied_items = sorted([d.rm_item_code for d in sco.supplied_items])
self.assertEqual(bom_items, supplied_items)
```

## Next Steps


---

*Source: test_bom.py:239 | Complexity: Advanced | Last updated: 2026-02-04*