# How To: Build Assets Size Check

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test build assets size check

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

### Step 1: Assign CURRENT_SIZE = 3.4

```python
CURRENT_SIZE = 3.4
```

### Step 2: Assign JS_ASSET_THRESHOLD = 0.01

```python
JS_ASSET_THRESHOLD = 0.01
```

### Step 3: Assign hooks = frappe.get_hooks(...)

```python
hooks = frappe.get_hooks()
```

### Step 4: Assign default_bundle = value

```python
default_bundle = hooks['app_include_js']
```

### Step 5: Assign default_bundle_size = 0.0

```python
default_bundle_size = 0.0
```

### Step 6: Call self.assertLessEqual()

```python
self.assertLessEqual(default_bundle_size / (1024 * 1024), CURRENT_SIZE * (1 + JS_ASSET_THRESHOLD), f'Default JS bundle size increased by {JS_ASSET_THRESHOLD:.2%} or more')
```

### Step 7: Assign abs_path = value

```python
abs_path = Path.cwd() / frappe.local.sites_path / bundled_asset(chunk)[1:]
```


## Complete Example

```python
# Workflow
CURRENT_SIZE = 3.4
JS_ASSET_THRESHOLD = 0.01
hooks = frappe.get_hooks()
default_bundle = hooks['app_include_js']
default_bundle_size = 0.0
for chunk in default_bundle:
    abs_path = Path.cwd() / frappe.local.sites_path / bundled_asset(chunk)[1:]
    default_bundle_size += abs_path.stat().st_size
self.assertLessEqual(default_bundle_size / (1024 * 1024), CURRENT_SIZE * (1 + JS_ASSET_THRESHOLD), f'Default JS bundle size increased by {JS_ASSET_THRESHOLD:.2%} or more')
```

## Next Steps


---

*Source: test_commands.py:942 | Complexity: Intermediate | Last updated: 2026-02-04*