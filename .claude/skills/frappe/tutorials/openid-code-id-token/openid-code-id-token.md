# How To: Openid Code Id Token

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test openid code id token

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

### Step 1: Call update_client_for_auth_code_grant()

```python
update_client_for_auth_code_grant(self.client_id)
```

### Step 2: Assign nonce = frappe.generate_hash(...)

```python
nonce = frappe.generate_hash()
```

### Step 3: Call self.TEST_CLIENT.set_cookie()

```python
self.TEST_CLIENT.set_cookie(key='sid', value=self.sid)
```

### Step 4: Assign resp = self.get(...)

```python
resp = self.get('/api/method/frappe.integrations.oauth2.authorize', {'client_id': self.client_id, 'scope': self.scope, 'response_type': 'code', 'redirect_uri': self.redirect_uri, 'nonce': nonce}, follow_redirects=True)
```

### Step 5: Assign query = parse_qs(...)

```python
query = parse_qs(resp.request.environ['QUERY_STRING'])
```

### Step 6: Assign auth_code = value

```python
auth_code = query.get('code')[0]
```

### Step 7: Assign token_response = self.post(...)

```python
token_response = self.post('/api/method/frappe.integrations.oauth2.get_token', headers=self.form_header, data=encode_params({'grant_type': 'authorization_code', 'code': auth_code, 'redirect_uri': self.redirect_uri, 'client_id': self.client_id, 'scope': self.scope}))
```

### Step 8: Assign bearer_token = value

```python
bearer_token = token_response.json
```

### Step 9: Assign payload = self.decode_id_token(...)

```python
payload = self.decode_id_token(bearer_token.get('id_token'))
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(payload['email'], 'test@example.com')
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(payload.get('nonce') == nonce)
```


## Complete Example

```python
# Workflow
update_client_for_auth_code_grant(self.client_id)
nonce = frappe.generate_hash()
self.TEST_CLIENT.set_cookie(key='sid', value=self.sid)
resp = self.get('/api/method/frappe.integrations.oauth2.authorize', {'client_id': self.client_id, 'scope': self.scope, 'response_type': 'code', 'redirect_uri': self.redirect_uri, 'nonce': nonce}, follow_redirects=True)
query = parse_qs(resp.request.environ['QUERY_STRING'])
auth_code = query.get('code')[0]
token_response = self.post('/api/method/frappe.integrations.oauth2.get_token', headers=self.form_header, data=encode_params({'grant_type': 'authorization_code', 'code': auth_code, 'redirect_uri': self.redirect_uri, 'client_id': self.client_id, 'scope': self.scope}))
bearer_token = token_response.json
payload = self.decode_id_token(bearer_token.get('id_token'))
self.assertEqual(payload['email'], 'test@example.com')
self.assertTrue(payload.get('nonce') == nonce)
```

## Next Steps


---

*Source: test_oauth20.py:319 | Complexity: Advanced | Last updated: 2026-02-04*