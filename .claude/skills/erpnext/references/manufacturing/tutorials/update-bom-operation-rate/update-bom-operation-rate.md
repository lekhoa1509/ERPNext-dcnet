# How To: Update Bom Operation Rate

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test update bom operation rate

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `erpnext.manufacturing.doctype.operation.test_operation`
- `erpnext.manufacturing.doctype.routing.test_routing`
- `erpnext.manufacturing.doctype.workstation.workstation`


## Step-by-Step Guide

### Step 1: Assign operations = value

```python
operations = [{'operation': 'Test Operation A', 'workstation': '_Test Workstation A', 'hour_rate_rent': 300, 'time_in_mins': 60}, {'operation': 'Test Operation B', 'workstation': '_Test Workstation B', 'hour_rate_rent': 1000, 'time_in_mins': 60}]
```

### Step 2: Assign test_routing_operations = value

```python
test_routing_operations = [{'operation': 'Test Operation A', 'workstation': '_Test Workstation A', 'time_in_mins': 60}, {'operation': 'Test Operation B', 'workstation': '_Test Workstation A', 'time_in_mins': 60}]
```

### Step 3: Assign routing_doc = create_routing(...)

```python
routing_doc = create_routing(routing_name='Routing Test', operations=test_routing_operations)
```

### Step 4: Assign bom_doc = setup_bom(...)

```python
bom_doc = setup_bom(item_code='_Testing Item', routing=routing_doc.name, currency='INR')
```

### Step 5: Assign w1 = frappe.get_doc(...)

```python
w1 = frappe.get_doc('Workstation', '_Test Workstation A')
```

### Step 6: Call w1.save()

```python
w1.save()
```

### Step 7: Call bom_doc.update_cost()

```python
bom_doc.update_cost()
```

### Step 8: Call bom_doc.reload()

```python
bom_doc.reload()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(w1.hour_rate, 300)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(bom_doc.operations[0].hour_rate, 300)
```

### Step 11: Call w1.save()

```python
w1.save()
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
self.assertEqual(w1.hour_rate, 250)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(bom_doc.operations[0].hour_rate, 250)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(bom_doc.operations[1].hour_rate, 250)
```

### Step 17: Call make_workstation()

```python
make_workstation(row)
```

### Step 18: Call make_operation()

```python
make_operation(row)
```

### Step 19: Assign row.operating_cost = 300

```python
row.operating_cost = 300
```

### Step 20: Assign row.operating_cost = 250

```python
row.operating_cost = 250
```


## Complete Example

```python
# Workflow
operations = [{'operation': 'Test Operation A', 'workstation': '_Test Workstation A', 'hour_rate_rent': 300, 'time_in_mins': 60}, {'operation': 'Test Operation B', 'workstation': '_Test Workstation B', 'hour_rate_rent': 1000, 'time_in_mins': 60}]
for row in operations:
    make_workstation(row)
    make_operation(row)
test_routing_operations = [{'operation': 'Test Operation A', 'workstation': '_Test Workstation A', 'time_in_mins': 60}, {'operation': 'Test Operation B', 'workstation': '_Test Workstation A', 'time_in_mins': 60}]
routing_doc = create_routing(routing_name='Routing Test', operations=test_routing_operations)
bom_doc = setup_bom(item_code='_Testing Item', routing=routing_doc.name, currency='INR')
w1 = frappe.get_doc('Workstation', '_Test Workstation A')
for row in w1.workstation_costs:
    if row.operating_component == _('Rent'):
        row.operating_cost = 300
        break
w1.save()
bom_doc.update_cost()
bom_doc.reload()
self.assertEqual(w1.hour_rate, 300)
self.assertEqual(bom_doc.operations[0].hour_rate, 300)
for row in w1.workstation_costs:
    if row.operating_component == _('Rent'):
        row.operating_cost = 250
        break
w1.save()
bom_doc.update_cost()
bom_doc.reload()
self.assertEqual(w1.hour_rate, 250)
self.assertEqual(bom_doc.operations[0].hour_rate, 250)
self.assertEqual(bom_doc.operations[1].hour_rate, 250)
```

## Next Steps


---

*Source: test_workstation.py:51 | Complexity: Advanced | Last updated: 2026-02-04*