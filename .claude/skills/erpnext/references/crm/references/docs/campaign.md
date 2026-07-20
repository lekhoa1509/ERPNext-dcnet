# Campaign DocType Reference

> Source: https://github.com/frappe/erpnext/tree/develop/erpnext/crm/doctype/campaign

## Overview

Campaign is used to track marketing campaigns and their associated email schedules. It integrates with Email Campaign to automate outreach to Leads, Customers, or other targets.

## Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `naming_series` | Select | Default: `SAL-CAM-.YYYY.-` |
| `campaign_name` | Data | **Required** - Campaign name |
| `campaign_schedules` | Table | Email schedule entries |
| `description` | Text | Campaign description |

## Campaign Email Schedule (Child Table)

| Field | Type | Description |
|-------|------|-------------|
| `email_template` | Link | Email template to send |
| `send_after_days` | Int | Days after start to send |

## API Reference

### Create Campaign

```python
campaign = frappe.new_doc("Campaign")
campaign.campaign_name = "Q1 2026 Golf Promotion"
campaign.description = "Quarterly promotion for golf equipment"
campaign.insert()
```

### Create Campaign with Email Schedule

```python
campaign = frappe.new_doc("Campaign")
campaign.campaign_name = "New Customer Onboarding"
campaign.description = "Welcome series for new customers"

# Day 0: Welcome email
campaign.append("campaign_schedules", {
    "email_template": "Welcome Email",
    "send_after_days": 0
})

# Day 3: Product introduction
campaign.append("campaign_schedules", {
    "email_template": "Product Overview",
    "send_after_days": 3
})

# Day 7: Special offer
campaign.append("campaign_schedules", {
    "email_template": "First Purchase Discount",
    "send_after_days": 7
})

campaign.insert()
```

## Email Campaign Integration

### Create Email Campaign

```python
email_campaign = frappe.new_doc("Email Campaign")
email_campaign.campaign_name = "Q1 2026 Golf Promotion"
email_campaign.email_campaign_for = "Lead"
email_campaign.recipient = "LEAD-00001"
email_campaign.sender = "marketing@company.com"
email_campaign.start_date = "2026-01-15"
email_campaign.insert()
email_campaign.submit()
```

### Bulk Email Campaign for Leads

```python
# Get all open leads
leads = frappe.get_all("Lead", filters={"status": "Open"}, pluck="name")

for lead in leads:
    email_campaign = frappe.new_doc("Email Campaign")
    email_campaign.campaign_name = "Q1 2026 Golf Promotion"
    email_campaign.email_campaign_for = "Lead"
    email_campaign.recipient = lead
    email_campaign.sender = "marketing@company.com"
    email_campaign.start_date = "2026-01-15"
    email_campaign.insert()
    email_campaign.submit()
```

### Email Campaign Status

```python
status: Literal[
    "Scheduled",  # Waiting to start
    "In Progress", # Currently running
    "Completed",  # All emails sent
    "Unsubscribed" # Recipient unsubscribed
]
```

## UTM Tracking

Campaigns link to UTM tracking:

```python
# Create UTM Campaign
utm = frappe.new_doc("UTM Campaign")
utm.name = "q1-golf-promo-2026"
utm.insert()

# Link in Lead
lead = frappe.new_doc("Lead")
lead.utm_campaign = "q1-golf-promo-2026"
lead.utm_source = "facebook"
lead.utm_medium = "paid-social"
# ...
```

## Campaign Efficiency Report

ERPNext includes a built-in report to track campaign ROI:

```
CRM > Reports > Campaign Efficiency
```

**Metrics tracked:**
- Number of Leads by campaign
- Lead conversion rate
- Opportunity value
- Revenue generated

## Naming Options (CRM Settings)

```python
# campaign_naming_by options:
# - "Campaign Name" (use campaign_name as document name)
# - "Naming Series" (use SAL-CAM-.YYYY.-)
```

## Related DocTypes

- **Email Campaign** - Individual campaign execution
- **Email Template** - Email content templates
- **UTM Campaign** - Marketing attribution
- **Lead** - Campaign targets
- **Customer** - Campaign targets
