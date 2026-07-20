# Integration Request Logging

Track all outgoing HTTP requests for debugging.

## Enable Logging

```python
# In hooks.py
integration_requests = [
    "frappe.integrations.doctype.integration_request.integration_request.log_outgoing_request"
]
```

## Manual Logging

```python
from frappe.integrations.doctype.integration_request.integration_request import (
    create_request_log
)

# Log request
request_log = create_request_log(
    data={
        "url": "https://api.example.com/orders",
        "method": "POST",
        "body": {"order_id": "ORD-001"}
    },
    integration_type="API Call",
    service_name="External Order System",
    status="Queued"
)

# Update after response
request_log.status = "Completed"
request_log.output = response.json()
request_log.save()
```

## Query Integration Logs

```python
# Find failed requests
failed = frappe.get_all(
    "Integration Request",
    filters={
        "status": "Failed",
        "creation": (">", "2026-02-01")
    },
    fields=["name", "url", "error", "creation"]
)

for req in failed:
    print(f"{req.creation}: {req.url}")
    print(f"  Error: {req.error}")
```

## Best Practices

### 1. Webhook Reliability

```python
# Implement retry logic in receiver
# Frappe retries 3 times with backoff

# Return 2xx status for success
# Return 4xx/5xx to trigger retry
```

### 2. Token Security

```python
# Never log access tokens
# Use get_password() for token retrieval
# Tokens auto-refresh when expired
```

### 3. Rate Limiting

```python
# Implement rate limiting for webhooks
webhook.timeout = 30  # seconds

# Use background queue for heavy processing
webhook.background_jobs_queue = "long"
```

### 4. Error Handling

```python
try:
    response = requests.post(url, json=data, timeout=30)
    response.raise_for_status()
except requests.exceptions.Timeout:
    frappe.log_error("Webhook timeout")
except requests.exceptions.HTTPError as e:
    frappe.log_error(f"Webhook HTTP error: {e}")
```
