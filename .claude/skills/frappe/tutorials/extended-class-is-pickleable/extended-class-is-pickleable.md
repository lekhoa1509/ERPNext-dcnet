# How To: Extended Class Is Pickleable

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test that extended class instances can be pickled and unpickled correctly

## Prerequisites

**Required Modules:**
- `pickle`
- `frappe`
- `frappe.desk.doctype.todo.todo`
- `frappe.model.base_document`
- `frappe.tests`
- `frappe.desk.doctype.todo.todo`
- `frappe.desk.doctype.todo.todo`
- `frappe.desk.doctype.todo.todo`


## Step-by-Step Guide

### Step 1: 'Test that extended class instances can be pickled and unpickled correctly'

```python
'Test that extended class instances can be pickled and unpickled correctly'
```

### Step 2: Assign extensions = value

```python
extensions = ['frappe.tests.test_base_document.TestToDoExtension']
```

### Step 3: Assign extended_class = _get_extended_class(...)

```python
extended_class = _get_extended_class(ToDo, 'ToDo')
```

### Step 4: Assign original_instance = extended_class(...)

```python
original_instance = extended_class({'doctype': 'ToDo', 'description': 'Test ToDo for pickling', 'status': 'Open'})
```

### Step 5: Call original_instance.validate()

```python
original_instance.validate()
```

### Step 6: Assign original_instance.custom_attribute = 'test_value'

```python
original_instance.custom_attribute = 'test_value'
```

### Step 7: Assign state = original_instance.__getstate__(...)

```python
state = original_instance.__getstate__()
```

### Step 8: Assign pickled_data = pickle.dumps(...)

```python
pickled_data = pickle.dumps(original_instance)
```

### Step 9: Call clear_todo_controller_cache()

```python
clear_todo_controller_cache()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(unpickled_instance.__class__.__name__, f'Extended{ToDo.__name__}')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(unpickled_instance.doctype, 'ToDo')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(unpickled_instance.description, 'Test ToDo for pickling')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(unpickled_instance.status, 'Open')
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(unpickled_instance.custom_attribute, 'test_value')
```

### Step 15: Call self.assertTrue()

```python
self.assertTrue(getattr(unpickled_instance, 'custom_validation_called', False))
```

### Step 16: Call self.assertTrue()

```python
self.assertTrue(hasattr(unpickled_instance, 'extension_method'))
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(unpickled_instance.extension_method(), 'extension_method_called')
```

### Step 18: Call self.assertTrue()

```python
self.assertTrue(hasattr(unpickled_instance, 'on_update'))
```

### Step 19: Call self.assertTrue()

```python
self.assertTrue(hasattr(unpickled_instance, 'validate'))
```

### Step 20: Call self.assertNotIn()

```python
self.assertNotIn(unpicklable_key, state)
```

### Step 21: Assign unpickled_instance = pickle.loads(...)

```python
unpickled_instance = pickle.loads(pickled_data)
```

### Step 22: Call clear_todo_controller_cache()

```python
clear_todo_controller_cache()
```


## Complete Example

```python
# Workflow
'Test that extended class instances can be pickled and unpickled correctly'
from frappe.desk.doctype.todo.todo import ToDo
extensions = ['frappe.tests.test_base_document.TestToDoExtension']
with self.patch_hooks({'extend_doctype_class': {'ToDo': extensions}}):
    extended_class = _get_extended_class(ToDo, 'ToDo')
    original_instance = extended_class({'doctype': 'ToDo', 'description': 'Test ToDo for pickling', 'status': 'Open'})
    original_instance.validate()
    original_instance.custom_attribute = 'test_value'
    state = original_instance.__getstate__()
    for unpicklable_key in ['meta', 'permitted_fieldnames', '_weakref']:
        self.assertNotIn(unpicklable_key, state)
    pickled_data = pickle.dumps(original_instance)
    clear_todo_controller_cache()
    try:
        unpickled_instance = pickle.loads(pickled_data)
    finally:
        clear_todo_controller_cache()
    self.assertEqual(unpickled_instance.__class__.__name__, f'Extended{ToDo.__name__}')
    self.assertEqual(unpickled_instance.doctype, 'ToDo')
    self.assertEqual(unpickled_instance.description, 'Test ToDo for pickling')
    self.assertEqual(unpickled_instance.status, 'Open')
    self.assertEqual(unpickled_instance.custom_attribute, 'test_value')
    self.assertTrue(getattr(unpickled_instance, 'custom_validation_called', False))
    self.assertTrue(hasattr(unpickled_instance, 'extension_method'))
    self.assertEqual(unpickled_instance.extension_method(), 'extension_method_called')
    self.assertTrue(hasattr(unpickled_instance, 'on_update'))
    self.assertTrue(hasattr(unpickled_instance, 'validate'))
```

## Next Steps


---

*Source: test_base_document.py:147 | Complexity: Advanced | Last updated: 2026-02-04*