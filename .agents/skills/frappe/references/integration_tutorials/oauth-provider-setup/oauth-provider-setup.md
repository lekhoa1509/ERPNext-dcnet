# How To: OAuth 2.0 Provider Setup

**Difficulty**: Advanced
**Estimated Time**: 30 minutes
**Tags**: oauth, provider, api, authentication, security

## Overview

Learn how to configure Frappe as an OAuth 2.0 Provider to allow external applications to access your Frappe/ERPNext API securely.

## Prerequisites

- Administrator access to Frappe
- Understanding of OAuth 2.0 concepts
- HTTPS enabled on your site (required for production)

## Step-by-Step Guide

### Step 1: Enable OAuth Settings

```python
import frappe

# Configure OAuth Settings
oauth_settings = frappe.get_single("OAuth Settings")

# Enable skip authorization for trusted clients (optional, not for production)
oauth_settings.skip_authorization = 0

# Enable authorization server metadata discovery (RFC 8414)
oauth_settings.show_auth_server_metadata = 1

# Enable dynamic client registration (RFC 7591)
oauth_settings.enable_dynamic_client_registration = 1

oauth_settings.save()
frappe.db.commit()
```

### Step 2: Create an OAuth Client

```python
import frappe

def create_oauth_client(
    app_name: str,
    redirect_uris: list,
    default_redirect_uri: str,
    scopes: list = None
) -> dict:
    """Create a new OAuth Client for external application."""

    # Generate client credentials
    client_id = frappe.generate_hash(length=10)
    client_secret = frappe.generate_hash(length=32)

    oauth_client = frappe.new_doc("OAuth Client")
    oauth_client.app_name = app_name
    oauth_client.client_id = client_id
    oauth_client.client_secret = client_secret
    oauth_client.redirect_uris = "\n".join(redirect_uris)
    oauth_client.default_redirect_uri = default_redirect_uri
    oauth_client.grant_type = "Authorization Code"

    # Add allowed scopes
    if scopes:
        for scope in scopes:
            oauth_client.append("scopes", {"scope": scope})
    else:
        # Default scopes
        oauth_client.append("scopes", {"scope": "openid"})
        oauth_client.append("scopes", {"scope": "all"})

    oauth_client.insert()
    frappe.db.commit()

    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "app_name": app_name
    }

# Usage
credentials = create_oauth_client(
    app_name="Mobile App",
    redirect_uris=[
        "https://myapp.com/callback",
        "myapp://callback"
    ],
    default_redirect_uri="https://myapp.com/callback",
    scopes=["openid", "all"]
)
print(f"Client ID: {credentials['client_id']}")
print(f"Client Secret: {credentials['client_secret']}")
```

### Step 3: Configure Client Roles (Optional)

Restrict which roles can authorize this client:

```python
oauth_client = frappe.get_doc("OAuth Client", "Mobile App")

# Clear existing roles
oauth_client.allowed_roles = []

# Add allowed roles
for role in ["Sales User", "Sales Manager", "Administrator"]:
    oauth_client.append("allowed_roles", {"role": role})

oauth_client.save()
frappe.db.commit()
```

### Step 4: Understanding OAuth Flow Endpoints

Frappe exposes these OAuth endpoints:

| Endpoint | URL | Description |
|----------|-----|-------------|
| Authorization | `/api/method/frappe.integrations.oauth2.authorize` | Start auth flow |
| Token | `/api/method/frappe.integrations.oauth2.get_token` | Exchange code for token |
| Revoke | `/api/method/frappe.integrations.oauth2.revoke_token` | Revoke tokens |
| Introspect | `/api/method/frappe.integrations.oauth2.introspect_token` | Validate token |
| UserInfo | `/api/method/frappe.integrations.oauth2.openid_profile` | Get user info |
| Metadata | `/.well-known/oauth-authorization-server` | Server metadata |

### Step 5: Client-Side Authorization Flow

```python
# Example client-side code (external application)
import requests
from urllib.parse import urlencode

FRAPPE_URL = "https://your-erp.com"
CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"
REDIRECT_URI = "https://your-app.com/callback"

def get_authorization_url():
    """Generate authorization URL for user redirect."""
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "openid all"
    }
    return f"{FRAPPE_URL}/api/method/frappe.integrations.oauth2.authorize?{urlencode(params)}"

def exchange_code_for_token(code: str) -> dict:
    """Exchange authorization code for access token."""
    response = requests.post(
        f"{FRAPPE_URL}/api/method/frappe.integrations.oauth2.get_token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
    )
    return response.json()

def refresh_access_token(refresh_token: str) -> dict:
    """Use refresh token to get new access token."""
    response = requests.post(
        f"{FRAPPE_URL}/api/method/frappe.integrations.oauth2.get_token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
    )
    return response.json()

def make_api_call(access_token: str):
    """Make authenticated API call."""
    response = requests.get(
        f"{FRAPPE_URL}/api/resource/Customer",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    return response.json()
```

## Complete Example

```python
import frappe

def setup_oauth_provider_for_mobile_app():
    """Complete setup for mobile app OAuth integration."""

    # 1. Configure OAuth Settings
    oauth_settings = frappe.get_single("OAuth Settings")
    oauth_settings.skip_authorization = 0
    oauth_settings.show_auth_server_metadata = 1
    oauth_settings.save()

    # 2. Create OAuth Client
    app_name = "ERPNext Mobile App"

    if frappe.db.exists("OAuth Client", {"app_name": app_name}):
        print(f"OAuth Client '{app_name}' already exists")
        client = frappe.get_doc("OAuth Client", {"app_name": app_name})
        return {
            "client_id": client.client_id,
            "message": "Client already exists"
        }

    client_id = frappe.generate_hash(length=10)
    client_secret = frappe.generate_hash(length=32)

    oauth_client = frappe.new_doc("OAuth Client")
    oauth_client.app_name = app_name
    oauth_client.client_id = client_id
    oauth_client.client_secret = client_secret
    oauth_client.redirect_uris = "erpnext-mobile://callback\nhttps://mobile.erpnext.com/callback"
    oauth_client.default_redirect_uri = "erpnext-mobile://callback"
    oauth_client.grant_type = "Authorization Code"

    # Add scopes
    oauth_client.append("scopes", {"scope": "openid"})
    oauth_client.append("scopes", {"scope": "all"})

    # Restrict to specific roles
    for role in ["Sales User", "Sales Manager", "Stock User", "Accounts User"]:
        oauth_client.append("allowed_roles", {"role": role})

    oauth_client.insert()
    frappe.db.commit()

    # 3. Generate documentation for mobile developers
    docs = f"""
# OAuth Configuration for {app_name}

## Credentials (KEEP SECRET!)
- Client ID: {client_id}
- Client Secret: {client_secret}

## Endpoints
- Authorization: https://your-site.com/api/method/frappe.integrations.oauth2.authorize
- Token: https://your-site.com/api/method/frappe.integrations.oauth2.get_token
- UserInfo: https://your-site.com/api/method/frappe.integrations.oauth2.openid_profile

## Scopes
- openid: Required for OIDC compliance
- all: Access all API endpoints

## Allowed Redirect URIs
- erpnext-mobile://callback (Mobile deep link)
- https://mobile.erpnext.com/callback (Web fallback)
"""

    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "documentation": docs
    }

# Execute
result = setup_oauth_provider_for_mobile_app()
print(result["documentation"])
```

## Managing OAuth Tokens

```python
def list_active_tokens(user: str = None) -> list:
    """List all active OAuth tokens."""
    filters = {"status": "Active"}
    if user:
        filters["user"] = user

    return frappe.get_all(
        "OAuth Bearer Token",
        filters=filters,
        fields=["name", "user", "client", "creation", "expiration_time"]
    )

def revoke_all_user_tokens(user: str):
    """Revoke all tokens for a specific user."""
    tokens = frappe.get_all(
        "OAuth Bearer Token",
        filters={"user": user, "status": "Active"}
    )

    for token in tokens:
        doc = frappe.get_doc("OAuth Bearer Token", token.name)
        doc.status = "Revoked"
        doc.save()

    frappe.db.commit()
    return len(tokens)

def cleanup_expired_tokens():
    """Clean up expired tokens (run as scheduled job)."""
    from frappe.integrations.doctype.oauth_bearer_token.oauth_bearer_token import clear_old_tokens
    clear_old_tokens()
```

## Security Best Practices

1. **Always Use HTTPS**: OAuth requires secure connections
2. **Rotate Client Secrets**: Periodically regenerate secrets
3. **Limit Scopes**: Only grant necessary permissions
4. **Set Token Expiry**: Configure reasonable token lifetimes
5. **Monitor Access**: Review OAuth Bearer Tokens regularly
6. **Use PKCE**: For public clients (mobile apps)

## Troubleshooting

### Invalid Grant Error
- Check client_id and client_secret match
- Verify redirect_uri matches exactly
- Check authorization code hasn't expired

### Access Denied
- Verify user has required roles
- Check scopes are allowed for client
- Review OAuth Settings

## Next Steps

- [OAuth Client Implementation](../oauth-client-implementation/oauth-client-implementation.md)
- [Connected Apps Configuration](../connected-apps-configuration/connected-apps-configuration.md)

---

*Source: Frappe Integration Documentation | Difficulty: Advanced | Last updated: 2026-02-04*
