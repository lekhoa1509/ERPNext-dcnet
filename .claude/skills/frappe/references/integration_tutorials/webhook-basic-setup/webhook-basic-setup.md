# How To: Webhook Basic Setup

**Difficulty**: Beginner
**Estimated Time**: 15 minutes
**Tags**: webhook, integration, http, callback

## Overview

Learn how to create and configure a basic webhook in Frappe to send HTTP callbacks when document events occur.

## Prerequisites

- Frappe Framework installed
- Administrator access
- Understanding of DocTypes and document events

## Step-by-Step Guide

### Step 1: Navigate to Webhook DocType

Access the Webhook list via Frappe Desk:
- Go to Search Bar > Type "Webhook"
- Or navigate to: Setup > Integrations > Webhook

### Step 2: Create a New Webhook

```python
import frappe

# Create webhook programmatically
webhook = frappe.new_doc("Webhook")
webhook.webhook_doctype = "Lead"
webhook.webhook_docevent = "after_insert"
webhook.enabled = 1
webhook.request_url = "https://your-endpoint.com/webhook"
webhook.request_method = "POST"
webhook.insert()
```

### Step 3: Configure Webhook Fields

Define the data fields to send with the webhook:

```python
webhook = frappe.get_doc("Webhook", "your-webhook-name")

# Add webhook data fields
webhook.append("webhook_data", {
    "fieldname": "name",
    "key": "document_id"
})
webhook.append("webhook_data", {
    "fieldname": "lead_name",
    "key": "lead_name"
})
webhook.append("webhook_data", {
    "fieldname": "email_id",
    "key": "email"
})
webhook.save()
```

### Step 4: Set Custom Headers

```python
# Add custom headers
webhook.append("webhook_headers", {
    "key": "Content-Type",
    "value": "application/json"
})
webhook.append("webhook_headers", {
    "key": "X-API-Key",
    "value": "your-api-key"
})
webhook.save()
```

### Step 5: Enable Webhook

```python
# Enable the webhook
webhook.enabled = 1
webhook.save()
```

## Complete Example

```python
import frappe

def create_lead_webhook():
    """Create a webhook that triggers when a new Lead is created."""

    # Check if webhook already exists
    if frappe.db.exists("Webhook", {"webhook_doctype": "Lead", "webhook_docevent": "after_insert"}):
        frappe.log("Lead webhook already exists")
        return

    webhook = frappe.new_doc("Webhook")

    # Basic configuration
    webhook.webhook_doctype = "Lead"
    webhook.webhook_docevent = "after_insert"
    webhook.enabled = 1
    webhook.request_url = "https://api.example.com/leads"
    webhook.request_method = "POST"

    # Data fields to send
    webhook.append("webhook_data", {"fieldname": "name", "key": "id"})
    webhook.append("webhook_data", {"fieldname": "lead_name", "key": "name"})
    webhook.append("webhook_data", {"fieldname": "email_id", "key": "email"})
    webhook.append("webhook_data", {"fieldname": "phone", "key": "phone"})
    webhook.append("webhook_data", {"fieldname": "company_name", "key": "company"})

    # Headers
    webhook.append("webhook_headers", {"key": "Content-Type", "value": "application/json"})
    webhook.append("webhook_headers", {"key": "Authorization", "value": "Bearer your-token"})

    webhook.insert()
    frappe.db.commit()

    return webhook.name

# Execute
webhook_name = create_lead_webhook()
print(f"Created webhook: {webhook_name}")
```

## Available Document Events

| Event | Description |
|-------|-------------|
| `after_insert` | After a new document is created |
| `on_update` | After a document is updated |
| `on_submit` | After a document is submitted |
| `on_cancel` | After a document is cancelled |
| `on_trash` | After a document is deleted |
| `on_change` | After any change to the document |

## Troubleshooting

### Webhook Not Firing
- Verify the webhook is enabled (`enabled = 1`)
- Check that the DocType and event match your use case
- Review Webhook Request Log for errors

### Request Failures
- Verify the request URL is accessible
- Check firewall rules and network connectivity
- Review response codes in Webhook Request Log

## Next Steps

- [Webhook Security with Signatures](../webhook-security-signatures/webhook-security-signatures.md)
- [Webhook Conditional Execution](../webhook-conditional-execution/webhook-conditional-execution.md)
- [Integration Request Debugging](../integration-request-debugging/integration-request-debugging.md)

---

*Source: Frappe Integration Documentation | Difficulty: Beginner | Last updated: 2026-02-04*
