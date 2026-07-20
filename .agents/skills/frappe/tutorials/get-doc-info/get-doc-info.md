# How To: Get Doc Info

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get doc info

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.custom.doctype.property_setter.property_setter`
- `frappe.desk.form.load`
- `frappe.tests`
- `frappe.tests.test_helpers`
- `frappe.utils.file_manager`


## Step-by-Step Guide

### Step 1: Assign note = frappe.new_doc(...)

```python
note = frappe.new_doc('Note')
```

### Step 2: Assign note.content = 'some content'

```python
note.content = 'some content'
```

### Step 3: Assign note.title = frappe.generate_hash(...)

```python
note.title = frappe.generate_hash(length=20)
```

### Step 4: Call note.insert()

```python
note.insert()
```

### Step 5: Assign note.content = 'new content'

```python
note.content = 'new content'
```

### Step 6: Call note.save()

```python
note.save(ignore_version=False)
```

### Step 7: Call note.add_comment()

```python
note.add_comment(text='test')
```

### Step 8: Call note.add_tag()

```python
note.add_tag('test_tag')
```

### Step 9: Call note.add_tag()

```python
note.add_tag('more_tag')
```

### Step 10: Call save_file()

```python
save_file('test_file', b'', note.doctype, note.name, decode=True)
```

### Step 11: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'Communication', 'communication_type': 'Communication', 'content': 'test email', 'reference_doctype': note.doctype, 'reference_name': note.name}).insert()
```

### Step 12: Call get_docinfo()

```python
get_docinfo(note)
```

### Step 13: Assign docinfo = value

```python
docinfo = frappe.response['docinfo']
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(len(docinfo.comments), 1)
```

### Step 15: Call self.assertIn()

```python
self.assertIn('test', docinfo.comments[0].content)
```

### Step 16: Call self.assertGreaterEqual()

```python
self.assertGreaterEqual(len(docinfo.versions), 1)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(set(docinfo.tags.split(',')), {'more_tag', 'test_tag'})
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(len(docinfo.attachments), 1)
```

### Step 19: Call self.assertIn()

```python
self.assertIn('test_file', docinfo.attachments[0].file_name)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(len(docinfo.communications), 1)
```

### Step 21: Call self.assertIn()

```python
self.assertIn('email', docinfo.communications[0].content)
```

### Step 22: Call note.delete()

```python
note.delete()
```


## Complete Example

```python
# Workflow
note = frappe.new_doc('Note')
note.content = 'some content'
note.title = frappe.generate_hash(length=20)
note.insert()
note.content = 'new content'
note.save(ignore_version=False)
note.add_comment(text='test')
note.add_tag('test_tag')
note.add_tag('more_tag')
save_file('test_file', b'', note.doctype, note.name, decode=True)
frappe.get_doc({'doctype': 'Communication', 'communication_type': 'Communication', 'content': 'test email', 'reference_doctype': note.doctype, 'reference_name': note.name}).insert()
get_docinfo(note)
docinfo = frappe.response['docinfo']
self.assertEqual(len(docinfo.comments), 1)
self.assertIn('test', docinfo.comments[0].content)
self.assertGreaterEqual(len(docinfo.versions), 1)
self.assertEqual(set(docinfo.tags.split(',')), {'more_tag', 'test_tag'})
self.assertEqual(len(docinfo.attachments), 1)
self.assertIn('test_file', docinfo.attachments[0].file_name)
self.assertEqual(len(docinfo.communications), 1)
self.assertIn('email', docinfo.communications[0].content)
note.delete()
```

## Next Steps


---

*Source: test_form_load.py:151 | Complexity: Advanced | Last updated: 2026-02-04*