# How To: Cold Start

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test cold start

## Prerequisites

**Required Modules:**
- `datetime`
- `frappe`
- `frappe.core.doctype.scheduled_job_type.scheduled_job_type`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.data`


## Step-by-Step Guide

### Step 1: Assign now = now_datetime(...)

```python
now = now_datetime()
```

### Step 2: Assign just_before_12_am = now.replace(...)

```python
just_before_12_am = now.replace(hour=11, minute=59, second=30)
```

### Step 3: Assign just_after_12_am = value

```python
just_after_12_am = now.replace(hour=0, minute=0, second=30) + timedelta(days=1)
```

### Step 4: Assign job = frappe.new_doc(...)

```python
job = frappe.new_doc('Scheduled Job Type')
```

### Step 5: Assign job.frequency = 'Daily'

```python
job.frequency = 'Daily'
```

### Step 6: Call job.set_user_and_timestamp()

```python
job.set_user_and_timestamp()
```

### Step 7: Call self.assertFalse()

```python
self.assertFalse(job.is_event_due())
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(job.is_event_due())
```


## Complete Example

```python
# Workflow
now = now_datetime()
just_before_12_am = now.replace(hour=11, minute=59, second=30)
just_after_12_am = now.replace(hour=0, minute=0, second=30) + timedelta(days=1)
job = frappe.new_doc('Scheduled Job Type')
job.frequency = 'Daily'
job.set_user_and_timestamp()
with self.freeze_time(just_before_12_am):
    self.assertFalse(job.is_event_due())
with self.freeze_time(just_after_12_am):
    self.assertTrue(job.is_event_due())
```

## Next Steps


---

*Source: test_scheduled_job_type.py:121 | Complexity: Advanced | Last updated: 2026-02-04*