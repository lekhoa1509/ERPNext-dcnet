# How To: Custom JSON Body with Jinja Templates

**Difficulty**: Intermediate
**Estimated Time**: 20 minutes
**Tags**: webhook, json, jinja, template, custom-body

## Overview

Learn how to create custom webhook JSON bodies using Jinja2 templating for complete control over the payload structure.

## Prerequisites

- Basic webhook setup knowledge
- Jinja2 templating basics
- JSON structure understanding

## Step-by-Step Guide

### Step 1: Enable Custom JSON Body

```python
import frappe

webhook = frappe.new_doc("Webhook")
webhook.webhook_doctype = "Sales Order"
webhook.webhook_docevent = "on_submit"
webhook.enabled = 1
webhook.request_url = "https://api.example.com/orders"
webhook.request_method = "POST"

# Use JSON structure instead of form data
webhook.request_structure = "JSON"
```

### Step 2: Basic Custom JSON Template

```python
# Set custom JSON using webhook_json field
webhook.webhook_json = """{
    "event": "order_submitted",
    "timestamp": "{{ frappe.utils.now() }}",
    "order": {
        "id": "{{ doc.name }}",
        "customer": "{{ doc.customer }}",
        "total": {{ doc.grand_total }},
        "currency": "{{ doc.currency }}"
    }
}"""
webhook.insert()
```

### Step 3: Including Child Table Data

```python
webhook.webhook_json = """{
    "order_id": "{{ doc.name }}",
    "customer": "{{ doc.customer }}",
    "items": [
        {% for item in doc.items %}
        {
            "item_code": "{{ item.item_code }}",
            "item_name": "{{ item.item_name }}",
            "quantity": {{ item.qty }},
            "rate": {{ item.rate }},
            "amount": {{ item.amount }}
        }{% if not loop.last %},{% endif %}
        {% endfor %}
    ],
    "totals": {
        "subtotal": {{ doc.total }},
        "tax": {{ doc.total_taxes_and_charges }},
        "grand_total": {{ doc.grand_total }}
    }
}"""
```

### Step 4: Conditional Fields in JSON

```python
webhook.webhook_json = """{
    "order_id": "{{ doc.name }}",
    "customer": "{{ doc.customer }}",
    {% if doc.shipping_address %}
    "shipping_address": "{{ doc.shipping_address_name }}",
    {% endif %}
    {% if doc.contact_person %}
    "contact": "{{ doc.contact_person }}",
    {% endif %}
    "has_discount": {{ 'true' if doc.discount_amount > 0 else 'false' }},
    "priority": "{{ 'high' if doc.grand_total > 10000 else 'normal' }}"
}"""
```

### Step 5: Including Linked Document Data

```python
webhook.webhook_json = """{
    "order": {
        "id": "{{ doc.name }}",
        "date": "{{ doc.transaction_date }}"
    },
    "customer": {
        {% set customer = frappe.get_doc('Customer', doc.customer) %}
        "name": "{{ customer.customer_name }}",
        "group": "{{ customer.customer_group }}",
        "territory": "{{ customer.territory }}",
        "email": "{{ customer.email_id or '' }}",
        "phone": "{{ customer.mobile_no or '' }}"
    },
    "company": {
        {% set company = frappe.get_doc('Company', doc.company) %}
        "name": "{{ company.company_name }}",
        "country": "{{ company.country }}"
    }
}"""
```

### Step 6: Array Response Format

```python
# For APIs expecting array format
webhook.webhook_json = """[
    {% for item in doc.items %}
    {
        "sku": "{{ item.item_code }}",
        "name": "{{ item.item_name }}",
        "qty": {{ item.qty }},
        "price": {{ item.rate }},
        "order_ref": "{{ doc.name }}"
    }{% if not loop.last %},{% endif %}
    {% endfor %}
]"""
```

## Complete Example

```python
import frappe

def create_external_api_webhook():
    """Create webhook for external API with custom JSON structure."""

    webhook = frappe.new_doc("Webhook")
    webhook.webhook_doctype = "Sales Order"
    webhook.webhook_docevent = "on_submit"
    webhook.enabled = 1
    webhook.request_url = "https://api.external-system.com/v1/orders"
    webhook.request_method = "POST"
    webhook.request_structure = "JSON"

    # Complex JSON template matching external API requirements
    webhook.webhook_json = """{
    "api_version": "1.0",
    "event_type": "ORDER_CREATED",
    "event_timestamp": "{{ frappe.utils.now_datetime().isoformat() }}",
    "source": {
        "system": "ERPNext",
        "site": "{{ frappe.local.site }}"
    },
    "payload": {
        "order": {
            "external_id": "{{ doc.name }}",
            "order_number": "{{ doc.po_no or doc.name }}",
            "created_date": "{{ doc.transaction_date }}",
            "delivery_date": "{{ doc.delivery_date or '' }}",
            "status": "{{ doc.status }}",
            "currency_code": "{{ doc.currency }}",
            "exchange_rate": {{ doc.conversion_rate }}
        },
        "customer": {
            "id": "{{ doc.customer }}",
            {% set customer = frappe.get_doc('Customer', doc.customer) %}
            "name": "{{ customer.customer_name }}",
            "email": "{{ customer.email_id or '' }}",
            "phone": "{{ customer.mobile_no or '' }}",
            "tax_id": "{{ customer.tax_id or '' }}",
            "type": "{{ 'COMPANY' if customer.customer_type == 'Company' else 'INDIVIDUAL' }}"
        },
        "billing_address": {
            {% if doc.customer_address %}
            {% set addr = frappe.get_doc('Address', doc.customer_address) %}
            "line1": "{{ addr.address_line1 }}",
            "line2": "{{ addr.address_line2 or '' }}",
            "city": "{{ addr.city }}",
            "state": "{{ addr.state or '' }}",
            "postal_code": "{{ addr.pincode or '' }}",
            "country_code": "{{ addr.country }}"
            {% else %}
            "line1": "",
            "city": "",
            "country_code": ""
            {% endif %}
        },
        "shipping_address": {
            {% if doc.shipping_address_name %}
            {% set ship_addr = frappe.get_doc('Address', doc.shipping_address_name) %}
            "line1": "{{ ship_addr.address_line1 }}",
            "line2": "{{ ship_addr.address_line2 or '' }}",
            "city": "{{ ship_addr.city }}",
            "state": "{{ ship_addr.state or '' }}",
            "postal_code": "{{ ship_addr.pincode or '' }}",
            "country_code": "{{ ship_addr.country }}"
            {% else %}
            "line1": "",
            "city": "",
            "country_code": ""
            {% endif %}
        },
        "line_items": [
            {% for item in doc.items %}
            {
                "line_number": {{ loop.index }},
                "sku": "{{ item.item_code }}",
                "description": "{{ item.description | replace('\n', ' ') | replace('"', '\\"') }}",
                "quantity": {{ item.qty }},
                "unit_of_measure": "{{ item.uom }}",
                "unit_price": {{ item.rate }},
                "discount_percent": {{ item.discount_percentage or 0 }},
                "tax_amount": {{ (item.amount * (doc.total_taxes_and_charges / doc.total)) if doc.total > 0 else 0 }},
                "line_total": {{ item.amount }},
                {% if item.warehouse %}
                "warehouse": "{{ item.warehouse }}",
                {% endif %}
                "delivery_date": "{{ item.delivery_date or doc.delivery_date or '' }}"
            }{% if not loop.last %},{% endif %}
            {% endfor %}
        ],
        "totals": {
            "subtotal": {{ doc.total }},
            "discount_amount": {{ doc.discount_amount or 0 }},
            "tax_amount": {{ doc.total_taxes_and_charges }},
            "shipping_amount": {{ doc.shipping_amount if doc.shipping_amount else 0 }},
            "grand_total": {{ doc.grand_total }},
            "outstanding_amount": {{ doc.grand_total }}
        },
        "payment_terms": "{{ doc.payment_terms_template or 'DEFAULT' }}",
        "notes": "{{ (doc.notes or '') | replace('\n', ' ') | replace('"', '\\"') }}"
    },
    "metadata": {
        "owner": "{{ doc.owner }}",
        "created": "{{ doc.creation }}",
        "modified": "{{ doc.modified }}"
    }
}"""

    # Headers
    webhook.append("webhook_headers", {
        "key": "Content-Type",
        "value": "application/json"
    })
    webhook.append("webhook_headers", {
        "key": "X-API-Key",
        "value": "{{ frappe.conf.external_api_key or 'not-configured' }}"
    })

    webhook.insert()
    frappe.db.commit()

    return webhook.name

# Usage
webhook_name = create_external_api_webhook()
print(f"Created webhook: {webhook_name}")
```

## Testing Custom JSON

```python
def preview_webhook_json(webhook_name: str, docname: str) -> dict:
    """Preview the rendered JSON for a specific document."""
    import json

    webhook = frappe.get_doc("Webhook", webhook_name)
    doc = frappe.get_doc(webhook.webhook_doctype, docname)

    # Render the template
    rendered = webhook.preview_request_body(doc.name)

    # Parse to verify it's valid JSON
    try:
        parsed = json.loads(rendered)
        return {"valid": True, "json": parsed}
    except json.JSONDecodeError as e:
        return {"valid": False, "error": str(e), "raw": rendered}

# Test
result = preview_webhook_json("Sales Order Webhook", "SO-2024-00001")
print(json.dumps(result, indent=2))
```

## Common Template Patterns

| Pattern | Example |
|---------|---------|
| Safe string (escape JSON) | `{{ field \| replace('"', '\\"') }}` |
| Default value | `{{ field or 'default' }}` |
| Number formatting | `{{ "%.2f" \| format(amount) }}` |
| Date formatting | `{{ frappe.utils.formatdate(date, 'yyyy-MM-dd') }}` |
| Boolean output | `{{ 'true' if condition else 'false' }}` |
| List join | `{{ items \| join(', ') }}` |

## Troubleshooting

### Invalid JSON Output
- Use `preview_request_body()` to test
- Check for trailing commas in loops
- Escape special characters in strings

### Missing Data
- Verify field names match DocType
- Handle None values with `or ''`
- Check if linked documents exist

## Next Steps

- [Webhook Event Handling Patterns](../webhook-event-handling/webhook-event-handling.md)
- [REST API Integration Patterns](../rest-api-integration-patterns/rest-api-integration-patterns.md)

---

*Source: Frappe Integration Documentation | Difficulty: Intermediate | Last updated: 2026-02-04*
