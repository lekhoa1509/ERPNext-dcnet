# How To: Capture Anonymizes User

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test that user is anonymized

## Prerequisites

**Required Modules:**
- `time`
- `unittest.mock`
- `frappe`
- `frappe.tests`
- `frappe.utils.telemetry.pulse.client`
- `frappe.utils.telemetry.pulse.utils`


## Step-by-Step Guide

### Step 1: 'Test that user is anonymized'

```python
'Test that user is anonymized'
```

### Step 2: Call is_enabled.clear_cache()

```python
is_enabled.clear_cache()
```

### Step 3: Assign mock_enabled.return_value = True

```python
mock_enabled.return_value = True
```

### Step 4: Assign eq = EventQueue(...)

```python
eq = EventQueue()
```

### Step 5: Assign test_user = 'test@example.com'

```python
test_user = 'test@example.com'
```

### Step 6: Call capture()

```python
capture('test_event', site='test.localhost', user=test_user)
```

### Step 7: Assign events = eq.collect(...)

```python
events = eq.collect(batch_size=1)
```

### Step 8: Call self.assertNotEqual()

```python
self.assertNotEqual(events[0]['user'], test_user)
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(events[0]['user'].startswith('anon_'))
```


## Complete Example

```python
# Workflow
'Test that user is anonymized'
is_enabled.clear_cache()
mock_enabled.return_value = True
eq = EventQueue()
test_user = 'test@example.com'
capture('test_event', site='test.localhost', user=test_user)
events = eq.collect(batch_size=1)
self.assertNotEqual(events[0]['user'], test_user)
self.assertTrue(events[0]['user'].startswith('anon_'))
```

## Next Steps


---

*Source: test_pulse_client.py:292 | Complexity: Advanced | Last updated: 2026-02-04*