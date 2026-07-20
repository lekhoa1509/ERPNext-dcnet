# How To: Remove Failed Jobs

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test remove failed jobs

## Prerequisites

**Required Modules:**
- `time`
- `contextlib`
- `unittest.mock`
- `rq`
- `werkzeug.local`
- `frappe`
- `frappe.core.doctype.rq_job.rq_job`
- `frappe.tests`
- `frappe.utils.background_jobs`


## Step-by-Step Guide

### Step 1: Call frappe.enqueue()

```python
frappe.enqueue(method='frappe.tests.test_background_jobs.fail_function', queue='short')
```

### Step 2: Call time.sleep()

```python
time.sleep(2)
```

### Step 3: Assign conn = get_redis_conn(...)

```python
conn = get_redis_conn()
```

### Step 4: Assign queues = Queue.all(...)

```python
queues = Queue.all(conn)
```

### Step 5: Call remove_failed_jobs()

```python
remove_failed_jobs()
```

### Step 6: Assign fail_registry = value

```python
fail_registry = queue.failed_job_registry
```

### Step 7: Call self.assertGreater()

```python
self.assertGreater(fail_registry.count, 0)
```

### Step 8: Assign fail_registry = value

```python
fail_registry = queue.failed_job_registry
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(fail_registry.count, 0)
```


## Complete Example

```python
# Workflow
frappe.enqueue(method='frappe.tests.test_background_jobs.fail_function', queue='short')
time.sleep(2)
conn = get_redis_conn()
queues = Queue.all(conn)
for queue in queues:
    if queue.name == generate_qname('short'):
        fail_registry = queue.failed_job_registry
        self.assertGreater(fail_registry.count, 0)
remove_failed_jobs()
for queue in queues:
    if queue.name == generate_qname('short'):
        fail_registry = queue.failed_job_registry
        self.assertEqual(fail_registry.count, 0)
```

## Next Steps


---

*Source: test_background_jobs.py:22 | Complexity: Advanced | Last updated: 2026-02-04*