# How To: Extension Overrides Todo Method

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test that an extension can override methods from the actual ToDo class

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

### Step 1: 'Test that an extension can override methods from the actual ToDo class'

```python
'Test that an extension can override methods from the actual ToDo class'
```

### Step 2: Assign extensions = value

```python
extensions = ['frappe.tests.test_base_document.TestToDoExtension']
```

### Step 3: Assign extended_class = _get_extended_class(...)

```python
extended_class = _get_extended_class(ToDo, 'ToDo')
```

### Step 4: Call self.assertNotEqual()

```python
self.assertNotEqual(extended_class, ToDo)
```

### Step 5: Assign instance = extended_class(...)

```python
instance = extended_class({'doctype': 'ToDo'})
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(hasattr(instance, 'extension_method'))
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(instance.extension_method(), 'extension_method_called')
```

### Step 8: Call instance.validate()

```python
instance.validate()
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(getattr(instance, 'custom_validation_called', False))
```

### Step 10: Assign mro_classes = value

```python
mro_classes = [cls.__name__ for cls in extended_class.__mro__]
```

### Step 11: Call self.assertIn()

```python
self.assertIn('TestToDoExtension', mro_classes)
```

### Step 12: Call self.assertIn()

```python
self.assertIn('ToDo', mro_classes)
```

### Step 13: Assign idx_extension = mro_classes.index(...)

```python
idx_extension = mro_classes.index('TestToDoExtension')
```

### Step 14: Assign idx_todo = mro_classes.index(...)

```python
idx_todo = mro_classes.index('ToDo')
```

### Step 15: Call self.assertLess()

```python
self.assertLess(idx_extension, idx_todo)
```


## Complete Example

```python
# Workflow
'Test that an extension can override methods from the actual ToDo class'
from frappe.desk.doctype.todo.todo import ToDo
extensions = ['frappe.tests.test_base_document.TestToDoExtension']
with self.patch_hooks({'extend_doctype_class': {'ToDo': extensions}}):
    extended_class = _get_extended_class(ToDo, 'ToDo')
    self.assertNotEqual(extended_class, ToDo)
    instance = extended_class({'doctype': 'ToDo'})
    self.assertTrue(hasattr(instance, 'extension_method'))
    self.assertEqual(instance.extension_method(), 'extension_method_called')
    instance.validate()
    self.assertTrue(getattr(instance, 'custom_validation_called', False))
    mro_classes = [cls.__name__ for cls in extended_class.__mro__]
    self.assertIn('TestToDoExtension', mro_classes)
    self.assertIn('ToDo', mro_classes)
    idx_extension = mro_classes.index('TestToDoExtension')
    idx_todo = mro_classes.index('ToDo')
    self.assertLess(idx_extension, idx_todo)
```

## Next Steps


---

*Source: test_base_document.py:91 | Complexity: Advanced | Last updated: 2026-02-04*