# How To: Set Global Conf

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test set global conf

## Prerequisites

**Required Modules:**
- `gzip`
- `importlib`
- `json`
- `os`
- `secrets`
- `shlex`
- `signal`
- `string`
- `subprocess`
- `sys`
- `time`
- `types`
- `unittest`
- `contextlib`
- `functools`
- `glob`
- `pathlib`
- `unittest.case`
- `unittest.mock`
- `click`
- `psutil`
- `requests`
- `click`
- `click.testing`
- `tenacity`
- `frappe`
- `frappe.commands.scheduler`
- `frappe.commands.site`
- `frappe.commands.utils`
- `frappe.recorder`
- `frappe.installer`
- `frappe.query_builder.utils`
- `frappe.tests`
- `frappe.tests.test_query_builder`
- `frappe.utils`
- `frappe.utils.backups`
- `frappe.utils.jinja_globals`
- `frappe.utils.scheduler`
- `frappe.utils.password`
- `frappe.installer`
- `frappe.utils.bench_helper`
- `frappe.database.mariadb.setup_db`
- `frappe.database.postgres.setup_db`


## Step-by-Step Guide

### Step 1: Assign key = 'answer'

```python
key = 'answer'
```

### Step 2: Assign value = frappe.generate_hash(...)

```python
value = frappe.generate_hash()
```

### Step 3: Assign _ = frappe.get_site_config(...)

```python
_ = frappe.get_site_config()
```

### Step 4: Call self.execute()

```python
self.execute(f'bench set-config {key} {value} -g')
```

### Step 5: Assign conf = frappe.get_site_config(...)

```python
conf = frappe.get_site_config()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(conf[key], value)
```


## Complete Example

```python
# Workflow
key = 'answer'
value = frappe.generate_hash()
_ = frappe.get_site_config()
self.execute(f'bench set-config {key} {value} -g')
conf = frappe.get_site_config()
self.assertEqual(conf[key], value)
```

## Next Steps


---

*Source: test_commands.py:532 | Complexity: Intermediate | Last updated: 2026-02-04*