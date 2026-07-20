# How To: Memory Usage

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test memory usage

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

### Step 1: Assign job = frappe.enqueue(...)

```python
job = frappe.enqueue('frappe.utils.data._get_rss_memory_usage')
```

### Step 2: Call self.check_status()

```python
self.check_status(job, 'finished')
```

### Step 3: Assign rss = value

```python
rss = job.latest_result().return_value
```

### Step 4: Assign msg = 'Memory usage of simple background job increased. Potential root cause can be a newly added python module import. Check and move them to approriate file/function to avoid loading the module by default.'

```python
msg = 'Memory usage of simple background job increased. Potential root cause can be a newly added python module import. Check and move them to approriate file/function to avoid loading the module by default.'
```

### Step 5: Assign LAST_MEASURED_USAGE = 46

```python
LAST_MEASURED_USAGE = 46
```

### Step 6: Call self.assertLessEqual()

```python
self.assertLessEqual(rss, LAST_MEASURED_USAGE * 1.05, msg)
```


## Complete Example

```python
# Workflow
if frappe.db.db_type != 'mariadb':
    return
job = frappe.enqueue('frappe.utils.data._get_rss_memory_usage')
self.check_status(job, 'finished')
rss = job.latest_result().return_value
msg = 'Memory usage of simple background job increased. Potential root cause can be a newly added python module import. Check and move them to approriate file/function to avoid loading the module by default.'
LAST_MEASURED_USAGE = 46
if frappe.conf.use_mysqlclient:
    LAST_MEASURED_USAGE += 2
LAST_MEASURED_USAGE += 6
self.assertLessEqual(rss, LAST_MEASURED_USAGE * 1.05, msg)
```

## Next Steps


---

*Source: test_rq_job.py:164 | Complexity: Intermediate | Last updated: 2026-02-04*