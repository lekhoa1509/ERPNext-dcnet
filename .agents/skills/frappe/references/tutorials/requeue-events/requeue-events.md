# How To: Requeue Events

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test requeueing events preserves order

## Prerequisites

**Required Modules:**
- `time`
- `unittest.mock`
- `frappe`
- `frappe.tests`
- `frappe.utils.telemetry.pulse.client`
- `frappe.utils.telemetry.pulse.utils`


## Step-by-Step Guide

### Step 1: 'Test requeueing events preserves order'

```python
'Test requeueing events preserves order'
```

### Step 2: Assign eq = EventQueue(...)

```python
eq = EventQueue()
```

### Step 3: Assign event_names = value

```python
event_names = ['event_1', 'event_2', 'event_3']
```

### Step 4: Assign events = eq.collect(...)

```python
events = eq.collect(batch_size=3)
```

### Step 5: Call eq._requeue_events()

```python
eq._requeue_events(events)
```

### Step 6: Assign requeued = eq.collect(...)

```python
requeued = eq.collect(batch_size=3)
```

### Step 7: Assign event = value

```python
event = {'event_name': name, 'captured_at': '2026-01-01T00:00:00', 'app': 'frappe', 'user': 'test@example.com', 'site': 'test.localhost', 'properties': {}}
```

### Step 8: Call eq.add()

```python
eq.add(event)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(event['event_name'], event_names[i])
```


## Complete Example

```python
# Workflow
'Test requeueing events preserves order'
eq = EventQueue()
event_names = ['event_1', 'event_2', 'event_3']
for name in event_names:
    event = {'event_name': name, 'captured_at': '2026-01-01T00:00:00', 'app': 'frappe', 'user': 'test@example.com', 'site': 'test.localhost', 'properties': {}}
    eq.add(event)
events = eq.collect(batch_size=3)
eq._requeue_events(events)
requeued = eq.collect(batch_size=3)
for i, event in enumerate(requeued):
    self.assertEqual(event['event_name'], event_names[i])
```

## Next Steps


---

*Source: test_pulse_client.py:73 | Complexity: Advanced | Last updated: 2026-02-04*