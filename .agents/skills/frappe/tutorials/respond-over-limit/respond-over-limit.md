# How To: Respond Over Limit

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test respond over limit

## Prerequisites

**Required Modules:**
- `time`
- `werkzeug.wrappers`
- `frappe`
- `frappe.rate_limiter`
- `frappe.rate_limiter`
- `frappe.tests`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Assign limiter = RateLimiter(...)

```python
limiter = RateLimiter(1, 86400)
```

### Step 2: Call time.sleep()

```python
time.sleep(1)
```

### Step 3: Call limiter.update()

```python
limiter.update()
```

### Step 4: Assign frappe.conf.rate_limit = value

```python
frappe.conf.rate_limit = {'window': 86400, 'limit': 1}
```

### Step 5: Call self.assertRaises()

```python
self.assertRaises(frappe.TooManyRequestsError, frappe.rate_limiter.apply)
```

### Step 6: Call frappe.rate_limiter.update()

```python
frappe.rate_limiter.update()
```

### Step 7: Assign response = frappe.rate_limiter.respond(...)

```python
response = frappe.rate_limiter.respond()
```

### Step 8: Call self.assertIsInstance()

```python
self.assertIsInstance(response, Response)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 429)
```

### Step 10: Assign headers = frappe.local.rate_limiter.headers(...)

```python
headers = frappe.local.rate_limiter.headers()
```

### Step 11: Call self.assertIn()

```python
self.assertIn('Retry-After', headers)
```

### Step 12: Call self.assertIn()

```python
self.assertIn('X-RateLimit-Reset', headers)
```

### Step 13: Call self.assertIn()

```python
self.assertIn('X-RateLimit-Limit', headers)
```

### Step 14: Call self.assertIn()

```python
self.assertIn('X-RateLimit-Remaining', headers)
```

### Step 15: Call self.assertTrue()

```python
self.assertTrue(int(headers['X-RateLimit-Reset']) <= 86400)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(int(headers['X-RateLimit-Limit']), 1000000)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(int(headers['X-RateLimit-Remaining']), 0)
```

### Step 18: Call frappe.cache.delete()

```python
frappe.cache.delete(limiter.key)
```

### Step 19: Call frappe.cache.delete()

```python
frappe.cache.delete(frappe.local.rate_limiter.key)
```

### Step 20: Call delattr()

```python
delattr(frappe.local, 'rate_limiter')
```


## Complete Example

```python
# Workflow
limiter = RateLimiter(1, 86400)
time.sleep(1)
limiter.update()
frappe.conf.rate_limit = {'window': 86400, 'limit': 1}
self.assertRaises(frappe.TooManyRequestsError, frappe.rate_limiter.apply)
frappe.rate_limiter.update()
response = frappe.rate_limiter.respond()
self.assertIsInstance(response, Response)
self.assertEqual(response.status_code, 429)
headers = frappe.local.rate_limiter.headers()
self.assertIn('Retry-After', headers)
self.assertIn('X-RateLimit-Reset', headers)
self.assertIn('X-RateLimit-Limit', headers)
self.assertIn('X-RateLimit-Remaining', headers)
self.assertTrue(int(headers['X-RateLimit-Reset']) <= 86400)
self.assertEqual(int(headers['X-RateLimit-Limit']), 1000000)
self.assertEqual(int(headers['X-RateLimit-Remaining']), 0)
frappe.cache.delete(limiter.key)
frappe.cache.delete(frappe.local.rate_limiter.key)
delattr(frappe.local, 'rate_limiter')
```

## Next Steps


---

*Source: test_rate_limiter.py:32 | Complexity: Advanced | Last updated: 2026-02-04*