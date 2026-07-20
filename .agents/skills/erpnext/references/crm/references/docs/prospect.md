# Prospect DocType Reference

> Source: https://github.com/frappe/erpnext/tree/develop/erpnext/crm/doctype/prospect

## Overview

Prospect represents a company or organization that aggregates multiple Leads. It provides a company-level view of sales opportunities, useful when dealing with B2B sales where multiple contacts from the same company may be leads.

## Field Reference

### Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `company_name` | Data | **Required** - Company name (also autoname) |
| `industry` | Link | Industry Type |
| `market_segment` | Link | Market Segment |
| `customer_group` | Link | Customer Group |
| `territory` | Link | Sales territory |

### Organization Details

| Field | Type | Description |
|-------|------|-------------|
| `no_of_employees` | Select | 1-10, 11-50, 51-200, 201-500, 501-1000, 1000+ |
| `annual_revenue` | Currency | Company revenue |
| `fax` | Data | Fax number |
| `website` | Data | Company website |

### Management

| Field | Type | Description |
|-------|------|-------------|
| `prospect_owner` | Link (User) | Assigned owner |
| `company` | Link | Internal company |

### Child Tables

| Field | Type | Description |
|-------|------|-------------|
| `leads` | Table (Prospect Lead) | Associated leads |
| `opportunities` | Table (Prospect Opportunity) | Associated opportunities |
| `notes` | Table (CRM Note) | Activity notes |

### Display Fields (HTML)

| Field | Description |
|-------|-------------|
| `address_html` | Rendered address |
| `contact_html` | Rendered contacts |
| `notes_html` | Rendered notes |
| `open_activities_html` | Open activities |
| `all_activities_html` | All activities |

## API Reference

### Create Prospect

```python
prospect = frappe.new_doc("Prospect")
prospect.company_name = "ABC Corporation"
prospect.industry = "Technology"
prospect.market_segment = "Enterprise"
prospect.territory = "Vietnam"
prospect.no_of_employees = "51-200"
prospect.annual_revenue = 50000000000
prospect.website = "https://abc-corp.com"
prospect.prospect_owner = "sales@company.com"
prospect.insert()
```

### Add Lead to Prospect

```python
# Method 1: Using API
from erpnext.crm.doctype.lead.lead import add_lead_to_prospect

add_lead_to_prospect(
    lead="LEAD-00001",
    prospect="ABC Corporation"
)

# Method 2: Manual
prospect = frappe.get_doc("Prospect", "ABC Corporation")
prospect.append("leads", {
    "lead": "LEAD-00001"
})
prospect.save()
```

### Add Opportunity to Prospect

```python
prospect = frappe.get_doc("Prospect", "ABC Corporation")
prospect.append("opportunities", {
    "opportunity": "CRM-OPP-2026-00001"
})
prospect.save()
```

### Convert Prospect to Customer

```python
from erpnext.crm.doctype.prospect.prospect import make_customer

customer = make_customer("ABC Corporation")
customer.customer_group = "Commercial"
customer.insert()
```

### Create Opportunity from Prospect

```python
from erpnext.crm.doctype.prospect.prospect import make_opportunity

opportunity = make_opportunity("ABC Corporation")
opportunity.opportunity_type = "Sales"
opportunity.expected_closing = "2026-03-15"
opportunity.insert()
```

### Get All Leads for Prospect

```python
prospect = frappe.get_doc("Prospect", "ABC Corporation")
leads = [row.lead for row in prospect.leads]

# Or direct query
leads = frappe.get_all(
    "Prospect Lead",
    filters={"parent": "ABC Corporation"},
    pluck="lead"
)
```

### Get All Opportunities for Prospect

```python
prospect = frappe.get_doc("Prospect", "ABC Corporation")
opportunities = [row.opportunity for row in prospect.opportunities]
```

## Child DocTypes

### Prospect Lead

| Field | Type | Description |
|-------|------|-------------|
| `lead` | Link (Lead) | Lead reference |

### Prospect Opportunity

| Field | Type | Description |
|-------|------|-------------|
| `opportunity` | Link (Opportunity) | Opportunity reference |

## Workflow

```
Multiple Leads ──────┐
                     │
Lead 1 ──────────────┼───► Prospect ───► Customer
Lead 2 ──────────────┤         │
Lead 3 ──────────────┘         │
                               ▼
                         Opportunities
```

## Use Cases

### B2B Sales Tracking

```python
# Create prospect for a company
prospect = frappe.new_doc("Prospect")
prospect.company_name = "Big Corp Ltd"
prospect.industry = "Manufacturing"
prospect.insert()

# Add multiple leads (different contacts from same company)
for lead_name in ["LEAD-001", "LEAD-002", "LEAD-003"]:
    prospect.append("leads", {"lead": lead_name})
prospect.save()

# Track all opportunities at company level
opportunities = frappe.get_all(
    "Opportunity",
    filters={
        "opportunity_from": "Prospect",
        "party_name": "Big Corp Ltd"
    }
)
```

### Aggregate Revenue from Prospects

```python
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum

Prospect = DocType("Prospect")
result = frappe.qb.from_(Prospect).select(
    Sum(Prospect.annual_revenue)
).where(
    Prospect.territory == "Vietnam"
).run()
```

## Notes

```python
prospect = frappe.get_doc("Prospect", "ABC Corporation")
prospect.add_note("Meeting scheduled with CEO next Monday")
frappe.db.commit()
```

## Related DocTypes

- **Lead** - Individual contacts aggregated by prospect
- **Opportunity** - Sales opportunities linked to prospect
- **Customer** - Conversion target
- **CRM Note** - Activity tracking
