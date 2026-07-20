# How To: Batch Process With Failure And Retry

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test batch processing with failure and retry

## Prerequisites

**Required Modules:**
- `time`
- `unittest.mock`
- `frappe`
- `frappe.tests`
- `frappe.utils.telemetry.pulse.client`
- `frappe.utils.telemetry.pulse.utils`


## Step-by-Step Guide

### Step 1: 'Test batch processing with failure and retry'

```python
'Test batch processing with failure and retry'
```

### Step 2: Assign eq = EventQueue(...)

```python
eq = EventQueue()
```

### Step 3: Assign call_count = 0

```python
call_count = 0
```

### Step 4: Call eq.batch_process()

```python
eq.batch_process(failing_fn, batch_size=10, max_retries=5, backoff_seconds=0.1)
```

### Step 5: Call self.assertGreaterEqual()

```python
self.assertGreaterEqual(call_count, 3)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(eq.length, 0)
```

### Step 7: Assign event = value

```python
event = {'event_name': f'test_event_{i}', 'captured_at': '2026-01-01T00:00:00', 'app': 'frappe', 'user': 'test@example.com', 'site': 'test.localhost', 'properties': {}}
```

### Step 8: Call eq.add()

```python
eq.add(event)
```


## Complete Example

```python
# Workflow
'Test batch processing with failure and retry'
eq = EventQueue()
call_count = 0

def failing_fn(events):
    nonlocal call_count
    call_count += 1
    if call_count < 3:
        raise Exception('Temporary failure')
    return True
for i in range(5):
    event = {'event_name': f'test_event_{i}', 'captured_at': '2026-01-01T00:00:00', 'app': 'frappe', 'user': 'test@example.com', 'site': 'test.localhost', 'properties': {}}
    eq.add(event)
eq.batch_process(failing_fn, batch_size=10, max_retries=5, backoff_seconds=0.1)
self.assertGreaterEqual(call_count, 3)
self.assertEqual(eq.length, 0)
```

## Next Steps


---

*Source: test_pulse_client.py:202 | Complexity: Advanced | Last updated: 2026-02-04*