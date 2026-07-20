# How To: Queue Operation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test queue operation

## Prerequisites

**Required Modules:**
- `time`
- `typing`
- `frappe`
- `frappe.tests`
- `frappe.utils.background_jobs`
- `rq.job`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.doctype.submission_queue.submission_queue`


## Step-by-Step Guide

### Step 1: Assign d = frappe.new_doc(...)

```python
d = frappe.new_doc('Test Submission Queue')
```

### Step 2: Call d.update()

```python
d.update({'some_fieldname': 'Random'})
```

### Step 3: Call d.insert()

```python
d.insert()
```

### Step 4: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 5: Call queue_submission()

```python
queue_submission(d, 'submit')
```

### Step 6: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 7: Call time.sleep()

```python
time.sleep(4)
```

### Step 8: Assign submission_queue = frappe.get_last_doc(...)

```python
submission_queue = frappe.get_last_doc('Submission Queue')
```

### Step 9: Assign job = self.queue.fetch_job(...)

```python
job = self.queue.fetch_job(submission_queue.job_id)
```

### Step 10: Call self.check_status()

```python
self.check_status(job, status='finished')
```

### Step 11: Assign doc = new_doctype(...)

```python
doc = new_doctype('Test Submission Queue', is_submittable=True, queue_in_background=True)
```

### Step 12: Call doc.insert()

```python
doc.insert()
```


## Complete Example

```python
# Workflow
from frappe.core.doctype.doctype.test_doctype import new_doctype
from frappe.core.doctype.submission_queue.submission_queue import queue_submission
if not frappe.db.table_exists('Test Submission Queue', cached=False):
    doc = new_doctype('Test Submission Queue', is_submittable=True, queue_in_background=True)
    doc.insert()
d = frappe.new_doc('Test Submission Queue')
d.update({'some_fieldname': 'Random'})
d.insert()
frappe.db.commit()
queue_submission(d, 'submit')
frappe.db.commit()
time.sleep(4)
submission_queue = frappe.get_last_doc('Submission Queue')
job = self.queue.fetch_job(submission_queue.job_id)
self.check_status(job, status='finished')
```

## Next Steps


---

*Source: test_submission_queue.py:30 | Complexity: Advanced | Last updated: 2026-02-04*