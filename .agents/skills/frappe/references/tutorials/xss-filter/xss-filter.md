# How To: Xss Filter

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test xss filter

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

### Step 1: Assign d = self.test_insert(...)

```python
d = self.test_insert()
```

### Step 2: Assign xss = '<script>alert("XSS")</script>'

```python
xss = '<script>alert("XSS")</script>'
```

### Step 3: Assign escaped_xss = xss.replace.replace(...)

```python
escaped_xss = xss.replace('<', '&lt;').replace('>', '&gt;')
```

### Step 4: Call d.save()

```python
d.save()
```

### Step 5: Call d.reload()

```python
d.reload()
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(xss not in d.subject)
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(escaped_xss in d.subject)
```

### Step 8: Assign xss = '<div onload="alert("XSS")">Test</div>'

```python
xss = '<div onload="alert("XSS")">Test</div>'
```

### Step 9: Assign escaped_xss = '<div>Test</div>'

```python
escaped_xss = '<div>Test</div>'
```

### Step 10: Call d.save()

```python
d.save()
```

### Step 11: Call d.reload()

```python
d.reload()
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue(xss not in d.subject)
```

### Step 13: Call self.assertTrue()

```python
self.assertTrue(escaped_xss in d.subject)
```

### Step 14: Assign xss = '<div style="something: doesn\'t work; color: red;">Test</div>'

```python
xss = '<div style="something: doesn\'t work; color: red;">Test</div>'
```

### Step 15: Assign escaped_xss = '<div style="">Test</div>'

```python
escaped_xss = '<div style="">Test</div>'
```

### Step 16: Call d.save()

```python
d.save()
```

### Step 17: Call d.reload()

```python
d.reload()
```

### Step 18: Call self.assertTrue()

```python
self.assertTrue(xss not in d.subject)
```

### Step 19: Call self.assertTrue()

```python
self.assertTrue(escaped_xss in d.subject)
```


## Complete Example

```python
# Workflow
d = self.test_insert()
xss = '<script>alert("XSS")</script>'
escaped_xss = xss.replace('<', '&lt;').replace('>', '&gt;')
d.subject += xss
d.save()
d.reload()
self.assertTrue(xss not in d.subject)
self.assertTrue(escaped_xss in d.subject)
xss = '<div onload="alert("XSS")">Test</div>'
escaped_xss = '<div>Test</div>'
d.subject += xss
d.save()
d.reload()
self.assertTrue(xss not in d.subject)
self.assertTrue(escaped_xss in d.subject)
xss = '<div style="something: doesn\'t work; color: red;">Test</div>'
escaped_xss = '<div style="">Test</div>'
d.subject += xss
d.save()
d.reload()
self.assertTrue(xss not in d.subject)
self.assertTrue(escaped_xss in d.subject)
```

## Next Steps


---

*Source: test_document.py:263 | Complexity: Advanced | Last updated: 2026-02-04*