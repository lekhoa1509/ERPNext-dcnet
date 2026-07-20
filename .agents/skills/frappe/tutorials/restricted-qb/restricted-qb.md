# How To: Restricted Qb

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test restricted qb

## Prerequisites

**Required Modules:**
- `requests`
- `frappe`
- `frappe.core.doctype.scheduled_job_type.scheduled_job_type`
- `frappe.core.doctype.server_script.server_script`
- `frappe.frappeclient`
- `frappe.tests`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Assign todo = frappe.get_doc(...)

```python
todo = frappe.get_doc(doctype='ToDo', description='QbScriptTestNote')
```

### Step 2: Call todo.insert()

```python
todo.insert()
```

### Step 3: Assign script = frappe.get_doc(...)

```python
script = frappe.get_doc(doctype='Server Script', name='test_qb_restrictions', script_type='API', api_method='test_qb_restrictions', allow_guest=1, script=f'\nfrappe.db.set_value("ToDo", "{todo.name}", "description", "safe")\n')
```

### Step 4: Call script.insert()

```python
script.insert()
```

### Step 5: Call script.execute_method()

```python
script.execute_method()
```

### Step 6: Call todo.reload()

```python
todo.reload()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(todo.description, 'safe')
```

### Step 8: Assign script.script = value

```python
script.script = f'\ntodo = frappe.qb.DocType("ToDo")\nfrappe.qb.update(todo).set(todo.description, "unsafe").where(todo.name == "{todo.name}").run()\n'
```

### Step 9: Call script.save()

```python
script.save()
```

### Step 10: Call self.assertRaises()

```python
self.assertRaises(frappe.PermissionError, script.execute_method)
```

### Step 11: Call todo.reload()

```python
todo.reload()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(todo.description, 'safe')
```

### Step 13: Assign script.script = value

```python
script.script = f'\ntodo = frappe.qb.DocType("ToDo")\nfrappe.qb.from_(todo).select(todo.name).where(todo.name == "{todo.name}").run()\n'
```

### Step 14: Call script.save()

```python
script.save()
```

### Step 15: Call script.execute_method()

```python
script.execute_method()
```


## Complete Example

```python
# Workflow
todo = frappe.get_doc(doctype='ToDo', description='QbScriptTestNote')
todo.insert()
script = frappe.get_doc(doctype='Server Script', name='test_qb_restrictions', script_type='API', api_method='test_qb_restrictions', allow_guest=1, script=f'\nfrappe.db.set_value("ToDo", "{todo.name}", "description", "safe")\n')
script.insert()
script.execute_method()
todo.reload()
self.assertEqual(todo.description, 'safe')
script.script = f'\ntodo = frappe.qb.DocType("ToDo")\nfrappe.qb.update(todo).set(todo.description, "unsafe").where(todo.name == "{todo.name}").run()\n'
script.save()
self.assertRaises(frappe.PermissionError, script.execute_method)
todo.reload()
self.assertEqual(todo.description, 'safe')
script.script = f'\ntodo = frappe.qb.DocType("ToDo")\nfrappe.qb.from_(todo).select(todo.name).where(todo.name == "{todo.name}").run()\n'
script.save()
script.execute_method()
```

## Next Steps


---

*Source: test_server_script.py:200 | Complexity: Advanced | Last updated: 2026-02-04*