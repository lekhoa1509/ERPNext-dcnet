# How To: Webhook Conditional Execution

**Difficulty**: Intermediate
**Estimated Time**: 20 minutes
**Tags**: webhook, conditions, jinja, filtering

## Overview

Learn how to configure webhooks to fire only when specific conditions are met using Frappe's condition field and Jinja templating.

## Prerequisites

- Basic webhook setup knowledge
- Understanding of Jinja2 templates
- Frappe document structure knowledge

## Step-by-Step Guide

### Step 1: Understanding the Condition Field

The `meets_condition` field in webhooks accepts Jinja expressions that evaluate to `True` or `False`:

```python
import frappe

# Create webhook with condition
webhook = frappe.new_doc("Webhook")
webhook.webhook_doctype = "Sales Order"
webhook.webhook_docevent = "on_submit"
webhook.enabled = 1
webhook.request_url = "https://api.example.com/orders"

# Only trigger for orders above $1000
webhook.meets_condition = "Yes"
webhook.condition = "doc.grand_total > 1000"

webhook.insert()
```

### Step 2: Simple Field Conditions

```python
# Only for specific status
webhook.condition = "doc.status == 'Approved'"

# Only for specific customer
webhook.condition = "doc.customer == 'Important Customer Ltd'"

# Only for specific territory
webhook.condition = "doc.territory == 'United States'"

# Numeric comparisons
webhook.condition = "doc.quantity >= 100"
webhook.condition = "doc.discount_percentage > 0"
```

### Step 3: Complex Conditions with Multiple Fields

```python
# Multiple conditions with AND
webhook.condition = "doc.grand_total > 1000 and doc.territory == 'Export'"

# Multiple conditions with OR
webhook.condition = "doc.status == 'Urgent' or doc.grand_total > 5000"

# Combined AND/OR
webhook.condition = "(doc.status == 'Approved' and doc.grand_total > 1000) or doc.is_priority == 1"
```

### Step 4: Checking Child Table Values

```python
# Check if any item matches a condition (using Jinja)
webhook.condition = """
{% set has_special_item = false %}
{% for item in doc.items %}
    {% if item.item_code.startswith('SPECIAL-') %}
        {% set has_special_item = true %}
    {% endif %}
{% endfor %}
{{ has_special_item }}
"""

# Simpler approach - check total items
webhook.condition = "len(doc.items) > 5"
```

### Step 5: Using Linked Document Data

```python
# Check customer's customer group
webhook.condition = """
{% set customer = frappe.get_doc('Customer', doc.customer) %}
{{ customer.customer_group == 'VIP' }}
"""

# Check if customer has outstanding invoices
webhook.condition = """
{% set has_outstanding = frappe.db.exists('Sales Invoice', {
    'customer': doc.customer,
    'outstanding_amount': ('>', 0),
    'docstatus': 1
}) %}
{{ not has_outstanding }}
"""
```

### Step 6: Date-Based Conditions

```python
from datetime import datetime

# Only during business hours
webhook.condition = """
{% set current_hour = frappe.utils.now_datetime().hour %}
{{ current_hour >= 9 and current_hour < 18 }}
"""

# Only for orders due this week
webhook.condition = """
{% set due_date = frappe.utils.getdate(doc.delivery_date) %}
{% set today = frappe.utils.today() %}
{% set days_until_due = (due_date - frappe.utils.getdate(today)).days %}
{{ days_until_due <= 7 }}
"""

# Exclude weekends
webhook.condition = """
{% set day = frappe.utils.now_datetime().weekday() %}
{{ day < 5 }}
"""
```

## Complete Example

```python
import frappe

def create_conditional_webhooks():
    """Create multiple webhooks with different conditions."""

    webhooks_config = [
        {
            "name": "High Value Orders",
            "doctype": "Sales Order",
            "event": "on_submit",
            "url": "https://api.example.com/high-value-orders",
            "condition": "doc.grand_total > 10000"
        },
        {
            "name": "Export Orders",
            "doctype": "Sales Order",
            "event": "on_submit",
            "url": "https://api.example.com/export-orders",
            "condition": "doc.territory in ['USA', 'Europe', 'Asia']"
        },
        {
            "name": "Urgent Leads",
            "doctype": "Lead",
            "event": "after_insert",
            "url": "https://api.example.com/urgent-leads",
            "condition": "'urgent' in (doc.source or '').lower() or doc.company_name and 'enterprise' in doc.company_name.lower()"
        },
        {
            "name": "VIP Customer Changes",
            "doctype": "Customer",
            "event": "on_update",
            "url": "https://api.example.com/vip-updates",
            "condition": "doc.customer_group == 'VIP'"
        },
        {
            "name": "Stock Alerts",
            "doctype": "Stock Entry",
            "event": "on_submit",
            "url": "https://api.example.com/stock-alerts",
            "condition": "doc.stock_entry_type == 'Material Issue' and doc.total_outgoing_value > 5000"
        }
    ]

    created = []

    for config in webhooks_config:
        # Skip if already exists
        existing = frappe.db.exists("Webhook", {
            "webhook_doctype": config["doctype"],
            "webhook_docevent": config["event"],
            "request_url": config["url"]
        })

        if existing:
            continue

        webhook = frappe.new_doc("Webhook")
        webhook.webhook_doctype = config["doctype"]
        webhook.webhook_docevent = config["event"]
        webhook.enabled = 1
        webhook.request_url = config["url"]
        webhook.request_method = "POST"
        webhook.meets_condition = "Yes"
        webhook.condition = config["condition"]

        # Add standard headers
        webhook.append("webhook_headers", {
            "key": "Content-Type",
            "value": "application/json"
        })

        webhook.insert()
        created.append(config["name"])

    frappe.db.commit()
    return created

# Usage
created_webhooks = create_conditional_webhooks()
print(f"Created webhooks: {created_webhooks}")
```

## Testing Conditions

```python
def test_webhook_condition(webhook_name: str, docname: str) -> bool:
    """Test if a document meets webhook condition."""

    webhook = frappe.get_doc("Webhook", webhook_name)
    doc = frappe.get_doc(webhook.webhook_doctype, docname)

    if webhook.meets_condition == "No":
        return True

    # Evaluate condition
    result = webhook.preview_meets_condition(doc.name)
    return result

# Test
result = test_webhook_condition("High Value Orders", "SO-2024-00001")
print(f"Meets condition: {result}")
```

## Common Condition Patterns

| Use Case | Condition |
|----------|-----------|
| Status filter | `doc.status == 'Approved'` |
| Numeric threshold | `doc.amount > 1000` |
| String match | `'keyword' in doc.description.lower()` |
| Null check | `doc.field is not none` |
| List membership | `doc.type in ['A', 'B', 'C']` |
| Negation | `doc.status != 'Cancelled'` |
| Date comparison | `doc.date >= frappe.utils.today()` |

## Troubleshooting

### Condition Always False
- Test condition with `preview_meets_condition()`
- Check field names are correct (case-sensitive)
- Verify field has value (not None/null)

### Syntax Errors
- Use Python syntax for conditions
- Escape special characters properly
- Test Jinja syntax separately

## Next Steps

- [Webhook Security with Signatures](../webhook-security-signatures/webhook-security-signatures.md)
- [Custom JSON Body with Jinja](../webhook-custom-json-body/webhook-custom-json-body.md)

---

*Source: Frappe Integration Documentation | Difficulty: Intermediate | Last updated: 2026-02-04*
