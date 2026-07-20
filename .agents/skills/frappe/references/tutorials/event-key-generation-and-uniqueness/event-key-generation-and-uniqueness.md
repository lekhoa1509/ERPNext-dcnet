# How To: Event Key Generation And Uniqueness

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test event key generation and uniqueness for rate limiting

## Prerequisites

**Required Modules:**
- `time`
- `unittest.mock`
- `frappe`
- `frappe.tests`
- `frappe.utils.telemetry.pulse.client`
- `frappe.utils.telemetry.pulse.utils`


## Step-by-Step Guide

### Step 1: 'Test event key generation and uniqueness for rate limiting'

```python
'Test event key generation and uniqueness for rate limiting'
```

### Step 2: Assign eq = EventQueue(...)

```python
eq = EventQueue()
```

### Step 3: Assign event1 = value

```python
event1 = {'event_name': 'event_1', 'app': 'frappe', 'user': 'user1@example.com', 'site': 'test.localhost'}
```

### Step 4: Assign event2 = value

```python
event2 = {'event_name': 'event_2', 'app': 'frappe', 'user': 'user1@example.com', 'site': 'test.localhost'}
```

### Step 5: Assign key1 = eq._get_event_key(...)

```python
key1 = eq._get_event_key(event1)
```

### Step 6: Call self.assertIn()

```python
self.assertIn('event_1', key1)
```

### Step 7: Call self.assertIn()

```python
self.assertIn('test.localhost', key1)
```

### Step 8: Call self.assertIn()

```python
self.assertIn('frappe', key1)
```

### Step 9: Assign key2 = eq._get_event_key(...)

```python
key2 = eq._get_event_key(event2)
```

### Step 10: Call self.assertNotEqual()

```python
self.assertNotEqual(key1, key2)
```


## Complete Example

```python
# Workflow
'Test event key generation and uniqueness for rate limiting'
eq = EventQueue()
event1 = {'event_name': 'event_1', 'app': 'frappe', 'user': 'user1@example.com', 'site': 'test.localhost'}
event2 = {'event_name': 'event_2', 'app': 'frappe', 'user': 'user1@example.com', 'site': 'test.localhost'}
key1 = eq._get_event_key(event1)
self.assertIn('event_1', key1)
self.assertIn('test.localhost', key1)
self.assertIn('frappe', key1)
key2 = eq._get_event_key(event2)
self.assertNotEqual(key1, key2)
```

## Next Steps


---

*Source: test_pulse_client.py:371 | Complexity: Advanced | Last updated: 2026-02-04*