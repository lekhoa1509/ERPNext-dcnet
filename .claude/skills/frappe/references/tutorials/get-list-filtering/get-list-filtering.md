# How To: Get List Filtering

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get list filtering

## Prerequisites

**Required Modules:**
- `time`
- `rq`
- `rq.job`
- `frappe`
- `frappe.core.doctype.rq_job.rq_job`
- `frappe.installer`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.background_jobs`


## Step-by-Step Guide

### Step 1: Call remove_failed_jobs()

```python
remove_failed_jobs()
```

### Step 2: Assign jobs = frappe.get_all(...)

```python
jobs = frappe.get_all('RQ Job', {'status': 'failed'})
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(jobs, [])
```

### Step 4: Assign job = frappe.enqueue(...)

```python
job = frappe.enqueue(method=self.BG_JOB, queue='short')
```

### Step 5: Call self.check_status()

```python
self.check_status(job, 'finished')
```

### Step 6: Assign job = frappe.enqueue(...)

```python
job = frappe.enqueue(method=self.BG_JOB, queue='short', fail=True)
```

### Step 7: Call self.check_status()

```python
self.check_status(job, 'failed')
```

### Step 8: Assign jobs = frappe.get_all(...)

```python
jobs = frappe.get_all('RQ Job', {'status': 'failed'})
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(jobs), 1)
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(jobs[0].exc_info)
```

### Step 11: Assign non_failed_jobs = frappe.get_all(...)

```python
non_failed_jobs = frappe.get_all('RQ Job', {'status': ('!=', 'failed')})
```

### Step 12: Call self.assertGreaterEqual()

```python
self.assertGreaterEqual(len(non_failed_jobs), 1)
```

### Step 13: Assign job = frappe.enqueue(...)

```python
job = frappe.enqueue(method=self.BG_JOB, queue='short', sleep=10)
```

### Step 14: Call time.sleep()

```python
time.sleep(3)
```

### Step 15: Call self.check_status()

```python
self.check_status(job, 'started', wait=False)
```

### Step 16: Call stop_job()

```python
stop_job(job_id=job.id)
```

### Step 17: Call self.check_status()

```python
self.check_status(job, 'stopped')
```


## Complete Example

```python
# Workflow
remove_failed_jobs()
jobs = frappe.get_all('RQ Job', {'status': 'failed'})
self.assertEqual(jobs, [])
job = frappe.enqueue(method=self.BG_JOB, queue='short')
self.check_status(job, 'finished')
job = frappe.enqueue(method=self.BG_JOB, queue='short', fail=True)
self.check_status(job, 'failed')
jobs = frappe.get_all('RQ Job', {'status': 'failed'})
self.assertEqual(len(jobs), 1)
self.assertTrue(jobs[0].exc_info)
non_failed_jobs = frappe.get_all('RQ Job', {'status': ('!=', 'failed')})
self.assertGreaterEqual(len(non_failed_jobs), 1)
job = frappe.enqueue(method=self.BG_JOB, queue='short', sleep=10)
time.sleep(3)
self.check_status(job, 'started', wait=False)
stop_job(job_id=job.id)
self.check_status(job, 'stopped')
```

## Next Steps


---

*Source: test_rq_job.py:68 | Complexity: Advanced | Last updated: 2026-02-04*