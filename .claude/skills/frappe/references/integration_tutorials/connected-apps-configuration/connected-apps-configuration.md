# How To: Connected Apps Configuration

**Difficulty**: Intermediate
**Estimated Time**: 25 minutes
**Tags**: connected-app, oauth, external-services, configuration

## Overview

Learn how to configure Connected Apps in Frappe to integrate with external OAuth 2.0 services like Google, Microsoft, Dropbox, and custom providers.

## Prerequisites

- OAuth credentials from external provider
- Understanding of OAuth 2.0 scopes
- Administrator access

## Step-by-Step Guide

### Step 1: Create Connected App via UI

Navigate to: **Setup > Integrations > Connected App**

Or via URL: `/app/connected-app/new-connected-app`

### Step 2: Configure Provider Details

```python
import frappe

# Create Connected App programmatically
def create_connected_app_for_google_drive():
    """Setup Google Drive Connected App."""

    app = frappe.new_doc("Connected App")

    # Basic Info
    app.provider_name = "Google Drive"

    # OAuth Credentials (from Google Cloud Console)
    app.client_id = "your-client-id.apps.googleusercontent.com"
    app.client_secret = "your-client-secret"

    # OAuth Endpoints
    app.authorization_uri = "https://accounts.google.com/o/oauth2/v2/auth"
    app.token_uri = "https://oauth2.googleapis.com/token"

    # Optional: OpenID Configuration URL (auto-fills endpoints)
    app.openid_configuration = "https://accounts.google.com/.well-known/openid-configuration"

    # Scopes
    app.append("scopes", {"scope": "https://www.googleapis.com/auth/drive.readonly"})
    app.append("scopes", {"scope": "https://www.googleapis.com/auth/drive.metadata.readonly"})
    app.append("scopes", {"scope": "email"})
    app.append("scopes", {"scope": "profile"})

    app.insert()
    frappe.db.commit()

    return app.name
```

### Step 3: Configure Scopes

Each Connected App requires specific scopes:

```python
# Google Scopes Examples
GOOGLE_SCOPES = {
    "Drive": [
        "https://www.googleapis.com/auth/drive.readonly",
        "https://www.googleapis.com/auth/drive.file"
    ],
    "Calendar": [
        "https://www.googleapis.com/auth/calendar.readonly",
        "https://www.googleapis.com/auth/calendar.events"
    ],
    "Contacts": [
        "https://www.googleapis.com/auth/contacts.readonly"
    ],
    "Gmail": [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://mail.google.com/"
    ]
}

# Microsoft Graph Scopes
MICROSOFT_SCOPES = {
    "User": ["User.Read", "User.ReadBasic.All"],
    "Mail": ["Mail.Read", "Mail.Send"],
    "Calendar": ["Calendars.Read", "Calendars.ReadWrite"],
    "Files": ["Files.Read", "Files.Read.All"],
    "Offline": ["offline_access"]  # Required for refresh tokens
}

# Salesforce Scopes
SALESFORCE_SCOPES = {
    "Basic": ["api", "refresh_token", "openid"],
    "Full": ["api", "refresh_token", "openid", "full"]
}

def add_scopes(app_name: str, scopes: list):
    """Add scopes to existing Connected App."""
    app = frappe.get_doc("Connected App", app_name)

    for scope in scopes:
        app.append("scopes", {"scope": scope})

    app.save()
    frappe.db.commit()
```

### Step 4: Configure Query Parameters

Some providers require additional query parameters:

```python
def add_query_parameters(app_name: str, params: dict):
    """Add query parameters to Connected App."""
    app = frappe.get_doc("Connected App", app_name)

    for key, value in params.items():
        app.append("query_parameters", {"key": key, "value": value})

    app.save()
    frappe.db.commit()

# Example: Google Drive force consent
add_query_parameters("Google Drive", {
    "access_type": "offline",  # Get refresh token
    "prompt": "consent"  # Force consent screen
})

# Example: Microsoft Graph
add_query_parameters("Microsoft Graph", {
    "response_mode": "query"
})
```

### Step 5: Use OpenID Configuration (Auto-Discovery)

```python
def setup_with_oidc_discovery(provider_name: str, oidc_url: str, client_id: str, client_secret: str):
    """Setup Connected App with OpenID Connect Discovery."""

    app = frappe.new_doc("Connected App")
    app.provider_name = provider_name
    app.client_id = client_id
    app.client_secret = client_secret
    app.openid_configuration = oidc_url

    # Fetch and populate configuration
    app.get_openid_configuration()

    # This will auto-fill:
    # - authorization_uri
    # - token_uri
    # - userinfo_endpoint (if available)
    # - etc.

    app.insert()
    frappe.db.commit()

    return {
        "name": app.name,
        "authorization_uri": app.authorization_uri,
        "token_uri": app.token_uri
    }

# Common OIDC Discovery URLs
OIDC_DISCOVERY = {
    "Google": "https://accounts.google.com/.well-known/openid-configuration",
    "Microsoft": "https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration",
    "Auth0": "https://YOUR_DOMAIN.auth0.com/.well-known/openid-configuration",
    "Okta": "https://YOUR_DOMAIN.okta.com/.well-known/openid-configuration",
    "Keycloak": "https://keycloak.example.com/realms/REALM/.well-known/openid-configuration"
}
```

## Complete Examples

### Google Drive Integration

```python
import frappe

def setup_google_drive_integration(client_id: str, client_secret: str):
    """Complete Google Drive Connected App setup."""

    if frappe.db.exists("Connected App", {"provider_name": "Google Drive"}):
        return {"status": "exists"}

    app = frappe.new_doc("Connected App")
    app.provider_name = "Google Drive"
    app.client_id = client_id
    app.client_secret = client_secret
    app.openid_configuration = "https://accounts.google.com/.well-known/openid-configuration"

    # Scopes for Drive access
    scopes = [
        "https://www.googleapis.com/auth/drive.readonly",
        "https://www.googleapis.com/auth/drive.metadata.readonly",
        "email",
        "profile",
        "openid"
    ]
    for scope in scopes:
        app.append("scopes", {"scope": scope})

    # Query parameters for offline access
    app.append("query_parameters", {"key": "access_type", "value": "offline"})
    app.append("query_parameters", {"key": "prompt", "value": "consent"})

    app.get_openid_configuration()
    app.insert()
    frappe.db.commit()

    return {"status": "created", "name": app.name}
```

### Dropbox Integration

```python
def setup_dropbox_integration(app_key: str, app_secret: str):
    """Setup Dropbox Connected App."""

    app = frappe.new_doc("Connected App")
    app.provider_name = "Dropbox"
    app.client_id = app_key
    app.client_secret = app_secret
    app.authorization_uri = "https://www.dropbox.com/oauth2/authorize"
    app.token_uri = "https://api.dropboxapi.com/oauth2/token"

    # Dropbox doesn't use traditional scopes
    # Access is determined by app type in Dropbox App Console

    # Query parameter for offline access
    app.append("query_parameters", {"key": "token_access_type", "value": "offline"})

    app.insert()
    frappe.db.commit()

    return app.name
```

### Salesforce Integration

```python
def setup_salesforce_integration(
    client_id: str,
    client_secret: str,
    instance_url: str = "https://login.salesforce.com"
):
    """Setup Salesforce Connected App."""

    app = frappe.new_doc("Connected App")
    app.provider_name = "Salesforce"
    app.client_id = client_id
    app.client_secret = client_secret
    app.authorization_uri = f"{instance_url}/services/oauth2/authorize"
    app.token_uri = f"{instance_url}/services/oauth2/token"

    # Salesforce scopes
    scopes = ["api", "refresh_token", "openid", "id"]
    for scope in scopes:
        app.append("scopes", {"scope": scope})

    app.insert()
    frappe.db.commit()

    return app.name
```

### Slack Integration

```python
def setup_slack_integration(client_id: str, client_secret: str):
    """Setup Slack Connected App."""

    app = frappe.new_doc("Connected App")
    app.provider_name = "Slack"
    app.client_id = client_id
    app.client_secret = client_secret
    app.authorization_uri = "https://slack.com/oauth/v2/authorize"
    app.token_uri = "https://slack.com/api/oauth.v2.access"

    # Slack bot scopes
    scopes = [
        "channels:read",
        "chat:write",
        "users:read",
        "files:read"
    ]
    for scope in scopes:
        app.append("scopes", {"scope": scope})

    app.insert()
    frappe.db.commit()

    return app.name
```

## Using Connected Apps

```python
def use_google_drive(user: str = None):
    """Example: List files from Google Drive."""

    if not user:
        user = frappe.session.user

    app = frappe.get_doc("Connected App", {"provider_name": "Google Drive"})

    # Check if user has token
    from frappe.integrations.doctype.connected_app.connected_app import has_token
    if not has_token("Google Drive", user):
        # Need to authorize
        auth_url = app.initiate_web_application_flow(user=user)
        return {"needs_authorization": True, "auth_url": auth_url}

    # Get OAuth session
    session = app.get_oauth2_session(user=user)

    # Make API call
    response = session.get(
        "https://www.googleapis.com/drive/v3/files",
        params={"pageSize": 10}
    )

    return response.json()
```

## Troubleshooting

### Invalid Client Error
- Verify client_id and client_secret
- Check redirect URI is registered in provider
- Ensure OAuth consent screen is configured

### Scope Errors
- Verify scopes are valid for the provider
- Some scopes require app verification
- Check if user has granted the scope

### Token Issues
- Ensure "offline_access" or equivalent scope
- Check Token Cache for stored tokens
- Verify token_uri is correct

## Next Steps

- [Social Login Setup](../social-login-setup/social-login-setup.md)
- [Token Management and Refresh](../token-management-refresh/token-management-refresh.md)

---

*Source: Frappe Integration Documentation | Difficulty: Intermediate | Last updated: 2026-02-04*
