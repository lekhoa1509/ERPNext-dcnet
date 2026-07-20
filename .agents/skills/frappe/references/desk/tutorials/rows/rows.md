# How To: Rows

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test rows

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign note = self.insert_note(...)

```python
note = self.insert_note()
```

### Step 2: Call note.append()

```python
note.append('seen_by', {'user': 'Administrator'})
```

### Step 3: Call note.save()

```python
note.save(ignore_version=False)
```

### Step 4: Assign version = frappe.get_doc(...)

```python
version = frappe.get_doc('Version', dict(docname=note.name))
```

### Step 5: Assign data = version.get_data(...)

```python
data = version.get_data()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(data.get('added')), 1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(data.get('removed')), 0)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(len(data.get('changed')), 0)
```

### Step 9: Assign unknown.user = 'Guest'

```python
note.seen_by[0].user = 'Guest'
```

### Step 10: Call note.save()

```python
note.save(ignore_version=False)
```

### Step 11: Assign version = frappe.get_doc(...)

```python
version = frappe.get_doc('Version', dict(docname=note.name))
```

### Step 12: Assign data = version.get_data(...)

```python
data = version.get_data()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(len(data.get('row_changed')), 1)
```

### Step 14: Assign note.seen_by = value

```python
note.seen_by = []
```

### Step 15: Call note.save()

```python
note.save(ignore_version=False)
```

### Step 16: Assign version = frappe.get_doc(...)

```python
version = frappe.get_doc('Version', dict(docname=note.name))
```

### Step 17: Assign data = version.get_data(...)

```python
data = version.get_data()
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(len(data.get('removed')), 1)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(row[0], 'seen_by')
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(row[1]['user'], 'Administrator')
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(row[0], 'seen_by')
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(row[1], 0)
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(row[2], note.seen_by[0].name)
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(row[3], [['user', 'Administrator', 'Guest']])
```

### Step 25: Call self.assertEqual()

```python
self.assertEqual(row[0], 'seen_by')
```

### Step 26: Call self.assertEqual()

```python
self.assertEqual(row[1]['user'], 'Guest')
```


## Complete Example

```python
# Workflow
note = self.insert_note()
note.append('seen_by', {'user': 'Administrator'})
note.save(ignore_version=False)
version = frappe.get_doc('Version', dict(docname=note.name))
data = version.get_data()
self.assertEqual(len(data.get('added')), 1)
self.assertEqual(len(data.get('removed')), 0)
self.assertEqual(len(data.get('changed')), 0)
for row in data.get('added'):
    self.assertEqual(row[0], 'seen_by')
    self.assertEqual(row[1]['user'], 'Administrator')
note.seen_by[0].user = 'Guest'
note.save(ignore_version=False)
version = frappe.get_doc('Version', dict(docname=note.name))
data = version.get_data()
self.assertEqual(len(data.get('row_changed')), 1)
for row in data.get('row_changed'):
    self.assertEqual(row[0], 'seen_by')
    self.assertEqual(row[1], 0)
    self.assertEqual(row[2], note.seen_by[0].name)
    self.assertEqual(row[3], [['user', 'Administrator', 'Guest']])
note.seen_by = []
note.save(ignore_version=False)
version = frappe.get_doc('Version', dict(docname=note.name))
data = version.get_data()
self.assertEqual(len(data.get('removed')), 1)
for row in data.get('removed'):
    self.assertEqual(row[0], 'seen_by')
    self.assertEqual(row[1]['user'], 'Guest')
```

## Next Steps


---

*Source: test_note.py:28 | Complexity: Advanced | Last updated: 2026-02-04*