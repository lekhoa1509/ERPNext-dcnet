# How To: Sync Jobs

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test sync jobs

## Prerequisites

**Required Modules:**
- `datetime`
- `frappe`
- `frappe.core.doctype.scheduled_job_type.scheduled_job_type`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.data`


## Step-by-Step Guide

### Step 1: Assign all_job = frappe.get_doc(...)

```python
all_job = frappe.get_doc('Scheduled Job Type', dict(method='frappe.email.queue.flush'))
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual(all_job.frequency, 'All')
```

### Step 3: Assign daily_job = frappe.get_doc(...)

```python
daily_job = frappe.get_doc('Scheduled Job Type', dict(method='frappe.desk.notifications.clear_notifications'))
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(daily_job.frequency, 'Daily Maintenance')
```

### Step 5: Assign cron_job = frappe.get_doc(...)

```python
cron_job = frappe.get_doc('Scheduled Job Type', dict(method='frappe.deferred_insert.save_to_db'))
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(cron_job.frequency, 'Cron')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(cron_job.cron_format, '0/15 * * * *')
```

### Step 8: Assign updated_scheduler_events = value

```python
updated_scheduler_events = {'hourly': ['frappe.email.queue.flush']}
```

### Step 9: Call sync_jobs()

```python
sync_jobs(updated_scheduler_events)
```

### Step 10: Assign updated_scheduled_job = frappe.get_doc(...)

```python
updated_scheduled_job = frappe.get_doc('Scheduled Job Type', {'method': 'frappe.email.queue.flush'})
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(updated_scheduled_job.frequency, 'Hourly')
```


## Complete Example

```python
# Workflow
all_job = frappe.get_doc('Scheduled Job Type', dict(method='frappe.email.queue.flush'))
self.assertEqual(all_job.frequency, 'All')
daily_job = frappe.get_doc('Scheduled Job Type', dict(method='frappe.desk.notifications.clear_notifications'))
self.assertEqual(daily_job.frequency, 'Daily Maintenance')
cron_job = frappe.get_doc('Scheduled Job Type', dict(method='frappe.deferred_insert.save_to_db'))
self.assertEqual(cron_job.frequency, 'Cron')
self.assertEqual(cron_job.cron_format, '0/15 * * * *')
updated_scheduler_events = {'hourly': ['frappe.email.queue.flush']}
sync_jobs(updated_scheduler_events)
updated_scheduled_job = frappe.get_doc('Scheduled Job Type', {'method': 'frappe.email.queue.flush'})
self.assertEqual(updated_scheduled_job.frequency, 'Hourly')
```

## Next Steps


---

*Source: test_scheduled_job_type.py:46 | Complexity: Advanced | Last updated: 2026-02-04*