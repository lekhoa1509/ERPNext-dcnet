# Opportunity DocType Reference

> Source: https://github.com/frappe/erpnext/tree/develop/erpnext/crm/doctype/opportunity

## Overview

Opportunity represents a qualified sales lead that has potential to convert into a sale. It tracks the sales pipeline, deal value, probability of closing, and the sales stage progression.

## Field Reference

### Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `naming_series` | Select | Default: `CRM-OPP-.YYYY.-` |
| `opportunity_from` | Link (DocType) | Lead, Customer, or Prospect |
| `party_name` | Dynamic Link | Reference to source document |
| `customer_name` | Data | Display name (read-only) |
| `status` | Select | Opportunity status |
| `opportunity_type` | Link | Sales, Support, etc. |
| `opportunity_owner` | Link (User) | Assigned sales person |

### Timeline & Dates

| Field | Type | Description |
|-------|------|-------------|
| `transaction_date` | Date | Opportunity creation date |
| `expected_closing` | Date | Expected close date |
| `first_response_time` | Duration | Time to first response |

### Financial

| Field | Type | Description |
|-------|------|-------------|
| `currency` | Link | Transaction currency |
| `opportunity_amount` | Currency | Deal value |
| `base_opportunity_amount` | Currency | Value in company currency |
| `total` | Currency | Calculated total from items |
| `base_total` | Currency | Total in company currency |
| `conversion_rate` | Float | Exchange rate |

### Sales Metrics

| Field | Type | Description |
|-------|------|-------------|
| `sales_stage` | Link | Current pipeline stage |
| `probability` | Percent | Win probability (%) |

### Contact Information

| Field | Type | Description |
|-------|------|-------------|
| `contact_person` | Link (Contact) | Primary contact |
| `contact_email` | Data | Email |
| `contact_mobile` | Data | Mobile |
| `job_title` | Data | Contact's job title |
| `phone` | Data | Phone |
| `whatsapp` | Data | WhatsApp |

### Address & Territory

| Field | Type | Description |
|-------|------|-------------|
| `customer_address` | Link (Address) | Billing address |
| `address_display` | Text | Formatted address |
| `city` | Data | City |
| `state` | Data | State/Province |
| `country` | Link | Country |
| `territory` | Link | Sales territory |

### Organization Details

| Field | Type | Description |
|-------|------|-------------|
| `no_of_employees` | Select | Company size |
| `annual_revenue` | Currency | Company revenue |
| `industry` | Link | Industry Type |
| `market_segment` | Link | Market Segment |
| `customer_group` | Link | Customer Group |

### Lost Deal Information

| Field | Type | Description |
|-------|------|-------------|
| `order_lost_reason` | Small Text | Detailed reason |
| `lost_reasons` | Table MultiSelect | Lost Reasons |
| `competitors` | Table MultiSelect | Competing vendors |

### UTM Tracking

| Field | Type | Description |
|-------|------|-------------|
| `utm_source` | Link | Traffic source |
| `utm_campaign` | Link | Campaign name |
| `utm_medium` | Link | Marketing medium |
| `utm_content` | Data | Content identifier |

### Items Table

| Field | Type | Description |
|-------|------|-------------|
| `items` | Table | Opportunity Item child table |

**Opportunity Item fields:**
- `item_code` - Item reference
- `item_name` - Item name
- `qty` - Quantity
- `rate` - Unit price
- `amount` - Line total

## Status Values

```python
status: Literal[
    "Open",      # Active opportunity
    "Quotation", # Quotation created
    "Converted", # Won - converted to order
    "Lost",      # Lost to competitor
    "Replied",   # Waiting for response
    "Closed"     # Closed without conversion
]
```

### Status Flow

```
        ┌─────────────┐
        │    Open     │
        └──────┬──────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼────┐ ┌───▼────┐ ┌───▼────┐
│Replied │ │  Lost  │ │ Closed │
└───┬────┘ └────────┘ └────────┘
    │
┌───▼────┐
│Quotation│
└───┬────┘
    │
┌───▼────┐
│Converted│
└─────────┘
```

## Sales Stage

Default Sales Stages in ERPNext:

| Stage | Probability |
|-------|-------------|
| Prospecting | 10% |
| Qualification | 20% |
| Needs Analysis | 40% |
| Value Proposition | 60% |
| Negotiation | 80% |
| Closed Won | 100% |

## API Reference

### Create Opportunity

```python
opportunity = frappe.new_doc("Opportunity")
opportunity.opportunity_from = "Lead"
opportunity.party_name = "LEAD-00001"
opportunity.company = "My Company"
opportunity.opportunity_type = "Sales"
opportunity.sales_stage = "Prospecting"
opportunity.expected_closing = "2026-02-28"
opportunity.probability = 20
opportunity.insert()
```

### Create Opportunity with Items

```python
opportunity = frappe.new_doc("Opportunity")
opportunity.opportunity_from = "Customer"
opportunity.party_name = "CUST-00001"
opportunity.company = "My Company"
opportunity.opportunity_type = "Sales"
opportunity.sales_stage = "Needs Analysis"
opportunity.expected_closing = "2026-03-15"

# Add items
opportunity.append("items", {
    "item_code": "GOLF-DRIVER-001",
    "qty": 1,
    "rate": 15000000
})
opportunity.append("items", {
    "item_code": "GOLF-IRON-SET",
    "qty": 1,
    "rate": 25000000
})

opportunity.insert()
# opportunity_amount will be calculated automatically
```

### Convert Opportunity to Quotation

```python
from erpnext.crm.doctype.opportunity.opportunity import make_quotation

quotation = make_quotation("CRM-OPP-2026-00001")
quotation.insert()
```

### Convert Opportunity to Customer

```python
from erpnext.crm.doctype.opportunity.opportunity import make_customer

customer = make_customer("CRM-OPP-2026-00001")
customer.customer_group = "Commercial"
customer.insert()
```

### Create Request for Quotation

```python
from erpnext.crm.doctype.opportunity.opportunity import make_request_for_quotation

rfq = make_request_for_quotation("CRM-OPP-2026-00001")
rfq.insert()
```

### Create Supplier Quotation

```python
from erpnext.crm.doctype.opportunity.opportunity import make_supplier_quotation

sq = make_supplier_quotation("CRM-OPP-2026-00001")
sq.supplier = "SUPP-00001"
sq.insert()
```

### Declare Opportunity Lost

```python
opportunity = frappe.get_doc("Opportunity", "CRM-OPP-2026-00001")
opportunity.declare_enquiry_lost(
    lost_reasons_list=[
        {"lost_reason": "Price too high"},
        {"lost_reason": "Competitor won"}
    ],
    competitors=[
        {"competitor": "Competitor A"},
        {"competitor": "Competitor B"}
    ],
    detailed_reason="Customer chose cheaper alternative with similar features"
)
```

### Update Multiple Opportunities Status

```python
from erpnext.crm.doctype.opportunity.opportunity import set_multiple_status

set_multiple_status(
    names=["CRM-OPP-2026-00001", "CRM-OPP-2026-00002"],
    status="Closed"
)
```

### Check Quotation Status

```python
opportunity = frappe.get_doc("Opportunity", "CRM-OPP-2026-00001")

# Check if has active quotation
has_active = opportunity.has_active_quotation()

# Check if has ordered quotation
has_ordered = opportunity.has_ordered_quotation()

# Check if has lost quotation
has_lost = opportunity.has_lost_quotation()
```

### Create Opportunity from Communication

```python
from erpnext.crm.doctype.opportunity.opportunity import make_opportunity_from_communication

opportunity = make_opportunity_from_communication("COMM-00001")
```

### Get Item Details

```python
from erpnext.crm.doctype.opportunity.opportunity import get_item_details

details = get_item_details(item_code="GOLF-DRIVER-001")
# Returns: item_name, description, item_group, brand, stock_uom
```

## Controller Events

### Lifecycle Hooks

```python
class Opportunity(Document):
    def onload(self):
        # Load address and contact from party
        pass

    def after_insert(self):
        # Update lead status to "Opportunity"
        # Link communication if created from email
        pass

    def validate(self):
        # Validate data, set defaults
        # Calculate totals
        pass

    def on_update(self):
        # Update linked Prospect
        pass
```

### Custom Events (hooks.py)

```python
# In your app's hooks.py
doc_events = {
    "Opportunity": {
        "validate": "myapp.crm.opp_validate",
        "on_update": "myapp.crm.opp_on_update",
        "after_insert": "myapp.crm.opp_after_insert"
    }
}
```

## Auto-Close Feature

CRM Settings can auto-close "Replied" opportunities:

```python
# Setting: close_opportunity_after_days (default: 15)

# Scheduler runs daily
from erpnext.crm.doctype.opportunity.opportunity import auto_close_opportunity
auto_close_opportunity()
```

## Notes (CRM Note)

```python
opportunity = frappe.get_doc("Opportunity", "CRM-OPP-2026-00001")
opportunity.add_note("Demo scheduled for Friday 2pm")
frappe.db.commit()
```

## Related DocTypes

- **Opportunity Type** - Sales, Support, etc.
- **Sales Stage** - Pipeline stages with probability
- **Lost Reason** - Why opportunities are lost
- **Competitor** - Competing vendors
- **Lead** - Source of opportunity
- **Customer** - Can also be source
- **Prospect** - Company-level aggregation
- **Quotation** - Next stage in sales
- **Sales Order** - Final conversion
