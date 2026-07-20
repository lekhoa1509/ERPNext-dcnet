# How To: Job Card Overlap With Capacity

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test job card overlap with capacity

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

### Step 2: Assign workstation = value

```python
workstation = make_workstation(workstation_name=random_string(5)).name
```

### Step 3: Call frappe.db.set_value()

```python
frappe.db.set_value('Workstation', workstation, 'production_capacity', 1)
```

### Step 4: Assign jc1 = frappe.get_last_doc(...)

```python
jc1 = frappe.get_last_doc('Job Card', {'work_order': self.work_order.name})
```

### Step 5: Assign jc2 = frappe.get_last_doc(...)

```python
jc2 = frappe.get_last_doc('Job Card', {'work_order': wo2.name})
```

### Step 6: Assign jc1.workstation = workstation

```python
jc1.workstation = workstation
```

### Step 7: Call jc1.append()

```python
jc1.append('time_logs', {'from_time': '2021-01-01 00:00:00', 'to_time': '2021-01-01 08:00:00', 'completed_qty': 1})
```

### Step 8: Call jc1.save()

```python
jc1.save()
```

### Step 9: Assign jc2.workstation = workstation

```python
jc2.workstation = workstation
```

### Step 10: Call jc2.append()

```python
jc2.append('time_logs', {'from_time': '2021-01-01 00:01:00', 'to_time': '2021-01-01 06:00:00', 'completed_qty': 1})
```

### Step 11: Call self.assertRaises()

```python
self.assertRaises(OverlapError, jc2.save)
```

### Step 12: Call frappe.db.set_value()

```python
frappe.db.set_value('Workstation', workstation, 'production_capacity', 2)
```

### Step 13: Call jc2.load_from_db()

```python
jc2.load_from_db()
```

### Step 14: Assign jc2.workstation = workstation

```python
jc2.workstation = workstation
```

### Step 15: Call jc2.append()

```python
jc2.append('time_logs', {'from_time': '2021-01-01 00:01:00', 'to_time': '2021-01-01 06:00:00', 'completed_qty': 1})
```

### Step 16: Call jc2.save()

```python
jc2.save()
```

### Step 17: Call self.assertTrue()

```python
self.assertTrue(jc2.name)
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
workstation = make_workstation(workstation_name=random_string(5)).name
frappe.db.set_value('Workstation', workstation, 'production_capacity', 1)
jc1 = frappe.get_last_doc('Job Card', {'work_order': self.work_order.name})
jc2 = frappe.get_last_doc('Job Card', {'work_order': wo2.name})
jc1.workstation = workstation
jc1.append('time_logs', {'from_time': '2021-01-01 00:00:00', 'to_time': '2021-01-01 08:00:00', 'completed_qty': 1})
jc1.save()
jc2.workstation = workstation
jc2.append('time_logs', {'from_time': '2021-01-01 00:01:00', 'to_time': '2021-01-01 06:00:00', 'completed_qty': 1})
self.assertRaises(OverlapError, jc2.save)
frappe.db.set_value('Workstation', workstation, 'production_capacity', 2)
jc2.load_from_db()
jc2.workstation = workstation
jc2.append('time_logs', {'from_time': '2021-01-01 00:01:00', 'to_time': '2021-01-01 06:00:00', 'completed_qty': 1})
jc2.save()
self.assertTrue(jc2.name)
```

## Next Steps


---

*Source: test_job_card.py:155 | Complexity: Advanced | Last updated: 2026-02-04*