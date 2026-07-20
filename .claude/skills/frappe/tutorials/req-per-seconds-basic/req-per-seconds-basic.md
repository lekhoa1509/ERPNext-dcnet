# How To: Req Per Seconds Basic

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Ideally should be ran against gunicorn worker, though I have not seen any difference
when using werkzeug's run_simple for synchronous requests.

## Prerequisites

**Required Modules:**
- `gc`
- `itertools`
- `sys`
- `time`
- `unittest.mock`
- `psutil`
- `tenacity`
- `frappe`
- `frappe.frappeclient`
- `frappe.model.base_document`
- `frappe.query_builder.utils`
- `frappe.tests`
- `frappe.tests.test_api`
- `frappe.tests.test_query_builder`
- `frappe.utils`
- `frappe.utils.caching`
- `frappe.website.path_resolver`
- `frappe.utils`
- `frappe._optimizations`


## Step-by-Step Guide

### Step 1: "Ideally should be ran against gunicorn worker, though I have not seen any difference\n\t\twhen using werkzeug's run_simple for synchronous requests."

```python
"Ideally should be ran against gunicorn worker, though I have not seen any difference\n\t\twhen using werkzeug's run_simple for synchronous requests."
```

### Step 2: Assign EXPECTED_RPS = 140

```python
EXPECTED_RPS = 140
```

### Step 3: Assign FAILURE_THREASHOLD = 0.1

```python
FAILURE_THREASHOLD = 0.1
```

### Step 4: Assign req_count = 1000

```python
req_count = 1000
```

### Step 5: Assign client = FrappeClient(...)

```python
client = FrappeClient(self.HOST, 'Administrator', self.ADMIN_PASSWORD)
```

### Step 6: Assign start = time.perf_counter(...)

```python
start = time.perf_counter()
```

### Step 7: Assign end = time.perf_counter(...)

```python
end = time.perf_counter()
```

### Step 8: Assign rps = value

```python
rps = req_count / (end - start)
```

### Step 9: Call print()

```python
print(f'Completed {req_count} in {end - start} @ {rps} requests per seconds')
```

### Step 10: Call self.assertGreaterEqual()

```python
self.assertGreaterEqual(rps, EXPECTED_RPS * (1 - FAILURE_THREASHOLD), 'Possible performance regression in basic /api/Resource list  requests')
```

### Step 11: Call client.get_list()

```python
client.get_list('ToDo', limit_page_length=1)
```


## Complete Example

```python
# Workflow
"Ideally should be ran against gunicorn worker, though I have not seen any difference\n\t\twhen using werkzeug's run_simple for synchronous requests."
EXPECTED_RPS = 140
FAILURE_THREASHOLD = 0.1
req_count = 1000
client = FrappeClient(self.HOST, 'Administrator', self.ADMIN_PASSWORD)
start = time.perf_counter()
for _ in range(req_count):
    client.get_list('ToDo', limit_page_length=1)
end = time.perf_counter()
rps = req_count / (end - start)
print(f'Completed {req_count} in {end - start} @ {rps} requests per seconds')
self.assertGreaterEqual(rps, EXPECTED_RPS * (1 - FAILURE_THREASHOLD), 'Possible performance regression in basic /api/Resource list  requests')
```

## Next Steps


---

*Source: test_perf.py:132 | Complexity: Advanced | Last updated: 2026-02-04*