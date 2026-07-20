# How To: Webhook Security with Signatures

**Difficulty**: Intermediate
**Estimated Time**: 20 minutes
**Tags**: webhook, security, hmac, signature, validation

## Overview

Learn how to secure webhooks using HMAC signatures to verify that incoming webhook requests are authentic and haven't been tampered with.

## Prerequisites

- Basic webhook setup knowledge
- Understanding of HMAC cryptography
- Python programming basics

## Step-by-Step Guide

### Step 1: Configure Webhook Secret

```python
import frappe

# Create webhook with secret
webhook = frappe.get_doc("Webhook", "your-webhook-name")
webhook.webhook_secret = frappe.generate_hash(length=32)  # Generate a secure secret
webhook.save()

# Store the secret securely for the receiving endpoint
print(f"Webhook Secret: {webhook.webhook_secret}")
```

### Step 2: Understanding the Signature Header

Frappe sends the HMAC-SHA256 signature in the `X-Frappe-Webhook-Signature` header. The signature is computed as:

```python
import hmac
import hashlib

def compute_signature(payload: str, secret: str) -> str:
    """Compute HMAC-SHA256 signature for webhook payload."""
    return hmac.new(
        key=secret.encode('utf-8'),
        msg=payload.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()
```

### Step 3: Validate Signature on Receiving Server

```python
import hmac
import hashlib
from flask import Flask, request, abort

app = Flask(__name__)
WEBHOOK_SECRET = "your-webhook-secret"  # Same as configured in Frappe

@app.route('/webhook', methods=['POST'])
def receive_webhook():
    # Get signature from header
    received_signature = request.headers.get('X-Frappe-Webhook-Signature')

    if not received_signature:
        abort(401, "Missing signature header")

    # Compute expected signature
    payload = request.get_data(as_text=True)
    expected_signature = hmac.new(
        key=WEBHOOK_SECRET.encode('utf-8'),
        msg=payload.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    # Validate signature using constant-time comparison
    if not hmac.compare_digest(received_signature, expected_signature):
        abort(401, "Invalid signature")

    # Process the webhook
    data = request.get_json()
    print(f"Received valid webhook: {data}")

    return {"status": "success"}, 200
```

### Step 4: Django Example

```python
import hmac
import hashlib
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

WEBHOOK_SECRET = "your-webhook-secret"

@csrf_exempt
@require_POST
def webhook_handler(request):
    # Get signature from header
    received_signature = request.headers.get('X-Frappe-Webhook-Signature')

    if not received_signature:
        return HttpResponseForbidden("Missing signature")

    # Compute expected signature
    payload = request.body.decode('utf-8')
    expected_signature = hmac.new(
        key=WEBHOOK_SECRET.encode('utf-8'),
        msg=payload.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    # Validate
    if not hmac.compare_digest(received_signature, expected_signature):
        return HttpResponseForbidden("Invalid signature")

    # Process webhook
    data = json.loads(payload)
    # ... handle data ...

    return JsonResponse({"status": "success"})
```

### Step 5: Node.js/Express Example

```javascript
const express = require('express');
const crypto = require('crypto');
const app = express();

const WEBHOOK_SECRET = 'your-webhook-secret';

app.use(express.json({
    verify: (req, res, buf) => {
        req.rawBody = buf.toString();
    }
}));

app.post('/webhook', (req, res) => {
    const receivedSignature = req.headers['x-frappe-webhook-signature'];

    if (!receivedSignature) {
        return res.status(401).json({ error: 'Missing signature' });
    }

    // Compute expected signature
    const expectedSignature = crypto
        .createHmac('sha256', WEBHOOK_SECRET)
        .update(req.rawBody)
        .digest('hex');

    // Validate using timing-safe comparison
    const sigBuffer = Buffer.from(receivedSignature);
    const expectedBuffer = Buffer.from(expectedSignature);

    if (sigBuffer.length !== expectedBuffer.length ||
        !crypto.timingSafeEqual(sigBuffer, expectedBuffer)) {
        return res.status(401).json({ error: 'Invalid signature' });
    }

    // Process webhook
    console.log('Valid webhook received:', req.body);
    res.json({ status: 'success' });
});

app.listen(3000);
```

## Complete Example

```python
import frappe
import hmac
import hashlib

def setup_secure_webhook(doctype: str, event: str, url: str) -> str:
    """Create a webhook with HMAC signature security."""

    # Generate a secure secret
    secret = frappe.generate_hash(length=32)

    webhook = frappe.new_doc("Webhook")
    webhook.webhook_doctype = doctype
    webhook.webhook_docevent = event
    webhook.enabled = 1
    webhook.request_url = url
    webhook.request_method = "POST"
    webhook.webhook_secret = secret

    # Add headers
    webhook.append("webhook_headers", {
        "key": "Content-Type",
        "value": "application/json"
    })

    webhook.insert()
    frappe.db.commit()

    return {
        "webhook_name": webhook.name,
        "secret": secret,
        "message": "Store this secret securely for signature validation"
    }

# Usage
result = setup_secure_webhook("Sales Order", "on_submit", "https://api.example.com/orders")
print(result)
```

## Security Best Practices

1. **Use Constant-Time Comparison**: Always use `hmac.compare_digest()` or equivalent to prevent timing attacks
2. **Rotate Secrets Regularly**: Update webhook secrets periodically
3. **Use HTTPS**: Always use HTTPS endpoints for webhooks
4. **Validate Timestamps**: Consider adding timestamp validation to prevent replay attacks
5. **Log Failed Attempts**: Monitor and log failed signature validations

## Troubleshooting

### Signature Mismatch
- Ensure the secret matches exactly on both ends
- Check that the payload encoding is consistent (UTF-8)
- Verify no middleware is modifying the request body

### Missing Header
- Ensure webhook secret is configured in Frappe
- Check that your web server isn't stripping custom headers

## Next Steps

- [Webhook Event Handling Patterns](../webhook-event-handling/webhook-event-handling.md)
- [Rate Limiting and Retry Logic](../rate-limiting-retry-logic/rate-limiting-retry-logic.md)

---

*Source: Frappe Integration Documentation | Difficulty: Intermediate | Last updated: 2026-02-04*
