# How To: Array Values In Request Args

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test array values in request args

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.client`
- `frappe.desk.doctype.note.note`
- `frappe.client`
- `frappe.handler`
- `frappe.handler`
- `frappe.handler`
- `requests`
- `frappe.auth`
- `frappe.client`
- `frappe.client`
- `frappe.client`
- `frappe.client`
- `frappe.client`


## Step-by-Step Guide

### Step 1: Call frappe.utils.set_request()

```python
frappe.utils.set_request(path='/')
```

### Step 2: Assign frappe.local.cookie_manager = CookieManager(...)

```python
frappe.local.cookie_manager = CookieManager()
```

### Step 3: Assign frappe.local.login_manager = LoginManager(...)

```python
frappe.local.login_manager = LoginManager()
```

### Step 4: Call frappe.local.login_manager.login_as()

```python
frappe.local.login_manager.login_as('Administrator')
```

### Step 5: Assign params = value

```python
params = {'doctype': 'DocType', 'fields': ['name', 'modified'], 'sid': frappe.session.sid}
```

### Step 6: Assign headers = value

```python
headers = {'accept': 'application/json', 'content-type': 'application/json'}
```

### Step 7: Assign url = get_site_url(...)

```python
url = get_site_url(frappe.local.site)
```

### Step 8: Assign res = requests.post(...)

```python
res = requests.post(url, json=params, headers=headers)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(res.status_code, 200)
```

### Step 10: Assign data = res.json(...)

```python
data = res.json()
```

### Step 11: Assign first_item = value

```python
first_item = data['message'][0]
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue('name' in first_item)
```

### Step 13: Call self.assertTrue()

```python
self.assertTrue('modified' in first_item)
```


## Complete Example

```python
# Workflow
import requests
from frappe.auth import CookieManager, LoginManager
frappe.utils.set_request(path='/')
frappe.local.cookie_manager = CookieManager()
frappe.local.login_manager = LoginManager()
frappe.local.login_manager.login_as('Administrator')
params = {'doctype': 'DocType', 'fields': ['name', 'modified'], 'sid': frappe.session.sid}
headers = {'accept': 'application/json', 'content-type': 'application/json'}
url = get_site_url(frappe.local.site)
url += '/api/method/frappe.client.get_list'
res = requests.post(url, json=params, headers=headers)
self.assertEqual(res.status_code, 200)
data = res.json()
first_item = data['message'][0]
self.assertTrue('name' in first_item)
self.assertTrue('modified' in first_item)
```

## Next Steps


---

*Source: test_client.py:117 | Complexity: Advanced | Last updated: 2026-02-04*