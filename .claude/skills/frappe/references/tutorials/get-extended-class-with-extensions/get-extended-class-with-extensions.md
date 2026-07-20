# How To: Get Extended Class With Extensions

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test that _get_extended_class properly combines extension classes with base class.

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

### Step 1: 'Test that _get_extended_class properly combines extension classes with base class.'

```python
'Test that _get_extended_class properly combines extension classes with base class.'
```

### Step 2: Assign extensions = value

```python
extensions = ['frappe.tests.test_base_document.TestExtensionA', 'frappe.tests.test_base_document.TestExtensionB']
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
self.assertTrue(hasattr(instance, 'extension_method_a'))
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(hasattr(instance, 'extension_method_b'))
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(instance.extension_method_a(), 'method_a')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(instance.extension_method_b(), 'method_b')
```

### Step 10: Assign mro_classes = value

```python
mro_classes = [cls.__name__ for cls in extended_class.__mro__]
```

### Step 11: Call self.assertIn()

```python
self.assertIn('TestExtensionB', mro_classes)
```

### Step 12: Call self.assertIn()

```python
self.assertIn('TestExtensionA', mro_classes)
```

### Step 13: Call self.assertIn()

```python
self.assertIn('ToDo', mro_classes)
```

### Step 14: Assign idx_b = mro_classes.index(...)

```python
idx_b = mro_classes.index('TestExtensionB')
```

### Step 15: Assign idx_a = mro_classes.index(...)

```python
idx_a = mro_classes.index('TestExtensionA')
```

### Step 16: Assign idx_base = mro_classes.index(...)

```python
idx_base = mro_classes.index('ToDo')
```

### Step 17: Call self.assertLess()

```python
self.assertLess(idx_b, idx_a)
```

### Step 18: Call self.assertLess()

```python
self.assertLess(idx_a, idx_base)
```


## Complete Example

```python
# Workflow
'Test that _get_extended_class properly combines extension classes with base class.'
extensions = ['frappe.tests.test_base_document.TestExtensionA', 'frappe.tests.test_base_document.TestExtensionB']
with self.patch_hooks({'extend_doctype_class': {'ToDo': extensions}}):
    extended_class = _get_extended_class(ToDo, 'ToDo')
    self.assertNotEqual(extended_class, ToDo)
    instance = extended_class({'doctype': 'ToDo'})
    self.assertTrue(hasattr(instance, 'extension_method_a'))
    self.assertTrue(hasattr(instance, 'extension_method_b'))
    self.assertEqual(instance.extension_method_a(), 'method_a')
    self.assertEqual(instance.extension_method_b(), 'method_b')
    mro_classes = [cls.__name__ for cls in extended_class.__mro__]
    self.assertIn('TestExtensionB', mro_classes)
    self.assertIn('TestExtensionA', mro_classes)
    self.assertIn('ToDo', mro_classes)
    idx_b = mro_classes.index('TestExtensionB')
    idx_a = mro_classes.index('TestExtensionA')
    idx_base = mro_classes.index('ToDo')
    self.assertLess(idx_b, idx_a)
    self.assertLess(idx_a, idx_base)
```

## Next Steps


---

*Source: test_base_document.py:55 | Complexity: Advanced | Last updated: 2026-02-04*