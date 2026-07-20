# How To: Is Allowed Referrer

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test is allowed referrer

## Prerequisites

**Required Modules:**
- `datetime`
- `time`
- `requests`
- `werkzeug.test`
- `werkzeug.wrappers`
- `frappe`
- `frappe.auth`
- `frappe.frappeclient`
- `frappe.sessions`
- `frappe.tests`
- `frappe.tests.test_api`
- `frappe.utils`
- `frappe.utils.data`
- `frappe.www.login`


## Step-by-Step Guide

### Step 1: Call frappe.cache.set_value()

```python
frappe.cache.set_value('allowed_referrers', ['https://example.com'])
```

### Step 2: Assign frappe.local.request = create_request(...)

```python
frappe.local.request = create_request({'Referer': 'https://example.com/some/path'})
```

### Step 3: Assign http_request = frappe.auth.HTTPRequest(...)

```python
http_request = frappe.auth.HTTPRequest()
```

### Step 4: Call self.assertTrue()

```python
self.assertTrue(http_request.is_allowed_referrer())
```

### Step 5: Assign frappe.local.request = create_request(...)

```python
frappe.local.request = create_request({'Referer': 'https://malicious.com'})
```

### Step 6: Assign http_request = frappe.auth.HTTPRequest(...)

```python
http_request = frappe.auth.HTTPRequest()
```

### Step 7: Call self.assertFalse()

```python
self.assertFalse(http_request.is_allowed_referrer())
```

### Step 8: Assign frappe.local.request = create_request(...)

```python
frappe.local.request = create_request({'Origin': 'https://example.com'})
```

### Step 9: Assign http_request = frappe.auth.HTTPRequest(...)

```python
http_request = frappe.auth.HTTPRequest()
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(http_request.is_allowed_referrer())
```

### Step 11: Assign frappe.local.request = create_request(...)

```python
frappe.local.request = create_request({'Origin': 'https://malicious.com'})
```

### Step 12: Assign http_request = frappe.auth.HTTPRequest(...)

```python
http_request = frappe.auth.HTTPRequest()
```

### Step 13: Call self.assertFalse()

```python
self.assertFalse(http_request.is_allowed_referrer())
```

### Step 14: Assign frappe.local.request = create_request(...)

```python
frappe.local.request = create_request({'Referer': 'https://example.com.evil.com'})
```

### Step 15: Assign http_request = frappe.auth.HTTPRequest(...)

```python
http_request = frappe.auth.HTTPRequest()
```

### Step 16: Call self.assertFalse()

```python
self.assertFalse(http_request.is_allowed_referrer())
```

### Step 17: Assign frappe.local.request = create_request(...)

```python
frappe.local.request = create_request({'Referer': 'https://example.com'})
```

### Step 18: Assign http_request = frappe.auth.HTTPRequest(...)

```python
http_request = frappe.auth.HTTPRequest()
```

### Step 19: Call self.assertTrue()

```python
self.assertTrue(http_request.is_allowed_referrer())
```

### Step 20: Call frappe.cache.delete_value()

```python
frappe.cache.delete_value('allowed_referrers')
```

### Step 21: Assign frappe.local.request = None

```python
frappe.local.request = None
```

### Step 22: Assign builder = EnvironBuilder(...)

```python
builder = EnvironBuilder(headers=headers)
```

### Step 23: Assign env = builder.get_environ(...)

```python
env = builder.get_environ()
```


## Complete Example

```python
# Workflow
def create_request(headers):
    builder = EnvironBuilder(headers=headers)
    env = builder.get_environ()
    return Request(env)
frappe.cache.set_value('allowed_referrers', ['https://example.com'])
frappe.local.request = create_request({'Referer': 'https://example.com/some/path'})
http_request = frappe.auth.HTTPRequest()
self.assertTrue(http_request.is_allowed_referrer())
frappe.local.request = create_request({'Referer': 'https://malicious.com'})
http_request = frappe.auth.HTTPRequest()
self.assertFalse(http_request.is_allowed_referrer())
frappe.local.request = create_request({'Origin': 'https://example.com'})
http_request = frappe.auth.HTTPRequest()
self.assertTrue(http_request.is_allowed_referrer())
frappe.local.request = create_request({'Origin': 'https://malicious.com'})
http_request = frappe.auth.HTTPRequest()
self.assertFalse(http_request.is_allowed_referrer())
frappe.local.request = create_request({'Referer': 'https://example.com.evil.com'})
http_request = frappe.auth.HTTPRequest()
self.assertFalse(http_request.is_allowed_referrer())
frappe.local.request = create_request({'Referer': 'https://example.com'})
http_request = frappe.auth.HTTPRequest()
self.assertTrue(http_request.is_allowed_referrer())
frappe.cache.delete_value('allowed_referrers')
frappe.local.request = None
```

## Next Steps


---

*Source: test_auth.py:173 | Complexity: Advanced | Last updated: 2026-02-04*