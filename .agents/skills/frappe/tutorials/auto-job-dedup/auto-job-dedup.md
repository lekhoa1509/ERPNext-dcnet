# How To: Auto Job Dedup

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test auto job dedup

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

### Step 1: Assign job_id = 'test_dedup'

```python
job_id = 'test_dedup'
```

### Step 2: Assign job1 = frappe.enqueue(...)

```python
job1 = frappe.enqueue(self.BG_JOB, sleep=2, job_id=job_id, deduplicate=True)
```

### Step 3: Assign job2 = frappe.enqueue(...)

```python
job2 = frappe.enqueue(self.BG_JOB, sleep=5, job_id=job_id, deduplicate=True)
```

### Step 4: Call self.assertIsNone()

```python
self.assertIsNone(job2)
```

### Step 5: Call self.check_status()

```python
self.check_status(job1, 'finished')
```

### Step 6: Assign job3 = frappe.enqueue(...)

```python
job3 = frappe.enqueue(self.BG_JOB, fail=True, job_id=job_id, deduplicate=True)
```

### Step 7: Call self.check_status()

```python
self.check_status(job3, 'failed')
```

### Step 8: Assign job4 = frappe.enqueue(...)

```python
job4 = frappe.enqueue(self.BG_JOB, sleep=1, job_id=job_id, deduplicate=True)
```

### Step 9: Call self.check_status()

```python
self.check_status(job4, 'finished')
```


## Complete Example

```python
# Workflow
job_id = 'test_dedup'
job1 = frappe.enqueue(self.BG_JOB, sleep=2, job_id=job_id, deduplicate=True)
job2 = frappe.enqueue(self.BG_JOB, sleep=5, job_id=job_id, deduplicate=True)
self.assertIsNone(job2)
self.check_status(job1, 'finished')
job3 = frappe.enqueue(self.BG_JOB, fail=True, job_id=job_id, deduplicate=True)
self.check_status(job3, 'failed')
job4 = frappe.enqueue(self.BG_JOB, sleep=1, job_id=job_id, deduplicate=True)
self.check_status(job4, 'finished')
```

## Next Steps


---

*Source: test_rq_job.py:131 | Complexity: Advanced | Last updated: 2026-02-04*