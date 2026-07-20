# How To: Alternative Item For Production Rm

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test alternative item for production rm

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.controllers.subcontracting_controller`
- `erpnext.controllers.tests.test_subcontracting_controller`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.manufacturing.doctype.work_order.test_work_order`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_reconciliation.stock_reconciliation`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.subcontracting.doctype.subcontracting_order.subcontracting_order`


## Step-by-Step Guide

### Step 1: Call create_stock_reconciliation()

```python
create_stock_reconciliation(item_code='Alternate Item For A RW 1', warehouse='_Test Warehouse - _TC', qty=5, rate=2000)
```

### Step 2: Call create_stock_reconciliation()

```python
create_stock_reconciliation(item_code='Test FG A RW 2', warehouse='_Test Warehouse - _TC', qty=5, rate=2000)
```

### Step 3: Assign pro_order = make_wo_order_test_record(...)

```python
pro_order = make_wo_order_test_record(production_item='Test Finished Goods - A', qty=5, source_warehouse='_Test Warehouse - _TC', wip_warehouse='Test Supplier Warehouse - _TC')
```

### Step 4: Assign reserved_qty_for_production = frappe.db.get_value(...)

```python
reserved_qty_for_production = frappe.db.get_value('Bin', {'item_code': 'Test FG A RW 1', 'warehouse': '_Test Warehouse - _TC'}, 'reserved_qty_for_production')
```

### Step 5: Assign ste = frappe.get_doc(...)

```python
ste = frappe.get_doc(make_stock_entry(pro_order.name, 'Material Transfer for Manufacture', 5))
```

### Step 6: Call ste.insert()

```python
ste.insert()
```

### Step 7: Call ste.submit()

```python
ste.submit()
```

### Step 8: Assign reserved_qty_for_production_after_transfer = frappe.db.get_value(...)

```python
reserved_qty_for_production_after_transfer = frappe.db.get_value('Bin', {'item_code': 'Test FG A RW 1', 'warehouse': '_Test Warehouse - _TC'}, 'reserved_qty_for_production')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(reserved_qty_for_production_after_transfer, flt(reserved_qty_for_production - 5))
```

### Step 10: Assign ste1 = frappe.get_doc(...)

```python
ste1 = frappe.get_doc(make_stock_entry(pro_order.name, 'Manufacture', 5))
```

### Step 11: Assign status = False

```python
status = False
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(status, True)
```

### Step 13: Call ste1.submit()

```python
ste1.submit()
```

### Step 14: Assign item.item_code = 'Alternate Item For A RW 1'

```python
item.item_code = 'Alternate Item For A RW 1'
```

### Step 15: Assign item.item_name = 'Alternate Item For A RW 1'

```python
item.item_name = 'Alternate Item For A RW 1'
```

### Step 16: Assign item.description = 'Alternate Item For A RW 1'

```python
item.description = 'Alternate Item For A RW 1'
```

### Step 17: Assign item.original_item = 'Test FG A RW 1'

```python
item.original_item = 'Test FG A RW 1'
```

### Step 18: Assign status = True

```python
status = True
```


## Complete Example

```python
# Workflow
create_stock_reconciliation(item_code='Alternate Item For A RW 1', warehouse='_Test Warehouse - _TC', qty=5, rate=2000)
create_stock_reconciliation(item_code='Test FG A RW 2', warehouse='_Test Warehouse - _TC', qty=5, rate=2000)
pro_order = make_wo_order_test_record(production_item='Test Finished Goods - A', qty=5, source_warehouse='_Test Warehouse - _TC', wip_warehouse='Test Supplier Warehouse - _TC')
reserved_qty_for_production = frappe.db.get_value('Bin', {'item_code': 'Test FG A RW 1', 'warehouse': '_Test Warehouse - _TC'}, 'reserved_qty_for_production')
ste = frappe.get_doc(make_stock_entry(pro_order.name, 'Material Transfer for Manufacture', 5))
ste.insert()
for item in ste.items:
    if item.item_code == 'Test FG A RW 1':
        item.item_code = 'Alternate Item For A RW 1'
        item.item_name = 'Alternate Item For A RW 1'
        item.description = 'Alternate Item For A RW 1'
        item.original_item = 'Test FG A RW 1'
ste.submit()
reserved_qty_for_production_after_transfer = frappe.db.get_value('Bin', {'item_code': 'Test FG A RW 1', 'warehouse': '_Test Warehouse - _TC'}, 'reserved_qty_for_production')
self.assertEqual(reserved_qty_for_production_after_transfer, flt(reserved_qty_for_production - 5))
ste1 = frappe.get_doc(make_stock_entry(pro_order.name, 'Manufacture', 5))
status = False
for d in ste1.items:
    if d.item_code == 'Alternate Item For A RW 1':
        status = True
self.assertEqual(status, True)
ste1.submit()
```

## Next Steps


---

*Source: test_item_alternative.py:121 | Complexity: Advanced | Last updated: 2026-02-04*