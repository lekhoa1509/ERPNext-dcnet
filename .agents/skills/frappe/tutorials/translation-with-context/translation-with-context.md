# How To: Translation With Context

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test translation with context

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

### Step 1: Assign t1 = frappe.new_doc(...)

```python
t1 = frappe.new_doc('Translation')
```

### Step 2: Assign t1.language = 'fr'

```python
t1.language = 'fr'
```

### Step 3: Assign t1.source_text = 'Change'

```python
t1.source_text = 'Change'
```

### Step 4: Assign t1.translated_text = 'Changement'

```python
t1.translated_text = 'Changement'
```

### Step 5: Call t1.save()

```python
t1.save()
```

### Step 6: Assign t2 = frappe.new_doc(...)

```python
t2 = frappe.new_doc('Translation')
```

### Step 7: Assign t2.language = 'fr'

```python
t2.language = 'fr'
```

### Step 8: Assign t2.source_text = 'Change'

```python
t2.source_text = 'Change'
```

### Step 9: Assign t2.translated_text = 'la monnaie'

```python
t2.translated_text = 'la monnaie'
```

### Step 10: Assign t2.context = 'Coins'

```python
t2.context = 'Coins'
```

### Step 11: Call t2.save()

```python
t2.save()
```

### Step 12: Assign frappe.local.lang = 'fr'

```python
frappe.local.lang = 'fr'
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(_('Change'), 'Changement')
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(_('Change', context='Coins'), 'la monnaie')
```

### Step 15: Call t1.delete()

```python
t1.delete()
```

### Step 16: Call t2.delete()

```python
t2.delete()
```


## Complete Example

```python
# Workflow
t1 = frappe.new_doc('Translation')
t1.language = 'fr'
t1.source_text = 'Change'
t1.translated_text = 'Changement'
t1.save()
t2 = frappe.new_doc('Translation')
t2.language = 'fr'
t2.source_text = 'Change'
t2.translated_text = 'la monnaie'
t2.context = 'Coins'
t2.save()
frappe.local.lang = 'fr'
self.assertEqual(_('Change'), 'Changement')
self.assertEqual(_('Change', context='Coins'), 'la monnaie')
t1.delete()
t2.delete()
```

## Next Steps


---

*Source: test_translate.py:96 | Complexity: Advanced | Last updated: 2026-02-04*