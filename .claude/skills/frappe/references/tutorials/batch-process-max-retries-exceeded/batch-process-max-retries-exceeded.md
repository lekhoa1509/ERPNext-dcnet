# How To: Batch Process Max Retries Exceeded

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test batch processing when max retries is exceeded

## Prerequisites

**Required Modules:**
- `time`
- `unittest.mock`
- `frappe`
- `frappe.tests`
- `frappe.utils.telemetry.pulse.client`
- `frappe.utils.telemetry.pulse.utils`


## Step-by-Step Guide

### Step 1: 'Test batch processing when max retries is exceeded'

```python
'Test batch processing when max retries is exceeded'
```

### Step 2: Assign eq = EventQueue(...)

```python
eq = EventQueue()
```

### Step 3: Call eq.batch_process()

```python
eq.batch_process(always_failing_fn, batch_size=10, max_retries=2, backoff_seconds=0.1)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(eq.length, 5)
```

### Step 5: Assign event = value

```python
event = {'event_name': f'test_event_{i}', 'captured_at': '2026-01-01T00:00:00', 'app': 'frappe', 'user': 'test@example.com', 'site': 'test.localhost', 'properties': {}}
```

### Step 6: Call eq.add()

```python
eq.add(event)
```


## Complete Example

```python
# Workflow
'Test batch processing when max retries is exceeded'
eq = EventQueue()

def always_failing_fn(events):
    raise Exception('Always fails')
for i in range(5):
    event = {'event_name': f'test_event_{i}', 'captured_at': '2026-01-01T00:00:00', 'app': 'frappe', 'user': 'test@example.com', 'site': 'test.localhost', 'properties': {}}
    eq.add(event)
eq.batch_process(always_failing_fn, batch_size=10, max_retries=2, backoff_seconds=0.1)
self.assertEqual(eq.length, 5)
```

## Next Steps


---

*Source: test_pulse_client.py:233 | Complexity: Intermediate | Last updated: 2026-02-04*