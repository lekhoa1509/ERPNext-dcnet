# How To: Base Class Set Correctly On Has Web View Change

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test base class set correctly on has web view change

## Prerequisites

**Required Modules:**
- `inspect`
- `contextlib`
- `copy`
- `datetime`
- `unittest.mock`
- `frappe`
- `frappe.app`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.doctype.user.user`
- `frappe.desk.doctype.note.note`
- `frappe.model.document`
- `frappe.model.naming`
- `frappe.tests`
- `frappe.utils`
- `frappe.website.serve`
- `frappe.desk.doctype.event.event`
- `pathlib`
- `frappe.modules.utils`
- `frappe.model.document`


## Step-by-Step Guide

### Step 1: Assign frappe.flags.allow_doctype_export = True

```python
frappe.flags.allow_doctype_export = True
```

### Step 2: Call frappe.delete_doc_if_exists()

```python
frappe.delete_doc_if_exists('DocType', 'Test WebViewDocType', force=1)
```

### Step 3: Assign test_doctype = new_doctype(...)

```python
test_doctype = new_doctype('Test WebViewDocType', custom=0, fields=[{'fieldname': 'test_field', 'fieldtype': 'Data'}, {'fieldname': 'route', 'fieldtype': 'Data'}, {'fieldname': 'is_published', 'fieldtype': 'Check'}])
```

### Step 4: Call test_doctype.insert()

```python
test_doctype.insert()
```

### Step 5: Assign doc_path = Path(...)

```python
doc_path = Path(get_doc_path(test_doctype.module, test_doctype.doctype, test_doctype.name))
```

### Step 6: Assign controller_file_path = value

```python
controller_file_path = doc_path / f'{scrub(test_doctype.name)}.py'
```

### Step 7: Assign test_doctype.has_web_view = 1

```python
test_doctype.has_web_view = 1
```

### Step 8: Assign test_doctype.is_published_field = 'is_published'

```python
test_doctype.is_published_field = 'is_published'
```

### Step 9: Call test_doctype.save()

```python
test_doctype.save()
```

### Step 10: Assign test_doctype.has_web_view = 0

```python
test_doctype.has_web_view = 0
```

### Step 11: Call test_doctype.save()

```python
test_doctype.save()
```

### Step 12: Assign file_content = f.read(...)

```python
file_content = f.read()
```

### Step 13: Call self.assertIn()

```python
self.assertIn('import WebsiteGenerator', file_content, '`WebsiteGenerator` not imported when web view is enabled!')
```

### Step 14: Call self.assertIn()

```python
self.assertIn('(WebsiteGenerator)', file_content, '`Document` class not replaced with `WebsiteGenerator` when web view is enabled!')
```

### Step 15: Assign file_content = f.read(...)

```python
file_content = f.read()
```

### Step 16: Call self.assertIn()

```python
self.assertIn('import Document', file_content, '`Document` not imported when web view is disabled!')
```

### Step 17: Call self.assertIn()

```python
self.assertIn('(Document)', file_content, '`WebsiteGenerator` class not replaced with `Document` when web view is disabled!')
```


## Complete Example

```python
# Workflow
from pathlib import Path
from frappe.modules.utils import get_doc_path, scrub
frappe.flags.allow_doctype_export = True
frappe.delete_doc_if_exists('DocType', 'Test WebViewDocType', force=1)
test_doctype = new_doctype('Test WebViewDocType', custom=0, fields=[{'fieldname': 'test_field', 'fieldtype': 'Data'}, {'fieldname': 'route', 'fieldtype': 'Data'}, {'fieldname': 'is_published', 'fieldtype': 'Check'}])
test_doctype.insert()
doc_path = Path(get_doc_path(test_doctype.module, test_doctype.doctype, test_doctype.name))
controller_file_path = doc_path / f'{scrub(test_doctype.name)}.py'
test_doctype.has_web_view = 1
test_doctype.is_published_field = 'is_published'
test_doctype.save()
with open(controller_file_path) as f:
    file_content = f.read()
    self.assertIn('import WebsiteGenerator', file_content, '`WebsiteGenerator` not imported when web view is enabled!')
    self.assertIn('(WebsiteGenerator)', file_content, '`Document` class not replaced with `WebsiteGenerator` when web view is enabled!')
test_doctype.has_web_view = 0
test_doctype.save()
with open(controller_file_path) as f:
    file_content = f.read()
    self.assertIn('import Document', file_content, '`Document` not imported when web view is disabled!')
    self.assertIn('(Document)', file_content, '`WebsiteGenerator` class not replaced with `Document` when web view is disabled!')
```

## Next Steps


---

*Source: test_document.py:583 | Complexity: Advanced | Last updated: 2026-02-04*