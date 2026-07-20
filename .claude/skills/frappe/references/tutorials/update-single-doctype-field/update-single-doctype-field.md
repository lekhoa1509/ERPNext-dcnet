# How To: Update Single Doctype Field

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test update single doctype field

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

### Step 1: Assign value = frappe.db.get_single_value(...)

```python
value = frappe.db.get_single_value('System Settings', 'deny_multiple_sessions')
```

### Step 2: Assign changed_value = value

```python
changed_value = not value
```

### Step 3: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('System Settings', 'deny_multiple_sessions', changed_value)
```

### Step 4: Assign current_value = frappe.db.get_single_value(...)

```python
current_value = frappe.db.get_single_value('System Settings', 'deny_multiple_sessions')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(current_value, changed_value)
```

### Step 6: Assign changed_value = value

```python
changed_value = not current_value
```

### Step 7: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('System Settings', 'deny_multiple_sessions', changed_value)
```

### Step 8: Assign current_value = frappe.db.get_single_value(...)

```python
current_value = frappe.db.get_single_value('System Settings', 'deny_multiple_sessions')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(current_value, changed_value)
```

### Step 10: Assign changed_value = value

```python
changed_value = not current_value
```

### Step 11: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('System Settings', 'deny_multiple_sessions', changed_value)
```

### Step 12: Assign current_value = frappe.db.get_single_value(...)

```python
current_value = frappe.db.get_single_value('System Settings', 'deny_multiple_sessions')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(current_value, changed_value)
```


## Complete Example

```python
# Workflow
value = frappe.db.get_single_value('System Settings', 'deny_multiple_sessions')
changed_value = not value
frappe.db.set_single_value('System Settings', 'deny_multiple_sessions', changed_value)
current_value = frappe.db.get_single_value('System Settings', 'deny_multiple_sessions')
self.assertEqual(current_value, changed_value)
changed_value = not current_value
frappe.db.set_single_value('System Settings', 'deny_multiple_sessions', changed_value)
current_value = frappe.db.get_single_value('System Settings', 'deny_multiple_sessions')
self.assertEqual(current_value, changed_value)
changed_value = not current_value
frappe.db.set_single_value('System Settings', 'deny_multiple_sessions', changed_value)
current_value = frappe.db.get_single_value('System Settings', 'deny_multiple_sessions')
self.assertEqual(current_value, changed_value)
```

## Next Steps


---

*Source: test_db.py:814 | Complexity: Advanced | Last updated: 2026-02-04*