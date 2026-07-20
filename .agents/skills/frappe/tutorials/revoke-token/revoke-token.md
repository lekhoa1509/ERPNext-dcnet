# How To: Revoke Token

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test revoke token

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

### Step 1: Assign client = frappe.get_doc(...)

```python
client = frappe.get_doc('OAuth Client', self.client_id)
```

### Step 2: Assign client.grant_type = 'Authorization Code'

```python
client.grant_type = 'Authorization Code'
```

### Step 3: Assign client.response_type = 'Code'

```python
client.response_type = 'Code'
```

### Step 4: Call client.save()

```python
client.save()
```

### Step 5: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 6: Call self.TEST_CLIENT.set_cookie()

```python
self.TEST_CLIENT.set_cookie(key='sid', value=self.sid)
```

### Step 7: Assign resp = self.get(...)

```python
resp = self.get('/api/method/frappe.integrations.oauth2.authorize', {'client_id': self.client_id, 'scope': self.scope, 'response_type': 'code', 'redirect_uri': self.redirect_uri}, follow_redirects=True)
```

### Step 8: Assign query = parse_qs(...)

```python
query = parse_qs(resp.request.environ['QUERY_STRING'])
```

### Step 9: Assign auth_code = value

```python
auth_code = query.get('code')[0]
```

### Step 10: Assign token_response = self.post(...)

```python
token_response = self.post('/api/method/frappe.integrations.oauth2.get_token', headers=self.form_header, data={'grant_type': 'authorization_code', 'code': auth_code, 'redirect_uri': self.redirect_uri, 'client_id': self.client_id})
```

### Step 11: Assign bearer_token = value

```python
bearer_token = token_response.json
```

### Step 12: Assign revoke_token_response = self.post(...)

```python
revoke_token_response = self.post('/api/method/frappe.integrations.oauth2.revoke_token', headers=self.form_header, data={'token': bearer_token.get('access_token')})
```

### Step 13: Call self.assertTrue()

```python
self.assertTrue(revoke_token_response.status_code == 200)
```

### Step 14: Call self.assertFalse()

```python
self.assertFalse(check_valid_openid_response(access_token=bearer_token.get('access_token'), client=self))
```


## Complete Example

```python
# Workflow
client = frappe.get_doc('OAuth Client', self.client_id)
client.grant_type = 'Authorization Code'
client.response_type = 'Code'
client.save()
frappe.db.commit()
self.TEST_CLIENT.set_cookie(key='sid', value=self.sid)
resp = self.get('/api/method/frappe.integrations.oauth2.authorize', {'client_id': self.client_id, 'scope': self.scope, 'response_type': 'code', 'redirect_uri': self.redirect_uri}, follow_redirects=True)
query = parse_qs(resp.request.environ['QUERY_STRING'])
auth_code = query.get('code')[0]
token_response = self.post('/api/method/frappe.integrations.oauth2.get_token', headers=self.form_header, data={'grant_type': 'authorization_code', 'code': auth_code, 'redirect_uri': self.redirect_uri, 'client_id': self.client_id})
bearer_token = token_response.json
revoke_token_response = self.post('/api/method/frappe.integrations.oauth2.revoke_token', headers=self.form_header, data={'token': bearer_token.get('access_token')})
self.assertTrue(revoke_token_response.status_code == 200)
self.assertFalse(check_valid_openid_response(access_token=bearer_token.get('access_token'), client=self))
```

## Next Steps


---

*Source: test_oauth20.py:198 | Complexity: Advanced | Last updated: 2026-02-04*