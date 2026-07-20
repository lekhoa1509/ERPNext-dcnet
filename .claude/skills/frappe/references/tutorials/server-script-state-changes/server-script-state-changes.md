# How To: Server Script State Changes

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test server script state changes

## Prerequisites

**Required Modules:**
- `requests`
- `frappe`
- `frappe.core.doctype.scheduled_job_type.scheduled_job_type`
- `frappe.core.doctype.server_script.server_script`
- `frappe.frappeclient`
- `frappe.tests`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Assign script.script_type = 'API'

```python
script.script_type = 'API'
```

### Step 2: Call script.save()

```python
script.save()
```

### Step 3: Call self.assertTrue()

```python
self.assertTrue(job.reload().stopped)
```

### Step 4: Assign script.script_type = 'Scheduler Event'

```python
script.script_type = 'Scheduler Event'
```

### Step 5: Call script.save()

```python
script.save()
```

### Step 6: Call self.assertFalse()

```python
self.assertFalse(job.reload().stopped)
```

### Step 7: Assign script.event_frequency = 'Monthly'

```python
script.event_frequency = 'Monthly'
```

### Step 8: Call script.save()

```python
script.save()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(job.reload().frequency, 'Monthly')
```

### Step 10: Assign script.event_frequency = 'Cron'

```python
script.event_frequency = 'Cron'
```

### Step 11: Assign script.cron_format = '* * * * *'

```python
script.cron_format = '* * * * *'
```

### Step 12: Call script.save()

```python
script.save()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(job.reload().frequency, 'Cron')
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(job.reload().cron_format, script.cron_format)
```

### Step 15: Assign script.disabled = 1

```python
script.disabled = 1
```

### Step 16: Call script.save()

```python
script.save()
```

### Step 17: Call self.assertTrue()

```python
self.assertTrue(job.reload().stopped)
```

### Step 18: Assign script.disabled = 0

```python
script.disabled = 0
```

### Step 19: Call script.save()

```python
script.save()
```

### Step 20: Call self.assertFalse()

```python
self.assertFalse(job.reload().stopped)
```


## Complete Example

```python
# Workflow
script: ServerScript = frappe.get_doc(doctype='Server Script', name='scheduled_script_state_change', script_type='Scheduler Event', script='frappe.flags = {"test": True}', event_frequency='Hourly').insert()
job: ScheduledJobType = frappe.get_doc('Scheduled Job Type', {'server_script': script.name})
script.script_type = 'API'
script.save()
self.assertTrue(job.reload().stopped)
script.script_type = 'Scheduler Event'
script.save()
self.assertFalse(job.reload().stopped)
script.event_frequency = 'Monthly'
script.save()
self.assertEqual(job.reload().frequency, 'Monthly')
script.event_frequency = 'Cron'
script.cron_format = '* * * * *'
script.save()
self.assertEqual(job.reload().frequency, 'Cron')
self.assertEqual(job.reload().cron_format, script.cron_format)
script.disabled = 1
script.save()
self.assertTrue(job.reload().stopped)
script.disabled = 0
script.save()
self.assertFalse(job.reload().stopped)
```

## Next Steps


---

*Source: test_server_script.py:345 | Complexity: Advanced | Last updated: 2026-02-04*