# How To: Parse And Map Trackers From Url

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test parse and map trackers from url

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

### Step 1: Assign url = 'https://example.com?utm_source=test_source&utm_medium=test_medium&utm_campaign=test_campaign&utm_content=test_content'

```python
url = 'https://example.com?utm_source=test_source&utm_medium=test_medium&utm_campaign=test_campaign&utm_content=test_content'
```

### Step 2: Assign expected = value

```python
expected = {'utm_source': 'test_source', 'utm_medium': 'test_medium', 'utm_campaign': 'test_campaign', 'utm_content': 'test_content'}
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(result, expected)
```

### Step 4: Assign mock_get_value.return_value = None

```python
mock_get_value.return_value = None
```

### Step 5: Assign result = parse_and_map_trackers_from_url(...)

```python
result = parse_and_map_trackers_from_url(url)
```


## Complete Example

```python
# Workflow
url = 'https://example.com?utm_source=test_source&utm_medium=test_medium&utm_campaign=test_campaign&utm_content=test_content'
with patch('frappe.db.get_value') as mock_get_value:
    mock_get_value.return_value = None
    result = parse_and_map_trackers_from_url(url)
expected = {'utm_source': 'test_source', 'utm_medium': 'test_medium', 'utm_campaign': 'test_campaign', 'utm_content': 'test_content'}
self.assertEqual(result, expected)
```

## Next Steps


---

*Source: test_utils.py:1597 | Complexity: Intermediate | Last updated: 2026-02-04*