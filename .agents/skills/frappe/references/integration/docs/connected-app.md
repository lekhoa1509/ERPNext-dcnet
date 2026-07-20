# OAuth 2.0 Client (Connected App)

Connect to external OAuth2 services (Google, Microsoft, custom).

## Create Connected App

```python
import frappe

app = frappe.new_doc("Connected App")
app.provider_name = "Google Calendar"
app.client_id = "your-google-client-id"
app.client_secret = "your-google-client-secret"
app.authorization_uri = "https://accounts.google.com/o/oauth2/v2/auth"
app.token_uri = "https://oauth2.googleapis.com/token"

# Add scopes
app.append("scopes", {"scope": "https://www.googleapis.com/auth/calendar.readonly"})
app.append("scopes", {"scope": "https://www.googleapis.com/auth/calendar.events"})

app.insert()
```

## Initiate OAuth Flow

```python
# Start authorization flow for current user
app = frappe.get_doc("Connected App", "Google Calendar")
auth_url = app.initiate_web_application_flow(
    user=frappe.session.user,
    success_uri="/app/my-calendar"
)
# Redirect user to auth_url
```

## Use Connected App Token

```python
import requests

app = frappe.get_doc("Connected App", "Google Calendar")

# Get active token (auto-refreshes if expired)
token_cache = app.get_active_token()

if token_cache:
    access_token = token_cache.get_password("access_token")

    # Make API call
    response = requests.get(
        "https://www.googleapis.com/calendar/v3/calendars/primary/events",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    events = response.json()
```

## Backend App Token (Client Credentials)

For server-to-server communication without user context:

```python
app = frappe.get_doc("Connected App", "My Service")

# Get token using client credentials grant
token_cache = app.get_backend_app_token()
access_token = token_cache.get_password("access_token")

# Use token for API calls
response = requests.get(
    "https://api.service.com/data",
    headers={"Authorization": f"Bearer {access_token}"}
)
```

## Check Token Status

```python
from frappe.integrations.doctype.connected_app.connected_app import has_token

# Check if user has valid token
if has_token("Google Calendar", frappe.session.user):
    print("User is connected")
else:
    print("User needs to authorize")
```

## Connected App Fields Reference

| Field | Type | Description |
|-------|------|-------------|
| `provider_name` | Data | Display name |
| `client_id` | Data | OAuth client ID |
| `client_secret` | Password | OAuth client secret |
| `authorization_uri` | SmallText | Auth endpoint |
| `token_uri` | Data | Token endpoint |
| `scopes` | Table | OAuth scopes |
| `redirect_uri` | Data | Callback URL (auto-set) |
