# How To: Lazy Translations

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test lazy translations

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

### Step 1: Assign frappe.local.lang = 'de'

```python
frappe.local.lang = 'de'
```

### Step 2: Assign eager_translation = _(...)

```python
eager_translation = _('Communication')
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(str(_lazy_translations), eager_translation)
```

### Step 4: Call self.assertRaises()

```python
self.assertRaises(NotImplementedError, lambda: _lazy_translations == 'blah')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(_lazy_translations + 'A', eager_translation + 'A')
```

### Step 6: Assign x = _lazy_translations

```python
x = _lazy_translations
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(x, eager_translation + 'A')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(f'{_lazy_translations}', eager_translation)
```


## Complete Example

```python
# Workflow
frappe.local.lang = 'de'
eager_translation = _('Communication')
self.assertEqual(str(_lazy_translations), eager_translation)
self.assertRaises(NotImplementedError, lambda: _lazy_translations == 'blah')
self.assertEqual(_lazy_translations + 'A', eager_translation + 'A')
x = _lazy_translations
x += 'A'
self.assertEqual(x, eager_translation + 'A')
self.assertEqual(f'{_lazy_translations}', eager_translation)
```

## Next Steps


---

*Source: test_translate.py:117 | Complexity: Advanced | Last updated: 2026-02-04*