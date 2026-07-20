# How To: Login Using Authorization Code With Pkce

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test login using authorization code with pkce

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

### Step 2: Call self.TEST_CLIENT.set_cookie()

```python
self.TEST_CLIENT.set_cookie(key='sid', value=self.sid)
```

### Step 3: Assign resp = self.get(...)

```python
resp = self.get('/api/method/frappe.integrations.oauth2.authorize', {'client_id': self.client_id, 'scope': self.scope, 'response_type': 'code', 'redirect_uri': self.redirect_uri, 'code_challenge_method': 'S256', 'code_challenge': '21XaP8MJjpxCMRxgEzBP82sZ73PRLqkyBUta1R309J0'}, follow_redirects=True)
```

### Step 4: Assign query = parse_qs(...)

```python
query = parse_qs(resp.request.environ['QUERY_STRING'])
```

### Step 5: Assign auth_code = value

```python
auth_code = query.get('code')[0]
```

### Step 6: Assign token_response = self.post(...)

```python
token_response = self.post('/api/method/frappe.integrations.oauth2.get_token', headers=self.form_header, data={'grant_type': 'authorization_code', 'code': auth_code, 'redirect_uri': self.redirect_uri, 'client_id': self.client_id, 'scope': self.scope, 'code_verifier': '420'})
```

### Step 7: Assign bearer_token = value

```python
bearer_token = token_response.json
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(bearer_token.get('access_token'))
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(bearer_token.get('id_token'))
```

### Step 10: Assign decoded_token = self.decode_id_token(...)

```python
decoded_token = self.decode_id_token(bearer_token.get('id_token'))
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(decoded_token['email'], 'test@example.com')
```


## Complete Example

```python
# Workflow
update_client_for_auth_code_grant(self.client_id)
self.TEST_CLIENT.set_cookie(key='sid', value=self.sid)
resp = self.get('/api/method/frappe.integrations.oauth2.authorize', {'client_id': self.client_id, 'scope': self.scope, 'response_type': 'code', 'redirect_uri': self.redirect_uri, 'code_challenge_method': 'S256', 'code_challenge': '21XaP8MJjpxCMRxgEzBP82sZ73PRLqkyBUta1R309J0'}, follow_redirects=True)
query = parse_qs(resp.request.environ['QUERY_STRING'])
auth_code = query.get('code')[0]
token_response = self.post('/api/method/frappe.integrations.oauth2.get_token', headers=self.form_header, data={'grant_type': 'authorization_code', 'code': auth_code, 'redirect_uri': self.redirect_uri, 'client_id': self.client_id, 'scope': self.scope, 'code_verifier': '420'})
bearer_token = token_response.json
self.assertTrue(bearer_token.get('access_token'))
self.assertTrue(bearer_token.get('id_token'))
decoded_token = self.decode_id_token(bearer_token.get('id_token'))
self.assertEqual(decoded_token['email'], 'test@example.com')
```

## Next Steps


---

*Source: test_oauth20.py:153 | Complexity: Advanced | Last updated: 2026-02-04*