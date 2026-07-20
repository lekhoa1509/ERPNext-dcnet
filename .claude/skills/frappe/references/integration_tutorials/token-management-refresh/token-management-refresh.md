# How To: Token Management and Refresh

**Difficulty**: Intermediate
**Estimated Time**: 25 minutes
**Tags**: token, oauth, refresh, cache, security

## Overview

Learn how to manage OAuth tokens, handle token refresh, and use Token Cache effectively in Frappe integrations.

## Prerequisites

- OAuth integration knowledge
- Understanding of access/refresh tokens
- Connected App configured

## Step-by-Step Guide

### Step 1: Understanding Token Cache

Token Cache stores OAuth tokens for users connecting to external services:

```python
import frappe

# View Token Cache structure
def inspect_token_cache():
    """Inspect Token Cache document structure."""
    meta = frappe.get_meta("Token Cache")
    for field in meta.fields:
        print(f"{field.fieldname}: {field.fieldtype}")

# Key fields:
# - user: The Frappe user
# - connected_app: Link to Connected App
# - access_token: Current access token
# - refresh_token: Token for getting new access token
# - expires_in: Token lifetime in seconds
# - expiry_time: When token expires (datetime)
# - state: OAuth state parameter
# - scope: Granted scopes
```

### Step 2: Check Token Status

```python
import frappe
from frappe.integrations.doctype.connected_app.connected_app import has_token

def check_token_status(connected_app_name: str, user: str = None) -> dict:
    """Check OAuth token status for a user."""

    if not user:
        user = frappe.session.user

    # Quick check if token exists
    if not has_token(connected_app_name, user):
        return {
            "has_token": False,
            "message": "No token found. User needs to authorize."
        }

    # Get Token Cache for details
    token_cache = frappe.get_all(
        "Token Cache",
        filters={
            "connected_app": connected_app_name,
            "user": user
        },
        fields=["name", "expiry_time", "scope", "creation", "modified"]
    )

    if not token_cache:
        return {"has_token": False}

    tc = token_cache[0]
    token = frappe.get_doc("Token Cache", tc.name)

    return {
        "has_token": True,
        "expires_at": tc.expiry_time,
        "is_expired": token.is_expired(),
        "expires_in_seconds": token.get_expires_in(),
        "scopes": tc.scope,
        "created": tc.creation,
        "last_refreshed": tc.modified
    }

# Usage
status = check_token_status("Google Drive")
print(f"Token status: {status}")
```

### Step 3: Manually Refresh Token

```python
import frappe
import requests

def refresh_oauth_token(connected_app_name: str, user: str = None) -> dict:
    """Manually refresh OAuth token."""

    if not user:
        user = frappe.session.user

    # Get Connected App
    app = frappe.get_doc("Connected App", connected_app_name)

    # Get Token Cache
    token_cache = app.get_token_cache(user)
    if not token_cache:
        return {"error": "No token cache found"}

    if not token_cache.refresh_token:
        return {"error": "No refresh token available"}

    # Request new token
    try:
        response = requests.post(
            app.token_uri,
            data={
                "grant_type": "refresh_token",
                "refresh_token": token_cache.refresh_token,
                "client_id": app.client_id,
                "client_secret": app.get_password("client_secret")
            },
            timeout=30
        )
        response.raise_for_status()
        token_data = response.json()

        # Update Token Cache
        token_cache.update_data(token_data)
        token_cache.save(ignore_permissions=True)
        frappe.db.commit()

        return {
            "success": True,
            "expires_in": token_data.get("expires_in"),
            "scope": token_data.get("scope")
        }

    except Exception as e:
        return {"error": str(e)}

# Manual refresh
result = refresh_oauth_token("Google Drive")
print(result)
```

### Step 4: Auto-Refresh with OAuth Session

The Connected App's `get_oauth2_session()` handles refresh automatically:

```python
import frappe
from requests_oauthlib import OAuth2Session

def get_auto_refresh_session(connected_app_name: str, user: str = None):
    """Get OAuth session with automatic token refresh."""

    if not user:
        user = frappe.session.user

    app = frappe.get_doc("Connected App", connected_app_name)

    # This session automatically refreshes tokens when expired
    session = app.get_oauth2_session(user=user)

    return session

# Usage - tokens refresh automatically on API calls
session = get_auto_refresh_session("Google Drive")
response = session.get("https://www.googleapis.com/drive/v3/files")
files = response.json()
```

### Step 5: Revoke Tokens

```python
def revoke_user_token(connected_app_name: str, user: str = None) -> dict:
    """Revoke OAuth token for a user."""

    if not user:
        user = frappe.session.user

    # Get Token Cache
    token_caches = frappe.get_all(
        "Token Cache",
        filters={
            "connected_app": connected_app_name,
            "user": user
        },
        pluck="name"
    )

    if not token_caches:
        return {"message": "No token found"}

    # Delete Token Cache entries
    for tc_name in token_caches:
        frappe.delete_doc("Token Cache", tc_name, force=True)

    frappe.db.commit()

    return {
        "success": True,
        "message": f"Revoked {len(token_caches)} token(s)"
    }

# Revoke Google Drive access
result = revoke_user_token("Google Drive")
```

## Complete Example: Token Manager Class

```python
import frappe
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class TokenManager:
    """Comprehensive token management for OAuth integrations."""

    def __init__(self, connected_app_name: str):
        self.connected_app_name = connected_app_name
        self._app = None

    @property
    def app(self):
        """Lazy load Connected App."""
        if not self._app:
            self._app = frappe.get_doc("Connected App", self.connected_app_name)
        return self._app

    def get_token_cache(self, user: str = None) -> Optional['frappe._dict']:
        """Get Token Cache for user."""
        if not user:
            user = frappe.session.user
        return self.app.get_token_cache(user)

    def has_valid_token(self, user: str = None) -> bool:
        """Check if user has valid (non-expired) token."""
        if not user:
            user = frappe.session.user

        from frappe.integrations.doctype.connected_app.connected_app import has_token
        if not has_token(self.connected_app_name, user):
            return False

        token_cache = self.get_token_cache(user)
        return token_cache and not token_cache.is_expired()

    def get_access_token(self, user: str = None) -> Optional[str]:
        """Get current access token, refresh if needed."""
        if not user:
            user = frappe.session.user

        token_cache = self.get_token_cache(user)
        if not token_cache:
            return None

        # Refresh if expired or about to expire (within 5 minutes)
        if token_cache.is_expired() or token_cache.get_expires_in() < 300:
            self.refresh_token(user)
            token_cache = self.get_token_cache(user)

        return token_cache.access_token if token_cache else None

    def get_auth_header(self, user: str = None) -> Dict[str, str]:
        """Get Authorization header for API calls."""
        token_cache = self.get_token_cache(user)
        if token_cache:
            return token_cache.get_auth_header()
        return {}

    def refresh_token(self, user: str = None) -> Dict[str, Any]:
        """Refresh OAuth token."""
        if not user:
            user = frappe.session.user

        token_cache = self.get_token_cache(user)
        if not token_cache:
            return {"error": "No token cache found"}

        if not token_cache.refresh_token:
            return {"error": "No refresh token available. User must re-authorize."}

        try:
            response = requests.post(
                self.app.token_uri,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": token_cache.refresh_token,
                    "client_id": self.app.client_id,
                    "client_secret": self.app.get_password("client_secret")
                },
                timeout=30
            )
            response.raise_for_status()
            token_data = response.json()

            # Update cache
            token_cache.update_data(token_data)
            token_cache.save(ignore_permissions=True)
            frappe.db.commit()

            return {
                "success": True,
                "expires_in": token_data.get("expires_in")
            }

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                # Token likely revoked, need re-authorization
                return {
                    "error": "Refresh token invalid or revoked",
                    "need_reauthorization": True
                }
            return {"error": str(e)}

        except Exception as e:
            return {"error": str(e)}

    def revoke(self, user: str = None) -> Dict[str, Any]:
        """Revoke token for user."""
        if not user:
            user = frappe.session.user

        token_caches = frappe.get_all(
            "Token Cache",
            filters={
                "connected_app": self.connected_app_name,
                "user": user
            },
            pluck="name"
        )

        for tc_name in token_caches:
            frappe.delete_doc("Token Cache", tc_name, force=True)

        frappe.db.commit()
        return {"success": True, "revoked": len(token_caches)}

    def get_status(self, user: str = None) -> Dict[str, Any]:
        """Get comprehensive token status."""
        if not user:
            user = frappe.session.user

        token_cache = self.get_token_cache(user)
        if not token_cache:
            return {
                "has_token": False,
                "authorized": False
            }

        return {
            "has_token": True,
            "authorized": True,
            "is_expired": token_cache.is_expired(),
            "expires_in_seconds": token_cache.get_expires_in(),
            "expiry_time": str(token_cache.expiry_time) if token_cache.expiry_time else None,
            "has_refresh_token": bool(token_cache.refresh_token),
            "scopes": token_cache.scope,
            "created": str(token_cache.creation),
            "last_modified": str(token_cache.modified)
        }

    def list_authorized_users(self) -> list:
        """List all users with tokens for this app."""
        return frappe.get_all(
            "Token Cache",
            filters={"connected_app": self.connected_app_name},
            fields=["user", "creation", "expiry_time", "modified"],
            order_by="creation desc"
        )

# Usage
token_manager = TokenManager("Google Drive")

# Check status
status = token_manager.get_status()
print(f"Authorized: {status['authorized']}")
print(f"Expired: {status.get('is_expired', 'N/A')}")

# Get access token (auto-refresh if needed)
access_token = token_manager.get_access_token()
if access_token:
    print("Token retrieved successfully")
else:
    print("User needs to authorize")

# Get auth header for API calls
headers = token_manager.get_auth_header()
# Use in requests: requests.get(url, headers=headers)
```

## Scheduled Token Maintenance

```python
def scheduled_token_refresh():
    """Refresh tokens about to expire (run hourly via scheduler)."""

    # Get tokens expiring in next 30 minutes
    from datetime import datetime, timedelta

    threshold = datetime.now() + timedelta(minutes=30)

    expiring_tokens = frappe.db.sql("""
        SELECT tc.name, tc.user, tc.connected_app, ca.provider_name
        FROM `tabToken Cache` tc
        JOIN `tabConnected App` ca ON tc.connected_app = ca.name
        WHERE tc.expiry_time IS NOT NULL
        AND tc.expiry_time < %s
        AND tc.expiry_time > NOW()
        AND tc.refresh_token IS NOT NULL
    """, [threshold], as_dict=True)

    results = []
    for token in expiring_tokens:
        try:
            manager = TokenManager(token.connected_app)
            result = manager.refresh_token(token.user)
            results.append({
                "user": token.user,
                "provider": token.provider_name,
                "result": result
            })
        except Exception as e:
            results.append({
                "user": token.user,
                "provider": token.provider_name,
                "error": str(e)
            })

    return results

# In hooks.py:
# scheduler_events = {
#     "hourly": [
#         "your_app.utils.scheduled_token_refresh"
#     ]
# }
```

## Troubleshooting

### Token Refresh Fails
- Verify refresh_token exists
- Check if token was revoked on provider side
- User may need to re-authorize

### Token Expired Immediately
- Check system timezone
- Verify expiry_time calculation
- Some providers return short-lived tokens

### Missing Scopes After Refresh
- Some providers don't return scope on refresh
- Original scope is preserved in Token Cache

## Next Steps

- [Connected Apps Configuration](../connected-apps-configuration/connected-apps-configuration.md)
- [Error Handling in Integrations](../error-handling-integrations/error-handling-integrations.md)

---

*Source: Frappe Integration Documentation | Difficulty: Intermediate | Last updated: 2026-02-04*
