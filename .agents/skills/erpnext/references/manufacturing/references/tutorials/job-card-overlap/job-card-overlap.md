# How To: Job Card Overlap

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test job card overlap

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

### Step 1: Assign wo2 = make_wo_order_test_record(...)

```python
wo2 = make_wo_order_test_record(item='_Test FG Item 2', qty=2)
```

### Step 2: Assign jc1 = frappe.get_last_doc(...)

```python
jc1 = frappe.get_last_doc('Job Card', {'work_order': self.work_order.name})
```

### Step 3: Assign jc2 = frappe.get_last_doc(...)

```python
jc2 = frappe.get_last_doc('Job Card', {'work_order': wo2.name})
```

### Step 4: Assign employee = value

```python
employee = self.employees[0].name
```

### Step 5: Call jc1.append()

```python
jc1.append('time_logs', {'from_time': '2021-01-01 00:00:00', 'to_time': '2021-01-01 08:00:00', 'completed_qty': 1, 'employee': employee})
```

### Step 6: Call jc1.save()

```python
jc1.save()
```

### Step 7: Call jc2.append()

```python
jc2.append('time_logs', {'from_time': '2021-01-01 00:01:00', 'to_time': '2021-01-01 06:00:00', 'completed_qty': 1, 'employee': employee})
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(OverlapError, jc2.save)
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
wo2 = make_wo_order_test_record(item='_Test FG Item 2', qty=2)
jc1 = frappe.get_last_doc('Job Card', {'work_order': self.work_order.name})
jc2 = frappe.get_last_doc('Job Card', {'work_order': wo2.name})
employee = self.employees[0].name
jc1.append('time_logs', {'from_time': '2021-01-01 00:00:00', 'to_time': '2021-01-01 08:00:00', 'completed_qty': 1, 'employee': employee})
jc1.save()
jc2.append('time_logs', {'from_time': '2021-01-01 00:01:00', 'to_time': '2021-01-01 06:00:00', 'completed_qty': 1, 'employee': employee})
self.assertRaises(OverlapError, jc2.save)
```

## Next Steps


---

*Source: test_job_card.py:124 | Complexity: Advanced | Last updated: 2026-02-04*