# How To: Parse Github Url

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test parse github url

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

### Step 1: Assign unknown = parse_github_url(...)

```python
owner, repo = parse_github_url('https://github.com/frappe/erpnext.git')
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual(owner, 'frappe')
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(repo, 'erpnext')
```

### Step 4: Assign unknown = parse_github_url(...)

```python
owner, repo = parse_github_url('https://github.com/frappe/erpnext')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(owner, 'frappe')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(repo, 'erpnext')
```

### Step 7: Assign unknown = parse_github_url(...)

```python
owner, repo = parse_github_url('git@github.com:frappe/erpnext.git')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(owner, 'frappe')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(repo, 'erpnext')
```

### Step 10: Assign unknown = parse_github_url(...)

```python
owner, repo = parse_github_url('https://gitlab.com/gitlab-org/gitlab')
```

### Step 11: Call self.assertIsNone()

```python
self.assertIsNone(owner)
```

### Step 12: Call self.assertIsNone()

```python
self.assertIsNone(repo)
```

### Step 13: Call self.assertRaises()

```python
self.assertRaises(ValueError, parse_github_url, remote_url=None)
```


## Complete Example

```python
# Workflow
owner, repo = parse_github_url('https://github.com/frappe/erpnext.git')
self.assertEqual(owner, 'frappe')
self.assertEqual(repo, 'erpnext')
owner, repo = parse_github_url('https://github.com/frappe/erpnext')
self.assertEqual(owner, 'frappe')
self.assertEqual(repo, 'erpnext')
owner, repo = parse_github_url('git@github.com:frappe/erpnext.git')
self.assertEqual(owner, 'frappe')
self.assertEqual(repo, 'erpnext')
owner, repo = parse_github_url('https://gitlab.com/gitlab-org/gitlab')
self.assertIsNone(owner)
self.assertIsNone(repo)
self.assertRaises(ValueError, parse_github_url, remote_url=None)
```

## Next Steps


---

*Source: test_utils.py:1552 | Complexity: Advanced | Last updated: 2026-02-04*