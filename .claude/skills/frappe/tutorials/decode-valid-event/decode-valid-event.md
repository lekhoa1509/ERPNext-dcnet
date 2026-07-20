# How To: Decode Valid Event

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test decoding valid event JSON

## Prerequisites

**Required Modules:**
- `time`
- `unittest.mock`
- `frappe`
- `frappe.tests`
- `frappe.utils.telemetry.pulse.client`
- `frappe.utils.telemetry.pulse.utils`


## Step-by-Step Guide

### Step 1: 'Test decoding valid event JSON'

```python
'Test decoding valid event JSON'
```

### Step 2: Assign eq = EventQueue(...)

```python
eq = EventQueue()
```

### Step 3: Assign event = value

```python
event = {'event_name': 'test_event', 'captured_at': '2026-01-01T00:00:00', 'app': 'frappe', 'user': 'test@example.com', 'site': 'test.localhost', 'properties': {}}
```

### Step 4: Call eq.add()

```python
eq.add(event)
```

### Step 5: Assign event_json = frappe.cache.rpop(...)

```python
event_json = frappe.cache.rpop(eq.queue)
```

### Step 6: Assign decoded = eq._decode_event(...)

```python
decoded = eq._decode_event(event_json)
```

### Step 7: Call self.assertIsNotNone()

```python
self.assertIsNotNone(decoded)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(decoded['event_name'], 'test_event')
```


## Complete Example

```python
# Workflow
'Test decoding valid event JSON'
eq = EventQueue()
event = {'event_name': 'test_event', 'captured_at': '2026-01-01T00:00:00', 'app': 'frappe', 'user': 'test@example.com', 'site': 'test.localhost', 'properties': {}}
eq.add(event)
event_json = frappe.cache.rpop(eq.queue)
decoded = eq._decode_event(event_json)
self.assertIsNotNone(decoded)
self.assertEqual(decoded['event_name'], 'test_event')
```

## Next Steps


---

*Source: test_pulse_client.py:340 | Complexity: Advanced | Last updated: 2026-02-04*