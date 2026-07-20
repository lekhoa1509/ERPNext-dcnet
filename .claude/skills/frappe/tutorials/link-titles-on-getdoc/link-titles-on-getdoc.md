# How To: Link Titles On Getdoc

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that link titles are added to the doctype on getdoc

## Prerequisites

**Required Modules:**
- `io`
- `json`
- `os`
- `sys`
- `datetime`
- `decimal`
- `enum`
- `io`
- `mimetypes`
- `unittest.mock`
- `hypothesis`
- `hypothesis`
- `PIL`
- `frappe`
- `frappe.installer`
- `frappe.model.document`
- `frappe.tests`
- `frappe.tests.utils`
- `frappe.utils`
- `frappe.utils.change_log`
- `frappe.utils.data`
- `frappe.utils.dateutils`
- `frappe.utils.diff`
- `frappe.utils.identicon`
- `frappe.utils.image`
- `frappe.utils.make_random`
- `frappe.utils.response`
- `frappe.utils.synchronization`
- `frappe.utils.typing_validations`
- `decimal`
- `decimal`
- `frappe.utils.html_utils`
- `frappe.utils.html_utils`
- `frappe`
- `frappe.utils.xlsxutils`
- `frappe.boot`
- `frappe.desk.form.load`
- `frappe.utils.lazy_loader`
- `unittest.mock`
- `frappe.core.doctype.doctype.doctype`


## Step-by-Step Guide

### Step 1: '\n\t\tTest that link titles are added to the doctype on getdoc\n\t\t'

```python
'\n\t\tTest that link titles are added to the doctype on getdoc\n\t\t'
```

### Step 2: Assign prop_setter = frappe.get_doc.insert(...)

```python
prop_setter = frappe.get_doc({'doctype': 'Property Setter', 'doc_type': 'User', 'property': 'show_title_field_in_link', 'property_type': 'Check', 'doctype_or_field': 'DocType', 'value': '1'}).insert()
```

### Step 3: Assign user = frappe.get_doc.insert(...)

```python
user = frappe.get_doc({'doctype': 'User', 'user_type': 'Website User', 'email': 'test_user_for_link_title@example.com', 'send_welcome_email': 0, 'first_name': 'Test User for Link Title'}).insert(ignore_permissions=True)
```

### Step 4: Assign todo = frappe.get_doc.insert(...)

```python
todo = frappe.get_doc({'doctype': 'ToDo', 'description': 'test-link-title-on-getdoc', 'allocated_to': user.name}).insert()
```

### Step 5: Call getdoc()

```python
getdoc('ToDo', todo.name)
```

### Step 6: Assign link_titles = value

```python
link_titles = frappe.local.response['_link_titles']
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(f'{user.doctype}::{user.name}' in link_titles)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(link_titles[f'{user.doctype}::{user.name}'], user.full_name)
```

### Step 9: Call todo.delete()

```python
todo.delete()
```

### Step 10: Call user.delete()

```python
user.delete()
```

### Step 11: Call prop_setter.delete()

```python
prop_setter.delete()
```


## Complete Example

```python
# Workflow
'\n\t\tTest that link titles are added to the doctype on getdoc\n\t\t'
prop_setter = frappe.get_doc({'doctype': 'Property Setter', 'doc_type': 'User', 'property': 'show_title_field_in_link', 'property_type': 'Check', 'doctype_or_field': 'DocType', 'value': '1'}).insert()
user = frappe.get_doc({'doctype': 'User', 'user_type': 'Website User', 'email': 'test_user_for_link_title@example.com', 'send_welcome_email': 0, 'first_name': 'Test User for Link Title'}).insert(ignore_permissions=True)
todo = frappe.get_doc({'doctype': 'ToDo', 'description': 'test-link-title-on-getdoc', 'allocated_to': user.name}).insert()
from frappe.desk.form.load import getdoc
getdoc('ToDo', todo.name)
link_titles = frappe.local.response['_link_titles']
self.assertTrue(f'{user.doctype}::{user.name}' in link_titles)
self.assertEqual(link_titles[f'{user.doctype}::{user.name}'], user.full_name)
todo.delete()
user.delete()
prop_setter.delete()
```

## Next Steps


---

*Source: test_utils.py:1070 | Complexity: Advanced | Last updated: 2026-02-04*