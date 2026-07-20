# How To: Delivery Trip Status Completed

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test delivery trip status completed

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext`
- `erpnext.stock.doctype.delivery_trip.delivery_trip`
- `erpnext.tests.utils`


## Step-by-Step Guide

### Step 1: Call self.delivery_trip.submit()

```python
self.delivery_trip.submit()
```

### Step 2: Call self.delivery_trip.save()

```python
self.delivery_trip.save()
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(self.delivery_trip.status, 'Completed')
```

### Step 4: Assign stop.visited = 1

```python
stop.visited = 1
```


## Complete Example

```python
# Workflow
self.delivery_trip.submit()
for stop in self.delivery_trip.delivery_stops:
    stop.visited = 1
self.delivery_trip.save()
self.assertEqual(self.delivery_trip.status, 'Completed')
```

## Next Steps


---

*Source: test_delivery_trip.py:94 | Complexity: Intermediate | Last updated: 2026-02-04*