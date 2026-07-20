# How To: Js Parser Arg Capturing

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Get non-flattened args in correct order so 3rd arg if present is always context.

## Prerequisites

**Required Modules:**
- `os`
- `textwrap`
- `random`
- `unittest.mock`
- `frappe`
- `frappe.translate`
- `frappe`
- `frappe.gettext.extractors.javascript`
- `frappe.tests`
- `frappe.translate`
- `frappe.utils`
- `pathlib`


## Step-by-Step Guide

### Step 1: 'Get non-flattened args in correct order so 3rd arg if present is always context.'

```python
'Get non-flattened args in correct order so 3rd arg if present is always context.'
```

### Step 2: Assign args = get_args(...)

```python
args = get_args('__("attr with", ["format", "replacements"], "context")')
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(args, ('attr with', None, 'context'))
```

### Step 4: Assign args = get_args(...)

```python
args = get_args('__("attr with", ["format", "replacements"])')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(args, 'attr with')
```

### Step 6: Assign args = get_args(...)

```python
args = get_args('__("attr with", null, "context")')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(args, ('attr with', None, 'context'))
```

### Step 8: Assign args = get_args(...)

```python
args = get_args('__(\n\t\t\t\t"Multiline translation with format replacements and context {0} {1}",\n\t\t\t\t[\n\t\t\t\t\t"format",\n\t\t\t\t\tcall("replacements", {\n\t\t\t\t\t\t"key": "value"\n\t\t\t\t\t}),\n\t\t\t\t],\n\t\t\t\t"context"\n\t\t\t)')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(args, ('Multiline translation with format replacements and context {0} {1}', None, 'context'))
```

### Step 10: Assign args = get_args(...)

```python
args = get_args('__(\n\t\t\t\t"Multiline translation with format replacements and no context {0} {1}",\n\t\t\t\t[\n\t\t\t\t\t"format",\n\t\t\t\t\tcall("replacements", {\n\t\t\t\t\t\t"key": "value"\n\t\t\t\t\t}),\n\t\t\t\t],\n\t\t\t)')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(args, ('Multiline translation with format replacements and no context {0} {1}', None))
```

### Step 12: Assign unknown = next(...)

```python
*__, args = next(extract_javascript(code))
```


## Complete Example

```python
# Workflow
'Get non-flattened args in correct order so 3rd arg if present is always context.'

def get_args(code):
    *__, args = next(extract_javascript(code))
    return args
args = get_args('__("attr with", ["format", "replacements"], "context")')
self.assertEqual(args, ('attr with', None, 'context'))
args = get_args('__("attr with", ["format", "replacements"])')
self.assertEqual(args, 'attr with')
args = get_args('__("attr with", null, "context")')
self.assertEqual(args, ('attr with', None, 'context'))
args = get_args('__(\n\t\t\t\t"Multiline translation with format replacements and context {0} {1}",\n\t\t\t\t[\n\t\t\t\t\t"format",\n\t\t\t\t\tcall("replacements", {\n\t\t\t\t\t\t"key": "value"\n\t\t\t\t\t}),\n\t\t\t\t],\n\t\t\t\t"context"\n\t\t\t)')
self.assertEqual(args, ('Multiline translation with format replacements and context {0} {1}', None, 'context'))
args = get_args('__(\n\t\t\t\t"Multiline translation with format replacements and no context {0} {1}",\n\t\t\t\t[\n\t\t\t\t\t"format",\n\t\t\t\t\tcall("replacements", {\n\t\t\t\t\t\t"key": "value"\n\t\t\t\t\t}),\n\t\t\t\t],\n\t\t\t)')
self.assertEqual(args, ('Multiline translation with format replacements and no context {0} {1}', None))
```

## Next Steps


---

*Source: test_translate.py:274 | Complexity: Advanced | Last updated: 2026-02-04*