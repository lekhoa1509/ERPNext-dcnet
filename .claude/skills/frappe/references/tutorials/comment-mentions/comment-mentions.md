# How To: Comment Mentions

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test comment mentions

## Prerequisites

**Required Modules:**
- `json`
- `time`
- `contextlib`
- `unittest.mock`
- `urllib.parse`
- `werkzeug.http`
- `frappe`
- `frappe.exceptions`
- `frappe.core.doctype.user.user`
- `frappe.desk.notifications`
- `frappe.frappeclient`
- `frappe.model.delete_doc`
- `frappe.tests`
- `frappe.tests.classes.context_managers`
- `frappe.tests.test_api`
- `frappe.tests.utils`
- `frappe.utils`
- `frappe.www.login`
- `frappe.website.utils`
- `frappe.auth`
- `frappe.utils`
- `frappe.desk.form.load`
- `frappe.utils.modules`


## Step-by-Step Guide

### Step 1: Assign comment = '\n\t\t\t<span class="mention" data-id="test.comment@example.com" data-value="Test" data-denotation-char="@">\n\t\t\t\t<span><span class="ql-mention-denotation-char">@</span>Test</span>\n\t\t\t</span>\n\t\t'

```python
comment = '\n\t\t\t<span class="mention" data-id="test.comment@example.com" data-value="Test" data-denotation-char="@">\n\t\t\t\t<span><span class="ql-mention-denotation-char">@</span>Test</span>\n\t\t\t</span>\n\t\t'
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual(extract_mentions(comment)[0], 'test.comment@example.com')
```

### Step 3: Assign comment = '\n\t\t\t<div>\n\t\t\t\tTesting comment,\n\t\t\t\t<span class="mention" data-id="test.comment@example.com" data-value="Test" data-denotation-char="@">\n\t\t\t\t\t<span><span class="ql-mention-denotation-char">@</span>Test</span>\n\t\t\t\t</span>\n\t\t\t\tplease check\n\t\t\t</div>\n\t\t'

```python
comment = '\n\t\t\t<div>\n\t\t\t\tTesting comment,\n\t\t\t\t<span class="mention" data-id="test.comment@example.com" data-value="Test" data-denotation-char="@">\n\t\t\t\t\t<span><span class="ql-mention-denotation-char">@</span>Test</span>\n\t\t\t\t</span>\n\t\t\t\tplease check\n\t\t\t</div>\n\t\t'
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(extract_mentions(comment)[0], 'test.comment@example.com')
```

### Step 5: Assign comment = '\n\t\t\t<div>\n\t\t\t\tTesting comment for\n\t\t\t\t<span class="mention" data-id="test_user@example.com" data-value="Test" data-denotation-char="@">\n\t\t\t\t\t<span><span class="ql-mention-denotation-char">@</span>Test</span>\n\t\t\t\t</span>\n\t\t\t\tand\n\t\t\t\t<span class="mention" data-id="test.again@example1.com" data-value="Test" data-denotation-char="@">\n\t\t\t\t\t<span><span class="ql-mention-denotation-char">@</span>Test</span>\n\t\t\t\t</span>\n\t\t\t\tplease check\n\t\t\t</div>\n\t\t'

```python
comment = '\n\t\t\t<div>\n\t\t\t\tTesting comment for\n\t\t\t\t<span class="mention" data-id="test_user@example.com" data-value="Test" data-denotation-char="@">\n\t\t\t\t\t<span><span class="ql-mention-denotation-char">@</span>Test</span>\n\t\t\t\t</span>\n\t\t\t\tand\n\t\t\t\t<span class="mention" data-id="test.again@example1.com" data-value="Test" data-denotation-char="@">\n\t\t\t\t\t<span><span class="ql-mention-denotation-char">@</span>Test</span>\n\t\t\t\t</span>\n\t\t\t\tplease check\n\t\t\t</div>\n\t\t'
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(extract_mentions(comment)[0], 'test_user@example.com')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(extract_mentions(comment)[1], 'test.again@example1.com')
```

### Step 8: Call frappe.delete_doc()

```python
frappe.delete_doc('User Group', 'Team')
```

### Step 9: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc({'doctype': 'User Group', 'name': 'Team', 'user_group_members': [{'user': 'test@example.com'}, {'user': 'test1@example.com'}]})
```

### Step 10: Call doc.insert()

```python
doc.insert()
```

### Step 11: Assign comment = '\n\t\t\t<div>\n\t\t\t\tTesting comment for\n\t\t\t\t<span class="mention" data-id="Team" data-value="Team" data-is-group="true" data-denotation-char="@">\n\t\t\t\t\t<span><span class="ql-mention-denotation-char">@</span>Team</span>\n\t\t\t\t</span> and\n\t\t\t\t<span class="mention" data-id="Unknown Team" data-value="Unknown Team" data-is-group="true"\n\t\t\t\tdata-denotation-char="@">\n\t\t\t\t\t<span><span class="ql-mention-denotation-char">@</span>Unknown Team</span>\n\t\t\t\t</span><!-- this should be ignored-->\n\t\t\t\tplease check\n\t\t\t</div>\n\t\t'

```python
comment = '\n\t\t\t<div>\n\t\t\t\tTesting comment for\n\t\t\t\t<span class="mention" data-id="Team" data-value="Team" data-is-group="true" data-denotation-char="@">\n\t\t\t\t\t<span><span class="ql-mention-denotation-char">@</span>Team</span>\n\t\t\t\t</span> and\n\t\t\t\t<span class="mention" data-id="Unknown Team" data-value="Unknown Team" data-is-group="true"\n\t\t\t\tdata-denotation-char="@">\n\t\t\t\t\t<span><span class="ql-mention-denotation-char">@</span>Unknown Team</span>\n\t\t\t\t</span><!-- this should be ignored-->\n\t\t\t\tplease check\n\t\t\t</div>\n\t\t'
```

### Step 12: Call self.assertListEqual()

```python
self.assertListEqual(extract_mentions(comment), ['test@example.com', 'test1@example.com'])
```


## Complete Example

```python
# Workflow
comment = '\n\t\t\t<span class="mention" data-id="test.comment@example.com" data-value="Test" data-denotation-char="@">\n\t\t\t\t<span><span class="ql-mention-denotation-char">@</span>Test</span>\n\t\t\t</span>\n\t\t'
self.assertEqual(extract_mentions(comment)[0], 'test.comment@example.com')
comment = '\n\t\t\t<div>\n\t\t\t\tTesting comment,\n\t\t\t\t<span class="mention" data-id="test.comment@example.com" data-value="Test" data-denotation-char="@">\n\t\t\t\t\t<span><span class="ql-mention-denotation-char">@</span>Test</span>\n\t\t\t\t</span>\n\t\t\t\tplease check\n\t\t\t</div>\n\t\t'
self.assertEqual(extract_mentions(comment)[0], 'test.comment@example.com')
comment = '\n\t\t\t<div>\n\t\t\t\tTesting comment for\n\t\t\t\t<span class="mention" data-id="test_user@example.com" data-value="Test" data-denotation-char="@">\n\t\t\t\t\t<span><span class="ql-mention-denotation-char">@</span>Test</span>\n\t\t\t\t</span>\n\t\t\t\tand\n\t\t\t\t<span class="mention" data-id="test.again@example1.com" data-value="Test" data-denotation-char="@">\n\t\t\t\t\t<span><span class="ql-mention-denotation-char">@</span>Test</span>\n\t\t\t\t</span>\n\t\t\t\tplease check\n\t\t\t</div>\n\t\t'
self.assertEqual(extract_mentions(comment)[0], 'test_user@example.com')
self.assertEqual(extract_mentions(comment)[1], 'test.again@example1.com')
frappe.delete_doc('User Group', 'Team')
doc = frappe.get_doc({'doctype': 'User Group', 'name': 'Team', 'user_group_members': [{'user': 'test@example.com'}, {'user': 'test1@example.com'}]})
doc.insert()
comment = '\n\t\t\t<div>\n\t\t\t\tTesting comment for\n\t\t\t\t<span class="mention" data-id="Team" data-value="Team" data-is-group="true" data-denotation-char="@">\n\t\t\t\t\t<span><span class="ql-mention-denotation-char">@</span>Team</span>\n\t\t\t\t</span> and\n\t\t\t\t<span class="mention" data-id="Unknown Team" data-value="Unknown Team" data-is-group="true"\n\t\t\t\tdata-denotation-char="@">\n\t\t\t\t\t<span><span class="ql-mention-denotation-char">@</span>Unknown Team</span>\n\t\t\t\t</span><!-- this should be ignored-->\n\t\t\t\tplease check\n\t\t\t</div>\n\t\t'
self.assertListEqual(extract_mentions(comment), ['test@example.com', 'test1@example.com'])
```

## Next Steps


---

*Source: test_user.py:223 | Complexity: Advanced | Last updated: 2026-02-04*