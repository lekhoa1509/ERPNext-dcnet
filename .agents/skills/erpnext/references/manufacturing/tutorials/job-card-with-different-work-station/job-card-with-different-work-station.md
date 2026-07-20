# How To: Job Card With Different Work Station

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test job card with different work station

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

### Step 1: Assign job_cards = frappe.get_all(...)

```python
job_cards = frappe.get_all('Job Card', filters={'work_order': self.work_order.name}, fields=['operation_id', 'workstation', 'name', 'for_quantity'])
```

### Step 2: Assign job_card = value

```python
job_card = job_cards[0]
```

### Step 3: Assign workstation = frappe.db.get_value(...)

```python
workstation = frappe.db.get_value('Workstation', {'name': ('not in', [job_card.workstation])}, 'name')
```

### Step 4: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc('Job Card', job_card.name)
```

### Step 5: Assign doc.workstation = workstation

```python
doc.workstation = workstation
```

### Step 6: Call doc.append()

```python
doc.append('time_logs', {'from_time': '2009-01-01 12:06:25', 'to_time': '2009-01-01 12:37:25', 'time_in_mins': '31.00002', 'completed_qty': job_card.for_quantity})
```

### Step 7: Call doc.submit()

```python
doc.submit()
```

### Step 8: Assign completed_qty = frappe.db.get_value(...)

```python
completed_qty = frappe.db.get_value('Work Order Operation', job_card.operation_id, 'completed_qty')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(completed_qty, job_card.for_quantity)
```

### Step 10: Assign workstation = value

```python
workstation = make_workstation(workstation_name=random_string(5)).name
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
job_cards = frappe.get_all('Job Card', filters={'work_order': self.work_order.name}, fields=['operation_id', 'workstation', 'name', 'for_quantity'])
job_card = job_cards[0]
if job_card:
    workstation = frappe.db.get_value('Workstation', {'name': ('not in', [job_card.workstation])}, 'name')
    if not workstation or job_card.workstation == workstation:
        workstation = make_workstation(workstation_name=random_string(5)).name
    doc = frappe.get_doc('Job Card', job_card.name)
    doc.workstation = workstation
    doc.append('time_logs', {'from_time': '2009-01-01 12:06:25', 'to_time': '2009-01-01 12:37:25', 'time_in_mins': '31.00002', 'completed_qty': job_card.for_quantity})
    doc.submit()
    completed_qty = frappe.db.get_value('Work Order Operation', job_card.operation_id, 'completed_qty')
    self.assertEqual(completed_qty, job_card.for_quantity)
```

## Next Steps


---

*Source: test_job_card.py:89 | Complexity: Advanced | Last updated: 2026-02-04*