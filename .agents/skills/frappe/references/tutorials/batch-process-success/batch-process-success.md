# How To: Batch Process Success

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test successful batch processing

## Prerequisites

**Required Modules:**
- `time`
- `unittest.mock`
- `frappe`
- `frappe.tests`
- `frappe.utils.telemetry.pulse.client`
- `frappe.utils.telemetry.pulse.utils`


## Step-by-Step Guide

### Step 1: 'Test successful batch processing'

```python
'Test successful batch processing'
```

### Step 2: Assign eq = EventQueue(...)

```python
eq = EventQueue()
```

### Step 3: Assign processed = value

```python
processed = []
```

### Step 4: Call eq.batch_process()

```python
eq.batch_process(process_fn, batch_size=10, max_batches=2)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(len(processed), 15)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(eq.length, 0)
```

### Step 7: Call processed.extend()

```python
processed.extend(events)
```

### Step 8: Assign event = value

```python
event = {'event_name': f'test_event_{i}', 'captured_at': '2026-01-01T00:00:00', 'app': 'frappe', 'user': 'test@example.com', 'site': 'test.localhost', 'properties': {}}
```

### Step 9: Call eq.add()

```python
eq.add(event)
```


## Complete Example

```python
# Workflow
'Test successful batch processing'
eq = EventQueue()
processed = []

def process_fn(events):
    processed.extend(events)
for i in range(15):
    event = {'event_name': f'test_event_{i}', 'captured_at': '2026-01-01T00:00:00', 'app': 'frappe', 'user': 'test@example.com', 'site': 'test.localhost', 'properties': {}}
    eq.add(event)
eq.batch_process(process_fn, batch_size=10, max_batches=2)
self.assertEqual(len(processed), 15)
self.assertEqual(eq.length, 0)
```

## Next Steps


---

*Source: test_pulse_client.py:175 | Complexity: Advanced | Last updated: 2026-02-04*