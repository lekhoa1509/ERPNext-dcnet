# How To: OAuth 2.0 Client Implementation

**Difficulty**: Advanced
**Estimated Time**: 30 minutes
**Tags**: oauth, client, external-api, authentication

## Overview

Learn how to implement OAuth 2.0 client functionality in Frappe to consume external APIs that require OAuth authentication.

## Prerequisites

- Understanding of OAuth 2.0 flows
- External OAuth provider credentials
- Frappe development knowledge

## Step-by-Step Guide

### Step 1: Create a Connected App

```python
import frappe

def create_connected_app(
    provider_name: str,
    client_id: str,
    client_secret: str,
    authorization_uri: str,
    token_uri: str,
    scopes: list
) -> str:
    """Create a Connected App for OAuth 2.0 client functionality."""

    app = frappe.new_doc("Connected App")
    app.provider_name = provider_name
    app.client_id = client_id
    app.client_secret = client_secret
    app.authorization_uri = authorization_uri
    app.token_uri = token_uri

    # Add scopes
    for scope in scopes:
        app.append("scopes", {"scope": scope})

    app.insert()
    frappe.db.commit()

    return app.name

# Example: Google OAuth
google_app = create_connected_app(
    provider_name="Google",
    client_id="your-google-client-id.apps.googleusercontent.com",
    client_secret="your-google-client-secret",
    authorization_uri="https://accounts.google.com/o/oauth2/v2/auth",
    token_uri="https://oauth2.googleapis.com/token",
    scopes=["https://www.googleapis.com/auth/drive.readonly", "email", "profile"]
)
```

### Step 2: Initiate OAuth Flow

```python
import frappe
from frappe.integrations.doctype.connected_app.connected_app import ConnectedApp

def start_oauth_flow(provider_name: str, user: str = None, success_uri: str = None) -> str:
    """Start the OAuth authorization flow for a user."""

    if not user:
        user = frappe.session.user

    # Get the Connected App
    app = frappe.get_doc("Connected App", {"provider_name": provider_name})

    # Initiate the flow
    auth_url = app.initiate_web_application_flow(
        user=user,
        success_uri=success_uri or "/app"
    )

    return auth_url

# Get authorization URL to redirect user
auth_url = start_oauth_flow("Google", success_uri="/app/google-drive")
# Redirect user to auth_url
```

### Step 3: Handle OAuth Callback

The callback is automatically handled by Frappe at:
`/api/method/frappe.integrations.doctype.connected_app.connected_app.callback`

After successful authorization, the token is stored in Token Cache.

### Step 4: Use the OAuth Session

```python
import frappe

def make_oauth_api_call(provider_name: str, endpoint: str, user: str = None) -> dict:
    """Make an API call using OAuth credentials."""

    if not user:
        user = frappe.session.user

    # Get Connected App
    app = frappe.get_doc("Connected App", {"provider_name": provider_name})

    # Get OAuth2 session (auto-refreshing)
    session = app.get_oauth2_session(user=user)

    # Make API call
    response = session.get(endpoint)
    return response.json()

# Example: Get Google Drive files
files = make_oauth_api_call(
    "Google",
    "https://www.googleapis.com/drive/v3/files"
)
```

### Step 5: Check Token Status

```python
from frappe.integrations.doctype.connected_app.connected_app import has_token

def check_user_authorization(provider_name: str, user: str = None) -> dict:
    """Check if user has valid OAuth token."""

    if not user:
        user = frappe.session.user

    has_valid_token = has_token(provider_name, user)

    if has_valid_token:
        app = frappe.get_doc("Connected App", {"provider_name": provider_name})
        token_cache = app.get_token_cache(user)

        return {
            "authorized": True,
            "expires_in": token_cache.get_expires_in() if token_cache else None,
            "is_expired": token_cache.is_expired() if token_cache else None
        }

    return {
        "authorized": False,
        "message": "User needs to authorize"
    }
```

## Complete Example: Microsoft Graph API Integration

```python
import frappe
from frappe import _

class MicrosoftGraphIntegration:
    """Integration with Microsoft Graph API using OAuth 2.0."""

    PROVIDER_NAME = "Microsoft Graph"
    BASE_URL = "https://graph.microsoft.com/v1.0"

    @classmethod
    def setup(cls, client_id: str, client_secret: str, tenant_id: str = "common"):
        """Setup Microsoft Graph Connected App."""

        if frappe.db.exists("Connected App", {"provider_name": cls.PROVIDER_NAME}):
            return {"status": "already_exists"}

        app = frappe.new_doc("Connected App")
        app.provider_name = cls.PROVIDER_NAME
        app.client_id = client_id
        app.client_secret = client_secret
        app.authorization_uri = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
        app.token_uri = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

        # Add scopes
        scopes = [
            "User.Read",
            "Mail.Read",
            "Calendars.Read",
            "offline_access"
        ]
        for scope in scopes:
            app.append("scopes", {"scope": scope})

        # Add query params
        app.append("query_parameters", {
            "key": "response_mode",
            "value": "query"
        })

        app.insert()
        frappe.db.commit()

        return {"status": "created", "name": app.name}

    @classmethod
    def get_session(cls, user: str = None):
        """Get OAuth session for Microsoft Graph."""
        if not user:
            user = frappe.session.user

        app = frappe.get_doc("Connected App", {"provider_name": cls.PROVIDER_NAME})
        return app.get_oauth2_session(user=user)

    @classmethod
    def check_authorization(cls, user: str = None) -> bool:
        """Check if user is authorized."""
        if not user:
            user = frappe.session.user
        return has_token(cls.PROVIDER_NAME, user)

    @classmethod
    def authorize(cls, user: str = None, success_uri: str = None) -> str:
        """Get authorization URL."""
        if not user:
            user = frappe.session.user

        app = frappe.get_doc("Connected App", {"provider_name": cls.PROVIDER_NAME})
        return app.initiate_web_application_flow(
            user=user,
            success_uri=success_uri or "/app"
        )

    @classmethod
    def get_user_profile(cls, user: str = None) -> dict:
        """Get Microsoft user profile."""
        session = cls.get_session(user)
        response = session.get(f"{cls.BASE_URL}/me")
        return response.json()

    @classmethod
    def get_emails(cls, user: str = None, top: int = 10) -> list:
        """Get user's recent emails."""
        session = cls.get_session(user)
        response = session.get(
            f"{cls.BASE_URL}/me/messages",
            params={"$top": top, "$orderby": "receivedDateTime DESC"}
        )
        data = response.json()
        return data.get("value", [])

    @classmethod
    def get_calendar_events(cls, user: str = None, days: int = 7) -> list:
        """Get user's upcoming calendar events."""
        from datetime import datetime, timedelta

        session = cls.get_session(user)

        start = datetime.now().isoformat()
        end = (datetime.now() + timedelta(days=days)).isoformat()

        response = session.get(
            f"{cls.BASE_URL}/me/calendarview",
            params={
                "startdatetime": start,
                "enddatetime": end,
                "$orderby": "start/dateTime"
            }
        )
        data = response.json()
        return data.get("value", [])

# Usage in a Frappe app

@frappe.whitelist()
def setup_microsoft_integration(client_id: str, client_secret: str):
    """API endpoint to setup Microsoft integration."""
    return MicrosoftGraphIntegration.setup(client_id, client_secret)

@frappe.whitelist()
def get_authorization_url():
    """Get URL to authorize Microsoft Graph."""
    if MicrosoftGraphIntegration.check_authorization():
        return {"already_authorized": True}

    auth_url = MicrosoftGraphIntegration.authorize(
        success_uri="/app/microsoft-integration"
    )
    return {"authorization_url": auth_url}

@frappe.whitelist()
def get_my_emails():
    """Get current user's Microsoft emails."""
    if not MicrosoftGraphIntegration.check_authorization():
        frappe.throw(_("Please authorize Microsoft Graph first"))

    return MicrosoftGraphIntegration.get_emails()

@frappe.whitelist()
def get_my_calendar():
    """Get current user's calendar events."""
    if not MicrosoftGraphIntegration.check_authorization():
        frappe.throw(_("Please authorize Microsoft Graph first"))

    return MicrosoftGraphIntegration.get_calendar_events()
```

## Using OpenID Connect Discovery

```python
def setup_oidc_connected_app(provider_name: str, openid_config_url: str, client_id: str, client_secret: str):
    """Setup Connected App using OpenID Connect discovery."""

    app = frappe.new_doc("Connected App")
    app.provider_name = provider_name
    app.client_id = client_id
    app.client_secret = client_secret
    app.openid_configuration = openid_config_url

    # Fetch configuration
    app.get_openid_configuration()

    # Authorization and token URIs will be populated automatically
    app.insert()
    frappe.db.commit()

    return app.name

# Example with Keycloak
setup_oidc_connected_app(
    provider_name="Keycloak",
    openid_config_url="https://keycloak.example.com/realms/myrealm/.well-known/openid-configuration",
    client_id="frappe-app",
    client_secret="your-client-secret"
)
```

## Troubleshooting

### Token Refresh Fails
- Ensure `offline_access` scope is included
- Check refresh token hasn't been revoked
- Verify token_uri is correct

### Authorization Error
- Verify redirect URI matches exactly
- Check client credentials
- Review scopes are valid for provider

### Session Expired
- Token Cache stores token status
- Check Token Cache for expiration
- Re-authorize if refresh fails

## Next Steps

- [Connected Apps Configuration](../connected-apps-configuration/connected-apps-configuration.md)
- [Token Management and Refresh](../token-management-refresh/token-management-refresh.md)

---

*Source: Frappe Integration Documentation | Difficulty: Advanced | Last updated: 2026-02-04*
