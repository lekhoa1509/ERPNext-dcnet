# How To: Update Bom Operation Time

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Update cost shouldn't update routing times.

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

### Step 1: "Update cost shouldn't update routing times."

```python
"Update cost shouldn't update routing times."
```

### Step 2: Assign operations = value

```python
operations = [{'operation': 'Test Operation A', 'workstation': '_Test Workstation A', 'hour_rate_rent': 300, 'hour_rate_labour': 750, 'time_in_mins': 30}, {'operation': 'Test Operation B', 'workstation': '_Test Workstation B', 'hour_rate_labour': 200, 'hour_rate_rent': 1000, 'time_in_mins': 20}]
```

### Step 3: Assign test_routing_operations = value

```python
test_routing_operations = [{'operation': 'Test Operation A', 'workstation': '_Test Workstation A', 'time_in_mins': 30}, {'operation': 'Test Operation B', 'workstation': '_Test Workstation A', 'time_in_mins': 20}]
```

### Step 4: Call setup_operations()

```python
setup_operations(operations)
```

### Step 5: Assign routing_doc = create_routing(...)

```python
routing_doc = create_routing(routing_name='Routing Test', operations=test_routing_operations)
```

### Step 6: Assign bom_doc = setup_bom(...)

```python
bom_doc = setup_bom(item_code='_Testing Item', routing=routing_doc.name, currency='INR')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(routing_doc.operations[0].time_in_mins, 30)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(routing_doc.operations[1].time_in_mins, 20)
```

### Step 9: Assign unknown.time_in_mins = 90

```python
routing_doc.operations[0].time_in_mins = 90
```

### Step 10: Assign unknown.time_in_mins = 42.2

```python
routing_doc.operations[1].time_in_mins = 42.2
```

### Step 11: Call routing_doc.save()

```python
routing_doc.save()
```

### Step 12: Call bom_doc.update_cost()

```python
bom_doc.update_cost()
```

### Step 13: Call bom_doc.reload()

```python
bom_doc.reload()
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(bom_doc.operations[0].time_in_mins, 30)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(bom_doc.operations[1].time_in_mins, 20)
```


## Complete Example

```python
# Workflow
"Update cost shouldn't update routing times."
operations = [{'operation': 'Test Operation A', 'workstation': '_Test Workstation A', 'hour_rate_rent': 300, 'hour_rate_labour': 750, 'time_in_mins': 30}, {'operation': 'Test Operation B', 'workstation': '_Test Workstation B', 'hour_rate_labour': 200, 'hour_rate_rent': 1000, 'time_in_mins': 20}]
test_routing_operations = [{'operation': 'Test Operation A', 'workstation': '_Test Workstation A', 'time_in_mins': 30}, {'operation': 'Test Operation B', 'workstation': '_Test Workstation A', 'time_in_mins': 20}]
setup_operations(operations)
routing_doc = create_routing(routing_name='Routing Test', operations=test_routing_operations)
bom_doc = setup_bom(item_code='_Testing Item', routing=routing_doc.name, currency='INR')
self.assertEqual(routing_doc.operations[0].time_in_mins, 30)
self.assertEqual(routing_doc.operations[1].time_in_mins, 20)
routing_doc.operations[0].time_in_mins = 90
routing_doc.operations[1].time_in_mins = 42.2
routing_doc.save()
bom_doc.update_cost()
bom_doc.reload()
self.assertEqual(bom_doc.operations[0].time_in_mins, 30)
self.assertEqual(bom_doc.operations[1].time_in_mins, 20)
```

## Next Steps


---

*Source: test_routing.py:61 | Complexity: Advanced | Last updated: 2026-02-04*