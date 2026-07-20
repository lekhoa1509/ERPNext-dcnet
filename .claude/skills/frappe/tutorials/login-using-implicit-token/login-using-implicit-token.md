# How To: Login Using Implicit Token

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test login using implicit token

## Prerequisites

**Required Modules:**
- `typing`
- `urllib.parse`
- `requests`
- `werkzeug.test`
- `frappe`
- `frappe.integrations.oauth2`
- `frappe.tests`
- `frappe.tests.test_api`
- `frappe.tests.utils`
- `frappe.utils.oauth`
- `frappe.integrations.doctype.social_login_key.social_login_key`
- `jwt`
- `frappe.auth`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Assign oauth_client = frappe.get_doc(...)

```python
oauth_client = frappe.get_doc('OAuth Client', self.client_id)
```

### Step 2: Assign oauth_client.grant_type = 'Implicit'

```python
oauth_client.grant_type = 'Implicit'
```

### Step 3: Assign oauth_client.response_type = 'Token'

```python
oauth_client.response_type = 'Token'
```

### Step 4: Call oauth_client.save()

```python
oauth_client.save()
```

### Step 5: Assign oauth_client_before = oauth_client.get_doc_before_save(...)

```python
oauth_client_before = oauth_client.get_doc_before_save()
```

### Step 6: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 7: Assign session = requests.Session(...)

```python
session = requests.Session()
```

### Step 8: Call login()

```python
login(session)
```

### Step 9: Assign redirect_destination = None

```python
redirect_destination = None
```

### Step 10: Assign response_dict = parse_qs(...)

```python
response_dict = parse_qs(urlparse(redirect_destination).fragment)
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(response_dict.get('access_token'))
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue(response_dict.get('expires_in'))
```

### Step 13: Call self.assertTrue()

```python
self.assertTrue(response_dict.get('scope'))
```

### Step 14: Call self.assertTrue()

```python
self.assertTrue(response_dict.get('token_type'))
```

### Step 15: Call self.assertTrue()

```python
self.assertTrue(check_valid_openid_response(response_dict.get('access_token')[0]))
```

### Step 16: Call oauth_client.delete()

```python
oauth_client.delete(force=True)
```

### Step 17: Call oauth_client_before.insert()

```python
oauth_client_before.insert()
```

### Step 18: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 19: Call session.get()

```python
session.get(get_full_url('/api/method/frappe.integrations.oauth2.authorize'), params=encode_params({'client_id': self.client_id, 'scope': self.scope, 'response_type': 'token', 'redirect_uri': self.redirect_uri}))
```

### Step 20: Assign redirect_destination = value

```python
redirect_destination = ex.request.url
```


## Complete Example

```python
# Workflow
oauth_client = frappe.get_doc('OAuth Client', self.client_id)
oauth_client.grant_type = 'Implicit'
oauth_client.response_type = 'Token'
oauth_client.save()
oauth_client_before = oauth_client.get_doc_before_save()
frappe.db.commit()
session = requests.Session()
login(session)
redirect_destination = None
try:
    session.get(get_full_url('/api/method/frappe.integrations.oauth2.authorize'), params=encode_params({'client_id': self.client_id, 'scope': self.scope, 'response_type': 'token', 'redirect_uri': self.redirect_uri}))
except requests.exceptions.ConnectionError as ex:
    redirect_destination = ex.request.url
response_dict = parse_qs(urlparse(redirect_destination).fragment)
self.assertTrue(response_dict.get('access_token'))
self.assertTrue(response_dict.get('expires_in'))
self.assertTrue(response_dict.get('scope'))
self.assertTrue(response_dict.get('token_type'))
self.assertTrue(check_valid_openid_response(response_dict.get('access_token')[0]))
oauth_client.delete(force=True)
oauth_client_before.insert()
frappe.db.commit()
```

## Next Steps


---

*Source: test_oauth20.py:279 | Complexity: Advanced | Last updated: 2026-02-04*