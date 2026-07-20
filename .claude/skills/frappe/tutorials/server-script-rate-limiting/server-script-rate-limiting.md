# How To: Server Script Rate Limiting

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test server script rate limiting

## Prerequisites

**Required Modules:**
- `requests`
- `frappe`
- `frappe.core.doctype.scheduled_job_type.scheduled_job_type`
- `frappe.core.doctype.server_script.server_script`
- `frappe.frappeclient`
- `frappe.tests`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Assign script1 = frappe.get_doc(...)

```python
script1 = frappe.get_doc(doctype='Server Script', name='rate_limited_server_script', script_type='API', enable_rate_limit=1, allow_guest=1, rate_limit_count=5, api_method='rate_limited_endpoint', script='frappe.flags = {"test": True}')
```

### Step 2: Call script1.insert()

```python
script1.insert()
```

### Step 3: Assign script2 = frappe.get_doc(...)

```python
script2 = frappe.get_doc(doctype='Server Script', name='rate_limited_server_script2', script_type='API', enable_rate_limit=1, allow_guest=1, rate_limit_count=5, api_method='rate_limited_endpoint2', script='frappe.flags = {"test": False}')
```

### Step 4: Call script2.insert()

```python
script2.insert()
```

### Step 5: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 6: Assign site = frappe.utils.get_site_url(...)

```python
site = frappe.utils.get_site_url(frappe.local.site)
```

### Step 7: Assign client = FrappeClient(...)

```python
client = FrappeClient(site)
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(FrappeException, client.get_api, script1.api_method)
```

### Step 9: Call self.assertRaises()

```python
self.assertRaises(FrappeException, client.get_api, script2.api_method)
```

### Step 10: Call script1.delete()

```python
script1.delete()
```

### Step 11: Call script2.delete()

```python
script2.delete()
```

### Step 12: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 13: Call client.get_api()

```python
client.get_api(script1.api_method)
```

### Step 14: Call client.get_api()

```python
client.get_api(script2.api_method)
```


## Complete Example

```python
# Workflow
script1 = frappe.get_doc(doctype='Server Script', name='rate_limited_server_script', script_type='API', enable_rate_limit=1, allow_guest=1, rate_limit_count=5, api_method='rate_limited_endpoint', script='frappe.flags = {"test": True}')
script1.insert()
script2 = frappe.get_doc(doctype='Server Script', name='rate_limited_server_script2', script_type='API', enable_rate_limit=1, allow_guest=1, rate_limit_count=5, api_method='rate_limited_endpoint2', script='frappe.flags = {"test": False}')
script2.insert()
frappe.db.commit()
site = frappe.utils.get_site_url(frappe.local.site)
client = FrappeClient(site)
for _ in range(5):
    client.get_api(script1.api_method)
self.assertRaises(FrappeException, client.get_api, script1.api_method)
for _ in range(5):
    client.get_api(script2.api_method)
self.assertRaises(FrappeException, client.get_api, script2.api_method)
script1.delete()
script2.delete()
frappe.db.commit()
```

## Next Steps


---

*Source: test_server_script.py:261 | Complexity: Advanced | Last updated: 2026-02-04*