# How To: System Console Sql

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test system console sql

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign system_console = frappe.get_doc(...)

```python
system_console = frappe.get_doc('System Console')
```

### Step 2: Assign system_console.type = 'SQL'

```python
system_console.type = 'SQL'
```

### Step 3: Assign system_console.console = "select 'test'"

```python
system_console.console = "select 'test'"
```

### Step 4: Call system_console.run()

```python
system_console.run()
```

### Step 5: Call self.assertIn()

```python
self.assertIn('test', system_console.output)
```

### Step 6: Assign system_console.console = "update `tabDocType` set is_virtual = 1 where name = 'xyz'"

```python
system_console.console = "update `tabDocType` set is_virtual = 1 where name = 'xyz'"
```

### Step 7: Call system_console.run()

```python
system_console.run()
```

### Step 8: Call self.assertIn()

```python
self.assertIn('PermissionError', system_console.output)
```


## Complete Example

```python
# Workflow
system_console = frappe.get_doc('System Console')
system_console.type = 'SQL'
system_console.console = "select 'test'"
system_console.run()
self.assertIn('test', system_console.output)
system_console.console = "update `tabDocType` set is_virtual = 1 where name = 'xyz'"
system_console.run()
self.assertIn('PermissionError', system_console.output)
```

## Next Steps


---

*Source: test_system_console.py:25 | Complexity: Advanced | Last updated: 2026-02-04*