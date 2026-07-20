# How To: Job Card Multiple Materials Transfer

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test transferring RMs separately against Job Card with multiple RMs.

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

### Step 1: 'Test transferring RMs separately against Job Card with multiple RMs.'

```python
'Test transferring RMs separately against Job Card with multiple RMs.'
```

### Step 2: Assign self.transfer_material_against = 'Job Card'

```python
self.transfer_material_against = 'Job Card'
```

### Step 3: Assign self.source_warehouse = 'Stores - _TC'

```python
self.source_warehouse = 'Stores - _TC'
```

### Step 4: Call self.generate_required_stock()

```python
self.generate_required_stock(self.work_order)
```

### Step 5: Assign job_card_name = frappe.db.get_value(...)

```python
job_card_name = frappe.db.get_value('Job Card', {'work_order': self.work_order.name})
```

### Step 6: Assign job_card = frappe.get_doc(...)

```python
job_card = frappe.get_doc('Job Card', job_card_name)
```

### Step 7: Assign transfer_entry_1 = make_stock_entry_from_jc(...)

```python
transfer_entry_1 = make_stock_entry_from_jc(job_card_name)
```

### Step 8: Call transfer_entry_1.insert()

```python
transfer_entry_1.insert()
```

### Step 9: Call transfer_entry_1.submit()

```python
transfer_entry_1.submit()
```

### Step 10: Call job_card.reload()

```python
job_card.reload()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(transfer_entry_1.fg_completed_qty, 2)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(job_card.transferred_qty, 2)
```

### Step 13: Assign transfer_entry_2 = make_stock_entry_from_jc(...)

```python
transfer_entry_2 = make_stock_entry_from_jc(job_card_name)
```

### Step 14: Call transfer_entry_2.insert()

```python
transfer_entry_2.insert()
```

### Step 15: Call transfer_entry_2.submit()

```python
transfer_entry_2.submit()
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(transfer_entry_2.fg_completed_qty, 0)
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
'Test transferring RMs separately against Job Card with multiple RMs.'
self.transfer_material_against = 'Job Card'
self.source_warehouse = 'Stores - _TC'
self.generate_required_stock(self.work_order)
job_card_name = frappe.db.get_value('Job Card', {'work_order': self.work_order.name})
job_card = frappe.get_doc('Job Card', job_card_name)
transfer_entry_1 = make_stock_entry_from_jc(job_card_name)
del transfer_entry_1.items[1]
transfer_entry_1.insert()
transfer_entry_1.submit()
job_card.reload()
self.assertEqual(transfer_entry_1.fg_completed_qty, 2)
self.assertEqual(job_card.transferred_qty, 2)
transfer_entry_2 = make_stock_entry_from_jc(job_card_name)
del transfer_entry_2.items[0]
transfer_entry_2.insert()
transfer_entry_2.submit()
self.assertEqual(transfer_entry_2.fg_completed_qty, 0)
```

## Next Steps


---

*Source: test_job_card.py:194 | Complexity: Advanced | Last updated: 2026-02-04*