# How To: Comment Creation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test comment creation

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.templates.includes.comments.comments`
- `frappe.tests`
- `frappe.tests.test_helpers`
- `frappe.tests.test_model_utils`


## Step-by-Step Guide

### Step 1: Assign test_doc = frappe.get_doc(...)

```python
test_doc = frappe.get_doc(doctype='ToDo', description='test')
```

### Step 2: Call test_doc.insert()

```python
test_doc.insert()
```

### Step 3: Assign comment = test_doc.add_comment(...)

```python
comment = test_doc.add_comment('Comment', 'test comment')
```

### Step 4: Call test_doc.reload()

```python
test_doc.reload()
```

### Step 5: Assign comments = json.loads(...)

```python
comments = json.loads(test_doc.get('_comments'))
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(comments[0].get('name'), comment.name)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(comments[0].get('comment'), comment.content)
```

### Step 8: Assign counts = frappe.get_all(...)

```python
counts = frappe.get_all('ToDo', {'name': test_doc.name}, ['*'], with_comment_count=True)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(counts[0]._comment_count, 1)
```

### Step 10: Assign comment = test_doc.add_comment(...)

```python
comment = test_doc.add_comment('Comment', 'test comment')
```

### Step 11: Assign counts = frappe.get_all(...)

```python
counts = frappe.get_all('ToDo', {'name': test_doc.name}, ['*'], with_comment_count=True)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(counts[0]._comment_count, 2)
```

### Step 13: Assign comment_1 = value

```python
comment_1 = frappe.get_all('Comment', fields=['*'], filters=dict(reference_doctype=test_doc.doctype, reference_name=test_doc.name))[0]
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(comment_1.content, 'test comment')
```


## Complete Example

```python
# Workflow
test_doc = frappe.get_doc(doctype='ToDo', description='test')
test_doc.insert()
comment = test_doc.add_comment('Comment', 'test comment')
test_doc.reload()
comments = json.loads(test_doc.get('_comments'))
self.assertEqual(comments[0].get('name'), comment.name)
self.assertEqual(comments[0].get('comment'), comment.content)
counts = frappe.get_all('ToDo', {'name': test_doc.name}, ['*'], with_comment_count=True)
self.assertEqual(counts[0]._comment_count, 1)
comment = test_doc.add_comment('Comment', 'test comment')
counts = frappe.get_all('ToDo', {'name': test_doc.name}, ['*'], with_comment_count=True)
self.assertEqual(counts[0]._comment_count, 2)
comment_1 = frappe.get_all('Comment', fields=['*'], filters=dict(reference_doctype=test_doc.doctype, reference_name=test_doc.name))[0]
self.assertEqual(comment_1.content, 'test comment')
```

## Next Steps


---

*Source: test_comment.py:18 | Complexity: Advanced | Last updated: 2026-02-04*