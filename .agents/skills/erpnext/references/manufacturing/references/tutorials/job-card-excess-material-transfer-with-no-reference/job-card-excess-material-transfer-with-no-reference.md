# How To: Job Card Excess Material Transfer With No Reference

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test job card excess material transfer with no reference

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `typing`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.data`
- `erpnext.manufacturing.doctype.job_card.job_card`
- `erpnext.manufacturing.doctype.job_card.job_card`
- `erpnext.manufacturing.doctype.work_order.test_work_order`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.manufacturing.doctype.workstation.test_workstation`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.tests.utils`
- `erpnext.manufacturing.doctype.operation.test_operation`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.stock.doctype.material_request.material_request`
- `erpnext.manufacturing.doctype.routing.test_routing`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.manufacturing.doctype.routing.test_routing`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.manufacturing.doctype.work_order.work_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.warehouse.test_warehouse`

**Setup Required:**
```python
self.make_employees()
self.make_bom_for_jc_tests()
self.transfer_material_against: Literal['Work Order', 'Job Card'] = 'Work Order'
self.source_warehouse = None
self._work_order = None
```

## Step-by-Step Guide

### Step 1: Assign self.transfer_material_against = 'Job Card'

```python
self.transfer_material_against = 'Job Card'
```

### Step 2: Assign self.source_warehouse = 'Stores - _TC'

```python
self.source_warehouse = 'Stores - _TC'
```

### Step 3: Call self.generate_required_stock()

```python
self.generate_required_stock(self.work_order)
```

### Step 4: Assign job_card_name = frappe.db.get_value(...)

```python
job_card_name = frappe.db.get_value('Job Card', {'work_order': self.work_order.name})
```

### Step 5: Assign transfer_entry_1 = make_stock_entry_from_jc(...)

```python
transfer_entry_1 = make_stock_entry_from_jc(job_card_name)
```

### Step 6: Assign row = value

```python
row = transfer_entry_1.items[0]
```

### Step 7: Call transfer_entry_1.append()

```python
transfer_entry_1.append('items', {'item_code': row.item_code, 'item_name': row.item_name, 'item_group': row.item_group, 'qty': row.qty, 'uom': row.uom, 'conversion_factor': row.conversion_factor, 'stock_uom': row.stock_uom, 'basic_rate': row.basic_rate, 'basic_amount': row.basic_amount, 'expense_account': row.expense_account, 'cost_center': row.cost_center, 's_warehouse': row.s_warehouse, 't_warehouse': row.t_warehouse})
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, transfer_entry_1.insert)
```


## Complete Example

```python
# Setup
self.make_employees()
self.make_bom_for_jc_tests()
self.transfer_material_against: Literal['Work Order', 'Job Card'] = 'Work Order'
self.source_warehouse = None
self._work_order = None

# Workflow
self.transfer_material_against = 'Job Card'
self.source_warehouse = 'Stores - _TC'
self.generate_required_stock(self.work_order)
job_card_name = frappe.db.get_value('Job Card', {'work_order': self.work_order.name})
transfer_entry_1 = make_stock_entry_from_jc(job_card_name)
row = transfer_entry_1.items[0]
transfer_entry_1.append('items', {'item_code': row.item_code, 'item_name': row.item_name, 'item_group': row.item_group, 'qty': row.qty, 'uom': row.uom, 'conversion_factor': row.conversion_factor, 'stock_uom': row.stock_uom, 'basic_rate': row.basic_rate, 'basic_amount': row.basic_amount, 'expense_account': row.expense_account, 'cost_center': row.cost_center, 's_warehouse': row.s_warehouse, 't_warehouse': row.t_warehouse})
self.assertRaises(frappe.ValidationError, transfer_entry_1.insert)
```

## Next Steps


---

*Source: test_job_card.py:291 | Complexity: Advanced | Last updated: 2026-02-04*