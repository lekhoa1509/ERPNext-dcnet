# Webhook Documentation

Webhooks notify external systems when document events occur in Frappe.

## Document Events

| Event | Trigger |
|-------|---------|
| `after_insert` | After new document created |
| `on_update` | After document updated |
| `on_submit` | After document submitted |
| `on_cancel` | After document cancelled |
| `on_trash` | Before document deleted |
| `on_update_after_submit` | After submitted doc updated |
| `on_change` | After any field changed |
| `workflow_transition` | After workflow state change |

## Create Webhook via UI

```
Integrations > Webhook > New
```

## Create Webhook via API

```python
import frappe

webhook = frappe.new_doc("Webhook")
webhook.webhook_doctype = "Sales Order"
webhook.webhook_docevent = "on_submit"
webhook.request_url = "https://external-api.com/webhooks/sales-order"
webhook.request_method = "POST"
webhook.request_structure = "JSON"
webhook.enabled = 1

# Add custom headers
webhook.append("webhook_headers", {
    "key": "Authorization",
    "value": "Bearer my-api-key"
})
webhook.append("webhook_headers", {
    "key": "Content-Type",
    "value": "application/json"
})

# Define payload fields
webhook.append("webhook_data", {
    "fieldname": "name",
    "key": "order_id"
})
webhook.append("webhook_data", {
    "fieldname": "customer",
    "key": "customer_name"
})
webhook.append("webhook_data", {
    "fieldname": "grand_total",
    "key": "total_amount"
})

webhook.insert()
```

## JSON Template Payload

```python
webhook.request_structure = "JSON"
webhook.webhook_json = '''
{
    "event": "sales_order_submitted",
    "data": {
        "order_id": "{{ doc.name }}",
        "customer": "{{ doc.customer }}",
        "items": [
            {% for item in doc.items %}
            {
                "item_code": "{{ item.item_code }}",
                "qty": {{ item.qty }},
                "rate": {{ item.rate }}
            }{% if not loop.last %},{% endif %}
            {% endfor %}
        ],
        "grand_total": {{ doc.grand_total }},
        "currency": "{{ doc.currency }}"
    },
    "timestamp": "{{ frappe.utils.now() }}"
}
'''
```

## Conditional Webhook

```python
# Only trigger for specific conditions
webhook.condition = "doc.grand_total > 10000 and doc.customer_group == 'VIP'"
```

## Webhook Security (HMAC Signature)

```python
webhook.enable_security = 1
webhook.webhook_secret = "my-secret-key"

# Receiver can verify signature:
# Header: X-Frappe-Webhook-Signature
# Signature = base64(hmac-sha256(secret, json_payload))
```

## Dynamic URL

```python
webhook.is_dynamic_url = 1
webhook.request_url = "https://api.example.com/customers/{{ doc.customer }}/orders"
```

## Check Webhook Logs

```python
# Get recent webhook logs
logs = frappe.get_all(
    "Webhook Request Log",
    filters={"webhook": "My Webhook"},
    fields=["name", "url", "response", "error", "creation"],
    order_by="creation desc",
    limit=10
)

for log in logs:
    print(f"{log.creation}: {log.url}")
    if log.error:
        print(f"  Error: {log.error}")
```

## Webhook Fields Reference

| Field | Type | Description |
|-------|------|-------------|
| `webhook_doctype` | Link | Trigger DocType |
| `webhook_docevent` | Select | Event type |
| `request_url` | SmallText | Target URL |
| `request_method` | Select | POST/PUT/DELETE |
| `request_structure` | Select | Form/JSON |
| `condition` | SmallText | Trigger condition |
| `enabled` | Check | Active status |
| `enable_security` | Check | HMAC signing |
| `webhook_secret` | Password | HMAC secret |
| `timeout` | Int | Request timeout (seconds) |
| `webhook_headers` | Table | Custom headers |
| `webhook_data` | Table | Field mapping |
| `webhook_json` | Code | JSON template |
