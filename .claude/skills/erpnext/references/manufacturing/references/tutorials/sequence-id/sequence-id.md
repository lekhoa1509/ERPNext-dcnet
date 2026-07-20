# How To: Sequence Id

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test sequence id

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.manufacturing.doctype.job_card.job_card`
- `erpnext.manufacturing.doctype.work_order.test_work_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.manufacturing.doctype.operation.test_operation`
- `erpnext.manufacturing.doctype.workstation.test_workstation`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`


## Step-by-Step Guide

### Step 1: Assign operations = value

```python
operations = [{'operation': 'Test Operation A', 'workstation': 'Test Workstation A', 'time_in_mins': 30}, {'operation': 'Test Operation B', 'workstation': 'Test Workstation A', 'time_in_mins': 20}]
```

### Step 2: Call setup_operations()

```python
setup_operations(operations)
```

### Step 3: Assign routing_doc = create_routing(...)

```python
routing_doc = create_routing(routing_name='Testing Route', operations=operations)
```

### Step 4: Assign bom_doc = setup_bom(...)

```python
bom_doc = setup_bom(item_code=self.item_code, routing=routing_doc.name)
```

### Step 5: Assign wo_doc = make_wo_order_test_record(...)

```python
wo_doc = make_wo_order_test_record(production_item=self.item_code, bom_no=bom_doc.name)
```

### Step 6: Call wo_doc.cancel()

```python
wo_doc.cancel()
```

### Step 7: Call wo_doc.delete()

```python
wo_doc.delete()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(row.sequence_id, row.idx)
```

### Step 9: Assign job_card_doc = frappe.get_doc(...)

```python
job_card_doc = frappe.get_doc('Job Card', data.name)
```

### Step 10: Assign unknown.completed_qty = 10

```python
job_card_doc.time_logs[0].completed_qty = 10
```

### Step 11: Call job_card_doc.append()

```python
job_card_doc.append('time_logs', {'from_time': row.from_time, 'to_time': row.to_time, 'time_in_mins': row.time_in_mins})
```

### Step 12: Call self.assertRaises()

```python
self.assertRaises(OperationSequenceError, job_card_doc.save)
```

### Step 13: Call job_card_doc.save()

```python
job_card_doc.save()
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(job_card_doc.total_completed_qty, 10)
```


## Complete Example

```python
# Workflow
operations = [{'operation': 'Test Operation A', 'workstation': 'Test Workstation A', 'time_in_mins': 30}, {'operation': 'Test Operation B', 'workstation': 'Test Workstation A', 'time_in_mins': 20}]
setup_operations(operations)
routing_doc = create_routing(routing_name='Testing Route', operations=operations)
bom_doc = setup_bom(item_code=self.item_code, routing=routing_doc.name)
wo_doc = make_wo_order_test_record(production_item=self.item_code, bom_no=bom_doc.name)
for row in routing_doc.operations:
    self.assertEqual(row.sequence_id, row.idx)
for data in frappe.get_all('Job Card', filters={'work_order': wo_doc.name}, order_by='sequence_id desc'):
    job_card_doc = frappe.get_doc('Job Card', data.name)
    for row in job_card_doc.scheduled_time_logs:
        job_card_doc.append('time_logs', {'from_time': row.from_time, 'to_time': row.to_time, 'time_in_mins': row.time_in_mins})
    job_card_doc.time_logs[0].completed_qty = 10
    if job_card_doc.sequence_id != 1:
        self.assertRaises(OperationSequenceError, job_card_doc.save)
    else:
        job_card_doc.save()
        self.assertEqual(job_card_doc.total_completed_qty, 10)
wo_doc.cancel()
wo_doc.delete()
```

## Next Steps


---

*Source: test_routing.py:23 | Complexity: Advanced | Last updated: 2026-02-04*