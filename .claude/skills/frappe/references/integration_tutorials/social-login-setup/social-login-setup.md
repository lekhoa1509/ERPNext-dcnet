# How To: Social Login Setup

**Difficulty**: Intermediate
**Estimated Time**: 30 minutes
**Tags**: social-login, authentication, google, github, facebook, oauth

## Overview

Learn how to configure social login providers (Google, GitHub, Facebook, Office 365) to allow users to log into Frappe using their existing social accounts.

## Prerequisites

- Administrator access to Frappe
- OAuth credentials from social providers
- HTTPS enabled on your site

## Step-by-Step Guide

### Step 1: Navigate to Social Login Key

Go to: **Setup > Integrations > Social Login Key**

Or via URL: `/app/social-login-key`

### Step 2: Setup Google Login

```python
import frappe

def setup_google_login(client_id: str, client_secret: str):
    """Setup Google social login."""

    # Check if already exists
    if frappe.db.exists("Social Login Key", {"provider_name": "Google"}):
        doc = frappe.get_doc("Social Login Key", {"provider_name": "Google"})
    else:
        doc = frappe.new_doc("Social Login Key")

    doc.provider_name = "Google"
    doc.enable_social_login = 1
    doc.social_login_provider = "Google"
    doc.client_id = client_id
    doc.client_secret = client_secret

    # Google OAuth endpoints
    doc.base_url = "https://www.googleapis.com"
    doc.authorize_url = "https://accounts.google.com/o/oauth2/v2/auth"
    doc.access_token_url = "https://oauth2.googleapis.com/token"

    # User info endpoint
    doc.api_endpoint = "https://www.googleapis.com/oauth2/v2/userinfo"
    doc.api_endpoint_args = None

    # Icon for login page
    doc.icon = "fa fa-google"

    # Allow signup for new users
    doc.sign_ups = "Allow"

    doc.save()
    frappe.db.commit()

    return doc.name

# Usage
# Get credentials from Google Cloud Console > APIs & Services > Credentials
setup_google_login(
    client_id="your-client-id.apps.googleusercontent.com",
    client_secret="your-client-secret"
)
```

### Step 3: Setup GitHub Login

```python
def setup_github_login(client_id: str, client_secret: str):
    """Setup GitHub social login."""

    if frappe.db.exists("Social Login Key", {"provider_name": "GitHub"}):
        doc = frappe.get_doc("Social Login Key", {"provider_name": "GitHub"})
    else:
        doc = frappe.new_doc("Social Login Key")

    doc.provider_name = "GitHub"
    doc.enable_social_login = 1
    doc.social_login_provider = "GitHub"
    doc.client_id = client_id
    doc.client_secret = client_secret

    # GitHub OAuth endpoints
    doc.base_url = "https://api.github.com"
    doc.authorize_url = "https://github.com/login/oauth/authorize"
    doc.access_token_url = "https://github.com/login/oauth/access_token"

    # User info endpoint
    doc.api_endpoint = "https://api.github.com/user"
    doc.api_endpoint_args = None

    # Icon
    doc.icon = "fa fa-github"
    doc.sign_ups = "Allow"

    doc.save()
    frappe.db.commit()

    return doc.name

# Get credentials from GitHub > Settings > Developer settings > OAuth Apps
setup_github_login(
    client_id="your-github-client-id",
    client_secret="your-github-client-secret"
)
```

### Step 4: Setup Facebook Login

```python
def setup_facebook_login(app_id: str, app_secret: str):
    """Setup Facebook social login."""

    if frappe.db.exists("Social Login Key", {"provider_name": "Facebook"}):
        doc = frappe.get_doc("Social Login Key", {"provider_name": "Facebook"})
    else:
        doc = frappe.new_doc("Social Login Key")

    doc.provider_name = "Facebook"
    doc.enable_social_login = 1
    doc.social_login_provider = "Facebook"
    doc.client_id = app_id
    doc.client_secret = app_secret

    # Facebook OAuth endpoints
    doc.base_url = "https://graph.facebook.com"
    doc.authorize_url = "https://www.facebook.com/v18.0/dialog/oauth"
    doc.access_token_url = "https://graph.facebook.com/v18.0/oauth/access_token"

    # User info endpoint with fields
    doc.api_endpoint = "https://graph.facebook.com/me"
    doc.api_endpoint_args = '{"fields": "id,name,email,picture"}'

    # Icon
    doc.icon = "fa fa-facebook"
    doc.sign_ups = "Allow"

    doc.save()
    frappe.db.commit()

    return doc.name
```

### Step 5: Setup Microsoft/Office 365 Login

```python
def setup_microsoft_login(client_id: str, client_secret: str, tenant_id: str = "common"):
    """Setup Microsoft/Office 365 social login."""

    if frappe.db.exists("Social Login Key", {"provider_name": "Office 365"}):
        doc = frappe.get_doc("Social Login Key", {"provider_name": "Office 365"})
    else:
        doc = frappe.new_doc("Social Login Key")

    doc.provider_name = "Office 365"
    doc.enable_social_login = 1
    doc.social_login_provider = "Office 365"
    doc.client_id = client_id
    doc.client_secret = client_secret

    # Microsoft OAuth endpoints
    doc.base_url = "https://graph.microsoft.com"
    doc.authorize_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
    doc.access_token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    # User info endpoint
    doc.api_endpoint = "https://graph.microsoft.com/v1.0/me"
    doc.api_endpoint_args = None

    # Icon
    doc.icon = "fa fa-windows"
    doc.sign_ups = "Allow"

    doc.save()
    frappe.db.commit()

    return doc.name

# For Azure AD: use your tenant ID
# For personal accounts: use "common" or "consumers"
```

### Step 6: Setup Keycloak Login

```python
def setup_keycloak_login(
    realm: str,
    keycloak_url: str,
    client_id: str,
    client_secret: str
):
    """Setup Keycloak social login."""

    provider_name = f"Keycloak ({realm})"

    if frappe.db.exists("Social Login Key", {"provider_name": provider_name}):
        doc = frappe.get_doc("Social Login Key", {"provider_name": provider_name})
    else:
        doc = frappe.new_doc("Social Login Key")

    doc.provider_name = provider_name
    doc.enable_social_login = 1
    doc.social_login_provider = "Custom"
    doc.client_id = client_id
    doc.client_secret = client_secret

    # Keycloak endpoints
    base_url = f"{keycloak_url}/realms/{realm}"
    doc.base_url = base_url
    doc.authorize_url = f"{base_url}/protocol/openid-connect/auth"
    doc.access_token_url = f"{base_url}/protocol/openid-connect/token"

    # User info endpoint
    doc.api_endpoint = f"{base_url}/protocol/openid-connect/userinfo"
    doc.api_endpoint_args = None

    # Icon
    doc.icon = "fa fa-key"
    doc.sign_ups = "Allow"

    doc.save()
    frappe.db.commit()

    return doc.name

# Usage
setup_keycloak_login(
    realm="myrealm",
    keycloak_url="https://keycloak.example.com",
    client_id="frappe-app",
    client_secret="your-client-secret"
)
```

## Complete Setup Script

```python
import frappe

class SocialLoginSetup:
    """Comprehensive social login setup helper."""

    PROVIDERS = {
        "Google": {
            "base_url": "https://www.googleapis.com",
            "authorize_url": "https://accounts.google.com/o/oauth2/v2/auth",
            "access_token_url": "https://oauth2.googleapis.com/token",
            "api_endpoint": "https://www.googleapis.com/oauth2/v2/userinfo",
            "icon": "fa fa-google"
        },
        "GitHub": {
            "base_url": "https://api.github.com",
            "authorize_url": "https://github.com/login/oauth/authorize",
            "access_token_url": "https://github.com/login/oauth/access_token",
            "api_endpoint": "https://api.github.com/user",
            "icon": "fa fa-github"
        },
        "Facebook": {
            "base_url": "https://graph.facebook.com",
            "authorize_url": "https://www.facebook.com/v18.0/dialog/oauth",
            "access_token_url": "https://graph.facebook.com/v18.0/oauth/access_token",
            "api_endpoint": "https://graph.facebook.com/me",
            "api_endpoint_args": '{"fields": "id,name,email,picture"}',
            "icon": "fa fa-facebook"
        },
        "Office 365": {
            "base_url": "https://graph.microsoft.com",
            "authorize_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
            "access_token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
            "api_endpoint": "https://graph.microsoft.com/v1.0/me",
            "icon": "fa fa-windows"
        }
    }

    @classmethod
    def setup_provider(cls, provider: str, client_id: str, client_secret: str, allow_signup: bool = True):
        """Setup a social login provider."""

        if provider not in cls.PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}")

        config = cls.PROVIDERS[provider]

        if frappe.db.exists("Social Login Key", {"provider_name": provider}):
            doc = frappe.get_doc("Social Login Key", {"provider_name": provider})
        else:
            doc = frappe.new_doc("Social Login Key")

        doc.provider_name = provider
        doc.enable_social_login = 1
        doc.social_login_provider = provider
        doc.client_id = client_id
        doc.client_secret = client_secret
        doc.base_url = config["base_url"]
        doc.authorize_url = config["authorize_url"]
        doc.access_token_url = config["access_token_url"]
        doc.api_endpoint = config["api_endpoint"]
        doc.api_endpoint_args = config.get("api_endpoint_args")
        doc.icon = config["icon"]
        doc.sign_ups = "Allow" if allow_signup else "Deny"

        doc.save()
        frappe.db.commit()

        return {"status": "success", "provider": provider}

    @classmethod
    def setup_all(cls, credentials: dict):
        """Setup multiple providers at once."""
        results = []

        for provider, creds in credentials.items():
            try:
                result = cls.setup_provider(
                    provider=provider,
                    client_id=creds["client_id"],
                    client_secret=creds["client_secret"],
                    allow_signup=creds.get("allow_signup", True)
                )
                results.append(result)
            except Exception as e:
                results.append({"status": "error", "provider": provider, "error": str(e)})

        return results

    @classmethod
    def list_enabled(cls):
        """List all enabled social login providers."""
        return frappe.get_all(
            "Social Login Key",
            filters={"enable_social_login": 1},
            fields=["provider_name", "icon", "sign_ups"]
        )

    @classmethod
    def disable_provider(cls, provider: str):
        """Disable a social login provider."""
        if frappe.db.exists("Social Login Key", {"provider_name": provider}):
            doc = frappe.get_doc("Social Login Key", {"provider_name": provider})
            doc.enable_social_login = 0
            doc.save()
            frappe.db.commit()
            return True
        return False

# Usage
credentials = {
    "Google": {
        "client_id": "google-client-id.apps.googleusercontent.com",
        "client_secret": "google-secret"
    },
    "GitHub": {
        "client_id": "github-client-id",
        "client_secret": "github-secret"
    }
}

results = SocialLoginSetup.setup_all(credentials)
print(results)
```

## Redirect URI Configuration

For each provider, configure the redirect URI in their developer console:

```
https://your-frappe-site.com/api/method/frappe.integrations.oauth2_logins.login_via_oauth2
```

Or for specific providers:
- Google: `https://your-site.com/api/method/frappe.integrations.oauth2_logins.login_via_google`
- GitHub: `https://your-site.com/api/method/frappe.integrations.oauth2_logins.login_via_github`
- Facebook: `https://your-site.com/api/method/frappe.integrations.oauth2_logins.login_via_facebook`

## Controlling User Signup

```python
def configure_signup_settings(provider: str, allow_signup: bool, restrict_domains: list = None):
    """Configure signup settings for a provider."""

    doc = frappe.get_doc("Social Login Key", {"provider_name": provider})

    # Allow or deny signups
    doc.sign_ups = "Allow" if allow_signup else "Deny"

    doc.save()
    frappe.db.commit()

    # Optionally restrict to specific email domains
    if restrict_domains:
        # Store in site_config.json or custom doctype
        frappe.conf.allowed_social_login_domains = restrict_domains

# Only allow @company.com emails
configure_signup_settings("Google", allow_signup=True, restrict_domains=["company.com"])
```

## Troubleshooting

### Login Fails Silently
- Check browser console for errors
- Verify redirect URI matches exactly
- Ensure HTTPS is properly configured

### User Not Created
- Check if `sign_ups` is set to "Allow"
- Verify email is returned from provider
- Check System Settings for disable_signup

### Invalid Token Error
- Verify client_secret is correct
- Check token endpoint URL
- Review provider's OAuth documentation

## Next Steps

- [Token Management and Refresh](../token-management-refresh/token-management-refresh.md)
- [OAuth Provider Setup](../oauth-provider-setup/oauth-provider-setup.md)

---

*Source: Frappe Integration Documentation | Difficulty: Intermediate | Last updated: 2026-02-04*
