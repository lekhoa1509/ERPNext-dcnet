# How To: Server Script Scheduled

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test server script scheduled

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

### Step 1: Assign scheduled_script = frappe.get_doc.insert(...)

```python
scheduled_script = frappe.get_doc(doctype='Server Script', name='scheduled_script_wo_cron', script_type='Scheduler Event', script='frappe.flags = {"test": True}', event_frequency='Hourly').insert()
```

### Step 2: Assign cron_script = frappe.get_doc.insert(...)

```python
cron_script = frappe.get_doc(doctype='Server Script', name='scheduled_script_w_cron', script_type='Scheduler Event', script='frappe.flags = {"test": True}', event_frequency='Cron', cron_format='0 0 1 1 *').insert()
```

### Step 3: Call sync_jobs()

```python
sync_jobs()
```

### Step 4: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('Scheduled Job Type', {'server_script': scheduled_script.name}))
```

### Step 5: Assign cron_job_name = frappe.db.get_value(...)

```python
cron_job_name = frappe.db.get_value('Scheduled Job Type', {'server_script': cron_script.name})
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(cron_job_name)
```

### Step 7: Assign cron_job = frappe.get_doc(...)

```python
cron_job = frappe.get_doc('Scheduled Job Type', cron_job_name)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(cron_job.next_execution.day, 1)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(cron_job.next_execution.month, 1)
```

### Step 10: Assign cron_script.cron_format = '0 0 2 1 *'

```python
cron_script.cron_format = '0 0 2 1 *'
```

### Step 11: Call cron_script.save()

```python
cron_script.save()
```

### Step 12: Assign updated_cron_job_name = frappe.db.get_value(...)

```python
updated_cron_job_name = frappe.db.get_value('Scheduled Job Type', {'server_script': cron_script.name})
```

### Step 13: Assign updated_cron_job = frappe.get_doc(...)

```python
updated_cron_job = frappe.get_doc('Scheduled Job Type', updated_cron_job_name)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(updated_cron_job.next_execution.day, 2)
```


## Complete Example

```python
# Workflow
scheduled_script = frappe.get_doc(doctype='Server Script', name='scheduled_script_wo_cron', script_type='Scheduler Event', script='frappe.flags = {"test": True}', event_frequency='Hourly').insert()
cron_script = frappe.get_doc(doctype='Server Script', name='scheduled_script_w_cron', script_type='Scheduler Event', script='frappe.flags = {"test": True}', event_frequency='Cron', cron_format='0 0 1 1 *').insert()
sync_jobs()
self.assertTrue(frappe.db.exists('Scheduled Job Type', {'server_script': scheduled_script.name}))
cron_job_name = frappe.db.get_value('Scheduled Job Type', {'server_script': cron_script.name})
self.assertTrue(cron_job_name)
cron_job = frappe.get_doc('Scheduled Job Type', cron_job_name)
self.assertEqual(cron_job.next_execution.day, 1)
self.assertEqual(cron_job.next_execution.month, 1)
cron_script.cron_format = '0 0 2 1 *'
cron_script.save()
updated_cron_job_name = frappe.db.get_value('Scheduled Job Type', {'server_script': cron_script.name})
updated_cron_job = frappe.get_doc('Scheduled Job Type', updated_cron_job_name)
self.assertEqual(updated_cron_job.next_execution.day, 2)
```

## Next Steps


---

*Source: test_server_script.py:309 | Complexity: Advanced | Last updated: 2026-02-04*