# How To: Webhook Event Handling Patterns

**Difficulty**: Intermediate
**Estimated Time**: 25 minutes
**Tags**: webhook, event-handling, patterns, async, queue

## Overview

Learn different patterns for handling webhook events, including synchronous processing, async queues, and idempotent handlers.

## Prerequisites

- Webhook basic setup knowledge
- Understanding of async processing
- Python/JavaScript basics

## Step-by-Step Guide

### Step 1: Basic Event Handler Pattern

```python
# receiver_app/webhooks.py
import frappe
from flask import Flask, request, jsonify

app = Flask(__name__)

def handle_lead_created(data):
    """Handle new lead creation event."""
    lead_id = data.get('id')
    lead_name = data.get('name')
    email = data.get('email')

    # Process the lead
    print(f"New lead created: {lead_name} ({email})")

    # Sync to external CRM
    sync_to_external_crm(data)

    return {"processed": True}

def handle_lead_updated(data):
    """Handle lead update event."""
    lead_id = data.get('id')

    # Update external systems
    update_external_crm(lead_id, data)

    return {"processed": True}

# Event dispatcher
EVENT_HANDLERS = {
    "after_insert": handle_lead_created,
    "on_update": handle_lead_updated,
}

@app.route('/webhook/lead', methods=['POST'])
def webhook_lead():
    data = request.get_json()
    event = request.headers.get('X-Frappe-Webhook-Event', 'after_insert')

    handler = EVENT_HANDLERS.get(event)
    if handler:
        result = handler(data)
        return jsonify(result), 200

    return jsonify({"error": "Unknown event"}), 400
```

### Step 2: Async Queue Pattern with Redis

```python
# Using Redis Queue (RQ) for async processing
import redis
from rq import Queue
import json

redis_conn = redis.Redis(host='localhost', port=6379)
webhook_queue = Queue('webhooks', connection=redis_conn)

def process_webhook_async(webhook_data):
    """Process webhook in background."""
    event_type = webhook_data.get('event')
    payload = webhook_data.get('payload')

    # Actual processing logic
    if event_type == 'lead_created':
        create_lead_in_crm(payload)
    elif event_type == 'order_submitted':
        process_order(payload)

    return {"status": "completed"}

@app.route('/webhook', methods=['POST'])
def receive_webhook():
    """Receive webhook and queue for async processing."""
    data = request.get_json()

    # Enqueue the job
    job = webhook_queue.enqueue(
        process_webhook_async,
        data,
        job_timeout=300  # 5 minutes timeout
    )

    # Return immediately
    return jsonify({
        "status": "queued",
        "job_id": job.id
    }), 202
```

### Step 3: Idempotent Handler Pattern

```python
import frappe
import hashlib

def get_webhook_idempotency_key(data: dict) -> str:
    """Generate unique key for webhook payload."""
    payload_str = json.dumps(data, sort_keys=True)
    return hashlib.sha256(payload_str.encode()).hexdigest()

def is_webhook_processed(idempotency_key: str) -> bool:
    """Check if webhook was already processed."""
    return frappe.db.exists("Webhook Processing Log", {
        "idempotency_key": idempotency_key
    })

def mark_webhook_processed(idempotency_key: str, data: dict):
    """Mark webhook as processed."""
    log = frappe.new_doc("Webhook Processing Log")
    log.idempotency_key = idempotency_key
    log.payload = json.dumps(data)
    log.processed_at = frappe.utils.now()
    log.insert(ignore_permissions=True)
    frappe.db.commit()

@app.route('/webhook', methods=['POST'])
def idempotent_webhook_handler():
    """Handle webhook with idempotency check."""
    data = request.get_json()

    # Generate idempotency key
    idempotency_key = get_webhook_idempotency_key(data)

    # Check if already processed
    if is_webhook_processed(idempotency_key):
        return jsonify({
            "status": "already_processed",
            "idempotency_key": idempotency_key
        }), 200

    try:
        # Process webhook
        result = process_webhook(data)

        # Mark as processed
        mark_webhook_processed(idempotency_key, data)

        return jsonify({"status": "success", "result": result}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
```

### Step 4: Event-Driven Architecture with Frappe

```python
# In your Frappe app
import frappe

def setup_webhook_event_handlers():
    """Configure webhook event handlers in Frappe."""

    # Custom DocType for Webhook Events
    if not frappe.db.exists("DocType", "Webhook Event"):
        doc = frappe.new_doc("DocType")
        doc.name = "Webhook Event"
        doc.module = "Integrations"
        doc.autoname = "WE-.#####"
        doc.fields = [
            {"fieldname": "event_type", "fieldtype": "Data", "label": "Event Type"},
            {"fieldname": "payload", "fieldtype": "JSON", "label": "Payload"},
            {"fieldname": "status", "fieldtype": "Select", "label": "Status",
             "options": "Pending\nProcessing\nCompleted\nFailed"},
            {"fieldname": "error_message", "fieldtype": "Text", "label": "Error Message"},
            {"fieldname": "processed_at", "fieldtype": "Datetime", "label": "Processed At"}
        ]
        doc.insert()

def create_webhook_event(event_type: str, payload: dict):
    """Create a new webhook event for processing."""
    event = frappe.new_doc("Webhook Event")
    event.event_type = event_type
    event.payload = json.dumps(payload)
    event.status = "Pending"
    event.insert(ignore_permissions=True)
    frappe.db.commit()

    # Trigger async processing
    frappe.enqueue(
        process_webhook_event,
        event_name=event.name,
        queue='long'
    )

    return event.name

def process_webhook_event(event_name: str):
    """Process a webhook event asynchronously."""
    event = frappe.get_doc("Webhook Event", event_name)
    event.status = "Processing"
    event.save()
    frappe.db.commit()

    try:
        payload = json.loads(event.payload)

        # Route to appropriate handler
        if event.event_type == "lead_created":
            handle_lead_created(payload)
        elif event.event_type == "order_submitted":
            handle_order_submitted(payload)

        event.status = "Completed"
        event.processed_at = frappe.utils.now()
    except Exception as e:
        event.status = "Failed"
        event.error_message = str(e)

    event.save()
    frappe.db.commit()
```

### Step 5: Retry Pattern with Exponential Backoff

```python
import time
import random

def process_with_retry(func, data, max_retries=3, base_delay=1):
    """Execute function with exponential backoff retry."""

    for attempt in range(max_retries + 1):
        try:
            return func(data)
        except Exception as e:
            if attempt == max_retries:
                raise e

            # Exponential backoff with jitter
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            print(f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s")
            time.sleep(delay)

@app.route('/webhook', methods=['POST'])
def webhook_with_retry():
    data = request.get_json()

    try:
        result = process_with_retry(
            process_webhook,
            data,
            max_retries=3,
            base_delay=1
        )
        return jsonify({"status": "success", "result": result}), 200
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)}), 500
```

## Complete Example

```python
# Complete webhook event handler with all patterns
import frappe
import json
import hashlib
from functools import wraps

class WebhookEventHandler:
    def __init__(self):
        self.handlers = {}

    def register(self, event_type):
        """Decorator to register event handlers."""
        def decorator(func):
            self.handlers[event_type] = func
            return func
        return decorator

    def get_idempotency_key(self, data):
        payload_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(payload_str.encode()).hexdigest()

    def is_processed(self, key):
        return frappe.cache().exists(f"webhook_processed:{key}")

    def mark_processed(self, key, ttl=86400):
        frappe.cache().set(f"webhook_processed:{key}", 1, ttl)

    def handle(self, event_type, data):
        """Handle webhook event with idempotency."""
        # Generate idempotency key
        key = self.get_idempotency_key({"event": event_type, **data})

        # Check if already processed
        if self.is_processed(key):
            return {"status": "duplicate", "key": key}

        # Get handler
        handler = self.handlers.get(event_type)
        if not handler:
            raise ValueError(f"No handler for event: {event_type}")

        # Process
        result = handler(data)

        # Mark as processed
        self.mark_processed(key)

        return {"status": "success", "result": result}

# Usage
webhook_handler = WebhookEventHandler()

@webhook_handler.register("lead_created")
def handle_lead_created(data):
    # Process new lead
    frappe.get_doc({
        "doctype": "Integration Log",
        "type": "Lead Created",
        "data": json.dumps(data)
    }).insert(ignore_permissions=True)
    return {"lead_id": data.get("id")}

@webhook_handler.register("order_submitted")
def handle_order_submitted(data):
    # Process submitted order
    return {"order_id": data.get("id")}

# In your webhook endpoint
def process_incoming_webhook(event_type, data):
    return webhook_handler.handle(event_type, data)
```

## Best Practices

1. **Always Return 2xx Quickly**: Respond to webhooks quickly to avoid timeouts
2. **Use Async Processing**: Process heavy operations in background jobs
3. **Implement Idempotency**: Handle duplicate deliveries gracefully
4. **Log Everything**: Keep detailed logs for debugging
5. **Validate Before Processing**: Verify payload structure before processing

## Next Steps

- [Error Handling in Integrations](../error-handling-integrations/error-handling-integrations.md)
- [Rate Limiting and Retry Logic](../rate-limiting-retry-logic/rate-limiting-retry-logic.md)

---

*Source: Frappe Integration Documentation | Difficulty: Intermediate | Last updated: 2026-02-04*
