# Social Login

Enable users to login with Google, GitHub, Facebook, etc.

## Supported Providers

| Provider | Key Features |
|----------|--------------|
| **Google** | Gmail login, Google Workspace |
| **GitHub** | Developer authentication |
| **Facebook** | Meta/Facebook accounts |
| **Office 365** | Microsoft/Azure AD |
| **Keycloak** | Self-hosted identity provider |
| **Salesforce** | Salesforce accounts |
| **Custom** | Any OAuth2 provider |

## Configure Social Login

```python
import frappe

# Create social login key
slk = frappe.new_doc("Social Login Key")
slk.social_login_provider = "Google"
slk.provider_name = "Google"
slk.client_id = "your-google-client-id.apps.googleusercontent.com"
slk.client_secret = "your-google-client-secret"
slk.enable_social_login = 1
slk.sign_ups = "Allow"  # or "Deny" to only allow existing users

# URLs are auto-populated for standard providers
slk.insert()
```

## Custom OAuth Provider

```python
slk = frappe.new_doc("Social Login Key")
slk.social_login_provider = "Custom"
slk.provider_name = "My Identity Provider"
slk.client_id = "client-id"
slk.client_secret = "client-secret"
slk.base_url = "https://idp.example.com"
slk.authorize_url = "https://idp.example.com/oauth/authorize"
slk.access_token_url = "https://idp.example.com/oauth/token"
slk.redirect_url = "/api/method/frappe.integrations.oauth2_logins.custom"
slk.api_endpoint = "userinfo"
slk.user_id_property = "email"
slk.enable_social_login = 1
slk.insert()
```

## Login Redirect URLs

| Provider | Redirect URL |
|----------|-------------|
| Google | `/api/method/frappe.integrations.oauth2_logins.login_via_google` |
| GitHub | `/api/method/frappe.integrations.oauth2_logins.login_via_github` |
| Facebook | `/api/method/frappe.integrations.oauth2_logins.login_via_facebook` |
| Office 365 | `/api/method/frappe.integrations.oauth2_logins.login_via_office365` |
| Custom | `/api/method/frappe.integrations.oauth2_logins.custom` |

## Social Login Key Fields Reference

| Field | Type | Description |
|-------|------|-------------|
| `social_login_provider` | Select | Provider type |
| `provider_name` | Data | Display name |
| `client_id` | Data | OAuth client ID |
| `client_secret` | Password | OAuth secret |
| `enable_social_login` | Check | Enable login |
| `sign_ups` | Select | Allow/Deny new users |
| `authorize_url` | Data | Auth endpoint |
| `access_token_url` | Data | Token endpoint |
