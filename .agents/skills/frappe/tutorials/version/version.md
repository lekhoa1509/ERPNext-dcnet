# How To: Version

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test version

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign note = self.insert_note(...)

```python
note = self.insert_note()
```

### Step 2: Assign note.title = 'test note 1'

```python
note.title = 'test note 1'
```

### Step 3: Assign note.content = '1'

```python
note.content = '1'
```

### Step 4: Call note.save()

```python
note.save(ignore_version=False)
```

### Step 5: Assign version = frappe.get_doc(...)

```python
version = frappe.get_doc('Version', dict(docname=note.name))
```

### Step 6: Assign data = version.get_data(...)

```python
data = version.get_data()
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(('title', 'test note', 'test note 1'), data['changed'])
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(('content', 'test note content', '1'), data['changed'])
```


## Complete Example

```python
# Workflow
note = self.insert_note()
note.title = 'test note 1'
note.content = '1'
note.save(ignore_version=False)
version = frappe.get_doc('Version', dict(docname=note.name))
data = version.get_data()
self.assertTrue(('title', 'test note', 'test note 1'), data['changed'])
self.assertTrue(('content', 'test note content', '1'), data['changed'])
```

## Next Steps


---

*Source: test_note.py:16 | Complexity: Advanced | Last updated: 2026-02-04*