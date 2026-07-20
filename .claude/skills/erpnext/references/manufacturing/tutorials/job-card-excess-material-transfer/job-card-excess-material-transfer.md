# How To: Job Card Excess Material Transfer

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test transferring more than required RM against Job Card.

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

### Step 1: 'Test transferring more than required RM against Job Card.'

```python
'Test transferring more than required RM against Job Card.'
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

### Step 5: Assign job_card = frappe.get_last_doc(...)

```python
job_card = frappe.get_last_doc('Job Card', {'work_order': self.work_order.name})
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(job_card.status, 'Open')
```

### Step 7: Assign transfer_entry_1 = make_stock_entry_from_jc(...)

```python
transfer_entry_1 = make_stock_entry_from_jc(job_card.name)
```

### Step 8: Call transfer_entry_1.insert()

```python
transfer_entry_1.insert()
```

### Step 9: Call transfer_entry_1.submit()

```python
transfer_entry_1.submit()
```

### Step 10: Assign transfer_entry_2 = make_stock_entry_from_jc(...)

```python
transfer_entry_2 = make_stock_entry_from_jc(job_card.name)
```

### Step 11: Assign transfer_entry_2.fg_completed_qty = 1

```python
transfer_entry_2.fg_completed_qty = 1
```

### Step 12: Assign unknown.qty = 5

```python
transfer_entry_2.items[0].qty = 5
```

### Step 13: Assign unknown.qty = 3

```python
transfer_entry_2.items[1].qty = 3
```

### Step 14: Call transfer_entry_2.insert()

```python
transfer_entry_2.insert()
```

### Step 15: Call transfer_entry_2.submit()

```python
transfer_entry_2.submit()
```

### Step 16: Call job_card.reload()

```python
job_card.reload()
```

### Step 17: Call self.assertGreater()

```python
self.assertGreater(job_card.transferred_qty, job_card.for_quantity)
```

### Step 18: Assign transfer_entry_3 = make_stock_entry_from_jc(...)

```python
transfer_entry_3 = make_stock_entry_from_jc(job_card.name)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(transfer_entry_3.fg_completed_qty, 0)
```

### Step 20: Call job_card.append()

```python
job_card.append('time_logs', {'from_time': '2021-01-01 00:01:00', 'to_time': '2021-01-01 06:00:00', 'completed_qty': 2})
```

### Step 21: Call job_card.save()

```python
job_card.save()
```

### Step 22: Call job_card.submit()

```python
job_card.submit()
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(job_card.status, 'Completed')
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
'Test transferring more than required RM against Job Card.'
self.transfer_material_against = 'Job Card'
self.source_warehouse = 'Stores - _TC'
self.generate_required_stock(self.work_order)
job_card = frappe.get_last_doc('Job Card', {'work_order': self.work_order.name})
self.assertEqual(job_card.status, 'Open')
transfer_entry_1 = make_stock_entry_from_jc(job_card.name)
transfer_entry_1.insert()
transfer_entry_1.submit()
transfer_entry_2 = make_stock_entry_from_jc(job_card.name)
transfer_entry_2.fg_completed_qty = 1
transfer_entry_2.items[0].qty = 5
transfer_entry_2.items[1].qty = 3
transfer_entry_2.insert()
transfer_entry_2.submit()
job_card.reload()
self.assertGreater(job_card.transferred_qty, job_card.for_quantity)
transfer_entry_3 = make_stock_entry_from_jc(job_card.name)
self.assertEqual(transfer_entry_3.fg_completed_qty, 0)
job_card.append('time_logs', {'from_time': '2021-01-01 00:01:00', 'to_time': '2021-01-01 06:00:00', 'completed_qty': 2})
job_card.save()
job_card.submit()
self.assertEqual(job_card.status, 'Completed')
```

## Next Steps


---

*Source: test_job_card.py:225 | Complexity: Advanced | Last updated: 2026-02-04*