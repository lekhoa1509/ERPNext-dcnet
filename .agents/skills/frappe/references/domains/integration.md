<!-- Source: frappe-integration skill -->

# Frappe Integration Skill

> Comprehensive guide for integrating Frappe/ERPNext with external systems.

## Quick Topic Reference

| Topic | Documentation | API Reference |
|-------|---------------|---------------|
| **Webhook** | [references/docs/webhook.md](references/docs/webhook.md) | [api_reference/webhook.md](api_reference/webhook.md) |
| **OAuth Provider** | [references/docs/oauth-provider.md](references/docs/oauth-provider.md) | [api_reference/oauth2.md](api_reference/oauth2.md) |
| **Connected App** | [references/docs/connected-app.md](references/docs/connected-app.md) | [api_reference/connected_app.md](api_reference/connected_app.md) |
| **Social Login** | [references/docs/social-login.md](references/docs/social-login.md) | [api_reference/social_login_key.md](api_reference/social_login_key.md) |
| **Integration Request** | [references/docs/integration-request.md](references/docs/integration-request.md) | [api_reference/integration_request.md](api_reference/integration_request.md) |
| **WooCommerce Pattern** | [references/docs/woocommerce-pattern.md](references/docs/woocommerce-pattern.md) | - |

## When to Use This Skill

Use this skill when you need to:
- Send HTTP callbacks on document events (Webhooks)
- Expose API via OAuth 2.0 (OAuth Provider)
- Connect to external OAuth2 services (Connected App)
- Enable social login (Google, GitHub, Facebook, etc.)
- Log and debug HTTP requests (Integration Request)
- Integrate with WooCommerce or similar e-commerce platforms

## Core DocTypes

| DocType | Purpose |
|---------|---------|
| **Webhook** | Send HTTP callbacks on document events |
| **Webhook Request Log** | Track webhook execution history |
| **Connected App** | OAuth2 client to external services |
| **Token Cache** | Store OAuth tokens per user |
| **OAuth Client** | OAuth2 provider (expose API) |
| **OAuth Bearer Token** | Issued access tokens |
| **Social Login Key** | Social login providers (Google, GitHub, etc.) |
| **Integration Request** | HTTP request/response logging |

## ⚡ Quick Reference

### Codebase Statistics

**Languages:**
- **Python**: 54 files (100.0%)

**Analysis Performed:**
- ✅ API Reference (C2.5)
- ✅ Dependency Graph (C2.6)
- ✅ Design Patterns (C3.1)
- ✅ Test Examples (C3.2)
- ✅ Configuration Patterns (C3.4)
- ✅ Architectural Analysis (C3.7)
- ✅ Project Documentation (C3.9)

### 🎨 Design Patterns Detected

*From C3.1 codebase analysis (confidence > 0.7)*

- **Factory**: 6 instances
- **TemplateMethod**: 1 instances

*Total: 7 high-confidence patterns*

*See `references/patterns/` for complete pattern analysis*

## 📝 Code Examples

*High-quality examples extracted from test files (C3.2)*

**Workflow: Create and test webhook with JSON array** (complexity: 0.80)

```python
wh_config = {
    'doctype': 'Webhook',
    'webhook_doctype': 'Note',
    'webhook_docevent': 'on_change',
    'enabled': 1,
    'request_url': 'https://httpbin.org/post',
    'request_method': 'POST',
    'request_structure': 'JSON',
    'webhook_json': '''[
        {% for n in range(3) %}
        {"title": "{{ doc.title }}"}
        {%- if not loop.last -%},{%endif%}
        {% endfor %}
    ]''',
    'meets_condition': 'Yes',
    'webhook_headers': [{'key': 'Content-Type', 'value': 'application/json'}]
}

doc = frappe.new_doc('Note')
doc.title = 'Test Webhook Note'
doc.insert()

# Test webhook execution
with get_test_webhook(wh_config):
    doc.title = frappe.generate_hash()
    doc.save()
    flush_webhook_execution_queue()
    log = frappe.get_last_doc('Webhook Request Log')
```

**Workflow: Test Connected App OAuth flow** (complexity: 0.80)

```python
# Create Connected App
app = frappe.new_doc("Connected App")
app.provider_name = "Test Provider"
app.client_id = "test-client-id"
app.client_secret = "test-secret"
app.authorization_uri = "https://example.com/oauth/authorize"
app.token_uri = "https://example.com/oauth/token"
app.insert()

# Initiate OAuth flow
auth_url = app.initiate_web_application_flow(
    user=frappe.session.user,
    success_uri="/app"
)

# Check token status
from frappe.integrations.doctype.connected_app.connected_app import has_token
has_valid_token = has_token("Test Provider", frappe.session.user)
```

*See `references/test_examples/` for all 40 extracted examples*

## ⚙️ Configuration Patterns

*From C3.4 configuration analysis*

**Configuration Files Analyzed:** 29
**Total Settings:** 531
**Patterns Detected:** 0

**Configuration Types:**
- DocType JSON: 29 files

*See `references/config_patterns/` for detailed configuration analysis*

## 📚 Available References

This skill includes detailed reference documentation:

- **Manual Docs**: `references/docs/` - Comprehensive how-to guides
  - [webhook.md](references/docs/webhook.md) - Webhook configuration & examples
  - [oauth-provider.md](references/docs/oauth-provider.md) - OAuth 2.0 Provider setup
  - [connected-app.md](references/docs/connected-app.md) - Connected App (OAuth Client)
  - [social-login.md](references/docs/social-login.md) - Social Login setup
  - [integration-request.md](references/docs/integration-request.md) - Request logging
  - [woocommerce-pattern.md](references/docs/woocommerce-pattern.md) - WooCommerce integration

- **API Reference**: `api_reference/` - Complete API documentation (54 files)
- **Dependencies**: `dependencies/` - Dependency graph and analysis
- **Patterns**: `patterns/` - Detected design patterns
- **Examples**: `test_examples/` - Usage examples from tests (40 examples)
- **Configuration**: `config_patterns/` - Configuration patterns
- **Tutorials**: `tutorials/` - How-to guides

## Related Skills

- **frappe** - Frappe Framework core (REST API, hooks)
- **frappe-data-import** - Data Import/Export
- **erpnext_accounting** - ERPNext Accounts (Payment gateways)

---

**Generated by Skill Seeker** | Codebase Analyzer with C3.x Analysis
