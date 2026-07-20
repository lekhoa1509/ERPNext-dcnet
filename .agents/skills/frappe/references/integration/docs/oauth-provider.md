# OAuth 2.0 Provider (Expose API)

Frappe can act as an OAuth 2.0 provider, allowing external applications to access your API.

## Create OAuth Client

```python
import frappe

client = frappe.new_doc("OAuth Client")
client.app_name = "My External App"
client.scopes = "all openid"
client.default_redirect_uri = "https://external-app.com/callback"
client.redirect_uris = "https://external-app.com/callback\nhttps://localhost:3000/callback"
client.grant_type = "Authorization Code"
client.response_type = "Code"
client.skip_authorization = 0  # Require user consent
client.insert()

# Get credentials
print(f"Client ID: {client.client_id}")
print(f"Client Secret: {client.client_secret}")
```

## OAuth Endpoints

| Endpoint | URL |
|----------|-----|
| Authorization | `/api/method/frappe.integrations.oauth2.authorize` |
| Token | `/api/method/frappe.integrations.oauth2.get_token` |
| Revoke | `/api/method/frappe.integrations.oauth2.revoke_token` |
| Introspect | `/api/method/frappe.integrations.oauth2.introspect_token` |
| OpenID Config | `/.well-known/openid-configuration` |

## Authorization Code Flow

```javascript
// Step 1: Redirect user to authorization URL
const authUrl = new URL('https://your-frappe-site.com/api/method/frappe.integrations.oauth2.authorize');
authUrl.searchParams.set('client_id', 'your-client-id');
authUrl.searchParams.set('response_type', 'code');
authUrl.searchParams.set('redirect_uri', 'https://your-app.com/callback');
authUrl.searchParams.set('scope', 'all openid');
authUrl.searchParams.set('state', 'random-state-string');

window.location.href = authUrl.toString();

// Step 2: Exchange code for token
const tokenResponse = await fetch('https://your-frappe-site.com/api/method/frappe.integrations.oauth2.get_token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
        grant_type: 'authorization_code',
        code: 'received-auth-code',
        redirect_uri: 'https://your-app.com/callback',
        client_id: 'your-client-id',
        client_secret: 'your-client-secret'
    })
});

const tokens = await tokenResponse.json();
// { access_token, refresh_token, token_type, expires_in }
```

## Use Access Token

```javascript
// API call with token
const response = await fetch('https://your-frappe-site.com/api/resource/Customer', {
    headers: {
        'Authorization': `Bearer ${tokens.access_token}`
    }
});
```
