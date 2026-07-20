# How To: List Apps

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test list apps

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

### Step 1: Call self.execute()

```python
self.execute('bench --site all list-apps')
```

### Step 2: Call self.assertIsNotNone()

```python
self.assertIsNotNone(self.returncode)
```

### Step 3: Call self.assertIsInstance()

```python
self.assertIsInstance(self.stdout or self.stderr, str)
```

### Step 4: Call self.execute()

```python
self.execute('bench --site {site} list-apps')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(self.returncode, 0)
```

### Step 6: Assign list_apps = value

```python
list_apps = {_x.split(maxsplit=1)[0] for _x in self.stdout.split('\n')}
```

### Step 7: Assign doctype = value

```python
doctype = frappe.get_single('Installed Applications').installed_applications
```

### Step 8: Call self.assertSetEqual()

```python
self.assertSetEqual(list_apps, installed_apps)
```

### Step 9: Call self.execute()

```python
self.execute('bench --site {site} list-apps --format json')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(self.returncode, 0)
```

### Step 11: Call self.assertIsInstance()

```python
self.assertIsInstance(json.loads(self.stdout), dict)
```

### Step 12: Call self.execute()

```python
self.execute('bench --site {site} list-apps -f json')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(self.returncode, 0)
```

### Step 14: Call self.assertIsInstance()

```python
self.assertIsInstance(json.loads(self.stdout), dict)
```

### Step 15: Assign installed_apps = value

```python
installed_apps = {x.app_name for x in doctype}
```

### Step 16: Assign installed_apps = set(...)

```python
installed_apps = set(frappe.get_installed_apps())
```


## Complete Example

```python
# Workflow
self.execute('bench --site all list-apps')
self.assertIsNotNone(self.returncode)
self.assertIsInstance(self.stdout or self.stderr, str)
self.execute('bench --site {site} list-apps')
self.assertEqual(self.returncode, 0)
list_apps = {_x.split(maxsplit=1)[0] for _x in self.stdout.split('\n')}
doctype = frappe.get_single('Installed Applications').installed_applications
if doctype:
    installed_apps = {x.app_name for x in doctype}
else:
    installed_apps = set(frappe.get_installed_apps())
self.assertSetEqual(list_apps, installed_apps)
self.execute('bench --site {site} list-apps --format json')
self.assertEqual(self.returncode, 0)
self.assertIsInstance(json.loads(self.stdout), dict)
self.execute('bench --site {site} list-apps -f json')
self.assertEqual(self.returncode, 0)
self.assertIsInstance(json.loads(self.stdout), dict)
```

## Next Steps


---

*Source: test_commands.py:370 | Complexity: Advanced | Last updated: 2026-02-04*