# Lead DocType Reference

> Source: https://github.com/frappe/erpnext/tree/develop/erpnext/crm/doctype/lead

## Overview

Lead is the starting point of CRM in ERPNext. A Lead represents a potential customer who has shown interest in your products or services but hasn't made a purchase yet.

## Field Reference

### Core Identity

| Field | Type | Description |
|-------|------|-------------|
| `naming_series` | Select | Default: `CRM-LEAD-.YYYY.-` |
| `lead_name` | Data | Full name (auto-computed from first/last) |
| `salutation` | Link | Mr., Mrs., Ms., etc. |
| `first_name` | Data | **Required** if no company_name |
| `middle_name` | Data | Optional |
| `last_name` | Data | Optional |

### Contact Information

| Field | Type | Description |
|-------|------|-------------|
| `email_id` | Data | Primary email (searchable) |
| `phone` | Data | Phone number |
| `mobile_no` | Data | Mobile number |
| `whatsapp_no` | Data | WhatsApp contact |
| `phone_ext` | Data | Phone extension |
| `fax` | Data | Fax number |

### Organization Details

| Field | Type | Description |
|-------|------|-------------|
| `company_name` | Data | **Required** if no first_name |
| `job_title` | Data | Job position |
| `no_of_employees` | Select | 1-10, 11-50, 51-200, 201-500, 501-1000, 1000+ |
| `annual_revenue` | Currency | Company revenue |
| `industry` | Link | Industry Type |
| `market_segment` | Link | Market Segment |
| `website` | Data | Website URL |

### Location

| Field | Type | Description |
|-------|------|-------------|
| `city` | Data | City name |
| `state` | Data | State/Province |
| `country` | Link | Country |
| `territory` | Link | Sales territory |

### Lead Management

| Field | Type | Description |
|-------|------|-------------|
| `status` | Select | Lead status (see Status Values) |
| `lead_owner` | Link (User) | Assigned sales person |
| `type` | Select | Client, Channel Partner, Consultant |
| `source` | Link | Lead Source |

### Qualification

| Field | Type | Description |
|-------|------|-------------|
| `qualification_status` | Select | Unqualified, In Process, Qualified |
| `qualified_by` | Link (User) | Who qualified |
| `qualified_on` | Date | When qualified |

### UTM Tracking

| Field | Type | Description |
|-------|------|-------------|
| `utm_source` | Link | Traffic source |
| `utm_medium` | Link | Marketing medium |
| `utm_campaign` | Link | Campaign name |
| `utm_content` | Data | Content identifier |

## Status Values

```python
status: Literal[
    "Lead",           # New lead, not yet contacted
    "Open",           # Being worked on
    "Replied",        # Responded to inquiry
    "Opportunity",    # Converted to opportunity
    "Quotation",      # Quotation sent
    "Lost Quotation", # Quotation lost
    "Interested",     # Showing interest
    "Converted",      # Converted to customer
    "Do Not Contact"  # Opted out
]
```

### Status Flow

```
                    ┌─────────────┐
                    │    Lead     │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │    Open     │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──────┐ ┌───▼────┐ ┌─────▼─────┐
       │   Replied   │ │Interest│ │Do Not Ctct│
       └──────┬──────┘ └────────┘ └───────────┘
              │
       ┌──────▼──────┐
       │ Opportunity │
       └──────┬──────┘
              │
       ┌──────▼──────┐
       │  Quotation  │
       └──────┬──────┘
              │
       ┌──────┴──────┐
       │             │
┌──────▼──────┐ ┌────▼────┐
│  Converted  │ │Lost Quot│
└─────────────┘ └─────────┘
```

## API Reference

### Create Lead

```python
lead = frappe.new_doc("Lead")
lead.first_name = "John"
lead.last_name = "Doe"
lead.company_name = "ABC Corporation"
lead.email_id = "john@abc.com"
lead.mobile_no = "0901234567"
lead.lead_owner = "sales@company.com"
lead.status = "Open"
lead.source = "Website"
lead.territory = "Vietnam"
lead.insert()
```

### Convert Lead to Customer

```python
from erpnext.crm.doctype.lead.lead import make_customer

# Basic conversion
customer = make_customer("LEAD-00001")
customer.customer_group = "Commercial"
customer.insert()

# With ignore_permissions
from erpnext.crm.doctype.lead.lead import _make_customer
customer = _make_customer("LEAD-00001", ignore_permissions=True)
customer.insert()
```

**Field Mapping (Lead → Customer):**
| Lead Field | Customer Field |
|------------|----------------|
| lead_name | customer_name (if individual) |
| company_name | customer_name (if company) |
| territory | territory |
| industry | industry |
| market_segment | market_segment |

### Convert Lead to Opportunity

```python
from erpnext.crm.doctype.lead.lead import make_opportunity

opportunity = make_opportunity("LEAD-00001")
opportunity.opportunity_type = "Sales"
opportunity.expected_closing = "2026-02-28"
opportunity.insert()
```

**Field Mapping (Lead → Opportunity):**
| Lead Field | Opportunity Field |
|------------|-------------------|
| doctype | opportunity_from |
| name | party_name |
| lead_name | contact_display |
| email_id | contact_email |
| mobile_no | contact_mobile |
| lead_owner | opportunity_owner |

### Convert Lead to Quotation

```python
from erpnext.crm.doctype.lead.lead import make_quotation

quotation = make_quotation("LEAD-00001")
quotation.append("items", {
    "item_code": "ITEM-001",
    "qty": 1
})
quotation.insert()
```

### Get Lead Details

```python
from erpnext.crm.doctype.lead.lead import get_lead_details

details = get_lead_details(
    lead="LEAD-00001",
    posting_date="2026-01-23",
    company="My Company"
)
# Returns: territory, customer_name, contact_display,
#          contact_email, taxes_and_charges, etc.
```

### Add Lead to Prospect

```python
from erpnext.crm.doctype.lead.lead import add_lead_to_prospect

add_lead_to_prospect(
    lead="LEAD-00001",
    prospect="PROS-00001"
)
```

### Create Lead from Communication

```python
from erpnext.crm.doctype.lead.lead import make_lead_from_communication

lead = make_lead_from_communication(
    communication="COMM-00001",
    ignore_communication_links=False
)
```

### Find Lead by Phone Number

```python
from erpnext.crm.doctype.lead.lead import get_lead_with_phone_number

lead = get_lead_with_phone_number("0901234567")
# Searches: phone, whatsapp_no, mobile_no
```

## Controller Events

### Lifecycle Hooks

```python
class Lead(Document):
    def validate(self):
        # Validates lead_name, sets full name
        pass

    def before_insert(self):
        # Sets default lead_owner, checks duplicates
        pass

    def after_insert(self):
        # Links communication if created from email
        pass

    def on_update(self):
        # Updates related records
        pass
```

### Custom Events (hooks.py)

```python
# In your app's hooks.py
doc_events = {
    "Lead": {
        "validate": "myapp.crm.lead_validate",
        "on_update": "myapp.crm.lead_on_update",
        "after_insert": "myapp.crm.lead_after_insert"
    }
}
```

## Duplicate Detection

CRM Settings controls duplicate behavior:

```python
# Check setting
allow_duplicates = frappe.db.get_single_value(
    "CRM Settings",
    "allow_lead_duplication_based_on_emails"
)

# Manual check
existing = frappe.db.exists("Lead", {"email_id": "john@abc.com"})
```

## Notes (CRM Note)

```python
lead = frappe.get_doc("Lead", "LEAD-00001")
lead.add_note("Called customer, will follow up next week")
frappe.db.commit()
```

## Related DocTypes

- **Lead Source** - Where the lead came from
- **Industry Type** - Industry classification
- **Market Segment** - Target market segment
- **UTM Source/Medium/Campaign** - Marketing tracking
- **Prospect** - Aggregates multiple leads
- **Opportunity** - Next stage in sales pipeline
- **Customer** - Final conversion target
