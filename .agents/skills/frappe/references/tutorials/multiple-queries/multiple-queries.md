# How To: Multiple Queries

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test multiple queries

## Prerequisites

**Required Modules:**
- `time`
- `sqlparse`
- `frappe`
- `frappe.recorder`
- `frappe.recorder`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.doctor`
- `frappe.website.serve`


## Step-by-Step Guide

### Step 1: Assign queries = value

```python
queries = [{'mariadb': 'SELECT * FROM tabDocType', 'postgres': 'SELECT * FROM "tabDocType"'}, {'mariadb': 'SELECT COUNT(*) FROM tabDocType', 'postgres': 'SELECT COUNT(*) FROM "tabDocType"'}, {'mariadb': 'COMMIT', 'postgres': 'COMMIT'}]
```

### Step 2: Assign sql_dialect = value

```python
sql_dialect = frappe.db.db_type or 'mariadb'
```

### Step 3: Call self.stop_recording()

```python
self.stop_recording()
```

### Step 4: Assign requests = frappe.recorder.get(...)

```python
requests = frappe.recorder.get()
```

### Step 5: Assign request = frappe.recorder.get(...)

```python
request = frappe.recorder.get(requests[0]['uuid'])
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(request['calls']), len(queries))
```

### Step 7: Call frappe.db.sql()

```python
frappe.db.sql(query[sql_dialect])
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(call['query'], sqlparse.format(query[sql_dialect].strip(), keyword_case='upper', reindent=True, strip_comments=True))
```


## Complete Example

```python
# Workflow
queries = [{'mariadb': 'SELECT * FROM tabDocType', 'postgres': 'SELECT * FROM "tabDocType"'}, {'mariadb': 'SELECT COUNT(*) FROM tabDocType', 'postgres': 'SELECT COUNT(*) FROM "tabDocType"'}, {'mariadb': 'COMMIT', 'postgres': 'COMMIT'}]
sql_dialect = frappe.db.db_type or 'mariadb'
for query in queries:
    frappe.db.sql(query[sql_dialect])
self.stop_recording()
requests = frappe.recorder.get()
request = frappe.recorder.get(requests[0]['uuid'])
self.assertEqual(len(request['calls']), len(queries))
for query, call in zip(queries, request['calls'], strict=False):
    self.assertEqual(call['query'], sqlparse.format(query[sql_dialect].strip(), keyword_case='upper', reindent=True, strip_comments=True))
```

## Next Steps


---

*Source: test_recorder.py:95 | Complexity: Advanced | Last updated: 2026-02-04*