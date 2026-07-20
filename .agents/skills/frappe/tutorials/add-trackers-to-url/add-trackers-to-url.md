# How To: Add Trackers To Url

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test add trackers to url

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

### Step 1: Assign url = 'https://example.com'

```python
url = 'https://example.com'
```

### Step 2: Assign source = 'test_source'

```python
source = 'test_source'
```

### Step 3: Assign campaign = 'test_campaign'

```python
campaign = 'test_campaign'
```

### Step 4: Assign medium = 'test_medium'

```python
medium = 'test_medium'
```

### Step 5: Assign content = 'test_content'

```python
content = 'test_content'
```

### Step 6: Assign expected = 'https://example.com?utm_source=test_source&utm_medium=test_medium&utm_campaign=test_campaign&utm_content=test_content'

```python
expected = 'https://example.com?utm_source=test_source&utm_medium=test_medium&utm_campaign=test_campaign&utm_content=test_content'
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(result, expected)
```

### Step 8: Assign mock_get_value.side_effect = value

```python
mock_get_value.side_effect = lambda *args: args[1]
```

### Step 9: Assign result = add_trackers_to_url(...)

```python
result = add_trackers_to_url(url, source, campaign, medium, content)
```


## Complete Example

```python
# Workflow
url = 'https://example.com'
source = 'test_source'
campaign = 'test_campaign'
medium = 'test_medium'
content = 'test_content'
with patch('frappe.db.get_value') as mock_get_value:
    mock_get_value.side_effect = lambda *args: args[1]
    result = add_trackers_to_url(url, source, campaign, medium, content)
expected = 'https://example.com?utm_source=test_source&utm_medium=test_medium&utm_campaign=test_campaign&utm_content=test_content'
self.assertEqual(result, expected)
```

## Next Steps


---

*Source: test_utils.py:1583 | Complexity: Advanced | Last updated: 2026-02-04*