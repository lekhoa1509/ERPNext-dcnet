# How To: Clean Email Html

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test clean email html

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

### Step 1: Assign sample = '<script>a=b</script><h1>Hello</h1><p>Para</p>'

```python
sample = '<script>a=b</script><h1>Hello</h1><p>Para</p>'
```

### Step 2: Assign clean = clean_email_html(...)

```python
clean = clean_email_html(sample)
```

### Step 3: Call self.assertFalse()

```python
self.assertFalse('<script>' in clean)
```

### Step 4: Call self.assertTrue()

```python
self.assertTrue('<h1>Hello</h1>' in clean)
```

### Step 5: Assign sample = '<style>body { font-family: Arial }</style><h1>Hello</h1><p>Para</p>'

```python
sample = '<style>body { font-family: Arial }</style><h1>Hello</h1><p>Para</p>'
```

### Step 6: Assign clean = clean_email_html(...)

```python
clean = clean_email_html(sample)
```

### Step 7: Call self.assertFalse()

```python
self.assertFalse('<style>' in clean)
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue('<h1>Hello</h1>' in clean)
```

### Step 9: Assign sample = '<h1>Hello</h1><p>Para</p><a href="http://test.com">text</a>'

```python
sample = '<h1>Hello</h1><p>Para</p><a href="http://test.com">text</a>'
```

### Step 10: Assign clean = clean_email_html(...)

```python
clean = clean_email_html(sample)
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue('<h1>Hello</h1>' in clean)
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue('<a href="http://test.com">text</a>' in clean)
```


## Complete Example

```python
# Workflow
from frappe.utils.html_utils import clean_email_html
sample = '<script>a=b</script><h1>Hello</h1><p>Para</p>'
clean = clean_email_html(sample)
self.assertFalse('<script>' in clean)
self.assertTrue('<h1>Hello</h1>' in clean)
sample = '<style>body { font-family: Arial }</style><h1>Hello</h1><p>Para</p>'
clean = clean_email_html(sample)
self.assertFalse('<style>' in clean)
self.assertTrue('<h1>Hello</h1>' in clean)
sample = '<h1>Hello</h1><p>Para</p><a href="http://test.com">text</a>'
clean = clean_email_html(sample)
self.assertTrue('<h1>Hello</h1>' in clean)
self.assertTrue('<a href="http://test.com">text</a>' in clean)
```

## Next Steps


---

*Source: test_utils.py:495 | Complexity: Advanced | Last updated: 2026-02-04*