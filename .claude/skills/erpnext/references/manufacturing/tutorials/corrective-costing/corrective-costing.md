# How To: Corrective Costing

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test corrective costing

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

### Step 1: Assign job_card = frappe.get_last_doc(...)

```python
job_card = frappe.get_last_doc('Job Card', {'work_order': self.work_order.name})
```

### Step 2: Call job_card.append()

```python
job_card.append('time_logs', {'from_time': now(), 'to_time': add_to_date(now(), hours=1), 'completed_qty': 2})
```

### Step 3: Call job_card.submit()

```python
job_card.submit()
```

### Step 4: Call self.work_order.reload()

```python
self.work_order.reload()
```

### Step 5: Assign original_cost = value

```python
original_cost = self.work_order.total_operating_cost
```

### Step 6: Assign corrective_action = frappe.get_doc.insert(...)

```python
corrective_action = frappe.get_doc(doctype='Operation', is_corrective_operation=1, name=frappe.generate_hash()).insert()
```

### Step 7: Assign corrective_job_card = make_corrective_job_card(...)

```python
corrective_job_card = make_corrective_job_card(job_card.name, operation=corrective_action.name, for_operation=job_card.operation)
```

### Step 8: Assign corrective_job_card.hour_rate = 100

```python
corrective_job_card.hour_rate = 100
```

### Step 9: Call corrective_job_card.insert()

```python
corrective_job_card.insert()
```

### Step 10: Call corrective_job_card.append()

```python
corrective_job_card.append('time_logs', {'from_time': add_to_date(now(), hours=2), 'to_time': add_to_date(now(), hours=2, minutes=30), 'completed_qty': 2})
```

### Step 11: Call corrective_job_card.submit()

```python
corrective_job_card.submit()
```

### Step 12: Call self.work_order.reload()

```python
self.work_order.reload()
```

### Step 13: Assign cost_after_correction = value

```python
cost_after_correction = self.work_order.total_operating_cost
```

### Step 14: Call self.assertGreater()

```python
self.assertGreater(cost_after_correction, original_cost)
```

### Step 15: Call corrective_job_card.cancel()

```python
corrective_job_card.cancel()
```

### Step 16: Call self.work_order.reload()

```python
self.work_order.reload()
```

### Step 17: Assign cost_after_cancel = value

```python
cost_after_cancel = self.work_order.total_operating_cost
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(cost_after_cancel, original_cost)
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
job_card = frappe.get_last_doc('Job Card', {'work_order': self.work_order.name})
job_card.append('time_logs', {'from_time': now(), 'to_time': add_to_date(now(), hours=1), 'completed_qty': 2})
job_card.submit()
self.work_order.reload()
original_cost = self.work_order.total_operating_cost
corrective_action = frappe.get_doc(doctype='Operation', is_corrective_operation=1, name=frappe.generate_hash()).insert()
corrective_job_card = make_corrective_job_card(job_card.name, operation=corrective_action.name, for_operation=job_card.operation)
corrective_job_card.hour_rate = 100
corrective_job_card.insert()
corrective_job_card.append('time_logs', {'from_time': add_to_date(now(), hours=2), 'to_time': add_to_date(now(), hours=2, minutes=30), 'completed_qty': 2})
corrective_job_card.submit()
self.work_order.reload()
cost_after_correction = self.work_order.total_operating_cost
self.assertGreater(cost_after_correction, original_cost)
corrective_job_card.cancel()
self.work_order.reload()
cost_after_cancel = self.work_order.total_operating_cost
self.assertEqual(cost_after_cancel, original_cost)
```

## Next Steps


---

*Source: test_job_card.py:401 | Complexity: Advanced | Last updated: 2026-02-04*