# How To: Casted Get Value Singles

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test casted get value singles

## Prerequisites

**Required Modules:**
- `datetime`
- `math`
- `random`
- `unittest.mock`
- `frappe`
- `frappe.core.utils`
- `frappe.custom.doctype.custom_field.custom_field`
- `frappe.database`
- `frappe.database.database`
- `frappe.database.utils`
- `frappe.query_builder`
- `frappe.query_builder.functions`
- `frappe.tests`
- `frappe.tests.test_query_builder`
- `frappe.utils`
- `frappe.utils.data`
- `frappe.utils.testutils`
- `frappe.database.database`
- `frappe.database.postgres.database`
- `frappe.database.postgres.database`
- `psycopg2.errors`
- `frappe.core.doctype.doctype.test_doctype`
- `contextlib`
- `os`
- `re`
- `frappe.database.postgres.database`


## Step-by-Step Guide

### Step 1: Assign telemetry = frappe.db.get_value(...)

```python
telemetry = frappe.db.get_value('System Settings', None, 'enable_telemetry')
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual(type(telemetry), int)
```

### Step 3: Assign telemetry = frappe.db.get_value(...)

```python
telemetry = frappe.db.get_value('System Settings', 'System Settings', 'enable_telemetry')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(type(telemetry), int)
```

### Step 5: Assign dt_name = frappe.db.get_value(...)

```python
dt_name = frappe.db.get_value('DocType', 'DocType', 'name')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(dt_name, 'DocType')
```

### Step 7: Assign timestamp = frappe.db.get_value(...)

```python
timestamp = frappe.db.get_value('System Settings', None, 'modified')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(type(timestamp), datetime.datetime)
```


## Complete Example

```python
# Workflow
telemetry = frappe.db.get_value('System Settings', None, 'enable_telemetry')
self.assertEqual(type(telemetry), int)
telemetry = frappe.db.get_value('System Settings', 'System Settings', 'enable_telemetry')
self.assertEqual(type(telemetry), int)
dt_name = frappe.db.get_value('DocType', 'DocType', 'name')
self.assertEqual(dt_name, 'DocType')
timestamp = frappe.db.get_value('System Settings', None, 'modified')
self.assertEqual(type(timestamp), datetime.datetime)
```

## Next Steps


---

*Source: test_db.py:183 | Complexity: Advanced | Last updated: 2026-02-04*